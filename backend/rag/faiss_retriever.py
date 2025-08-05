
import faiss
import numpy as np
from .base import BaseRetriever
from .embedder import Embedder

class FaissRetriever(BaseRetriever):
    def __init__(self):
        self.embedder = Embedder()
        self.index = faiss.IndexFlatL2(384)
        self.texts = []

    def add_texts(self, texts: list[str], metadatas: list[dict] = None):
        embeddings = self.embedder.encode(texts)
        self.index.add(np.array(embeddings))
        self.texts.extend(texts)

    def search(self, query: str, top_k=3, where: dict = None):
        embedding = self.embedder.encode([query])
        D, I = self.index.search(embedding, top_k)
        return [self.texts[i] for i in I[0]]

