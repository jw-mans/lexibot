from typing import List
from ..base import Retriever

class SimpleRetriever(Retriever):
    def __init__(self, chunk_size: int = 500):
        self.chunk_size = chunk_size

    def split_document(self, document: str) -> List[str]:
        words = document.split()
        return [" ".join(words[i:i+self.chunk_size]) for i in range(0, len(words), self.chunk_size)]

    def add_document(self, user_id: int, chunks: List[str]):
        self.sessions = getattr(self, "sessions", {})
        self.sessions[user_id] = chunks

    def retrieve(self, document: str, query: str, top_k: int = 3) -> str:
        chunks = self.split_document(document)
        query_words = set(query.lower().split())
        scored_chunks = [(len(query_words & set(chunk.lower().split())), chunk) for chunk in chunks]
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        top_chunks = [chunk for score, chunk in scored_chunks[:top_k] if score > 0]
        return "\n".join(top_chunks) if top_chunks else "\n".join(chunks[:top_k])
