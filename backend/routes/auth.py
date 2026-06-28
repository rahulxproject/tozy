from flask import Blueprint, request, jsonify
from models.user import User
from database import db
import jwt
from datetime import datetime, timedelta
from functools import wraps

auth_bp = Blueprint('auth', __name__)

# JWT Configuration
SECRET_KEY = 'your-secret-key-change-in-production'

def generate_token(user_id):
    """Generate JWT token"""
    payload = {
        'user_id': str(user_id),
        'exp': datetime.utcnow() + timedelta(hours=24),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def token_required(f):
    """Decorator to require JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token[7:]
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    return decorated

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    email = data['email']
    password = data['password']
    name = data.get('name')
    
    user_model = User(db)
    
    # Check if user already exists
    existing_user = user_model.get_user_by_email(email)
    if existing_user:
        return jsonify({'error': 'User already exists'}), 409
    
    # Create new user
    user = user_model.create_user(email, password, name)
    
    if user:
        token = generate_token(user['id'])
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'id': str(user['id']),
                'email': user['email'],
                'name': user['name']
            },
            'token': token
        }), 201
    
    return jsonify({'error': 'Failed to create user'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    email = data['email']
    password = data['password']
    
    user_model = User(db)
    user = user_model.get_user_by_email(email)
    
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if not User.verify_password(password, user['password_hash']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = generate_token(user['id'])
    
    return jsonify({
        'message': 'Login successful',
        'user': {
            'id': str(user['id']),
            'email': user['email'],
            'name': user['name'],
            'subscription_tier': user['subscription_tier']
        },
        'token': token
    }), 200

@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user():
    """Get current user info"""
    user_model = User(db)
    user = user_model.get_user_by_id(request.user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'user': {
            'id': str(user['id']),
            'email': user['email'],
            'name': user['name'],
            'subscription_tier': user['subscription_tier'],
            'preferences': user['preferences']
        }
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout():
    """Logout user (client-side token removal)"""
    return jsonify({'message': 'Logout successful'}), 200
