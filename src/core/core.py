from ..config import settings
from .llm.client import GPTClient
from .llm.pipeline import Pipeline
from .store import UserStore, HistoryStore
from .retriever import Retriever, chunking

class Core:

    chunk_size_words = 500
    top_k = 3
    max_context_words = 1500

    @staticmethod
    def get_chunk_size_words() -> int:
        return Core.chunk_size_words
    
    @staticmethod
    def get_top_k() -> int:
        return Core.top_k
    
    @staticmethod
    def get_max_context_words() -> int:  
        return Core.max_context_words
    
    def __init__(self):
        self.client = GPTClient()
        self.pipeline = Pipeline(self.client)
        self.user_store = UserStore(settings.UPLOAD_DIR)
        self.history_store = HistoryStore()
        self.retriever = Retriever()

    def save_file(self,
        user_id: int,
        file_name: str,
        content: str
    ) -> str:
        path = self.user_store.save_file(user_id, file_name, content)
        chunks = chunking(content,
            chunk_size=Core.get_chunk_size_words()
        )
        self.retriever.add_document(user_id, chunks)
        return path

    async def ask(self,
        user_id: int, 
        question: str,
        history: list[dict] = [],    
    ):
        chunks = self.retriever.get_relevant_chunks(
            user_id=user_id,
            query=question,
            top_k=Core.get_top_k()
        )
        if not chunks: context = self.user_store.get_content(user_id)
        else:
            context_words = []
            total = 0
            for chunk in chunks:
                words = chunk.split()
                if total + len(words) > Core.get_max_context_words():
                    break
                context_words.extend(words)
                total += len(words)
            context = ' '.join(context_words)

        return await self.pipeline.ask(
            context=context,
            question=question,
            history=history
        )
    
    def get_user_content(self, 
        user_id: int
    ) -> str:
        return self.user_store.get_content(user_id)
    
    def add_history(self,
        user_id: int,
        role: str,
        text: str,
    ):
        self.history_store.add_message(
            user_id=user_id,
            role=role,
            text=text
        )
    
    def get_history(self,
        user_id: int,
    ) -> list[dict]:
        return self.history_store.get_history(user_id)
    
    