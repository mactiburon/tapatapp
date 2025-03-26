from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from utils.decorators import role_required
from dao.child_dao import ChildDAO

medico_bp = Blueprint('medico', __name__)

@medico_bp.route('/children', methods=['GET'])
@jwt_required()
@role_required(2)  # Solo médico
def medico_get_children():
    children = ChildDAO.get_all_children()
    return jsonify([child.to_dict() for child in children]), 200