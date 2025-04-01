from models.treatment import Treatment
from utils.database import get_db_connection
from mysql.connector import Error

class TreatmentDAO:
    @staticmethod
    def get_all_treatments():
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM treatments")
                return [Treatment(**treatment) for treatment in cursor.fetchall()]
        except Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn.is_connected():
                conn.close()

    @staticmethod
    def get_treatment_by_id(treatment_id):
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM treatments WHERE id = %s", (treatment_id,))
                result = cursor.fetchone()
                return Treatment(**result) if result else None
        except Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn.is_connected():
                conn.close()