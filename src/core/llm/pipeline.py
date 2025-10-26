from .client import GPTClient

class Pipeline:
    def __init__(self, client: GPTClient):
        self.client = client

    def ask(self, 
        context: str, 
        question: str,
        max_tokens: int = 2000,
    ) -> str:
        messages = [
            {
                "role": "system",
                "text": f"""
                Ты - умный ассистент, анализирующий документы. 
                Необходимо ответить на вопрос пользователя, 
                используя предоставленный документ.
                """,
            },
            {
                "role": "assistant",
                "text": f"Документ: \n{context[:4000]}",
            },
            {
                "role": "user",
                "text": f"Вопрос: {question}",
            }
        ]
        return self.client.complete(messages, 
            max_tokens=max_tokens
        )