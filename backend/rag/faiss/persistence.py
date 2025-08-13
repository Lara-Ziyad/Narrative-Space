import os, json
import faiss

STORE_DIR = os.path.join("backend", "storage", "faiss")
INDEX_PATH = os.path.join(STORE_DIR, "index.faiss")
META_PATH = os.path.join(STORE_DIR, "meta.jsonl")

def ensure_store():
    os.makedirs(STORE_DIR, exist_ok=True)

def save(index, items):
    ensure_store()
    faiss.write_index(index, INDEX_PATH)
    with open(META_PATH, "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")

def load(dim: int):
    ensure_store()
    index = None
    items = []
    if os.path.exists(INDEX_PATH):
        index = faiss.read_index(INDEX_PATH)
    if os.path.exists(META_PATH):
        with open(META_PATH, "r", encoding="utf-8") as f:
            items = [json.loads(line) for line in f]
    return index, items

def clear():
    ensure_store()
    for p in (INDEX_PATH, META_PATH):
        if os.path.exists(p):
            os.remove(p)
