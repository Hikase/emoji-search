from collections.abc import Sequence

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchText

from app.domain.value_object import Emoji, EmojiKeyword, EmojiShortcode, F32Array
from app.infrastructure.vector_db import qdrant_exception_manager

__all__ = ["SearchGateway"]


class SearchGateway:
    def __init__(
        self,
        *,
        client: AsyncQdrantClient,
        collection_name: str,
    ) -> None:
        self._client = client
        self._collection_name = collection_name

    @qdrant_exception_manager
    async def semantic_search(
        self,
        embedding: F32Array,
        *,
        limit: int = 32,
        score_threshold: float | None = None,
    ) -> Sequence[Emoji]:
        return [
            Emoji(
                emoji=point.payload["emoji"],
                shortcode=EmojiShortcode(point.payload["shortcode"]),
                keywords=[
                    EmojiKeyword(keyword) for keyword in point.payload["keywords"]
                ],
            )
            for point in await self._client.search(
                collection_name=self._collection_name,
                query_vector=embedding,
                limit=limit,
                score_threshold=score_threshold,
            )
            if point.payload is not None
        ]

    @qdrant_exception_manager
    async def search_by_shortcode(
        self, shortcode: str, limit: int = 10
    ) -> Sequence[Emoji]:
        return [
            Emoji(
                emoji=record.payload["emoji"],
                shortcode=EmojiShortcode(record.payload["shortcode"]),
                keywords=[
                    EmojiKeyword(keyword) for keyword in record.payload["keywords"]
                ],
            )
            for record in (
                await self._client.scroll(
                    collection_name=self._collection_name,
                    scroll_filter=Filter(
                        must=FieldCondition(
                            key="shortcode", match=MatchText(text=shortcode)
                        )
                    ),
                    limit=limit,
                )
            )[0]
            if record.payload is not None
        ]
