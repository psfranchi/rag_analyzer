"""Example notes domain — local markdown files under data/notes/<entity>/."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import AnalysisReport, Entity
from app.domains.registry import register_domain
from app.rag.retriever import RetrievedChunk

Decision = Literal["relevant", "needs_review", "insufficient_data"]

SCHEMA_TEXT = """{
  "entity_key": "string",
  "decision": "relevant|needs_review|insufficient_data",
  "confidence": 0.0,
  "summary": "string",
  "key_points": ["string"],
  "open_questions": ["string"],
  "missing_data": ["string"]
}"""

SYSTEM_PROMPT = """You are a careful research assistant for notes and documents.

You must not invent facts. Use only the supplied facts and retrieved context.

Classify with exactly one decision:
- relevant — material is useful and coherent for the entity
- needs_review — mixed or uncertain; a human should look
- insufficient_data — too little reliable context

Return valid JSON only. No markdown. No commentary outside JSON."""

_DATA_ROOT = Path(__file__).resolve().parents[3] / "data" / "notes"


class NotesResult(BaseModel):
    entity_key: str
    decision: Decision
    confidence: float = Field(ge=0.0, le=1.0)
    summary: str = ""
    key_points: list[str] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)
    missing_data: list[str] = Field(default_factory=list)


class LocalNotesSource:
    """Load *.md / *.txt from data/notes/<entity_key>/."""

    def fetch(self, entity_key: str) -> list[dict[str, Any]]:
        folder = _DATA_ROOT / entity_key.strip()
        if not folder.is_dir():
            return []
        docs: list[dict[str, Any]] = []
        for path in sorted(folder.iterdir()):
            if path.suffix.lower() not in {".md", ".txt"}:
                continue
            text = path.read_text(encoding="utf-8")
            docs.append(
                {
                    "source_type": "note",
                    "source_url": f"file://{path.resolve()}",
                    "title": path.name,
                    "published_at": None,
                    "raw_text": text,
                }
            )
        return docs


class NotesDomain:
    name = "notes"

    def upsert_entity(self, session: Session, entity_key: str) -> Entity:
        key = entity_key.strip()
        existing = session.scalar(
            select(Entity).where(Entity.domain == self.name, Entity.entity_key == key)
        )
        if existing:
            return existing
        entity = Entity(domain=self.name, entity_key=key, display_name=key, metadata_={})
        session.add(entity)
        session.flush()
        return entity

    def refresh_facts(self, session: Session, entity: Entity) -> dict[str, Any]:
        folder = _DATA_ROOT / entity.entity_key
        files = []
        if folder.is_dir():
            files = [
                p.name for p in sorted(folder.iterdir()) if p.suffix.lower() in {".md", ".txt"}
            ]
        return {
            "entity_key": entity.entity_key,
            "display_name": entity.display_name,
            "note_files": files,
            "notes_dir": str(folder),
        }

    def document_sources(self) -> list[LocalNotesSource]:
        return [LocalNotesSource()]

    def source_quality(self) -> dict[str, float]:
        return {"note": 0.70, "manual": 0.60}

    def build_queries(self, entity: Entity, facts: dict[str, Any]) -> list[str]:
        name = entity.display_name or entity.entity_key
        return [
            f"{name} overview summary",
            f"{name} key points risks questions",
            f"{entity.entity_key} details",
        ]

    def score_chunk(self, chunk: RetrievedChunk) -> float:
        return 0.0

    def system_prompt(self) -> str:
        return SYSTEM_PROMPT

    def output_schema(self) -> type[BaseModel]:
        return NotesResult

    def schema_text(self) -> str:
        return SCHEMA_TEXT

    def build_user_prompt(
        self,
        *,
        entity: Entity,
        facts: dict[str, Any],
        rag_context: str,
    ) -> str:
        return f"""SYSTEM:
{self.system_prompt()}

TASK:
Analyze notes for this entity. Research notes only — not advice.

ENTITY:
{entity.entity_key}

FACTS (deterministic):
{json.dumps(facts, indent=2)}

RETRIEVED CONTEXT:
{rag_context}

OUTPUT REQUIREMENTS:
Return valid JSON only matching this schema:

{self.schema_text()}
"""

    def persist_report(
        self,
        session: Session,
        *,
        entity: Entity,
        result: BaseModel,
        raw_model_output: str,
        refs: list[dict[str, Any]],
        prompt_text: str,
        prompt_sha256: str,
        input_snapshot: dict[str, Any],
    ) -> None:
        data = result.model_dump()
        report = AnalysisReport(
            entity_id=entity.id,
            domain=self.name,
            entity_key=entity.entity_key,
            decision=data.get("decision"),
            confidence=data.get("confidence"),
            result_json=data,
            summary=data.get("summary"),
            missing_data=data.get("missing_data"),
            retrieved_context_refs=refs,
            input_snapshot=input_snapshot,
            prompt_text=prompt_text,
            prompt_sha256=prompt_sha256,
            raw_model_output=raw_model_output,
        )
        session.add(report)
        session.flush()


def _factory() -> NotesDomain:
    return NotesDomain()


register_domain("notes", _factory)
