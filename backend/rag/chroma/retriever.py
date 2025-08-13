import chromadb
from uuid import uuid4
from backend.rag.base import BaseRetriever
from backend.rag.embedder import Embedder
from .persistence import get_chroma_path

class ChromaRetriever(BaseRetriever):
    def __init__(self, collection_name="architecture_knowledge"):
        path = get_chroma_path()
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.embedder = Embedder()

    def add_texts(self, texts: list[str], metadatas: list[dict] = None):
        metadatas = metadatas or [{} for _ in texts]
        embeddings = self.embedder.encode(texts)
        ids = [str(uuid4()) for _ in texts]
        self.collection.upsert(documents=texts, embeddings=embeddings, ids=ids, metadatas=metadatas)

    def search(self, query: str, top_k=3, where: dict = None):
        embedding = self.embedder.encode([query])
        if where:
            result = self.collection.query(query_embeddings=embedding, n_results=top_k, where=where)
        else:
            result = self.collection.query(query_embeddings=embedding, n_results=top_k)

        docs = result.get("documents", [[]])[0]
        mids = result.get("metadatas", [[]])[0]
        ids = result.get("ids", [[]])[0]
        dists = result.get("distances", [[]])[0]
        out = []
        for i, txt in enumerate(docs):
            dist = dists[i] if dists and i < len(dists) else None
            score = (1.0 / (1.0 + dist)) if dist is not None else None
            out.append({"id": ids[i], "text": txt, "score": score, "metadata": mids[i]})
        return out

    def clear(self):
        """
        Deletes and recreates the Chroma collection to remove all stored data.
        Works for both in-memory and persistent Chroma clients.
        """
        name = self.collection.name
        try:
            self.client.delete_collection(name)  # Drop the current collection
        except Exception:
            # If collection does not exist or an error occurs, just recreate it
            pass

        # Create a fresh empty collection
        self.collection = self.client.get_or_create_collection(name=name)
