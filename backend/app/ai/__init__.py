from flask import Blueprint
from .generate import generate_bp
from .routes import ai_bp as routes_bp
from .routes_kb import kb_bp
from .routes_search import search_bp
from .models import models_bp

ai_bp = Blueprint("ai", __name__)


ai_bp.register_blueprint(generate_bp)
ai_bp.register_blueprint(routes_bp)

ai_bp.register_blueprint(kb_bp)
ai_bp.register_blueprint(search_bp)

ai_bp.register_blueprint(models_bp)