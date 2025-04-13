from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from web_builder.app.auth import bp
from web_builder.app.models.user import User

@bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    
    # Validate request data
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    # Check password length
    if len(data['password']) < 8:
        return jsonify({'error': 'Password must be at least 8 characters long'}), 400
    
    # Create user
    user = User.create_user(data['email'], data['password'])
    
    if not user:
        return jsonify({'error': 'Email already exists'}), 409
    
    # Generate JWT token
    access_token = create_access_token(identity=str(user['_id']))
    
    return jsonify({
        'message': 'User registered successfully',
        'access_token': access_token,
        'user': user
    }), 201

@bp.route('/login', methods=['POST'])
def login():
    """Login an existing user."""
    data = request.get_json()
    
    # Validate request data
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    # Find user by email (password check needs the original document)
    user_doc = User.find_by_email(data['email'])
    print('user doc')
    print(user_doc)
    if not user_doc or not User.check_password(user_doc['password'], data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Update last login timestamp
    User.update_last_login(user_doc['_id'])
    
    # Convert to JSON-serializable format
    user = User.to_json(user_doc)
    user.pop('password', None)
    
    # Generate JWT token
    access_token = create_access_token(identity=user['_id'])
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': user
    }), 200

@bp.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    """Get the current user's information."""
    current_user_id = get_jwt_identity()
    
    user = User.find_by_id(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'user': user
    }), 200