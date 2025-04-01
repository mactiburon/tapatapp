# utils/decorators.py
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Importación diferida para romper el ciclo
            from dao.user_dao import UserDAO
            user_id = get_jwt_identity()
            user = UserDAO.get_user_by_id(user_id)
            
            if user and user.role_id == role:
                return f(*args, **kwargs)
            return jsonify({"error": "Access forbidden: insufficient permissions"}), 403
        return decorated_function
    return decorator