from functools import cache
from pathlib import Path

from dotenv import find_dotenv
from pydantic import HttpUrl, Secret, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.domain.value_object import SqliteDsn

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
    collection_name: str = "emojis"

    model_path: Path

    sqlite_dsn: SqliteDsn = SqliteDsn("sqlite+aiosqlite:///emoji_search.db")


@cache
def get_app_settings() -> _AppSettings:
    return _AppSettings()  # pyright: ignore [reportCallIssue]
