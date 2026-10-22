import json
from functools import lru_cache
from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment or .env file."""

    DATABASE_URL: str = "postgresql+psycopg://taskflow:taskflow@localhost:5432/taskflow"
    TEST_DATABASE_URL: str = "postgresql+psycopg://taskflow:taskflow@localhost:5432/taskflow_test"
    CORS_ORIGINS: Union[List[str], str] = ["http://localhost:5173"]
    APP_ENV: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("CORS_ORIGINS", mode="after")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            # Try parsing as JSON list first (e.g. '["http://..."]')
            stripped = v.strip()
            if stripped.startswith("[") and stripped.endswith("]"):
                try:
                    parsed = json.loads(stripped)
                    if isinstance(parsed, list):
                        return [str(item).strip() for item in parsed if str(item).strip()]
                except json.JSONDecodeError:
                    pass
            # Fall back to comma-separated parsing (e.g. 'http://localhost:5173,https://...')
            return [origin.strip() for origin in stripped.split(",") if origin.strip()]
        return v


@lru_cache
def get_settings() -> Settings:
    """Returns a cached instance of application settings."""
    return Settings()
