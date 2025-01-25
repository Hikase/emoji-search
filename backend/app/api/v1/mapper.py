from app.api.v1.model import EmojiModel
from app.domain.value_object import Emoji

__all__ = ["create_emoji_model"]


def create_emoji_model(emoji: Emoji, /) -> EmojiModel:
    return EmojiModel(emoji=emoji.emoji, shortcode=emoji.shortcode)
