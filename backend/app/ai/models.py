# [NS-STEP6-PR1] Added: standalone endpoint to list available AI models for the UI (versioned path).
from flask import Blueprint, jsonify
from flask_login import login_required

models_bp = Blueprint("ai_models", __name__)

@models_bp.route("/models/", methods=['GET'])  # <= versioned to avoid collisions with any legacy /ai/models
@login_required
def list_models_v1():
    # [NS-STEP6-PR1] Curated list (6 items). UI shows label=id only.
    curated = [
        {"provider": "openai",     "id": "gpt-4.1-mini",   "label": "gpt-4.1-mini"},
        {"provider": "openai",     "id": "gpt-4o-mini",    "label": "gpt-4o-mini"},
        {"provider": "openai",     "id": "gpt-4o",         "label": "gpt-4o"},
        {"provider": "anthropic",  "id": "claude-3-haiku", "label": "claude-3-haiku"},
        {"provider": "google",     "id": "gemini-1.5-pro", "label": "gemini-1.5-pro"},
        {"provider": "ollama",     "id": "llama3",         "label": "llama3"},
    ]
    resp = jsonify(curated)
    resp.headers["X-NS-Models-Source"] = "curated-v1"
    return resp, 200
