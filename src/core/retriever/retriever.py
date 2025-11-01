from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Retriever:
    """
    Retriever realisation on TF-IDF + cosine similarity
    Holds for every user:
    - chunk list: List[str]
    - vectorizer (TfidfVectorizer)
    - matrix (sparse matrix)

    TODO : replace on FAISS + embeddings in prod
    """

    def __init__(self):
        self.store: Dict[int, Dict[str, Any]] = {}

    def add_document(self,
        user_id: int, 
        chunks: List[str]
    ) -> None:
        if not chunks:
            self.store[user_id] = {
                "chunks": [],
                "vectorizer": None,
                "matrix": None
            }
            return
        
        vectorizer = TfidfVectorizer()
        matrix = vectorizer.fit_transform(chunks)
        self.store[user_id] = {
            "chunks": chunks,
            "vectorizer": vectorizer,
            "matrix": matrix
        }

    def get_relevant_chunks(self,
        user_id: int, 
        query: str, 
        top_k: int = 3
    ) -> List[str]:
        entry = self.store.get(user_id)
        if not entry:
            return []
        
        vectorizer = entry.get('vectorizer')
        matrix = entry.get('matrix')
        chunks = entry.get('chunks')
        
        emptiness_condition = (
            vectorizer is None
            or matrix is None
            or len(chunks) == 0
        )
        if emptiness_condition:
            return []

        query_vec = vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, matrix).flatten()
        idxs = similarities.argsort()[::-1]  # descending similarity sort

        res = []
        for idx in idxs[:top_k]:
            res.append(chunks[int(idx)])
        return res


def chunking(
    text: str,
    chunk_size: int = 500,
) -> list[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks