from models.tap import Tap
from utils.database import get_db_connection
from mysql.connector import Error

class TapDAO:
    @staticmethod
    def get_all_taps():
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM taps")
                return [Tap(**tap) for tap in cursor.fetchall()]
        except Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn.is_connected():
                conn.close()

    @staticmethod
    def get_tap_by_id(tap_id):
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM taps WHERE id = %s", (tap_id,))
                result = cursor.fetchone()
                return Tap(**result) if result else None
        except Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn.is_connected():
                conn.close()

    @staticmethod
    def get_taps_by_child(child_id):
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM taps WHERE child_id = %s", (child_id,))
                return [Tap(**tap) for tap in cursor.fetchall()]
        except Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn.is_connected():
                conn.close()

    @staticmethod
    def create_tap(child_id, status_id, user_id, init, end):
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO taps (child_id, status_id, user_id, init, end) VALUES (%s, %s, %s, %s, %s)",
                    (child_id, status_id, user_id, init, end)
                )
                conn.commit()
                return cursor.lastrowid
        except Error as e:
            print(f"Database error: {e}")
            conn.rollback()
            return None
        finally:
            if conn.is_connected():
                conn.close()

    @staticmethod
    def update_tap(tap_id, **kwargs):
        conn = get_db_connection()
        if not conn:
            return False
        
        try:
            with conn.cursor() as cursor:
                updates = []
                params = []
                
                for key, value in kwargs.items():
                    if value is not None:
                        updates.append(f"{key} = %s")
                        params.append(value)
                
                if not updates:
                    return False
                
                query = "UPDATE taps SET " + ", ".join(updates) + " WHERE id = %s"
                params.append(tap_id)
                cursor.execute(query, tuple(params))
                conn.commit()
                return cursor.rowcount > 0
        except Error as e:
            print(f"Database error: {e}")
            conn.rollback()
            return False
        finally:
            if conn.is_connected():
                conn.close()

    @staticmethod
    def delete_tap(tap_id):
        conn = get_db_connection()
        if not conn:
            return False
        
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM taps WHERE id = %s", (tap_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Error as e:
            print(f"Database error: {e}")
            conn.rollback()
            return False
        finally:
            if conn.is_connected():
                conn.close()