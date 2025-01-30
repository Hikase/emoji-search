from functools import cache
from typing import NoReturn

from qdrant_client import AsyncQdrantClient
from qdrant_client.http.exceptions import ResponseHandlingException

from app.domain.exception import ErrorCode, ErrorDetail, ServiceUnavailableError
from app.settings import get_app_settings
from app.utils.exception_handling import ExceptionManager

__all__ = ["get_qdrant_client", "qdrant_exception_manager"]


@cache
def get_qdrant_client() -> AsyncQdrantClient:
    api_key = get_app_settings().qdrant_api_key
    return AsyncQdrantClient(
        url=get_app_settings().qdrant_url.get_secret_value().unicode_string(),
        api_key=(api_key.get_secret_value() if api_key else None),
    )


qdrant_exception_manager = ExceptionManager[NoReturn]()


@qdrant_exception_manager.register(ResponseHandlingException)
def handle_response_handling_exception(exc: ResponseHandlingException) -> NoReturn:
    if "connection attempts failed" in str(exc):
        raise ServiceUnavailableError(
            ErrorDetail(
                code=ErrorCode.SERVICE_UNAVAILABLE_ERROR,
                detail="Please try again later.",
            )
        ) from exc
    raise exc
