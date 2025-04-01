from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from dao.tap_dao import TapDAO

taps_bp = Blueprint('taps', __name__)

@taps_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_taps():
    taps = TapDAO.get_all_taps()
    return jsonify([tap.to_dict() for tap in taps]) if taps else jsonify([]), 200

@taps_bp.route('/<int:tap_id>', methods=['GET'])
@jwt_required()
def get_tap(tap_id):
    tap = TapDAO.get_tap_by_id(tap_id)
    return jsonify(tap.to_dict()) if tap else (jsonify({"error": "Tap not found"}), 404)

@taps_bp.route('/', methods=['POST'])
@jwt_required()
def create_tap():
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