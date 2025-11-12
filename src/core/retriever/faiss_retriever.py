# WARNING!!!!!!
# UNTESTED AND INCOMPLETE FILE!!!
# DO NOT USE OR EDIT UNTIL MARKED AS COMPLETE!!!
# TODO: DELETE THIS WARNING WHEN DONE


from __future__ import annotations
import os
import math
import pickle
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import faiss
from sentence_transformers import SentenceTransformer

import numpy as np

from ...config import settings

def default_chunking(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Chunk text by words with overlap. Returns list of chunks."""
    words = text.split()
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")
    chunks = []
    i = 0
    n = len(words)
    while i < n:
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))
        i += (chunk_size - overlap)
    return chunks

class FAISSRetriever:
    """
    FAISS-backed per-user retriever:
    - When add_document called: chunk text -> embed chunks -> upsert into user index and metadata
    - get_relevant_chunks: embed query -> search faiss -> return text chunks
    - Persistence: index and meta saved into VECTOR_DB_DIR per user
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2", vector_dim: Optional[int] = None):
        self.base_dir = Path(settings.VECTOR_DB_DIR)
        self.base_dir.mkdir(parents=True, exist_ok=True)

        self.model_name = model_name
        self.emb_model = None
        self.emb_model = SentenceTransformer(self.model_name)
        vector_dim = self.emb_model.get_sentence_embedding_dimension()
        self.vector_dim = vector_dim or 384

        self.store_meta: Dict[int, Dict[str, Any]] = {}  # in-memory mapping for quick access
                                                         # WARNING! do not scale for large data! Use on-disk only
                                                         # TODO: implement proper on-disk only management

    # some persistence helpers
    def _user_dir(self, user_id: int) -> Path:
        d = self.base_dir / str(user_id)
        d.mkdir(parents=True, exist_ok=True)
        return d

    def _index_path(self, user_id: int) -> str:
        return str(self._user_dir(user_id) / "faiss.index")

    def _meta_path(self, user_id: int) -> str:
        return str(self._user_dir(user_id) / "meta.pkl")

    def _load_user(self, user_id: int) -> Tuple[Optional[Any], List[str]]:
        """
        Load FAISS index and metadata for user if present.
        """
        idx_path = self._index_path(user_id)
        meta_path = self._meta_path(user_id)
        texts = []
        idx = None
        if os.path.exists(meta_path):
            with open(meta_path, "rb") as f:
                meta = pickle.load(f)
                texts = meta.get("texts", [])
                self.store_meta[user_id] = meta
        if os.path.exists(idx_path):
            idx = faiss.read_index(idx_path)
        return idx, texts

    def _save_user(self, user_id: int, index, texts: List[str]):
        meta = {"texts": texts}
        with open(self._meta_path(user_id), "wb") as f:
            pickle.dump(meta, f)
        if index is not None:
            faiss.write_index(index, self._index_path(user_id))
        self.store_meta[user_id] = meta

    # ---- interface ----
    def add_document(self, user_id: int, text: str, chunk_size: int = 400, overlap: int = 50) -> None:
        """
        Chunk text, compute embeddings, and add to user's FAISS index (or create new).
        """
        chunks = default_chunking(text, chunk_size=chunk_size, overlap=overlap)
        if len(chunks) == 0:
            return

        # embed chunks
        if self.emb_model is None:
            # fallback simple hashing to vector (NOT ideal) — but keep backward compat
            embeddings = [self._fallback_embed(c) for c in chunks]
        else:
            embeddings = self.emb_model.encode(chunks, convert_to_numpy=True, show_progress_bar=False)

        # load existing
        idx, existing_texts = self._load_user(user_id)
        existing_count = len(existing_texts)

        if idx is None:
            index = faiss.IndexFlatIP(self.vector_dim)  # inner product (cosine with normalized vectors)
            # we will normalize vectors to unit norm
        else:
            index = idx
        # normalize embeddings
        emb = np.array(embeddings, dtype=np.float32)
        # L2 normalize to use inner product as cosine
        norms = np.linalg.norm(emb, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        emb = emb / norms
        index.add(emb)
        texts = existing_texts + chunks
        self._save_user(user_id, index, texts)

    def get_relevant_chunks(self, user_id: int, query: str, top_k: int = 3) -> List[str]:
        """
        Return top_k most similar chunks for query.
        """
        if self.emb_model is None:
            q_emb = self._fallback_embed(query)
            q_emb = np.array(q_emb, dtype=np.float32).reshape(1, -1)
        else:
            q_emb = self.emb_model.encode([query], convert_to_numpy=True)

        # normalize q
        q_emb = q_emb.astype(np.float32)
        q_norm = np.linalg.norm(q_emb, axis=1, keepdims=True)
        q_norm[q_norm == 0] = 1.0
        q_emb = q_emb / q_norm

        idx, texts = self._load_user(user_id)
        if idx is not None:
            D, I = idx.search(q_emb, top_k)
            idxs = [int(i) for i in I[0] if i != -1]
            results = [texts[i] for i in idxs]
            return results
        else:
            # fallback: dot product with stored embeddings
            meta = self.store_meta.get(user_id)
            if meta is None:
                # try load
                meta_path = self._meta_path(user_id)
                if os.path.exists(meta_path):
                    with open(meta_path, "rb") as f:
                        meta = pickle.load(f)
                        self.store_meta[user_id] = meta
            if meta is None:
                return []

            emb_arr = meta.get("embeddings")  # shape (n, dim)
            texts = meta.get("texts", [])
            if emb_arr is None or len(texts) == 0:
                return []

            # compute cosine similarity
            emb_arr = np.array(emb_arr, dtype=np.float32)
            qv = q_emb[0]
            sims = emb_arr.dot(qv)
            idxs = np.argsort(sims)[::-1][:top_k]
            return [texts[int(i)] for i in idxs.tolist()]

    def _fallback_embed(self, text: str):
        # Very rough fallback: character-level hashing to vector
        v = np.zeros(self.vector_dim, dtype=np.float32)
        for i, ch in enumerate(text):
            v[i % self.vector_dim] += ord(ch)
        # normalize
        norm = np.linalg.norm(v)
        if norm == 0:
            return v.tolist()
        return (v / norm).tolist()
