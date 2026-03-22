import mysql.connector
from mysql.connector import errorcode
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_config():
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'auth_system')
    }

def create_database():
    config = get_db_config()
    db_name = config['database']
    
    # Connect without database first to create it
    temp_config = config.copy()
    temp_config.pop('database')
    
    try:
        conn = mysql.connector.connect(**temp_config)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Database '{db_name}' ensured.")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        exit(1)

def setup_tables():
    create_database()
    config = get_db_config()
    
    TABLES = {}
    TABLES['users'] = (
        "CREATE TABLE IF NOT EXISTS `users` ("
        "  `id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `full_name` varchar(100) NOT NULL,"
        "  `email` varchar(150) NOT NULL UNIQUE,"
        "  `mobile` varchar(15) UNIQUE,"
        "  `password_hash` varchar(255) NOT NULL,"
        "  `role` varchar(50) DEFAULT 'user',"
        "  `status` ENUM('active','inactive','locked') DEFAULT 'active',"
        "  `failed_attempts` int DEFAULT 0,"
        "  `created_at` timestamp DEFAULT CURRENT_TIMESTAMP,"
        "  `last_login` timestamp NULL,"
        "  PRIMARY KEY (`id`)"
        ") ENGINE=InnoDB"
    )

    TABLES['login_attempts'] = (
        "CREATE TABLE IF NOT EXISTS `login_attempts` ("
        "  `id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `user_id` int(11) NOT NULL,"
        "  `attempt_time` timestamp DEFAULT CURRENT_TIMESTAMP,"
        "  `status` varchar(20) NOT NULL,"
        "  `ip_address` varchar(50),"
        "  PRIMARY KEY (`id`),"
        "  KEY `user_id` (`user_id`),"
        "  CONSTRAINT `login_attempts_ibfk_1` FOREIGN KEY (`user_id`) "
        "     REFERENCES `users` (`id`) ON DELETE CASCADE"
        ") ENGINE=InnoDB"
    )

    TABLES['password_reset_tokens'] = (
        "CREATE TABLE IF NOT EXISTS `password_reset_tokens` ("
        "  `id` int(11) NOT NULL AUTO_INCREMENT,"
        "  `user_id` int(11) NOT NULL,"
        "  `token` varchar(255) NOT NULL,"
        "  `expires_at` timestamp NOT NULL,"
        "  `used` boolean DEFAULT FALSE,"
        "  PRIMARY KEY (`id`),"
        "  KEY `user_id` (`user_id`),"
        "  CONSTRAINT `password_reset_tokens_ibfk_1` FOREIGN KEY (`user_id`) "
        "     REFERENCES `users` (`id`) ON DELETE CASCADE"
        ") ENGINE=InnoDB"
    )

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print(f"Creating table {table_name}: ", end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    setup_tables()
