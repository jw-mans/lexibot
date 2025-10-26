from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    YANDEX_API_KEY: str
    YANDEX_API_KEY_ID: str
    YANDEX_API_MODEL_URI: str
    YANDEX_API_URL: str
    YANDEX_CLOUD_CATALOG_ID: str

    UPLOAD_DIR: str = str(BASE_DIR / "lexibot" / "storage" / "uploads")
    VECTOR_DB_DIR: str = str(BASE_DIR / "lexibot"/ "storage" / "db")

    class Config:
        env_file = BASE_DIR / "src" / "config" / ".env"

settings = Settings()
