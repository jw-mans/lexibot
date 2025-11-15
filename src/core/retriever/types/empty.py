from ..base import Retriever
from typing import List

class EmptyRetriever(Retriever):
    def retrieve(self,
        document: str,
        query: str,
        top_k: int = 3
    ) -> str:
        pass