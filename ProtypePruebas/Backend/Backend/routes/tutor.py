from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from utils.decorators import role_required
from dao.tap_dao import TapDAO

tutor_bp = Blueprint('tutor', __name__)

@tutor_bp.route('/taps', methods=['POST'])
@jwt_required()
@role_required(3)  # Solo tutor
def tutor_create_tap():
    data = request.get_json()
    required_fields = ['child_id', 'status_id', 'init', 'end']
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    tap_id = TapDAO.create_tap(
        data['child_id'],
        data['status_id'],
        get_jwt_identity(),
        data['init'],
        data['end']
    )
    
    if tap_id:
        tap = TapDAO.get_tap_by_id(tap_id)
        return jsonify(tap.to_dict()), 201
    return jsonify({"error": "Failed to create tap"}), 400