from .faiss_retriever import FaissRetriever
from .chroma_retriever import ChromaRetriever

def get_retriever(mode: str = "faiss"):
    if mode == "chroma":
        return ChromaRetriever()
    return FaissRetriever()
