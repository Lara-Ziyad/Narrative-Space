
from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts: list[str], to_numpy=True):
        return self.model.encode(texts, convert_to_numpy=to_numpy)
