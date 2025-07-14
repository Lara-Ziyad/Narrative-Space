from flask import Flask
from dotenv import load_dotenv
from models import db
from flask_sqlalchemy import SQLAlchemy
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

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

