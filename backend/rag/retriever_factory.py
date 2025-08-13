import os
from .chroma import ChromaRetriever
from .faiss import FaissRetriever

def get_retriever(mode: str | None = None):
    mode = (mode or os.environ.get("RAG_BACKEND", "chroma")).lower()
    if mode == "chroma":
        return ChromaRetriever()
    if mode == "faiss":
        return FaissRetriever()
    raise ValueError(f"Unknown retriever mode: {mode}")