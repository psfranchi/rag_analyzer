"""pgvector retrieval for one entity (domain supplies queries / scoring)."""

from __future__ import annotations

import hashlib
import logging
import re
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Document, DocumentChunk
from app.ingestion.document_quality import DEFAULT_QUALITY
from app.ingestion.embeddings import embed_text
from app.ollama.client import OllamaClient

logger = logging.getLogger(__name__)

TOP_K = 8
PER_QUERY_K = 8
QUALITY_SCORE_WEIGHT = 0.2


@dataclass
class RetrievedChunk:
    chunk_id: int
    document_id: int
    content: str
    title: str | None
    source_type: str | None
    source_url: str | None
    published_at: datetime | None
    distance: float
    score: float
    quality_score: float = DEFAULT_QUALITY


def _content_fingerprint(text: str) -> str:
    normalized = re.sub(r"\s+", " ", text.strip().lower())
    return hashlib.sha1(normalized[:400].encode("utf-8")).hexdigest()


def select_top_chunks(
    ranked: list[RetrievedChunk],
    *,
    top_k: int = TOP_K,
) -> list[RetrievedChunk]:
    deduped: list[RetrievedChunk] = []
    seen_fp: set[str] = set()
    for item in ranked:
        fp = _content_fingerprint(item.content)
        if fp in seen_fp:
            continue
        seen_fp.add(fp)
        deduped.append(item)
        if len(deduped) >= top_k:
            break
    return deduped


ScoreFn = Callable[[RetrievedChunk], float]


def retrieve_chunks(
    session: Session,
    *,
    entity_id: int,
    queries: Sequence[str],
    ollama: OllamaClient,
    top_k: int = TOP_K,
    score_chunk: ScoreFn | None = None,
) -> list[RetrievedChunk]:
    """Multi-query cosine retrieval + fingerprint dedupe."""
    by_id: dict[int, RetrievedChunk] = {}

    for query in queries:
        q = (query or "").strip()
        if not q:
            continue
        try:
            vector = embed_text(ollama, q)
        except Exception as exc:
            logger.warning("query embed failed: %s", exc)
            continue

        distance = DocumentChunk.embedding.cosine_distance(vector)
        stmt = (
            select(DocumentChunk, Document, distance.label("distance"))
            .join(Document, Document.id == DocumentChunk.document_id)
            .where(Document.entity_id == entity_id)
            .where(DocumentChunk.embedding.is_not(None))
            .order_by(distance)
            .limit(PER_QUERY_K)
        )
        rows = session.execute(stmt).all()
        for chunk, doc, dist in rows:
            dist_f = float(dist)
            quality = float(doc.quality_score) if doc.quality_score is not None else DEFAULT_QUALITY
            base = (1.0 - dist_f) + QUALITY_SCORE_WEIGHT * quality
            item = RetrievedChunk(
                chunk_id=chunk.id,
                document_id=doc.id,
                content=chunk.content,
                title=doc.title,
                source_type=doc.source_type,
                source_url=doc.source_url,
                published_at=doc.published_at,
                distance=dist_f,
                score=base,
                quality_score=quality,
            )
            if score_chunk is not None:
                item.score = base + float(score_chunk(item))
            prev = by_id.get(chunk.id)
            if prev is None or item.score > prev.score:
                by_id[chunk.id] = item

    ranked = sorted(by_id.values(), key=lambda c: c.score, reverse=True)
    return select_top_chunks(ranked, top_k=top_k)
