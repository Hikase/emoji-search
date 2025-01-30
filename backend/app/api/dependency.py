from typing import Annotated

from fastapi import Depends
from qdrant_client import AsyncQdrantClient

from app.infrastructure.db import DBConnection, create_connection
from app.infrastructure.feature_extractor import FeatureExtractor, get_feature_extractor
from app.infrastructure.gateway import SearchGateway
from app.infrastructure.vector_db import get_qdrant_client
from app.settings import (
    _AppSettings,  # pyright: ignore [reportPrivateUsage]
    get_app_settings,
)

__all__ = [
    "AppSettingsDep",
    "DBConnectionDep",
    "FeatureExtractorDep",
    "QdrantClientDep",
    "SearchGatewayDep",
]

AppSettingsDep = Annotated[_AppSettings, Depends(get_app_settings)]
QdrantClientDep = Annotated[AsyncQdrantClient, Depends(get_qdrant_client)]
FeatureExtractorDep = Annotated[FeatureExtractor, Depends(get_feature_extractor)]
DBConnectionDep = Annotated[DBConnection, Depends(create_connection)]


def _get_search_gateway(
    client: QdrantClientDep, settings: AppSettingsDep
) -> SearchGateway:
    return SearchGateway(
        client=client,
        collection_name=settings.collection_name,
    )


SearchGatewayDep = Annotated[SearchGateway, Depends(_get_search_gateway)]
