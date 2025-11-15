import openai
from ...config import config

class GPTClient(openai.OpenAI):
    def __init__(self,
                 api_key: str = config.yandex_api_key,
                 base_url: str = config.yandex_api_url,
                 project: str = config.yandex_cloud_catalog_id):
        super().__init__(
            api_key=api_key,
            base_url=base_url,
            project=project
        )

    async def complete(self,
                       messages: list[dict],
                       model: str = config.yandex_gpt_model,
                       max_tokens: int = 2000,
                       temperature: float = 0.6,
                       stream: bool = False) -> str:
        return self.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            stream=stream
        ).choices[0].message.content
