from flask import Blueprint, request, jsonify
from backend.rag.retriever_factory import get_retriever
import json

search_bp = Blueprint("search", __name__, url_prefix="/search")

@search_bp.get("")
def search():
    q = request.args.get("q", "", type=str)
    k = request.args.get("k", 5, type=int)
    mode = request.args.get("mode", "faiss")
    where_str = request.args.get("where")
    where = None
    if where_str:
        try:
            where = json.loads(where_str)
        except Exception:
            return jsonify({"ok": False, "error": "invalid where JSON"}), 400

    if not q:
        return jsonify({"ok": False, "error": "missing q"}), 400

    retriever = get_retriever(mode)
    hits = retriever.search(q, top_k=k, where=where)
    return jsonify({"ok": True, "query": q, "k": k, "hits": hits})
