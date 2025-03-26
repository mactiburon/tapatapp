from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity  # Añade esta importación
)
from dao.user_dao import UserDAO

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = UserDAO.get_user_by_credentials(email, password)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    
    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user.to_dict()
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)  # Ahora jwt_required está definido
def refresh():
    current_user = get_jwt_identity()  # get_jwt_identity ahora está definido
    new_token = create_access_token(identity=current_user)
    return jsonify(access_token=new_token), 200

@auth_bp.route('/protected', methods=['GET'])
@jwt_required()  # Decorador correctamente importado
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200