# dao/user_dao.py
from mysql.connector import Error
from utils.database import get_db_connection
from models.user import User

class UserDAO:
    @staticmethod
    def get_all_users():
        conn = get_db_connection()
        if not conn:
            print("Error: No se pudo establecer conexión con la base de datos")
            return None
        
        try:
            with conn.cursor(dictionary=True) as cursor:
                # Verifica que la tabla 'users' existe y tiene datos
                cursor.execute("SELECT id, username, email, role_id FROM users")  # No seleccionamos la contraseña
                return [User(**user) for user in cursor.fetchall()]
        except Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn.is_connected():
                conn.close()

    @staticmethod
    def get_user_by_id(user_id):
        conn = get_db_connection()
        if not conn:
            print("Error: No se pudo establecer conexión con la base de datos")
            return None
        
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                result = cursor.fetchone()
                return User(**result) if result else None
        except Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn.is_connected():
                conn.close()

    @staticmethod
    def get_user_by_credentials(email, password):
        conn = get_db_connection()
        if not conn:
            print("Error: No se pudo establecer conexión con la base de datos")
            return None
        
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
                result = cursor.fetchone()
                return User(**result) if result else None
        except Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn.is_connected():
                conn.close()

    @staticmethod
    def create_user(username, password, email, role_id):
        conn = get_db_connection()
        if not conn:
            print("Error: No se pudo establecer conexión con la base de datos")
            return None
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (username, password, email, role_id) VALUES (%s, %s, %s, %s)",
                    (username, password, email, role_id)
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
    def update_user(user_id, username=None, password=None, email=None, role_id=None):
        conn = get_db_connection()
        if not conn:
            print("Error: No se pudo establecer conexión con la base de datos")
            return False
        
        try:
            with conn.cursor() as cursor:
                updates = []
                params = []
                
                if username:
                    updates.append("username = %s")
                    params.append(username)
                if password:
                    updates.append("password = %s")
                    params.append(password)
                if email:
                    updates.append("email = %s")
                    params.append(email)
                if role_id:
                    updates.append("role_id = %s")
                    params.append(role_id)
                
                if not updates:
                    return False
                
                query = "UPDATE users SET " + ", ".join(updates) + " WHERE id = %s"
                params.append(user_id)
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
    def delete_user(user_id):
        conn = get_db_connection()
        if not conn:
            print("Error: No se pudo establecer conexión con la base de datos")
            return False
        
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
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
    def get_users_by_role(role_id):
        conn = get_db_connection()
        if not conn:
            print("Error: No se pudo establecer conexión con la base de datos")
            return None
        
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM users WHERE role_id = %s", (role_id,))
                return [User(**user) for user in cursor.fetchall()]
        except Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn.is_connected():
                conn.close()