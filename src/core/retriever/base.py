from abc import ABC, abstractmethod
from typing import List

class Retriever(ABC):
    # @abstractmethod
    # def add_document(self, user_id: int, chunks: List[str]):
    #     pass

    @abstractmethod
    def retrieve(self, document: str, query: str, top_k: int = 3) -> str:
        pass
