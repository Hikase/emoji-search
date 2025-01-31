from typing import Annotated

from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse

from app.api.dependency import (
    DBConnectionDep,
    FeatureExtractorDep,
    SearchGatewayDep,
)
from app.api.model import ListModel, MessageModel
from app.api.response import get_json_response
from app.api.v1.mapper import create_emoji_model
from app.api.v1.model import FeedbackModel, SearchResultModel
from app.domain.use_case import uc_autocomplete, uc_search, uc_send_feedback

__all__ = ["api_v1"]

api_v1 = APIRouter(prefix="/v1", tags=["v1"])


@api_v1.get(
    path="/search",
    status_code=status.HTTP_200_OK,
    response_model=SearchResultModel,
)
async def search_emoji(
    query: Annotated[str, Query(alias="q")],
    connection: DBConnectionDep,
    search_gateway: SearchGatewayDep,
    feature_extractor: FeatureExtractorDep,
) -> JSONResponse:
    result = await uc_search(
        query=query,
        connection=connection,
        search_gateway=search_gateway,
        feature_extractor=feature_extractor,
    )

    return get_json_response(
        SearchResultModel(
            items=[create_emoji_model(emoji) for emoji in result["items"]],
            search_uid=result["search_uid"],
        )
    )


@api_v1.get(
    path="/autocomplete",
    status_code=status.HTTP_200_OK,
    response_model=SearchResultModel,
)
async def autocomplete_shortcode(
    shortcode: Annotated[str, Query(alias="q", max_length=127)],
    search_gateway: SearchGatewayDep,
) -> JSONResponse:
    return get_json_response(
        ListModel(
            items=[
                create_emoji_model(emoji)
                for emoji in await uc_autocomplete(
                    shortcode=(shortcode or ":").lower(), search_gateway=search_gateway
                )
            ]
        )
    )


@api_v1.post(
    path="/feedback",
    status_code=status.HTTP_201_CREATED,
    response_model=MessageModel,
)
async def feedback(
    feedback: FeedbackModel,
    connection: DBConnectionDep,
) -> JSONResponse:
    await uc_send_feedback(
        search_uid=feedback.search_uid,
        relevant_emoji=feedback.relevant_emoji,
        rationale=feedback.rationale,
        connection=connection,
    )

    return get_json_response(
        MessageModel(message="Feedback received."),
        status_code=status.HTTP_201_CREATED,
    )
