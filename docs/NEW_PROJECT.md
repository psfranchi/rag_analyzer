# Start a new analyzer project

This repo is a **template**. Clone it, then specialize it for one research topic (laws, games, product reviews, …).

**Before the prompt:** read [`CONCEPTS.md`](CONCEPTS.md) (domain vs entity, many entities, how ids relate to data).

## Steps

1. Smoke-test the template (see [`SETUP.md`](SETUP.md)).
2. Copy the repo (or create a new GitHub repo from this template). Remove the template `origin` remote, then add *your* repo when ready.
3. Create a Postgres DB + set `.env` from `.env.example`.
4. Open [`prompts/START_NEW_PROJECT.md`](prompts/START_NEW_PROJECT.md), fill the blanks, paste into any coding agent or chat LLM.
5. Drop the example `notes` domain once yours works (the prompt covers this).

## What gets customized

| Customize | Leave alone (platform) |
|-----------|------------------------|
| `app/domains/<your_domain>/` | `app/db/`, `app/ollama/`, `app/ingestion/`, `app/rag/`, `app/analysis/` |
| Labels, prompts, Pydantic schema | Dual-model Ollama wiring |
| Document sources / fetchers | Chunking, embeddings, retrieval loop |
| `data/<domain>/<entity>/…` sample files | Generic `Entity` / `Document` / `AnalysisReport` tables |
| Domain tests under `tests/` | `scripts/ingest_entity.py`, `scripts/analyze_entity.py` |

Your domain package must call `register_domain(...)` at import time. Subpackages under `app/domains/` are **auto-discovered** — no edit to `registry.py`.

## DomainAdapter checklist (what the agent implements)

1. Copy `app/domains/notes/` → `app/domains/<slug>/`.
2. Entity ids: short stable slugs (see [`CONCEPTS.md`](CONCEPTS.md)); support **many** entities under one domain.
3. `DocumentSource.fetch(entity_key)` returns `source_type`, `source_url`, `title`, `published_at`, `raw_text`.
4. `source_quality`, `build_queries`, `score_chunk`.
5. `refresh_facts` — deterministic only; never invent from the LLM.
6. Labels + Pydantic schema + `schema_text` + system prompt, kept in sync.
7. `persist_report` into generic `analysis_reports`.
8. Sample data for **at least one** entity + tests + any new env vars in `.env.example` / `SETUP.md`.

## Success criteria

```bash
uv run python scripts/ingest_entity.py --domain <your_domain> --entity <key>
uv run python scripts/analyze_entity.py --domain <your_domain> --entity <key>
uv run pytest -q
```

Validated JSON research notes grounded in retrieved context — not invented facts.

Document for users that the product has two faces (**ingest** and **analyze**) and that `scripts/run_entity.py` runs both together.
