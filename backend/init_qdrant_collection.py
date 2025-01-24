from pathlib import Path
from typing import Annotated, TypedDict, cast

import typer
from datasets import (  # pyright: ignore [reportMissingTypeStubs]
    Dataset,
    disable_progress_bars,
    load_from_disk,  # pyright: ignore [reportUnknownVariableType]
)
from qdrant_client import QdrantClient
from qdrant_client.models import Batch, Distance, VectorParams
from rich import print

from app.settings import get_app_settings


class EmojiDatasetBatch(TypedDict):
    emoji: list[str]
    shortcode: list[str]
    keywords: list[list[str]]
    description: str
    embedding: list[list[float]]


def _create_collection(client: QdrantClient, collection_name: str) -> None:
    try:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.DOT),
        )
    except ValueError as exc:
        if "Collection already exists" not in str(exc):
            raise
        print(f"[bold yellow]WARN[/bold yellow] {exc}")

    print("[bold green]OK[/bold green] Collection created")


def _upload_dataset(
    client: QdrantClient, collection_name: str, dataset_path: Path
) -> None:
    emodij_dataset = cast(Dataset, load_from_disk(dataset_path)).batch(256)

    begin = 0
    for batch in emodij_dataset:  # pyright: ignore [reportUnknownVariableType]
        batch = cast(EmojiDatasetBatch, batch)
        end = begin + len(batch["emoji"])

        client.upsert(
            collection_name=collection_name,
            points=Batch(
                ids=list(range(begin, end)),
                vectors=batch["embedding"],
                payloads=[
                    {
                        "emoji": emoji,
                        "shortcode": shortcode,
                        "keywords": keywords,
                        "description": description,
                    }
                    for emoji, shortcode, keywords, description in zip(
                        batch["emoji"],
                        batch["shortcode"],
                        batch["keywords"],
                        batch["description"],
                        strict=True,
                    )
                ],
            ),
        )

        begin = end

    print("[bold green]OK[/bold green] Dataset uploaded")


def main(
    emoji_dataset: Annotated[
        Path,
        typer.Argument(
            exists=True,
            dir_okay=True,
            readable=True,
            resolve_path=True,
        ),
    ],
) -> None:
    settings = get_app_settings()
    api_key = get_app_settings().qdrant_api_key
    client = QdrantClient(
        url=get_app_settings().qdrant_url.get_secret_value().unicode_string(),
        api_key=(api_key.get_secret_value() if api_key else None),
    )

    try:
        _create_collection(client=client, collection_name=settings.collection_name)
        _upload_dataset(
            client=client,
            collection_name=settings.collection_name,
            dataset_path=emoji_dataset,
        )
    finally:
        client.close()


if __name__ == "__main__":
    disable_progress_bars()
    typer.run(main)
