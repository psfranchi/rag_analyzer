"""Embedding helpers with dimension validation for ingest."""

from __future__ import annotations

from app.db.models import EMBEDDING_DIMENSION
from app.ollama.client import OllamaClient, OllamaConnectionError


class EmbeddingDimensionError(ValueError):
    """Raised when embedding length does not match the expected model dimension."""


def embed_text(client: OllamaClient, text: str) -> list[float]:
    vector = client.embed(text)
    if len(vector) != EMBEDDING_DIMENSION:
        raise EmbeddingDimensionError(
            f"expected embedding length {EMBEDDING_DIMENSION}, got {len(vector)}"
        )
    return vector


def is_connection_failure(exc: BaseException) -> bool:
    return isinstance(exc, OllamaConnectionError)
