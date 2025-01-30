from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.api.model import ErrorModel
from app.api.response import get_json_response
from app.domain.exception import EmojiSearchError, ErrorDetail

__all__ = ["emoji_search_error_fastapi_handler", "unexpected_exception_fastapi_handler"]


def unexpected_exception_fastapi_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    return get_json_response(
        ErrorModel(
            title="Request could not be processed.",
            errors=[
                ErrorDetail(
                    detail="An unexpected error occurred. Please try again later.",
                )
            ],
        ),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def emoji_search_error_fastapi_handler(
    request: Request, exc: EmojiSearchError
) -> JSONResponse:
    """Default FastAPI exception handler"""
    return get_json_response(
        ErrorModel(title=exc.title, errors=exc.errors),
        status_code=exc.status_code,
        headers=exc.headers,
    )
