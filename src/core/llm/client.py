import requests
from ...config import settings

class GPTClient:
    def __init__(self,
            api_key: str = settings.YANDEX_API_KEY,
            api_model_uri: str = settings.YANDEX_API_MODEL_URI,
            api_url: str = settings.YANDEX_API_URL
        ):
        self.api_key = api_key
        self.api_model_uri = api_model_uri
        self.api_url = api_url
    
    def complete(self, 
        messages: list[dict], 
        temperature: float = 0.6, 
        max_tokens: int = 2000, 
        stream: bool = False
    ) -> str:
        payload = {
            "modelUri": self.api_model_uri,
            "completionOptions": {
                "stream": stream,
                "temperature": temperature,
                "maxTokens": str(max_tokens)
            },
            "messages": messages
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Api-Key {self.api_key}"
        }

        response = requests.post(self.api_url, 
            headers=headers, 
            json=payload,
        )
        return response.json()
        