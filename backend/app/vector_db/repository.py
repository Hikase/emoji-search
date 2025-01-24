from collections.abc import Sequence
from typing import cast

from qdrant_client import AsyncQdrantClient

from app.domain.value_object import Emoji, F32Array


class EmojiRepository:
    def __init__(self, *, client: AsyncQdrantClient, collection_name: str) -> None:
        self.client = client
        self.collection_name = collection_name

    async def semantic_search(
        self,
        embedding: F32Array,
        *,
        limit: int = 32,
        score_threshold: float | None = None,
    ) -> Sequence[Emoji]:
        return [
            Emoji(
                emoji=cast(str, point.payload.get("emoji")),
                shortcode=cast(str, point.payload.get("shortcode")),
                keywords=cast(Sequence[str], point.payload.get("keywords")),
            )
            for point in await self.client.search(
                collection_name=self.collection_name,
                query_vector=embedding,
                limit=limit,
                score_threshold=score_threshold,
            )
            if point.payload is not None
        ]
