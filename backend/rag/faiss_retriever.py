import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from .base import BaseRetriever

class FaissRetriever(BaseRetriever):
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(384)
        self.texts = []

    def add_texts(self, texts: list[str], metadatas: list[dict] = None):
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        self.index.add(np.array(embeddings))
        self.texts.extend(texts)

    def search(self, query: str, top_k=3, where: dict = None):
        embedding = self.model.encode([query], convert_to_numpy=True)
        D, I = self.index.search(embedding, top_k)
        return [self.texts[i] for i in I[0]]
