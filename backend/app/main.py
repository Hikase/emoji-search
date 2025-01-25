from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_v1
from app.lifespan import lifespan

origins = [
    "*",
]

app = FastAPI(title="Emoji Search", lifespan=lifespan)
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
    return {"message": "Emoji Search 🤔 API"}
