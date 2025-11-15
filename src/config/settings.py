from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    YANDEX_API_KEY: str
    YANDEX_API_KEY_ID: str
    YANDEX_API_MODEL_URI: str
    YANDEX_CLOUD_CATALOG_ID: str

    UPLOAD_DIR: str = str(BASE_DIR / "storage" / "uploads")
    VECTOR_DB_DIR: str = str(BASE_DIR / "storage" / "db")

    class Config:
        env_file = BASE_DIR / "src" / "config" / ".env"


class Config:
    def __init__(self):
        settings = Settings()

        self.telegram_bot_token = settings.TELEGRAM_BOT_TOKEN
        self.upload_dir = settings.UPLOAD_DIR
        self.vector_db_dir = settings.VECTOR_DB_DIR

        self.yandex_api_key = settings.YANDEX_API_KEY
        self.yandex_api_key_id = settings.YANDEX_API_KEY_ID
        self.yandex_api_model_uri = settings.YANDEX_API_MODEL_URI
        self.yandex_cloud_catalog_id = settings.YANDEX_CLOUD_CATALOG_ID

        self.yandex_api_url = 'https://llm.api.cloud.yandex.net/v1'
        self.yandex_gpt_model = f'gpt://{self.yandex_cloud_catalog_id}/yandexgpt/rc'


config = Config()
