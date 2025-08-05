
import chromadb
from uuid import uuid4
from .base import BaseRetriever
from .embedder import Embedder

class ChromaRetriever(BaseRetriever):
    def __init__(self, collection_name="architecture_knowledge"):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.embedder = Embedder()

    def add_texts(self, texts: list[str], metadatas: list[dict] = None):
        embeddings = self.embedder.encode(texts)
        ids = [str(uuid4()) for _ in texts]
        self.collection.add(documents=texts, embeddings=embeddings, ids=ids, metadatas=metadatas)

    def search(self, query: str, top_k=3, where: dict = None):
        embedding = self.embedder.encode([query])
        result = self.collection.query(query_embeddings=embedding, n_results=top_k, where=where)
        return result["documents"][0] if result["documents"] else []
