from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.controllers import users

user_bp = Blueprint('user', __name__)


@user_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """Get all the users"""
    return jsonify(users.get_users())


@user_bp.route('/users', methods=['POST'])
@jwt_required()
def create_user():
    """Creates a user"""
    data = request.get_json()
    try:
        user = users.create_user(data['name'])
    except ValueError as error:
        return jsonify({'error': str(error)})
    return jsonify({'message': f'Created user {user.name} with id {str(user.id)}'})


@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """Deletes user"""
    try:
        users.delete_user(user_id)
    except FileNotFoundError:
        return jsonify({'error': 'User not found'}, 404)
    return jsonify({'message': 'User deleted successfully'})
