
from flask import Blueprint
from .generate import generate_bp
from .routes import ai_bp as routes_bp

ai_bp = Blueprint("ai", __name__)

ai_bp.register_blueprint(generate_bp)
ai_bp.register_blueprint(routes_bp)
