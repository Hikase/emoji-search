from pydantic import UUID4, BaseModel, Field

from app.api.model import ListModel
from app.domain.value_object import EmojiShortcode

__all__ = ["EmojiModel", "FeedbackModel", "SearchResultModel"]


class EmojiModel(BaseModel):
    emoji: str
    shortcode: EmojiShortcode


class SearchResultModel(ListModel[EmojiModel]):
    search_uid: UUID4 | None = None


class FeedbackModel(BaseModel):
    search_uid: UUID4
    relevant_emoji: str = Field(max_length=15)
    rationale: str = Field(max_length=511)
