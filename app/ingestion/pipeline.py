"""Ingest documents for one entity via its DomainAdapter."""

from __future__ import annotations

import logging
from typing import Any

from sqlalchemy.orm import Session

from app.domains.base import DomainAdapter
from app.ingestion.store import store_documents
from app.ollama.client import OllamaClient

logger = logging.getLogger(__name__)


def ingest_entity(
    session: Session,
    *,
    adapter: DomainAdapter,
    entity_key: str,
    ollama: OllamaClient,
    progress: Any | None = None,
) -> dict[str, int]:
    entity = adapter.upsert_entity(session, entity_key)
    adapter.refresh_facts(session, entity)

    docs: list[dict[str, Any]] = []
    for source in adapter.document_sources():
        docs.extend(source.fetch(entity.entity_key))

    if progress:
        progress(f"fetched {len(docs)} document(s)")

    counts = store_documents(
        session,
        entity_id=entity.id,
        documents=docs,
        ollama=ollama,
        quality_map=dict(adapter.source_quality()),
        progress=progress,
    )
    logger.info(
        "ingest domain=%s entity=%s docs=%s chunks=%s skipped=%s",
        adapter.name,
        entity.entity_key,
        counts["documents"],
        counts["chunks"],
        counts["skipped"],
    )
    return counts
