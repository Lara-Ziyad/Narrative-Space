import uuid
import numpy as np
import faiss
from backend.rag.base import BaseRetriever
from backend.rag.embedder import Embedder
from .persistence import save, load, clear as clear_store
from .utils import l2_to_score

class FaissRetriever(BaseRetriever):
    def __init__(self):
        self.embedder = Embedder()
        # Ensure we can robustly determine the embedding dim
        probe = self.embedder.encode(["__probe__"])
        probe = np.array(probe, dtype="float32")
        if probe.ndim == 1:  # (dim,) -> (1, dim)
            probe = probe.reshape(1, -1)
        self.dim = probe.shape[1]

        self.index, self.items = load(self.dim)
        if self.index is None:
            self.index = faiss.IndexFlatL2(self.dim)
            self.items = []

    def add_texts(self, texts: list[str], metadatas: list[dict] = None):
        metadatas = metadatas or [{} for _ in texts]
        embeddings = self.embedder.encode(texts)
        embeddings = np.array(embeddings, dtype="float32")
        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)
        self.index.add(embeddings)
        for txt, meta in zip(texts, metadatas):
            self.items.append({"id": str(uuid.uuid4()), "text": txt, "metadata": meta})
        save(self.index, self.items)

    def search(self, query: str, top_k=3, where: dict = None):
        try:
            q_emb = self.embedder.encode([query])
            q_emb = np.array(q_emb, dtype="float32")
            if q_emb.ndim == 1:
                q_emb = q_emb.reshape(1, -1)

            D, I = self.index.search(q_emb, top_k)
            out = []
            for rank, idx in enumerate(I[0]):
                if idx < 0 or idx >= len(self.items):
                    continue
                item = self.items[idx]
                if where and not all(item["metadata"].get(k_) == v_ for k_, v_ in where.items()):
                    continue
                score = l2_to_score(float(D[0][rank]))
                out.append({"id": item["id"], "text": item["text"], "score": score, "metadata": item["metadata"]})
            return out
        except Exception as e:
            print("[FaissRetriever.search] ERROR:", repr(e))
            raise

    def clear(self):
        """
        Clears all data from the FAISS index and resets it to an empty state.
        Also resets the in-memory list of stored texts.
        """
        try:
            from .persistence import clear as clear_store  # Clear persisted FAISS data if available
            clear_store()
        except Exception:
            # If no persistence layer exists or an error occurs, just proceed with reset
            pass

        # Reinitialize FAISS index and stored items
        self.index = faiss.IndexFlatL2(self.dim)
        self.texts = []
