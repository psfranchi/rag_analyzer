"""Build compact RAG context blocks for analysis prompts."""

from __future__ import annotations

from typing import Any

from app.rag.retriever import RetrievedChunk

EMPTY_CONTEXT_SENTINEL = "No relevant retrieved context was found."


def build_context(chunks: list[RetrievedChunk]) -> tuple[str, list[dict[str, Any]]]:
    if not chunks:
        return EMPTY_CONTEXT_SENTINEL, []

    blocks: list[str] = []
    refs: list[dict[str, Any]] = []
    for i, chunk in enumerate(chunks, start=1):
        published = chunk.published_at.isoformat() if chunk.published_at else ""
        blocks.append(
            "\n".join(
                [
                    f"[Context {i}]",
                    f"Title: {chunk.title or ''}",
                    f"Source: {chunk.source_type or ''}",
                    f"Published: {published}",
                    f"Text: {chunk.content}",
                ]
            )
        )
        refs.append(
            {
                "chunk_id": chunk.chunk_id,
                "document_id": chunk.document_id,
                "title": chunk.title,
                "source_url": chunk.source_url,
                "source_type": chunk.source_type,
            }
        )
    return "\n\n".join(blocks), refs
