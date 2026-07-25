"""Domain plugin protocol."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Protocol

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.models import Entity
from app.rag.retriever import RetrievedChunk


class DocumentSource(Protocol):
    def fetch(self, entity_key: str) -> list[dict[str, Any]]:
        """Return normalized docs: source_type, source_url, title, published_at, raw_text."""
        ...


class DomainAdapter(Protocol):
    name: str

    def upsert_entity(self, session: Session, entity_key: str) -> Entity: ...

    def refresh_facts(self, session: Session, entity: Entity) -> dict[str, Any]: ...

    def document_sources(self) -> Sequence[DocumentSource]: ...

    def source_quality(self) -> Mapping[str, float]: ...

    def build_queries(self, entity: Entity, facts: dict[str, Any]) -> list[str]: ...

    def score_chunk(self, chunk: RetrievedChunk) -> float: ...

    def system_prompt(self) -> str: ...

    def output_schema(self) -> type[BaseModel]: ...

    def schema_text(self) -> str: ...

    def build_user_prompt(
        self,
        *,
        entity: Entity,
        facts: dict[str, Any],
        rag_context: str,
    ) -> str: ...

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
    ) -> None: ...
