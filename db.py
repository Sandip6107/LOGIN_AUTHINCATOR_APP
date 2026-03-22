import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'auth_system')
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def execute_query(query, params=None, fetch=False):
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchall()
        else:
            conn.commit()
            result = cursor.lastrowid if query.strip().upper().startswith("INSERT") else cursor.rowcount
            
        cursor.close()
        conn.close()
        return result
    except mysql.connector.Error as err:
        print(f"Query Error: {err}")
        if conn:
            conn.close()
        return None
