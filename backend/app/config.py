"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Backend configuration loaded from environment variables."""

    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3"
    database_path: str = "../data/devbot.db"
    host: str = "0.0.0.0"
    port: int = 8000
    github_webhook_secret: str = ""
    discord_token: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
