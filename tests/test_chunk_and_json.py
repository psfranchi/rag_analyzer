"""Tests for chunker and JSON extract."""

from app.analysis.json_extract import extract_json_object
from app.ingestion.chunker import chunk_text


def test_chunk_text_splits_paragraphs() -> None:
    text = "First paragraph.\n\n" + ("Word " * 200)
    chunks = chunk_text(text)
    assert len(chunks) >= 1
    assert all(isinstance(c, str) and c.strip() for c in chunks)


def test_extract_json_object_plain_and_fenced() -> None:
    assert extract_json_object('{"a": 1}')["a"] == 1
    assert extract_json_object('```json\n{"b": 2}\n```')["b"] == 2
