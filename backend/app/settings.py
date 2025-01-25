from functools import cache
from pathlib import Path

from dotenv import find_dotenv
from pydantic import HttpUrl, Secret, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = []


class _AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=find_dotenv(),
        env_prefix="emoji_search_",
        env_file_encoding="utf-8",
        extra="ignore",
        frozen=True,
    )

    qdrant_url: Secret[HttpUrl]
    qdrant_api_key: SecretStr | None = None
    collection_name: str = "emojis-2"

    model_path: Path


@cache
def get_app_settings() -> _AppSettings:
    return _AppSettings()  # pyright: ignore [reportCallIssue]
