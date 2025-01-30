from collections.abc import AsyncIterator
from typing import NoReturn

from sqlalchemy import Engine, event
from sqlalchemy.engine.interfaces import DBAPIConnection
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncConnection, create_async_engine
from sqlalchemy.pool import ConnectionPoolEntry

from app.domain.exception import ErrorCode, ErrorDetail, ServiceUnavailableError
from app.settings import get_app_settings
from app.utils.exception_handling import ExceptionManager

__all__ = ["DBConnection", "create_connection", "db_exception_manager"]

engine = create_async_engine(url=get_app_settings().sqlite_dsn.unicode_string())


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(
    dbapi_connection: DBAPIConnection, connection_record: ConnectionPoolEntry
) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


type DBConnection = AsyncConnection


async def create_connection() -> AsyncIterator[DBConnection]:
    async with engine.connect() as connection:
        try:
            yield connection
        except Exception:
            await connection.rollback()
            raise


db_exception_manager = ExceptionManager[NoReturn]()


@db_exception_manager.register(OperationalError)
def handle_operational_error(exc: OperationalError) -> NoReturn:
    if "no such table" in str(exc):
        raise ServiceUnavailableError(
            ErrorDetail(
                code=ErrorCode.SERVICE_UNAVAILABLE_ERROR,
                detail="Please try again later.",
            )
        ) from exc
    raise exc
