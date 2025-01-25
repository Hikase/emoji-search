from typing import Annotated

from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse

from app.api.dependency import FeatureExtractorDep, QdrantClientDep
from app.api.model import ListModel
from app.api.response import get_json_response
from app.api.v1.mapper import create_emoji_model
from app.api.v1.model import EmojiModel
from app.domain.use_case import uc_search

__all__ = ["api_v1"]

api_v1 = APIRouter(prefix="/v1", tags=["v1"])


@api_v1.get(
    path="/search",
    status_code=status.HTTP_200_OK,
    response_model=ListModel[EmojiModel],
)
async def search_emoji(
    query: Annotated[str, Query(alias="q")],
    client: QdrantClientDep,
    feature_extractor: FeatureExtractorDep,
) -> JSONResponse:
    result = await uc_search(
        query=query, client=client, feature_extractor=feature_extractor
    )

    return get_json_response(
        ListModel(items=[create_emoji_model(emoji) for emoji in result])
    )
