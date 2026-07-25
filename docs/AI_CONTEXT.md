# AI context (tool-agnostic)

Short brief for any coding assistant or human working in this repo.

## What this is

Local **dual-model RAG** template:

1. **Embedding model** (Ollama) → chunk vectors in Postgres/pgvector  
2. **Analysis model** (Ollama) → JSON research notes  
3. **DomainAdapter** → topic-specific sources, prompts, labels, persistence  

**Tool-agnostic:** works with any editor or coding agent. No vendor agent folders, rules packs, or IDE plugins are part of this template.

## Domain vs entity

**Domain** = topic plugin. **Entity** = one subject per run; many entities per domain.  
You choose `--entity`; sources fetch docs for that id. Details: [`CONCEPTS.md`](CONCEPTS.md).

## Non-negotiables

- Hard facts (prices, statutes, citations, dates, IDs) come from **deterministic sources / facts bundles**, never invented by the LLM.
- Analysis output is **validated JSON** (Pydantic) with one repair attempt.
- Empty RAG → sentinel string in context and usually `missing_data`.
- Domains live under `app/domains/<name>/` and call `register_domain(...)` at import; platform code stays domain-neutral. Subpackages are auto-discovered.

## How to specialize

Clone this template → replace the **IDEA** in [`prompts/START_NEW_PROJECT.md`](prompts/START_NEW_PROJECT.md) → paste into a coding agent ([`NEW_PROJECT.md`](NEW_PROJECT.md)). The agent invents domain, sources, and schema from your idea.

## Commands

```bash
uv sync
uv run python scripts/init_db.py
uv run python scripts/ingest_entity.py --domain notes --entity demo
uv run python scripts/analyze_entity.py --domain notes --entity demo
uv run python scripts/run_entity.py --domain notes --entity demo   # ingest + analyze
uv run pytest -q
uv run ruff check .
```

## Stack

Python 3.11+, uv, Postgres + pgvector, Ollama (`nomic-embed-text`, `qwen3:8b` by default).

Env: `DATABASE_URL`, `OLLAMA_URL`, `EMBEDDING_MODEL`, `ANALYSIS_MODEL` — see [`SETUP.md`](SETUP.md) (includes macOS and Linux install notes). Same `.env` on both OSes.
