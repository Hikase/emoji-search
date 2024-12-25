from collections.abc import Sequence
from functools import cache
from typing import Any

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.openapi.constants import REF_PREFIX
from fastapi.responses import JSONResponse
from multidict import CIMultiDict
from pydantic import BaseModel

__all__ = ["get_json_response", "get_response_schema"]

HTTP_PORT = 80
HTTPS_PORT = 443
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


# def get_error_json_response(
#     exception: BmnGalleryErrorsException,
#     /,
#     *,
#     headers: CIMultiDict[str] | None = None,
# ) -> JSONResponse:
#     headers = headers or CIMultiDict()
#     if exception.headers:
#         headers.extend(exception.headers)

#     return get_json_response(
#         ErrorResponseScheme(
#             title=exception.title,
#             detail=exception.detail,
#             errors=exception.errors,
#         ),
#         status_code=exception.status_code,
#         headers=headers,
#     )


@cache
def get_response_schema(
    *,
    model: type[BaseModel],
    is_error: bool = False,
) -> dict[str, Any]:
    media_type = "application/problem+json" if is_error else "application/json"
    return {
        "model": model,
        "content": {media_type: {"schema": {"$ref": f"{REF_PREFIX}{model.__name__}"}}},
    }
