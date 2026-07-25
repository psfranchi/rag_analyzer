"""Document quality helpers."""

from app.ingestion.document_quality import content_hash, quality_for_source_type


def test_content_hash_stable() -> None:
    assert content_hash("a  b") == content_hash("a b")
    assert content_hash("  ") is None


def test_quality_map() -> None:
    assert quality_for_source_type("note", {"note": 0.7}) == 0.7
    assert 0.0 <= quality_for_source_type("unknown") <= 1.0
