import chromadb
from uuid import uuid4
from sentence_transformers import SentenceTransformer
from .base import BaseRetriever

class ChromaRetriever(BaseRetriever):
    def __init__(self, collection_name="architecture_knowledge"):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def add_texts(self, texts: list[str], metadatas: list[dict] = None):
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        ids = [str(uuid4()) for _ in texts]
        self.collection.add(documents=texts, embeddings=embeddings, ids=ids, metadatas=metadatas)

    def search(self, query: str, top_k=3, where: dict = None):
        embedding = self.model.encode([query], convert_to_numpy=True)
        result = self.collection.query(query_embeddings=embedding, n_results=top_k, where=where)
        return result["documents"][0] if result["documents"] else []
