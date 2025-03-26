from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from dao.historial_dao import HistorialDAO

historial_bp = Blueprint('historial', __name__)

@historial_bp.route('/child/<int:child_id>', methods=['GET'])
@jwt_required()
def get_historial_by_child(child_id):
    historial = HistorialDAO.get_historial_by_child(child_id)
    return jsonify([h.to_dict() for h in historial]) if historial else jsonify([]), 200

@historial_bp.route('/', methods=['POST'])
@jwt_required()
def create_historial():
    data = request.get_json()
    required_fields = ['child_id', 'data', 'hora', 'estat', 'totalHores']
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    historial_id = HistorialDAO.create_historial(
        data['child_id'],
        data['data'],
        data['hora'],
        data['estat'],
        data['totalHores']
    )
    
    if historial_id:
        historial = HistorialDAO.get_historial_by_id(historial_id)
        return jsonify(historial.to_dict()), 201
    return jsonify({"error": "Failed to create historial"}), 400