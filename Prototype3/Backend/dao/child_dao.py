from models.child import Child
from utils.database import get_db_connection
from mysql.connector import Error

class ChildDAO:
    @staticmethod
    def get_all_children():
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM children")
                return [Child(**child) for child in cursor.fetchall()]
        except Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn.is_connected():
                conn.close()

    @staticmethod
    def get_child_by_id(child_id):
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM children WHERE id = %s", (child_id,))
                result = cursor.fetchone()
                return Child(**result) if result else None
        except Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn.is_connected():
                conn.close()

    @staticmethod
    def get_child_by_name(child_name):
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM children WHERE child_name = %s", (child_name,))
                result = cursor.fetchone()
                return Child(**result) if result else None
        except Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn.is_connected():
                conn.close()

    @staticmethod
    def create_child(child_name, sleep_average, treatment_id, time, informacioMedica):
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO children (child_name, sleep_average, treatment_id, time, informacioMedica) VALUES (%s, %s, %s, %s, %s)",
                    (child_name, sleep_average, treatment_id, time, informacioMedica)
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
    def update_child(child_id, **kwargs):
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
                
                query = "UPDATE children SET " + ", ".join(updates) + " WHERE id = %s"
                params.append(child_id)
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
    def delete_child(child_id):
        conn = get_db_connection()
        if not conn:
            return False
        
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM children WHERE id = %s", (child_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Error as e:
            print(f"Database error: {e}")
            conn.rollback()
            return False
        finally:
            if conn.is_connected():
                conn.close()
