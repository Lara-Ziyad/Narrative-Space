import os
from flask import Flask
from dotenv import load_dotenv
from .main.routes import main_bp
from .auth.routes import auth_bp
from backend.extensions import db, bcrypt, login_manager, client
from flask_cors import CORS
from .ai import  ai_bp, generate_bp, models_bp, ai_bp
from openai import OpenAI



def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret')
    CORS(app, supports_credentials=True)
    app.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
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
    app.register_blueprint(generate_bp, url_prefix='/ai')
    app.register_blueprint(models_bp, url_prefix="/ai")

    # ensure DB tables exist
    with app.app_context():
        # db.drop_all()
        # print("🔻 Dropped all tables")
        db.create_all()
        print("🔺 Creates tables")

    # Test
    try:
        import inspect
        with app.app_context():
            matches = [r for r in app.url_map.iter_rules() if r.rule == "/ai/models"]
            print("[NS] /ai/models rules count:", len(matches))
            for r in matches:
                fn = app.view_functions[r.endpoint]
                print(" ->", r.rule, "| endpoint:", r.endpoint,
                      "| methods:", sorted(r.methods),
                      "| module:", fn.__module__,
                      "| file:", inspect.getsourcefile(fn))
    except Exception as e:
        print("[NS] route debug error:", e)

    return app
