"""Notes domain registry and local file source."""

from pathlib import Path
from types import SimpleNamespace

from app.domains.notes import LocalNotesSource, NotesDomain, NotesResult
from app.domains.registry import get_domain, list_domains


def test_notes_registered() -> None:
    assert "notes" in list_domains()
    adapter = get_domain("notes")
    assert adapter.name == "notes"
    assert adapter.output_schema() is NotesResult


def test_local_notes_source_reads_demo() -> None:
    docs = LocalNotesSource().fetch("demo")
    assert docs
    assert docs[0]["source_type"] == "note"
    assert "Dual-model RAG" in docs[0]["raw_text"]
    assert Path(docs[0]["source_url"].removeprefix("file://")).exists()


def test_notes_prompt_includes_schema() -> None:
    domain = NotesDomain()
    entity = SimpleNamespace(entity_key="demo", display_name="demo")
    prompt = domain.build_user_prompt(
        entity=entity,  # type: ignore[arg-type]
        facts={"entity_key": "demo"},
        rag_context="No relevant retrieved context was found.",
    )
    assert "relevant|needs_review|insufficient_data" in prompt
    assert "JSON" in domain.system_prompt()
