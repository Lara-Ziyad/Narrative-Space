import os
from .retriever_factory import get_retriever

def load_knowledge_from_folder(folder_path: str) -> list[str]:
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            path = os.path.join(folder_path, filename)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

                chunks = [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]
                documents.extend(chunks)
    return documents

def main():
    mode = "faiss"
    retriever = get_retriever(mode)

    folder = os.path.join(os.path.dirname(__file__), "..", "data")
    docs = load_knowledge_from_folder(folder)


    print(f"📚 Loaded {len(docs)} total chunks from data")
    retriever.add_texts(docs)
    print(f"✅ Embedded and stored into: {mode}")



if __name__ == "__main__":
    main()
