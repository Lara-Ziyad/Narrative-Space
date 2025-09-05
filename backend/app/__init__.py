import os
from flask import Flask
from dotenv import load_dotenv
from .main.routes import main_bp
from .auth.routes import auth_bp
from backend.extensions import db, bcrypt, login_manager, client
from flask_cors import CORS
from .ai import  ai_bp
# from .ai.models.routes import models_bp

print("[NS] backend package __init__ loaded")  # TEMP debug; remove later if you want.
__all__ = []

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret')
    CORS(app, supports_credentials=True)

    # Provider clients (import here to avoid circular imports during tests)
    from backend.app.ai.clients_bootstrap import attach_openai, attach_anthropic,attach_ollama,attach_gemini

    if not hasattr(app, "openai_client"):
        attach_openai(app)
    if not hasattr(app, "anthropic_client"):
        attach_anthropic(app)
    if not hasattr(app, "ollama_client"):
        attach_ollama(app)
    if not hasattr(app, "gemini_on"):
        attach_gemini(app)

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
    # app.register_blueprint(models_bp)
    # ensure DB tables exist
    with app.app_context():
        # db.drop_all()
        # print("🔻 Dropped all tables")
        db.create_all()
        print("🔺 Creates tables")
        # Check routers
        print([r.rule for r in app.url_map.iter_rules() if r.rule.startswith("/ai/")])
        routes = sorted({r.rule for r in app.url_map.iter_rules() if r.rule.startswith("/ai/")})
        print("[NS] AI routes:", routes)
    return app
