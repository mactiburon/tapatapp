from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from dao.user_dao import UserDAO
from utils.decorators import role_required
from models.user import User

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
@jwt_required()
@role_required(1)  # Solo admin puede listar todos los usuarios
def get_all_users():
    """
    Obtiene todos los usuarios (solo administrador)
    ---
    tags:
      - Users
    security:
      - JWT: []
    responses:
      200:
        description: Lista de usuarios
        schema:
          type: array
          items:
            $ref: '#/definitions/User'
      403:
        description: No autorizado
    """
    users = UserDAO.get_all_users()
    return jsonify([user.to_dict() for user in users]) if users else jsonify([]), 200

@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """
    Obtiene un usuario específico por ID
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    security:
      - JWT: []
    responses:
      200:
        description: Datos del usuario
        schema:
          $ref: '#/definitions/User'
      404:
        description: Usuario no encontrado
    """
    current_user_id = get_jwt_identity()
    
    # Solo permite ver el propio perfil o si es admin
    if int(current_user_id) != user_id and not UserDAO.get_user_by_id(current_user_id).role_id == 1:
        return jsonify({"error": "Unauthorized"}), 403
    
    user = UserDAO.get_user_by_id(user_id)
    return jsonify(user.to_dict()) if user else (jsonify({"error": "User not found"}), 404)

@users_bp.route('/', methods=['POST'])
@jwt_required()
@role_required(1)  # Solo admin puede crear usuarios
def create_user():
    """
    Crea un nuevo usuario (solo administrador)
    ---
    tags:
      - Users
    parameters:
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/UserCreate'
    security:
      - JWT: []
    responses:
      201:
        description: Usuario creado
        schema:
          $ref: '#/definitions/User'
      400:
        description: Datos inválidos
    """
    data = request.get_json()
    required_fields = ['username', 'password', 'email', 'role_id']
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Validar que el rol existe
    if data['role_id'] not in [1, 2, 3, 4]:  # IDs de roles válidos
        return jsonify({"error": "Invalid role"}), 400

    # Verificar si el email ya existe
    if UserDAO.get_user_by_credentials(data['email'], data['password']):
        return jsonify({"error": "Email already in use"}), 400

    user_id = UserDAO.create_user(
        data['username'],
        data['password'],
        data['email'],
        data['role_id']
    )
    
    if user_id:
        user = UserDAO.get_user_by_id(user_id)
        return jsonify(user.to_dict()), 201
    return jsonify({"error": "Failed to create user"}), 400

@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """
    Actualiza un usuario
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          $ref: '#/definitions/UserUpdate'
    security:
      - JWT: []
    responses:
      200:
        description: Usuario actualizado
        schema:
          $ref: '#/definitions/User'
      403:
        description: No autorizado
    """
    current_user_id = get_jwt_identity()
    current_user = UserDAO.get_user_by_id(current_user_id)
    
    # Solo permite actualizar el propio perfil o si es admin
    if int(current_user_id) != user_id and not current_user.role_id == 1:
        return jsonify({"error": "Unauthorized"}), 403
    
    data = request.get_json()
    updates = {}
    
    if 'username' in data:
        updates['username'] = data['username']
    if 'email' in data:
        updates['email'] = data['email']
    if 'password' in data and data['password']:
        updates['password'] = data['password']
    if 'role_id' in data and current_user.role_id == 1:  # Solo admin puede cambiar roles
        updates['role_id'] = data['role_id']
    
    if not updates:
        return jsonify({"error": "No fields to update"}), 400
    
    success = UserDAO.update_user(user_id, **updates)
    if success:
        updated_user = UserDAO.get_user_by_id(user_id)
        return jsonify(updated_user.to_dict()), 200
    return jsonify({"error": "Failed to update user"}), 400

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required(1)  # Solo admin puede eliminar usuarios
def delete_user(user_id):
    """
    Elimina un usuario (solo administrador)
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    security:
      - JWT: []
    responses:
      200:
        description: Usuario eliminado
      404:
        description: Usuario no encontrado
    """
    # No permitir eliminarse a sí mismo
    if int(get_jwt_identity()) == user_id:
        return jsonify({"error": "Cannot delete yourself"}), 400
    
    user = UserDAO.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    success = UserDAO.delete_user(user_id)
    return jsonify({"success": success}), 200 if success else 400

@users_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """r_id = get_jwt_identity()
    Obtiene el usuario actualy_id(user_id)
    ---urn jsonify(user.to_dict()), 200    tags:      - Users    security:      - JWT: []    responses:      200:        description: Datos del usuario actual        schema:          $ref: '#/definitions/User'    """    
    user_id = get_jwt_identity()    
    user = UserDAO.get_user_by_id(user_id)    
    return jsonify(user.to_dict()), 200