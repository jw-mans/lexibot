from functools import lru_cache
from ..core import Core
from ..core.llm import GPTClient
from ..core.history import HistoryStore
from ..core.retriever import (
    Retriever, EmptyRetriever, SimpleRetriever
)

@lru_cache
def get_core() -> Core:
    """
    Единый экземпляр Core (Singleton-like).
    Используется и FastAPI, и Telegram, и Gradio.
    """
    client = GPTClient()
    history = HistoryStore()
    retriever: SimpleRetriever = SimpleRetriever()   # можно заменить на FAISS/TF-IDF/etc

    return Core(
        client=client,
        history_store=history,
        retriever=retriever
    )
