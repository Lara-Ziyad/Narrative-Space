from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from openai import OpenAI

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
client = OpenAI