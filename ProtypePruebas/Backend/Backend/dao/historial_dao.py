from models.historial import Historial
from utils.database import get_db_connection
from mysql.connector import Error

class HistorialDAO:
    @staticmethod
    def get_historial_by_child(child_id):
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM historial_tapat WHERE child_id = %s", (child_id,))
                return [Historial(**hist) for hist in cursor.fetchall()]
        except Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn.is_connected():
                conn.close()

    @staticmethod
    def get_historial_by_child_and_date(child_id, date):
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM historial_tapat WHERE child_id = %s AND data = %s", (child_id, date))
                result = cursor.fetchone()
                return Historial(**result) if result else None
        except Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn.is_connected():
                conn.close()

    @staticmethod
    def create_historial(child_id, data, hora, estat, totalHores):
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO historial_tapat (child_id, data, hora, estat, totalHores) VALUES (%s, %s, %s, %s, %s)",
                    (child_id, data, hora, estat, totalHores)
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
    def update_historial(historial_id, **kwargs):
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
                
                query = "UPDATE historial_tapat SET " + ", ".join(updates) + " WHERE id = %s"
                params.append(historial_id)
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
    def delete_historial(historial_id):
        conn = get_db_connection()
        if not conn:
            return False
        
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM historial_tapat WHERE id = %s", (historial_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Error as e:
            print(f"Database error: {e}")
            conn.rollback()
            return False
        finally:
            if conn.is_connected():
                conn.close()