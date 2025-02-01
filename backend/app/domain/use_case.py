from collections.abc import Sequence
from typing import TypedDict

from pydantic import UUID4

from app.domain.value_object import Emoji
from app.infrastructure.db import DBConnection
from app.infrastructure.feature_extractor import FeatureExtractor
from app.infrastructure.gateway import SearchGateway
from app.infrastructure.repo import FeedbackRepo, SearchHistoryRepo
from app.utils.time import stopwatch


class SearchResult(TypedDict):
    items: Sequence[Emoji]
    search_uid: UUID4 | None


async def uc_search(
    *,
    query: str,
    connection: DBConnection,
    search_gateway: SearchGateway,
    feature_extractor: FeatureExtractor,
) -> SearchResult:
    if not query:
        return SearchResult(items=[], search_uid=None)

    with stopwatch() as search_time:
        search_result = await search_gateway.semantic_search(
            feature_extractor.embed(f"query: {query}")[0]
        )

    async with connection.begin():
        search_uid = await SearchHistoryRepo(connection).save(
            query=query,
            duration=search_time.duration,
            result=[emoji.emoji for emoji in search_result],
        )

    return SearchResult(items=search_result, search_uid=search_uid)


async def uc_autocomplete(
    *,
    shortcode: str,
    search_gateway: SearchGateway,
) -> Sequence[Emoji]:
    return await search_gateway.search_by_shortcode(shortcode)


async def uc_send_feedback(
    *,
    search_uid: UUID4,
    relevant_emoji: str,
    rationale: str,
    connection: DBConnection,
) -> None:
    async with connection.begin():
        await FeedbackRepo(connection).save(
            search_uid=search_uid, relevant_emoji=relevant_emoji, rationale=rationale
        )
