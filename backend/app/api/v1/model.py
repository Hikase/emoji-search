from pydantic import BaseModel

__all__ = ["EmojiModel"]


class EmojiModel(BaseModel):
    emoji: str
    shortcode: str
