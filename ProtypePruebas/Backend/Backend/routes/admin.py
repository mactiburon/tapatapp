from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from utils.decorators import role_required
from dao.user_dao import UserDAO

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@role_required(1)  # Solo admin
def admin_get_users():
    users = UserDAO.get_all_users()
    return jsonify([user.to_dict() for user in users]), 200

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required(1)
def admin_delete_user(user_id):
    success = UserDAO.delete_user(user_id)
    return jsonify({"success": success}), 200 if success else 400