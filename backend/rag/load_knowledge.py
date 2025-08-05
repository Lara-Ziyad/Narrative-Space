import os
from .retriever_factory import get_retriever

def chunk_text(text: str, max_length=300) -> list[str]:

    chunks = [chunk.strip() for chunk in text.split("\n") if chunk.strip()]
    return [c for c in chunks if len(c) <= max_length]

def load_knowledge_file(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def main():
    mode = "faiss"
    retriever = get_retriever(mode)

    path = os.path.join(os.path.dirname(__file__), "..", "data", "knowledge.txt")
    raw_text = load_knowledge_file(path)
    chunks = chunk_text(raw_text)

    print(f"📚 Loaded {len(chunks)} chunks from knowledge base.")
    retriever.add_texts(chunks)
    print(f"✅ Embedded and stored using:", mode)

if __name__ == "__main__":
    main()
