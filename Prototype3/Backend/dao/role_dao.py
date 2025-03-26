from models.role import Role
from utils.database import get_db_connection
from mysql.connector import Error

class RoleDAO:
    @staticmethod
    def get_all_roles():
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM roles")
                return [Role(**role) for role in cursor.fetchall()]
        except Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn.is_connected():
                conn.close()

    @staticmethod
    def get_role_by_id(role_id):
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM roles WHERE id = %s", (role_id,))
                result = cursor.fetchone()
                return Role(**result) if result else None
        except Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn.is_connected():
                conn.close()