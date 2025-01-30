from collections.abc import Sequence
from uuid import uuid4

from pydantic import UUID4
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

from app.domain.exception import DataConflictError, ErrorCode, ErrorDetail
from app.infrastructure.db import DBConnection, db_exception_manager
from app.infrastructure.table import feedback_table, search_history_table

__all__ = ["FeedbackRepo", "SearchHistoryRepo"]


class SearchHistoryRepo:
    def __init__(self, /, connection: DBConnection) -> None:
        self._connection = connection

    @db_exception_manager
    async def save(
        self, /, *, query: str, duration: float, result: Sequence[str]
    ) -> UUID4:
        search_uid = uuid4()

        await self._connection.execute(
            insert(search_history_table).values(
                search_uid=search_uid,
                query=query,
                duration=duration,
                result=", ".join(result[:10]),
            )
        )

        return search_uid


class FeedbackRepo:
    def __init__(self, /, connection: DBConnection) -> None:
        self._connection = connection

    @db_exception_manager
    async def save(
        self, /, *, search_uid: UUID4, relevant_emoji: str, rationale: str
    ) -> None:
        try:
            await self._connection.execute(
                insert(feedback_table).values(
                    feedback_uid=uuid4(),
                    search_uid=search_uid,
                    relevant_emoji=relevant_emoji,
                    rationale=rationale,
                )
            )
        except IntegrityError as exc:
            raise DataConflictError(
                ErrorDetail(
                    detail=f"Search query with '{search_uid}' uid not found.",
                    code=ErrorCode.NOT_FOUND_ERROR,
                )
            ) from exc
