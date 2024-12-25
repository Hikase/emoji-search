from collections.abc import Sequence

from pydantic import BaseModel

__all__ = ["ErrorModel", "ListModel"]


class ErrorModel(BaseModel):
    title: str
    detail: str | None = None


class ListModel[T: BaseModel | str | int](BaseModel):
    type: str = "list"
    items: Sequence[T]
