# backend/app/ai/models/routes.py

from flask import Blueprint, jsonify, request
from flask_login import login_required
from .registry import curated_models, now_iso

models_bp = Blueprint("ai_models", __name__)

def _pick_text_default(curated):
    # chose the first available model
    for m in curated:
        if m.get("available"):
            return f'{m["provider"]}:{m["id"]}'
    return "openai:gpt-4o-mini" # fallback


@models_bp.route("/models", methods=["GET"], strict_slashes=False)
@login_required
def list_models():
    curated = curated_models()
    fmt = (request.args.get("format") or "").lower()
    compact = (fmt == "compact") or (request.args.get("compact") in {"1", "true", "yes"})

    if compact:
        simple = [{"provider": m["provider"], "id": m["id"], "label": m["label"]} for m in curated]
        return jsonify(simple), 200

    defaults = {"text": _pick_text_default(curated)}
    envelope = {"models": curated, "meta": {"count": len(curated), "ts": now_iso(), "defaults": defaults}}
    return jsonify(envelope), 200


@models_bp.route("/models/<provider>/<model_id>", methods=["GET"], strict_slashes=False)
@login_required
def get_model(provider: str, model_id: str):
    provider = (provider or "").lower()
    for m in curated_models():
        if m["provider"] == provider and m["id"] == model_id:
            return jsonify(m), 200
    return jsonify({"error": "Model not found"}), 404
