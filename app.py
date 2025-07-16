from flask import Flask,  request, jsonify
from dotenv import load_dotenv
from models import db, User
import os
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
import openai

# Load environment variables from .env file
load_dotenv()


# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret')  # Session security
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'         # SQLite DB configuration

# Bind SQLAlchemy to the app
db.init_app(app)

# Initialize Bcrypt after app is created
bcrypt = Bcrypt(app)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Add OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Basic route to test the API
@app.route('/')
def index():
    return "NarrativeSpace API is running!"

# Route to register a new user
@app.route('/register', methods=['POST'])
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

# Route to log in an existing user
@app.route('/login', methods=['POST'])
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

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/profile')
@login_required
def profile():
    return jsonify({
        'message': 'Welcome to your profile',
        'username': current_user.username,
        'email': current_user.email
    })

@app.route('/openai-status')
def openai_status():
    try:
        models = openai.Model.list()
        return jsonify({"status": "OpenAI connected", "models": len(models.data)})
    except Exception as e:
        return jsonify({"status": "Error", "details": str(e)}), 500

@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({'message': 'You are not logged in. Please log in to continue.'}), 401

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=8000, debug=True)
print(User)
