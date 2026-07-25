"""Store normalized documents as chunks + embeddings for one entity."""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Document, DocumentChunk
from app.ingestion.chunker import chunk_text
from app.ingestion.document_quality import content_hash, enrich_document_fields
from app.ingestion.embeddings import embed_text, is_connection_failure
from app.ollama.client import OllamaClient

logger = logging.getLogger(__name__)


def store_documents(
    session: Session,
    *,
    entity_id: int,
    documents: list[dict[str, Any]],
    ollama: OllamaClient,
    quality_map: dict[str, float] | None = None,
    progress: Any | None = None,
) -> dict[str, int]:
    """Dedupe by URL/hash, chunk, embed, store. Returns counts."""

    def _p(msg: str) -> None:
        if progress:
            progress(msg)

    added_docs = 0
    added_chunks = 0
    skipped = 0

    for doc_data in documents:
        raw_text = (doc_data.get("raw_text") or "").strip()
        if not raw_text:
            skipped += 1
            continue

        url = doc_data.get("source_url")
        c_hash, q_score = enrich_document_fields(doc_data, quality_map)

        if url:
            existing = session.scalar(
                select(Document).where(
                    Document.entity_id == entity_id,
                    Document.source_url == url,
                )
            )
            if existing is not None:
                skipped += 1
                continue
        if c_hash:
            existing_hash = session.scalar(
                select(Document).where(
                    Document.entity_id == entity_id,
                    Document.content_hash == c_hash,
                )
            )
            if existing_hash is not None:
                skipped += 1
                continue

        published = doc_data.get("published_at")
        if isinstance(published, str) and published:
            try:
                published = datetime.fromisoformat(published.replace("Z", "+00:00"))
            except ValueError:
                published = None
        elif not isinstance(published, datetime):
            published = None

        document = Document(
            entity_id=entity_id,
            source_type=doc_data.get("source_type"),
            source_url=url,
            title=doc_data.get("title"),
            published_at=published,
            raw_text=raw_text,
            content_hash=c_hash or content_hash(raw_text),
            quality_score=q_score,
        )
        session.add(document)
        session.flush()
        added_docs += 1

        pieces = chunk_text(raw_text)
        for idx, piece in enumerate(pieces):
            try:
                vector = embed_text(ollama, piece)
            except Exception as exc:
                if is_connection_failure(exc):
                    raise
                logger.warning("embed failed doc=%s chunk=%s: %s", document.id, idx, exc)
                continue
            session.add(
                DocumentChunk(
                    document_id=document.id,
                    chunk_index=idx,
                    content=piece,
                    embedding=vector,
                    metadata_={
                        "title": document.title,
                        "source_type": document.source_type,
                        "source_url": document.source_url,
                    },
                )
            )
            added_chunks += 1
        _p(f"stored document id={document.id} chunks={len(pieces)}")

    return {"documents": added_docs, "chunks": added_chunks, "skipped": skipped}
