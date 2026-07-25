# Start a new analyzer project

This repo is a **template**. Clone or copy it, then specialize it for one research topic (laws, medical notes, product reviews, …).

## Path A — one new domain in this repo (fastest)

Use when you want another topic beside `notes`.

1. Smoke-test the template (see [`SETUP.md`](SETUP.md)).
2. Open [`prompts/START_NEW_DOMAIN.md`](prompts/START_NEW_DOMAIN.md), fill the blanks, paste into any coding agent or chat LLM.
3. Or follow the manual checklist in [`ADDING_A_DOMAIN.md`](ADDING_A_DOMAIN.md).

New domains are **auto-discovered**: add `app/domains/<name>/` with `register_domain(...)` at import time. No edit to `registry.py`.

## Path B — fork the whole repo for one product

Use when this becomes a dedicated app (rename, own DB, own domain only).

1. Copy the repo (or create a new GitHub repo from this template).
2. Rename in `pyproject.toml` / README if you want a product name.
3. Create a Postgres DB + set `.env` from `.env.example`.
4. Open [`prompts/START_NEW_PROJECT.md`](prompts/START_NEW_PROJECT.md), fill the blanks, paste into any coding agent or chat LLM.
5. Keep or delete the example `notes` domain once yours works.

## What you customize vs leave alone

| Customize | Leave alone (platform) |
|-----------|------------------------|
| `app/domains/<your_domain>/` | `app/db/`, `app/ollama/`, `app/ingestion/`, `app/rag/`, `app/analysis/` |
| Labels, prompts, Pydantic schema | Dual-model Ollama wiring |
| Document sources / fetchers | Chunking, embeddings, retrieval loop |
| `data/<domain>/…` sample files | Generic `Entity` / `Document` / `AnalysisReport` tables |
| Domain tests under `tests/` | `scripts/ingest_entity.py`, `scripts/analyze_entity.py` |

## Success criteria

After specialization you can run:

```bash
uv run python scripts/ingest_entity.py --domain <your_domain> --entity <key>
uv run python scripts/analyze_entity.py --domain <your_domain> --entity <key>
uv run pytest -q
```

and get validated JSON research notes grounded in retrieved context — not invented facts.
