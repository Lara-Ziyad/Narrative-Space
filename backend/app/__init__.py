import os
from flask import Flask
from dotenv import load_dotenv
from .main.routes import main_bp
from .auth.routes import auth_bp
from .ai.routes import ai_bp
from extensions import db, bcrypt, login_manager, client


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret')

    # Set a reliable absolute path for SQLite
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, '..', 'instance', 'db.sqlite3')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

    # init extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    # init OpenAI client
    app.openai_client = client(api_key=os.getenv("OPENAI_API_KEY"))

    # register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(ai_bp, url_prefix='/ai')

    # ensure DB tables exist
    with app.app_context():
        db.drop_all()
        print("🔻 Dropped all tables")
        db.create_all()
        print("🔺 Creates tables")

    return app
