import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infrastructure.feature_extractor import get_feature_extractor
from app.infrastructure.vector_db import get_qdrant_client

__all__ = ["lifespan"]


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    get_feature_extractor()

    yield

    await get_qdrant_client().close()
