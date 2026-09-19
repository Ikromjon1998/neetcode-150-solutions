"""Typed settings, read from the environment and validated at import time.

`pydantic-settings` is the FastAPI ecosystem's answer to NestJS's `ConfigModule` and
Laravel's `config/*.php` + `.env`. All three solve the same problem; the difference is when
they fail. This one fails at process start with a readable validation error, which is the
behaviour you want in a container that is about to serve traffic.
"""

from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="NEETCODE_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "NeetCode API (Python / FastAPI)"
    version: str = "1.0.0"
    debug: bool = False
    docs_url: str = "/docs"
    openapi_url: str = "/openapi.json"


@lru_cache
def get_settings() -> Settings:
    """Cached so the whole process shares one instance; override in tests via DI."""
    return Settings()
