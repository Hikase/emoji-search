from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_v1
from app.feature_extractor import get_feature_extractor
from app.vector_db.client import get_qdrant_client


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    get_feature_extractor()

    yield

    await get_qdrant_client().close()


origins = [
    "*",
]

app = FastAPI(lifespan=lifespan)
app.include_router(api_v1)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello Bigger Applications!"}
