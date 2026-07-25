"""Run analysis for one entity using a DomainAdapter."""

from __future__ import annotations

import hashlib
import logging
from typing import Any

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.analysis.json_extract import extract_json_object
from app.domains.base import DomainAdapter
from app.ollama.client import OllamaClient
from app.rag.context_builder import EMPTY_CONTEXT_SENTINEL, build_context
from app.rag.retriever import retrieve_chunks

logger = logging.getLogger(__name__)

MAX_PROMPT_CHARS = 200_000


class AnalysisError(Exception):
    """Hard failure during analysis."""


_REPAIR_TEMPLATE = """The following response is not valid JSON.

Fix it so it matches the required schema.
Return JSON only.

INVALID RESPONSE:
{invalid_response}

REQUIRED SCHEMA:
{schema}"""


def _truncate_prompt(prompt: str) -> str:
    if len(prompt) <= MAX_PROMPT_CHARS:
        return prompt
    return prompt[:MAX_PROMPT_CHARS].rstrip() + "\n\n[truncated]"


def _prompt_sha256(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def _validate_or_repair(
    client: OllamaClient,
    raw: str,
    *,
    schema_model: type[BaseModel],
    schema_text: str,
) -> tuple[BaseModel, str]:
    try:
        data = extract_json_object(raw)
        return schema_model.model_validate(data), raw
    except Exception as first_exc:
        logger.warning("Initial analysis JSON invalid: %s", first_exc)

    repair_prompt = _REPAIR_TEMPLATE.format(invalid_response=raw, schema=schema_text)
    repaired_raw = client.generate(repair_prompt, format="json")
    try:
        data = extract_json_object(repaired_raw)
        return schema_model.model_validate(data), repaired_raw
    except Exception as second_exc:
        raise AnalysisError(
            f"analysis JSON validation failed after repair: {second_exc}"
        ) from second_exc


def analyze_entity(
    session: Session,
    *,
    adapter: DomainAdapter,
    entity_key: str,
    ollama: OllamaClient,
) -> BaseModel:
    """Full analyze loop: facts → RAG → prompt → validate/repair → persist."""
    key = entity_key.strip()
    if not key:
        raise AnalysisError("entity_key must be non-empty")

    entity = adapter.upsert_entity(session, key)
    facts = adapter.refresh_facts(session, entity)
    queries = adapter.build_queries(entity, facts)
    chunks = retrieve_chunks(
        session,
        entity_id=entity.id,
        queries=queries,
        ollama=ollama,
        score_chunk=adapter.score_chunk,
    )
    rag_context, refs = build_context(chunks)
    prompt = adapter.build_user_prompt(entity=entity, facts=facts, rag_context=rag_context)
    prompt_stored = _truncate_prompt(prompt)
    prompt_hash = _prompt_sha256(prompt)

    raw = ollama.generate(prompt, format="json")
    result, raw_used = _validate_or_repair(
        ollama,
        raw,
        schema_model=adapter.output_schema(),
        schema_text=adapter.schema_text(),
    )

    result_dict: dict[str, Any] = result.model_dump()
    missing = list(result_dict.get("missing_data") or [])
    if rag_context == EMPTY_CONTEXT_SENTINEL and EMPTY_CONTEXT_SENTINEL not in missing:
        missing.append(EMPTY_CONTEXT_SENTINEL)
        if hasattr(result, "missing_data"):
            result.missing_data = missing  # type: ignore[attr-defined]
            result_dict["missing_data"] = missing

    input_snapshot = {
        "facts": facts,
        "rag_context_chars": len(rag_context or ""),
        "retrieval_query_count": len(queries),
        "retrieved_chunk_count": len(chunks),
    }
    adapter.persist_report(
        session,
        entity=entity,
        result=result,
        raw_model_output=raw_used,
        refs=refs,
        prompt_text=prompt_stored,
        prompt_sha256=prompt_hash,
        input_snapshot=input_snapshot,
    )
    return result
