from flask import Flask
from dotenv import load_dotenv
from models import db, User
import os
from flask_login import LoginManager

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret')  # Session security
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'         # SQLite DB configuration

# Bind SQLAlchemy to the app
db.init_app(app)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Basic route to test the API
@app.route('/')
def index():
    return "NarrativeSpace API is running!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

