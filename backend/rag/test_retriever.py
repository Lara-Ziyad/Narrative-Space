from .retriever_factory import get_retriever

retriever = get_retriever(mode="chroma")  # أو "faiss"

texts = [
    "A quiet room with soft walls and filtered light.",
    "A spiraling staircase symbolizing infinity.",
    "A mirrored corridor reflecting endless depth."
]
metas = [{"type": "poetic"}, {"type": "symbolic"}, {"type": "philosophical"}]

retriever.add_texts(texts, metadatas=metas)
results = retriever.search("A structure that twists upward", top_k=2)

print("🔍 Results:")
for r in results:
    print("-", r)
