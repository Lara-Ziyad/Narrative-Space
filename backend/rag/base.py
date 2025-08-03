from abc import ABC, abstractmethod

class BaseRetriever(ABC):
    @abstractmethod
    def add_texts(self, texts: list[str], metadatas: list[dict] = None):
        pass

    @abstractmethod
    def search(self, query: str, top_k=3, where: dict = None) -> list[str]:
        pass
