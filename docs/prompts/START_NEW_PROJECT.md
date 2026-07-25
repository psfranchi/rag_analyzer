# Prompt: specialize this repo into a single-topic project

Fill every `YOUR_…` field, then paste everything below the line into any coding agent or chat LLM.

---

```text
You are specializing the rag_analyzer template into a dedicated research analyzer for one topic.

Read first:
- docs/AI_CONTEXT.md
- docs/NEW_PROJECT.md
- docs/ADDING_A_DOMAIN.md
- docs/ARCHITECTURE.md
- app/domains/base.py
- app/domains/notes/__init__.py

## Product brief

- Product / project name: YOUR_PROJECT_NAME
- Research topic in one sentence: YOUR_TOPIC
- Primary domain slug: YOUR_DOMAIN_SLUG
- Who the user is and what question they answer with each run: YOUR_USER_JOB
- Entity identity (stable keys): YOUR_ENTITY_KEYS
- Document sources: YOUR_SOURCES
- Output labels + JSON fields that matter: YOUR_OUTPUT_SCHEMA
- Facts that must stay deterministic (never LLM-invented): YOUR_FACTS
- Keep the example `notes` domain? YOUR_KEEP_NOTES (yes/no)
- New env vars: YOUR_ENV_VARS (or "none")

## Deliverables

1. Rename branding in README.md and pyproject.toml description to YOUR_PROJECT_NAME (keep package layout unless clearly better).
2. Implement app/domains/YOUR_DOMAIN_SLUG/ as the primary DomainAdapter.
3. If YOUR_KEEP_NOTES is no, remove notes domain + its tests/demo data only after the new domain has tests and a smoke path.
4. Sample data + docs so a newcomer can: uv sync → .env → init_db → ingest → analyze.
5. Update docs/SETUP.md, docs/ADDING_A_DOMAIN.md examples, and docs/AI_CONTEXT.md to describe THIS product (still mention DomainAdapter for future domains).
6. Ensure domain auto-discovery works (register_domain in the package; no hardcoded registry imports).
7. Add/adjust tests; run pytest and ruff.

Platform rules (non-negotiable):
- Do not fold topic logic into app/rag, app/ollama, or app/ingestion.
- Empty RAG → sentinel + missing_data behavior stays.
- Validated JSON + one repair stays.
- No financial/legal/medical “advice” framing — research notes only.
- Stay tool-agnostic: do not add IDE-/vendor-specific agent or rules files unless I ask.

End with a short “How to run” section I can paste into the README.
```
