from ..config import settings
from .llm.client import GPTClient
from .llm.pipeline import Pipeline
from .store import UserStore, HistoryStore

class Core:
    def __init__(self):
        self.client = GPTClient()
        self.pipeline = Pipeline(self.client)
        self.user_store = UserStore(settings.UPLOAD_DIR)
        self.history_store = HistoryStore()

    def get_user_content(self, user_id: int) -> str:
        return self.user_store.get_content(user_id)
    
    def add_history(self, user_id: int, role: str, text: str):
        self.history_store.add_message(user_id, role, text)

    def get_history(self, user_id: int):
        return self.history_store.get_history(user_id)