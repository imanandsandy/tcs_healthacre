import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
    OLLAMA_HOST = os.getenv(
        "OLLAMA_HOST",
        "http://localhost:11434"
    )
    APP_ENV = os.getenv("APP_ENV", "development")


settings = Settings()