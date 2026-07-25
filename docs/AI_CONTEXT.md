# AI context (tool-agnostic)

Short brief for any coding assistant or human working in this repo.

## What this is

Local **dual-model RAG** template:

1. **Embedding model** (Ollama) → chunk vectors in Postgres/pgvector  
2. **Analysis model** (Ollama) → JSON research notes  
3. **DomainAdapter** → domain-specific sources, prompts, labels, persistence  

**Tool-agnostic:** works with any editor or coding agent. No vendor agent folders, rules packs, or IDE plugins are part of this template.

## Non-negotiables

- Hard facts (prices, statutes, citations, dates, IDs) come from **deterministic sources / facts bundles**, never invented by the LLM.
- Analysis output is **validated JSON** (Pydantic) with one repair attempt.
- Empty RAG → sentinel string in context and usually `missing_data`.
- Domains live under `app/domains/<name>/` and call `register_domain(...)` at import; platform code stays domain-neutral. Subpackages are auto-discovered.

## How to specialize

| Goal | Doc / prompt |
|------|----------------|
| New domain in this repo | [`ADDING_A_DOMAIN.md`](ADDING_A_DOMAIN.md) + [`prompts/START_NEW_DOMAIN.md`](prompts/START_NEW_DOMAIN.md) |
| Fork into one product | [`NEW_PROJECT.md`](NEW_PROJECT.md) + [`prompts/START_NEW_PROJECT.md`](prompts/START_NEW_PROJECT.md) |
| Tighten an existing domain | [`prompts/REFINE_DOMAIN.md`](prompts/REFINE_DOMAIN.md) |

## Commands

```bash
uv sync
uv run python scripts/init_db.py
uv run python scripts/ingest_entity.py --domain notes --entity demo
uv run python scripts/analyze_entity.py --domain notes --entity demo
uv run pytest -q
uv run ruff check .
```

## Stack

Python 3.11+, uv, Postgres + pgvector, Ollama (`nomic-embed-text`, `qwen3:8b` by default).
