"""Paragraph-oriented text chunking for RAG ingest."""

from __future__ import annotations

import re

DEFAULT_TARGET_SIZE = 800
DEFAULT_MAX_SIZE = 1000
_MIN_MERGE_SIZE = 80

_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+")


def chunk_text(
    text: str,
    *,
    target_size: int = DEFAULT_TARGET_SIZE,
    max_size: int = DEFAULT_MAX_SIZE,
) -> list[str]:
    """Split text into ordered chunks (~target_size, soft max max_size)."""
    if max_size < target_size:
        raise ValueError("max_size must be >= target_size")
    cleaned = (text or "").strip()
    if not cleaned:
        return []

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", cleaned) if p.strip()]
    if not paragraphs:
        paragraphs = [cleaned]

    pieces: list[str] = []
    for para in paragraphs:
        if len(para) <= max_size:
            pieces.append(para)
        else:
            pieces.extend(_split_oversized(para, max_size=max_size))

    chunks: list[str] = []
    current = ""
    for piece in pieces:
        if not current:
            current = piece
            continue
        candidate = f"{current}\n\n{piece}"
        if (
            len(candidate) <= target_size
            or len(candidate) <= max_size
            and len(current) < target_size
        ):
            current = candidate
        else:
            chunks.append(current)
            current = piece
    if current:
        chunks.append(current)

    return _merge_tiny_tails(chunks, min_size=_MIN_MERGE_SIZE, max_size=max_size)


def _split_oversized(text: str, *, max_size: int) -> list[str]:
    sentences = [s.strip() for s in _SENTENCE_SPLIT.split(text) if s.strip()]
    if not sentences:
        return _hard_wrap(text, max_size=max_size)

    out: list[str] = []
    current = ""
    for sentence in sentences:
        if len(sentence) > max_size:
            if current:
                out.append(current)
                current = ""
            out.extend(_hard_wrap(sentence, max_size=max_size))
            continue
        if not current:
            current = sentence
            continue
        candidate = f"{current} {sentence}"
        if len(candidate) <= max_size:
            current = candidate
        else:
            out.append(current)
            current = sentence
    if current:
        out.append(current)
    return out


def _hard_wrap(text: str, *, max_size: int) -> list[str]:
    return [text[i : i + max_size] for i in range(0, len(text), max_size)]


def _merge_tiny_tails(chunks: list[str], *, min_size: int, max_size: int) -> list[str]:
    if len(chunks) < 2:
        return chunks
    merged = chunks[:-1]
    last = chunks[-1]
    if len(last) < min_size:
        candidate = f"{merged[-1]}\n\n{last}"
        if len(candidate) <= max_size:
            merged[-1] = candidate
            return merged
    merged.append(last)
    return merged
