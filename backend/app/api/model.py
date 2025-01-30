from collections.abc import Sequence

from pydantic import BaseModel

from app.domain.exception import ErrorDetail

__all__ = ["ErrorModel", "ListModel", "MessageModel"]


class ErrorModel(BaseModel):
    title: str
    errors: Sequence[ErrorDetail]


class ListModel[T: BaseModel | str | int](BaseModel):
    items: Sequence[T]


class MessageModel(BaseModel):
    message: str
