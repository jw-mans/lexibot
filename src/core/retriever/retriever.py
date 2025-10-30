from typing import List

# TODO: Implement a embedding-based retriever

class Retriever:
    def __init__(self):
        self.store: dict[int, List[str]] = {}

    def add_document(self, 
        user_id: int, 
        chunks: List[str]
    ):
        self.store[user_id] = chunks

    def get_relevant_chunks(self, 
        user_id: int, 
        top_k: int = 3
    ) -> List[str]:
        chunks = self.store.get(user_id, [])
        return chunks[-top_k:]
    
    