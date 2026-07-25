"""Typed settings from environment / .env."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Required env for CLI flows — missing vars fail at construction."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str
    ollama_url: str
    analysis_model: str
    embedding_model: str


@lru_cache
def get_settings() -> Settings:
    """Load and cache settings; raises ValidationError if required vars missing."""
    return Settings()
