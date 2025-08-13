import os

def get_chroma_path():
    path = os.path.join("backend", "storage", "chroma")
    os.makedirs(path, exist_ok=True)
    return path
