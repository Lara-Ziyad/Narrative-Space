
from flask import Blueprint, jsonify, request
from flask_login import login_required
from .registry import curated_models, now_iso

models_bp = Blueprint("ai_models", __name__)

@models_bp.get("/models")
@login_required
def list_models():
    """
    Default: descriptive envelope:
      {
        "models": [ {provider,id,label,description,capabilities,available,requires,limits,default_for}, ... ],
        "meta": { "count": N, "ts": "...", "defaults": {"text": "openai:gpt-4o-mini"} }
      }

    Backward-compatible compact mode:
      /ai/models?format=compact   OR   /ai/models?compact=1
      -> returns [ {provider,id,label}, ... ]
    """
    curated = curated_models()
    fmt = (request.args.get("format") or "").lower()
    compact = (fmt == "compact") or (request.args.get("compact") in {"1", "true", "yes"})

    header = "ns-descriptive" if not compact else "ns-compact"

    if compact:
        simple = [{"provider": m["provider"], "id": m["id"], "label": m["label"]} for m in curated]
        resp = jsonify(simple)
        resp.headers["X-NS-Models-Source"] = header
        return resp, 200

    defaults = {"text": "openai:gpt-4o-mini"}
    envelope = {
        "models": curated,
        "meta": {
            "count": len(curated),
            "ts": now_iso(),
            "defaults": defaults,
        },
    }
    resp = jsonify(envelope)
    resp.headers["X-NS-Models-Source"] = header
    return resp, 200


@models_bp.get("/models/<provider>/<model_id>")
@login_required
def get_model(provider: str, model_id: str):
    """
    Return a single model descriptor (404 if not found).
    Keeping it simple by searching the curated list.
    """
    provider = (provider or "").lower()
    items = curated_models()
    for m in items:
        if m["provider"] == provider and m["id"] == model_id:
            resp = jsonify(m)
            resp.headers["X-NS-Models-Source"] = "ns-descriptive"
            return resp, 200
    return jsonify({"error": "Model not found"}), 404
