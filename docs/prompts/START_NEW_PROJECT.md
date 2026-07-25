# Prompt: start a new project

Fill every `YOUR_…` field, then paste everything below the line into any coding agent or chat LLM.

If **entity** vs **domain** is unclear, read [`../CONCEPTS.md`](../CONCEPTS.md) first.

- **Domain** = topic plugin (one for the whole product), e.g. `games`
- **Entity** = one item you analyze per run (you can have many), e.g. `hades`, `celeste`
- You pick the entity id; document sources load data *for* that id (often `data/<domain>/<entity>/`)

---

```text
You are specializing the rag_analyzer template into a dedicated research analyzer for one topic.

Read first:
- docs/AI_CONTEXT.md
- docs/CONCEPTS.md
- docs/NEW_PROJECT.md
- docs/ARCHITECTURE.md
- app/domains/base.py
- app/domains/notes/__init__.py

## Product brief

- Product / project name: YOUR_PROJECT_NAME
- Research topic in one sentence: YOUR_TOPIC
- Domain slug (folder name under app/domains/ — the topic, not one item): YOUR_DOMAIN_SLUG
- Who the user is and what question they answer with each run: YOUR_USER_JOB
- Entity identity (how users name one item; many allowed — e.g. short slugs / folder names, not a single fixed list): YOUR_ENTITY_KEYS
- Document sources (how docs are loaded for a given entity id): YOUR_SOURCES
- Output labels + JSON fields that matter: YOUR_OUTPUT_SCHEMA
- Facts that must stay deterministic (never LLM-invented): YOUR_FACTS
- New env vars: YOUR_ENV_VARS (or "none")

## Deliverables

1. Rename branding in README.md and pyproject.toml description to YOUR_PROJECT_NAME (keep package layout unless clearly better).
2. Implement app/domains/YOUR_DOMAIN_SLUG/ as the DomainAdapter (copy notes, then specialize).
3. Remove the example notes domain, its tests, and demo data only after the new domain has tests and a smoke path.
4. Sample data for one or two example entities + docs so a newcomer can: uv sync → .env → init_db → ingest → analyze.
5. Update docs/SETUP.md, docs/NEW_PROJECT.md, docs/CONCEPTS.md examples, and docs/AI_CONTEXT.md to describe THIS product.
6. Ensure domain auto-discovery works (register_domain in the package; no hardcoded registry imports).
7. Add/adjust tests; run pytest and ruff.
8. README must show how to run the same domain against multiple --entity values, and that ingest / analyze are separate faces that can also run together via scripts/run_entity.py.

Platform rules (non-negotiable):
- Do not fold topic logic into app/rag, app/ollama, or app/ingestion.
- Empty RAG → sentinel + missing_data behavior stays.
- Validated JSON + one repair stays.
- No financial/legal/medical “advice” framing — research notes only.
- Stay tool-agnostic: do not add IDE-/vendor-specific agent or rules files unless I ask.
- Default loop is per-entity analysis (see docs/CONCEPTS.md); do not pretend a catalog-wide “search interesting items” API exists unless explicitly building that on top.

End with a short “How to run” section I can paste into the README.
```
