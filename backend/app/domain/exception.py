from collections.abc import Sequence
from enum import StrEnum, auto
from typing import override

from fastapi import status
from multidict import CIMultiDict
from pydantic.dataclasses import dataclass

__all__ = [
    "DataConflictError",
    "EmojiSearchError",
    "ErrorCode",
    "ErrorDetail",
    "ServiceUnavailableError",
]


class ErrorCode(StrEnum):
    @override
    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[str]
    ) -> str:
        return name.upper()

    GENERIC_ERROR = auto()
    NOT_FOUND_ERROR = auto()
    VALIDATION_ERROR = auto()
    SERVICE_UNAVAILABLE_ERROR = auto()


@dataclass(kw_only=True, slots=True, frozen=True)
class ErrorDetail:
    code: ErrorCode = ErrorCode.GENERIC_ERROR
    detail: str


class EmojiSearchError(Exception):
    """The base class for all emoji search app exceptions."""

    title: str = "An unexpected error occurred."
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(
        self,
        errors: Sequence[ErrorDetail] | ErrorDetail,
        /,
        *,
        title: str | None = None,
        status_code: int | None = None,
        headers: CIMultiDict[str] | None = None,
    ) -> None:
        super().__init__(title)

        if isinstance(errors, ErrorDetail):
            errors = [errors]

        if title:
            self.title = title
        if status_code is not None:
            self.status_code = status_code

        self.errors: Sequence[ErrorDetail] = errors
        self.headers = headers


class DataConflictError(EmojiSearchError):
    title = "Data conflict error."
    status_code = status.HTTP_409_CONFLICT


class ServiceUnavailableError(EmojiSearchError):
    title = "Service unavailable."
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
