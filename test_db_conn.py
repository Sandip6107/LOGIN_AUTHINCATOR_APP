import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "")
        )
        if conn.is_connected():
            print("Successfully connected to MySQL")
            conn.close()
            return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False

if __name__ == "__main__":
    test_connection()
