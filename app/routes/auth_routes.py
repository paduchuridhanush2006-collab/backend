from flask import Blueprint, request, jsonify
from ..models import User
from ..utils.auth_utils import validate_email, validate_password, generate_token
from flask_jwt_extended import jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400

    if not validate_email(email):
        return jsonify({'message': 'Invalid email format'}), 400

    if not validate_password(password):
        return jsonify({'message': 'Password must be at least 6 characters'}), 400

    if User.find_by_email(email):
        return jsonify({'message': 'Email already exists'}), 400

    user_id = User.create_user(username, email, password)
    token = generate_token(user_id)

    return jsonify({
        'token': token,
        'user': {
            'id': str(user_id),
            'username': username,
            'email': email
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Missing email or password'}), 400

    user = User.find_by_email(email)
    if not user or not User.verify_password(user['password'], password):
        return jsonify({'message': 'Invalid credentials'}), 401

    token = generate_token(user['_id'])

    return jsonify({
        'token': token,
        'user': {
            'id': str(user['_id']),
            'username': user['username'],
            'email': user['email']
        }
    }), 200

@auth_bp.route('/verify', methods=['GET'])
@jwt_required()
def verify():
    current_user_id = get_jwt_identity()
    user = User.find_by_id(current_user_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404

    return jsonify({
        'user': {
            'id': str(user['_id']),
            'username': user['username'],
            'email': user['email']
        }
    }), 200
