# Start a new analyzer project

This repo is a **template**. The platform is fixed; your topic is not.

## What you get out of the box

| Capability | Meaning |
|------------|---------|
| Dual-model RAG | Embedding model + analysis model (Ollama) |
| Ingest | Get documents for one subject → chunk → embed → Postgres/pgvector |
| Analyze | Retrieve → JSON research notes (validated) |
| Together | `scripts/run_entity.py` runs ingest then analyze |
| Domain plugin | Your topic’s sources, prompts, and labels in `app/domains/<slug>/` |

Vocabulary (domain vs entity, many subjects): [`CONCEPTS.md`](CONCEPTS.md) — useful background, not a form to fill.

## Steps

1. Smoke-test the template ([`SETUP.md`](SETUP.md)).
2. Copy/clone this repo into a new folder. Remove the template `origin` remote; add yours later.
3. `.env` + Postgres + Ollama as in SETUP.
4. Open [`prompts/START_NEW_PROJECT.md`](prompts/START_NEW_PROJECT.md), replace the **IDEA** paragraph with what you want, paste into any coding agent.
5. Let the agent invent domain name, sources, schema, and sample data. Iterate in chat if needed.

## What the agent customizes vs leaves alone

| Customize | Leave alone |
|-----------|-------------|
| `app/domains/<slug>/`, sample `data/…`, prompts, labels, schema | `app/db/`, `app/ollama/`, `app/ingestion/`, `app/rag/`, `app/analysis/` |
| Product README / docs tone | Thin CLIs (`ingest_entity`, `analyze_entity`, `run_entity`) |

## Success

```bash
uv run python scripts/run_entity.py --domain <slug> --entity <example>
uv run pytest -q
```
