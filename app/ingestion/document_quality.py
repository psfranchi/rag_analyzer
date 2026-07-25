"""Document content hashing and source-type quality scores."""

from __future__ import annotations

import hashlib
import re
from typing import Any

DEFAULT_QUALITY = 0.40


def normalize_for_hash(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def content_hash(text: str | None) -> str | None:
    normalized = normalize_for_hash(text or "")
    if not normalized:
        return None
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def quality_for_source_type(
    source_type: str | None,
    quality_map: dict[str, float] | None = None,
) -> float:
    mapping = quality_map or {}
    if not source_type or not str(source_type).strip():
        return DEFAULT_QUALITY
    key = str(source_type).strip().lower()
    return mapping.get(key, DEFAULT_QUALITY)


def enrich_document_fields(
    doc_data: dict[str, Any],
    quality_map: dict[str, float] | None = None,
) -> tuple[str | None, float]:
    return content_hash(doc_data.get("raw_text")), quality_for_source_type(
        doc_data.get("source_type"), quality_map
    )
