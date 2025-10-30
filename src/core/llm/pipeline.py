from .client import GPTClient

class Pipeline:
    def __init__(self, client: GPTClient):
        self.client = client

    async def ask(self, 
        context: str, 
        question: str,
        history: list[dict] = [],
        max_tokens: int = 2000,
    ) -> str:
        messages = [
            {
                "role": "system", 
                "text": (
                "Ты — интеллектуальный ассистент, который отвечает на вопросы по документу. "
                "Используй контекст документа и историю диалога для более точных ответов."
                )
            },
            {
                "role": "assistant", 
                "text": f"Документ:\n{context}"
            },
            *history,
            {
                "role": "user", 
                "text": question
            }
        ]
        
        return await self.client.complete(messages,
            max_tokens=max_tokens
        )