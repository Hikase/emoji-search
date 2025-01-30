from collections.abc import Sequence

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from multidict import CIMultiDict
from pydantic import BaseModel

__all__ = ["get_json_response"]

MINIMUM_STATUS_PROBLEM_JSON = 400


def get_json_response(
    payload: BaseModel | Sequence[BaseModel],
    /,
    *,
    status_code: int = status.HTTP_200_OK,
    headers: CIMultiDict[str] | None = None,
) -> JSONResponse:
    headers = headers or CIMultiDict()
    headers.setdefault("Content-Language", "en")

    return JSONResponse(
        content=jsonable_encoder(payload),
        status_code=status_code,
        headers=headers,
        media_type=(
            "application/json"
            if status_code < MINIMUM_STATUS_PROBLEM_JSON
            else "application/problem+json"
        ),
    )
