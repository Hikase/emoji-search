import json
from collections.abc import Sequence
from functools import cache
from pathlib import Path
from typing import TYPE_CHECKING, Self, TypedDict, cast

import numpy as np
import numpy.typing as npt
from onnxruntime import InferenceSession  # pyright: ignore [reportMissingTypeStubs]
from tokenizers import AddedToken, Encoding, Tokenizer

from app.domain.value_object import F32Array
from app.settings import get_app_settings

__all__ = [
    "FeatureExtractor",
    "get_feature_extractor",
    "load_tokenizer",
    "mean_pooling",
    "normalize",
]


if TYPE_CHECKING:

    class AddedTokenDict(TypedDict):
        content: str
        single_word: bool
        lstrip: bool
        rstrip: bool
        normalized: bool
        special: bool


def load_tokenizer(model_dir: str | Path, /) -> Tokenizer:
    model_dir = Path(model_dir)

    try:
        with open(model_dir / "config.json") as model_config_file:
            model_config = json.load(model_config_file)

        with open(model_dir / "tokenizer_config.json") as tokenizer_config_file:
            tokenizer_config = json.load(tokenizer_config_file)

        with open(model_dir / "special_tokens_map.json") as special_tokens_map_file:
            special_tokens_map: dict[str, str | AddedTokenDict] = json.load(
                special_tokens_map_file
            )

        tokenizer = cast(
            Tokenizer,
            Tokenizer.from_file(str(model_dir / "tokenizer.json")),  # pyright: ignore [reportUnknownMemberType]
        )
    except FileNotFoundError as exc:
        # TODO: add custom exception
        raise exc

    tokenizer.enable_padding(  # pyright: ignore [reportUnknownMemberType]
        pad_id=model_config.get("pad_token_id", 0),
        pad_token=tokenizer_config["pad_token"],
    )

    if (
        "model_max_length" not in tokenizer_config
        and "max_length" not in tokenizer_config
    ):
        msg = (
            "Models without the model_max_length"
            " or max_length parameter are not supported."
        )
        raise ValueError(msg)  # TODO: add custom exception
    tokenizer.enable_truncation(  # pyright: ignore [reportUnknownMemberType]
        max_length=tokenizer_config.get("max_length")
        or tokenizer_config.get("model_max_length")
    )

    tokenizer.add_special_tokens(  # pyright: ignore [reportUnknownMemberType]
        [
            token if isinstance(token, str) else AddedToken(**token)
            for token in special_tokens_map.values()
        ]
    )

    return tokenizer


def mean_pooling(
    *, embeddings: F32Array, attention_mask: npt.NDArray[np.int64]
) -> F32Array:
    mask_expanded = np.expand_dims(attention_mask, axis=-1)
    mask_expanded = np.broadcast_to(mask_expanded, embeddings.shape).astype(np.float32)
    return np.sum(embeddings * mask_expanded, axis=1) / np.maximum(
        mask_expanded.sum(axis=1), 1e-9
    )


def normalize(
    input: F32Array, *, p: float = 2, dim: int = 1, eps: float = 1e-12
) -> F32Array:
    norm = np.linalg.norm(input, ord=p, axis=dim, keepdims=True)
    norm = np.maximum(norm, eps)
    return input / norm


class FeatureExtractor:
    def __init__(self, model: InferenceSession, tokenizer: Tokenizer) -> None:
        self._tokenizer = tokenizer
        self._model = model

        output_names: Sequence[str] = [
            node.name  # pyright: ignore [reportUnknownMemberType]
            for node in self._model.get_outputs()  # pyright: ignore [reportUnknownVariableType]
        ]
        if "sentence_embedding" in output_names:
            self._output_name = "sentence_embedding"
        else:
            self._output_name = "last_hidden_state"

        self._has_token_type_ids = "token_type_ids" in [
            node.name  # pyright: ignore [reportUnknownMemberType]
            for node in self._model.get_inputs()  # pyright: ignore [reportUnknownVariableType]
        ]

    @classmethod
    def load(cls, model_path: str | Path, *, file_name: str | None = None) -> Self:
        if not isinstance(model_path, Path):
            model_path = Path(model_path)

        if model_path.is_dir():
            if file_name is None:
                onnx_files = list(model_path.glob("*.onnx"))

                if len(onnx_files) == 0:
                    msg = f"Could not find any ONNX model file in {model_path}"
                    raise FileNotFoundError(msg)
                if len(onnx_files) > 1:
                    msg = (
                        f"Too many ONNX model files were found in {model_path}, "
                        "specify which one to load by using the file_name argument."
                    )
                    raise ValueError(msg)

                file_name = onnx_files[0].name
        elif model_path.is_file():
            file_name = model_path.name
            model_path = model_path.parent
        else:
            msg = f"Invalid model path: {model_path}"
            raise ValueError(msg)

        model = InferenceSession(model_path / file_name)
        tokenizer = load_tokenizer(model_path)

        return cls(model, tokenizer)

    def embed(self, docs: str | Sequence[str]) -> F32Array:
        if isinstance(docs, str):
            docs = [docs]

        docs = [f"query: {doc}" for doc in docs]

        encodings = cast(Sequence[Encoding], self._tokenizer.encode_batch(docs))  # pyright: ignore [reportUnknownMemberType]

        input_ids: npt.NDArray[np.int64] = np.array(
            [encoding.ids for encoding in encodings],  # pyright: ignore [reportUnknownMemberType]
            dtype=np.int64,
        )
        attention_mask: npt.NDArray[np.int64] = np.array(
            [encoding.attention_mask for encoding in encodings],  # pyright: ignore [reportUnknownMemberType]
            dtype=np.int64,
        )

        input_feed = {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
        }

        if self._has_token_type_ids:
            input_feed["token_type_ids"] = npt.NDArray[np.int64] = np.array(
                [encoding.type_ids for encoding in encodings],  # pyright: ignore [reportUnknownMemberType]
                dtype=np.int64,
            )

        result: F32Array = np.array(
            self._model.run(  # pyright: ignore [reportUnknownMemberType, reportUnknownArgumentType]
                output_names=[self._output_name],
                input_feed=input_feed,
            )[0]
        )

        if self._output_name == "sentence_embedding":
            return result

        return normalize(mean_pooling(embeddings=result, attention_mask=attention_mask))


@cache
def get_feature_extractor() -> FeatureExtractor:
    return FeatureExtractor.load(get_app_settings().model_path)
