from collections.abc import Sequence

import numpy as np
import numpy.typing as npt
from pydantic.dataclasses import dataclass

__all__ = ["Emoji", "F32Array"]


@dataclass(frozen=True, slots=True, kw_only=True)
class Emoji:
    emoji: str
    shortcode: str
    keywords: Sequence[str]


type F32Array = npt.NDArray[np.float32]
