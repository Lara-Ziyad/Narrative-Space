from flask import Blueprint, request, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from backend.models import User
from backend.extensions import db, bcrypt, login_manager

auth_bp = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check if username or email already exists
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return jsonify({'message': 'Username or email already exists'}), 409

    # Hash the password before storing
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password_hash=hashed_password)

    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Find user by email
    user = User.query.filter_by(email=email).first()

    # Check password hash
    if user and bcrypt.check_password_hash(user.password_hash, password):
        login_user(user)
        return jsonify({'message': 'Login successful'}), 200

    return jsonify({'message': 'Invalid email or password'}), 401

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/profile')
@login_required
def profile():
    return jsonify({
        'message': 'Welcome to your profile',
        'username': current_user.username,
        'email': current_user.email
    })


@auth_bp.app_errorhandler(401)
def unauthorized(e):
    return jsonify({'message': 'You are not logged in. Please log in to continue.'}), 401
