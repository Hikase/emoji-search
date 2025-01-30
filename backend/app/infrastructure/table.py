from pydantic import UUID4
from sqlalchemy import (
    UUID,
    Column,
    DateTime,
    Float,
    ForeignKey,
    MetaData,
    String,
    Table,
    func,
)

__all__ = ["feedback_table", "metadata", "search_history_table"]


metadata = MetaData()

search_history_table = Table(
    "search_history",
    metadata,
    Column[UUID4]("search_uid", UUID, primary_key=True),
    Column("query", String, nullable=False),
    Column[float]("duration", Float, nullable=False),
    Column("result", String, nullable=False),
    Column("searched_at", DateTime, nullable=False, default=func.now()),
)

feedback_table = Table(
    "feedback",
    metadata,
    Column[UUID4]("feedback_uid", UUID, primary_key=True),
    Column[UUID4]("search_uid", UUID, ForeignKey("search_history.search_uid")),
    Column("relevant_emoji", String, nullable=False),
    Column("rationale", String, nullable=True),
)
