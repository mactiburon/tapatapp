import mysql.connector
from mysql.connector import Error
from config import Config

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            user=Config.DB_CONFIG['user'],
            password=Config.DB_CONFIG['password'],
            host=Config.DB_CONFIG['host'],
            database=Config.DB_CONFIG['database'],
            port=Config.DB_CONFIG['port']
        )
        if conn.is_connected():
            return conn
        else:
            print("Database connection failed: Not connected")
            return None
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None