from collections.abc import Sequence

from fastembed import TextEmbedding  # pyright: ignore [reportMissingTypeStubs]
from qdrant_client import AsyncQdrantClient

from app.domain.value_object import Embedding, Emoji
from app.settings import get_app_settings
from app.vector_db.repository import EmojiRepository


async def uc_search(
    *,
    query: str,
    client: AsyncQdrantClient,
    feature_extractor: TextEmbedding,
) -> Sequence[Emoji]:
    if not query:
        return []

    embedding: Embedding = next(
        iter(feature_extractor.embed(query))  # pyright: ignore [reportUnknownMemberType, reportUnknownArgumentType]
    )
    return await EmojiRepository(
        client=client, collection_name=get_app_settings().collection_name
    ).semantic_search(embedding, score_threshold=0.1)
