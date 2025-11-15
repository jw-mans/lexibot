from typing import List
from ..config import config
from .llm.client import GPTClient
from .history.history import HistoryStore
from .retriever.types.simple import SimpleRetriever
from .user_store.user_store import UserStore

class Core:

    user_store = UserStore(config.upload_dir)

    @staticmethod
    def save_file(user_id: int, file_name: str, content: str) -> str:
        return Core.user_store.save_file(user_id, file_name, content)

    @staticmethod
    def make_messages(context: str, history: List[dict], question: str) -> List[dict]:
        return [
            {
                "role": "system", 
                "content": (
                    "Ты — интеллектуальный ассистент, который отвечает на вопросы по документу. "
                    "Используй контекст документа и историю диалога для более точных ответов."
                )
            },
            {
                "role": "assistant", 
                "content": f"Документ:\n{context}"
            },
            *history,
            {
                "role": "user", 
                "content": question
            }
        ]

    def __init__(self,
                 client: GPTClient = GPTClient(),
                 history_store: HistoryStore = HistoryStore(),
                 retriever: SimpleRetriever = SimpleRetriever()):
        self.client = client
        self.retriever = retriever
        self.history_store = history_store

    async def ask(self, user_id: int, question: str, max_tokens: int = 2000) -> str:
        # 1. История
        history = self.history_store.get_history(user_id)
        # 2. Контент пользователя
        document = self.user_store.get_content(user_id)
        if not document:
            return "Документы пользователя не найдены."
        # 3. Релевантные чанки
        context = self.retriever.retrieve(document, question)
        # 4. Сообщения для LLM
        messages = Core.make_messages(context, history, question)
        # 5. Ответ от LLM
        answer = await self.client.complete(messages, max_tokens=max_tokens)
        # 6. Сохраняем историю
        self.history_store.add_message(user_id, role='user', text=question)
        self.history_store.add_message(user_id, role='assistant', text=answer)
        return answer
