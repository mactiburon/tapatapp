from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from dao.child_dao import ChildDAO

children_bp = Blueprint('children', __name__)

@children_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_children():
    children = ChildDAO.get_all_children()
    return jsonify([child.to_dict() for child in children]) if children else jsonify([]), 200

@children_bp.route('/<int:child_id>', methods=['GET'])
@jwt_required()
def get_child(child_id):
    child = ChildDAO.get_child_by_id(child_id)
    return jsonify(child.to_dict()) if child else (jsonify({"error": "Child not found"}), 404)

@children_bp.route('/', methods=['POST'])
@jwt_required()
def create_child():
    data = request.get_json()
    required_fields = ['child_name', 'sleep_average', 'treatment_id', 'time', 'informacioMedica']
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    child_id = ChildDAO.create_child(
        data['child_name'],
        data['sleep_average'],
        data['treatment_id'],
        data['time'],
        data['informacioMedica']
    )
    
    if child_id:
        child = ChildDAO.get_child_by_id(child_id)
        return jsonify(child.to_dict()), 201
    return jsonify({"error": "Failed to create child"}), 400