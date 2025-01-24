from collections.abc import Sequence

from qdrant_client import AsyncQdrantClient

from app.domain.value_object import Emoji
from app.feature_extractor import FeatureExtractor
from app.settings import get_app_settings
from app.vector_db.repository import EmojiRepository


async def uc_search(
    *,
    query: str,
    client: AsyncQdrantClient,
    feature_extractor: FeatureExtractor,
) -> Sequence[Emoji]:
    if not query:
        return []

    return await EmojiRepository(
        client=client, collection_name=get_app_settings().collection_name
    ).semantic_search(embedding=feature_extractor.embed(query)[0])
