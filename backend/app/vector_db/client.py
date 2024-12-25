from functools import cache

from qdrant_client import AsyncQdrantClient

from app.settings import get_app_settings


@cache
def get_qdrant_client() -> AsyncQdrantClient:
    api_key = get_app_settings().qdrant_api_key
    return AsyncQdrantClient(
        url=get_app_settings().qdrant_url.get_secret_value().unicode_string(),
        api_key=(api_key.get_secret_value() if api_key else None),
    )
