from models.status import Status
from utils.database import get_db_connection
from mysql.connector import Error

class StatusDAO:
    @staticmethod
    def get_all_statuses():
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM statuses")
                return [Status(**status) for status in cursor.fetchall()]
        except Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn.is_connected():
                conn.close()

    @staticmethod
    def get_status_by_id(status_id):
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM statuses WHERE id = %s", (status_id,))
                result = cursor.fetchone()
                return Status(**result) if result else None
        except Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn.is_connected():
                conn.close()