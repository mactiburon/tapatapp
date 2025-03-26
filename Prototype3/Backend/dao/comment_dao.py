from models.comment import Comment
from utils.database import get_db_connection
from mysql.connector import Error
from datetime import datetime

class CommentDAO:
    @staticmethod
    def get_comments_by_child(child_id):
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM comments WHERE child_id = %s", (child_id,))
                return [Comment(**comment) for comment in cursor.fetchall()]
        except Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn.is_connected():
                conn.close()

    @staticmethod
    def get_comment_by_id(comment_id):
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM comments WHERE id = %s", (comment_id,))
                result = cursor.fetchone()
                return Comment(**result) if result else None
        except Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            if conn.is_connected():
                conn.close()

    @staticmethod
    def create_comment(child_id, user_id, text, important=False):
        conn = get_db_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO comments (child_id, user_id, text, important, timestamp) VALUES (%s, %s, %s, %s, %s)",
                    (child_id, user_id, text, important, datetime.now())
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
    def update_comment(comment_id, text=None, important=None):
        conn = get_db_connection()
        if not conn:
            return False
        
        try:
            with conn.cursor() as cursor:
                updates = []
                params = []
                
                if text is not None:
                    updates.append("text = %s")
                    params.append(text)
                if important is not None:
                    updates.append("important = %s")
                    params.append(important)
                
                if not updates:
                    return False
                
                query = "UPDATE comments SET " + ", ".join(updates) + " WHERE id = %s"
                params.append(comment_id)
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
    def delete_comment(comment_id):
        conn = get_db_connection()
        if not conn:
            return False
        
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM comments WHERE id = %s", (comment_id,))
                conn.commit()
                return cursor.rowcount > 0
        except Error as e:
            print(f"Database error: {e}")
            conn.rollback()
            return False
        finally:
            if conn.is_connected():
                conn.close()