"""Application configuration loaded from environment variables."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


ENV_FILE = Path(__file__).resolve().parents[1] / ".env"


class Settings(BaseSettings):
    """Runtime settings for the backend service."""

    app_name: str = "Lenny Growth Assistant"
    app_env: str = "development"
    database_url: str = Field(
        min_length=1,
        validation_alias="DATABASE_URL",
        description="PostgreSQL SQLAlchemy connection URL.",
    )
    database_pool_size: int = 5
    database_max_overflow: int = 10
    llm_provider: str = "ollama"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    knowledge_base_path: Path = Path("knowledge")

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached settings, failing clearly for missing configuration."""

    if not ENV_FILE.is_file():
        raise RuntimeError(
            f"Required environment file was not found: {ENV_FILE}. "
            "Create it from .env.example and set DATABASE_URL."
        )

    return Settings()
