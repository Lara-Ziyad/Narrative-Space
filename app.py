from flask import Flask
from dotenv import load_dotenv
from models import db, User
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret')  # Session security
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'         # SQLite DB configuration

# Bind SQLAlchemy to the app
db.init_app(app)

# Basic route to test the API
@app.route('/')
def index():
    return "NarrativeSpace API is running!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

