from typing import Annotated

from fastapi import Depends
from fastembed import TextEmbedding  # pyright: ignore [reportMissingTypeStubs]
from qdrant_client import AsyncQdrantClient

from app.feature_extractor import get_feature_extractor
from app.vector_db.client import get_qdrant_client

__all__ = ["FeatureExtractorDep", "QdrantClientDep"]

QdrantClientDep = Annotated[AsyncQdrantClient, Depends(get_qdrant_client)]
FeatureExtractorDep = Annotated[TextEmbedding, Depends(get_feature_extractor)]
