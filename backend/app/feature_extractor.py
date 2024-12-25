from functools import cache

from fastembed import TextEmbedding  # pyright: ignore [reportMissingTypeStubs]

__all__ = ["get_feature_extractor"]

@cache
def get_feature_extractor() -> TextEmbedding:
    return TextEmbedding("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
