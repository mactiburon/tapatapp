from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from dao.comment_dao import CommentDAO

comments_bp = Blueprint('comments', __name__)

@comments_bp.route('/child/<int:child_id>', methods=['GET'])
@jwt_required()
def get_comments_by_child(child_id):
    comments = CommentDAO.get_comments_by_child(child_id)
    return jsonify([comment.to_dict() for comment in comments]) if comments else jsonify([]), 200

@comments_bp.route('/', methods=['POST'])
@jwt_required()
def create_comment():
    data = request.get_json()
    required_fields = ['child_id', 'text']
    
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    comment_id = CommentDAO.create_comment(
        data['child_id'],
        get_jwt_identity(),
        data['text'],
        data.get('important', False)
    )
    
    if comment_id:
        comment = CommentDAO.get_comment_by_id(comment_id)
        return jsonify(comment.to_dict()), 201
    return jsonify({"error": "Failed to create comment"}), 400