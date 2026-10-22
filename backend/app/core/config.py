from functools import lru_cache
from typing import List
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment or .env file."""

    DATABASE_URL: str = "postgresql+psycopg://taskflow:taskflow@localhost:5432/taskflow"
    TEST_DATABASE_URL: str = "postgresql+psycopg://taskflow:taskflow@localhost:5432/taskflow_test"
    CORS_ORIGINS: List[str] = ["http://localhost:5173"]
    APP_ENV: str = "development"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        if isinstance(v, str):
            # Parse comma-separated string into cleaned list of origin URLs
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v


@lru_cache
def get_settings() -> Settings:
    """Returns a cached instance of application settings."""
    return Settings()
