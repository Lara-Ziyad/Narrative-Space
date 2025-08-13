from flask import Blueprint, request, jsonify
from backend.rag.retriever_factory import get_retriever
import uuid

kb_bp = Blueprint("kb", __name__, url_prefix="/kb")

@kb_bp.post("/add")
def kb_add():
    data = request.get_json(silent=True) or {}
    docs = data.get("docs", [])
    if not docs:
        return jsonify({"ok": False, "error": "no docs"}), 400

    texts = [d["text"] for d in docs]
    metadatas = [d.get("metadata", {}) for d in docs]
    retriever = get_retriever(data.get("mode", "faiss"))
    retriever.add_texts(texts, metadatas)
    return jsonify({"ok": True, "count": len(texts)})

@kb_bp.post("/clear")
def kb_clear():
    data = request.get_json(silent=True) or {}
    retriever = get_retriever(data.get("mode", "faiss"))
    retriever.clear()
    return jsonify({"ok": True})

@kb_bp.post("/reindex")
def kb_reindex():
    """
    Rebuild the index from scratch:
    1. Clear the current index for the selected mode.
    2. Add all provided documents.
    """
    data = request.get_json(silent=True) or {}
    mode = data.get("mode", "faiss")
    docs = data.get("docs", [])

    if not docs:
        return jsonify({"ok": False, "error": "No docs provided"}), 400

    retriever = get_retriever(mode)

    # Step 1: Clear existing index
    retriever.clear()

    # Step 2: Add new documents
    texts = [d["text"] for d in docs]
    metadatas = [d.get("metadata", {}) for d in docs]
    retriever.add_texts(texts, metadatas)

    return jsonify({"ok": True, "mode": mode, "count": len(texts)})