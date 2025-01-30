from contextlib import (
    AbstractContextManager,
)
from time import perf_counter
from types import TracebackType
from typing import Self


class stopwatch(AbstractContextManager["stopwatch"]):  # noqa: N801
    def __init__(self) -> None:
        self._start = 0
        self._end = 0

    @property
    def duration(self) -> float:
        if self._end != 0:
            return self._end - self._start
        return perf_counter() - self._start

    @property
    def start(self) -> float:
        return self._start

    def __enter__(self) -> Self:
        self._start = perf_counter()

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        self._end = perf_counter()

        return None
