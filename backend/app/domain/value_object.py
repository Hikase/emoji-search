from collections.abc import Sequence
from typing import NewType

import numpy as np
import numpy.typing as npt
from pydantic import AnyUrl, UrlConstraints, constr
from pydantic.dataclasses import dataclass

__all__ = ["Emoji", "EmojiKeyword", "EmojiShortcode", "F32Array", "SqliteDsn"]


EmojiShortcode = NewType("EmojiShortcode", constr(max_length=127))

EmojiKeyword = NewType("EmojiKeyword", constr(max_length=127))


@dataclass(frozen=True, slots=True, kw_only=True)
class Emoji:
    emoji: str
    shortcode: EmojiShortcode
    keywords: Sequence[EmojiKeyword]


type F32Array = npt.NDArray[np.float32]


class SqliteDsn(AnyUrl):
    _constraints = UrlConstraints(
        allowed_schemes=["sqlite", "sqlite+aiosqlite", "sqlite+pysqlcipher"],
        host_required=False,
    )

    @property
    def host(self) -> str:
        """The required URL host."""
        return self._url.host  # pyright: ignore[reportReturnType]
