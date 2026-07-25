# Prompt: add a new DomainAdapter

Fill every `YOUR_…` field, then paste everything below the line into any coding agent or chat LLM.

---

```text
You are working in the rag_analyzer template (local dual-model RAG: Ollama embeddings + analysis, Postgres/pgvector, DomainAdapter plugins).

Read first:
- docs/AI_CONTEXT.md
- docs/ADDING_A_DOMAIN.md
- docs/ARCHITECTURE.md
- app/domains/base.py
- app/domains/notes/__init__.py  (reference implementation)

Task: add a new domain plugin. Do NOT change platform packages (app/db, app/ollama, app/ingestion, app/rag, app/analysis) except if a tiny bug blocks the domain. Domains are auto-discovered — register with register_domain() inside the new package; do not hardcode imports in registry.py.

## Domain brief

- Domain slug (snake_case, folder name): YOUR_DOMAIN_SLUG
- What an "entity" is (one analyzed subject): YOUR_ENTITY_DEFINITION
- Example entity keys (stable IDs, not free titles): YOUR_EXAMPLE_KEYS
- Document sources (files, APIs, scrapers — be concrete): YOUR_SOURCES
- Decision labels (replace notes' relevant|needs_review|insufficient_data): YOUR_LABELS
- Deterministic facts the LLM must NOT invent (dates, citations, prices, IDs, …): YOUR_FACTS
- Any new env vars / API keys: YOUR_ENV_VARS (or "none")

## Deliverables

1. Create app/domains/YOUR_DOMAIN_SLUG/ with a full DomainAdapter (copy notes, then specialize).
2. Implement DocumentSource(s) returning source_type, source_url, title, published_at, raw_text.
3. Set source_quality, build_queries, score_chunk, system_prompt, Pydantic output_schema, schema_text, build_user_prompt, persist_report.
4. refresh_facts must be deterministic only.
5. Add sample data under data/YOUR_DOMAIN_SLUG/<example_entity>/ if local files are used.
6. Add focused tests under tests/ (registry, source fetch, prompt/schema).
7. Document any env vars in .env.example and docs/SETUP.md.
8. Show the exact ingest + analyze CLI commands for the example entity.

Constraints:
- Never invent statutes, citations, prices, or dates in prompts — require them in FACTS or retrieved text.
- Analysis returns validated JSON only; keep one-repair behavior via the platform runner.
- Keep the repo tool-agnostic (no IDE-/vendor-specific agent or rules files unless I ask).

When done, run: uv run pytest -q && uv run ruff check .
```
