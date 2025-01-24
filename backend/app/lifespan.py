from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from huggingface_hub.utils import (  # pyright: ignore [reportMissingTypeStubs]
    disable_progress_bars,
)

from app.feature_extractor import get_feature_extractor
from app.vector_db.client import get_qdrant_client

__all__ = ["lifespan"]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Disable huggingface progress bars globally
    disable_progress_bars()
    get_feature_extractor()

    yield

    await get_qdrant_client().close()
