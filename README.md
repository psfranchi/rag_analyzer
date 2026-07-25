# RAG Analyzer

Local **dual-model RAG** template: one Ollama model for **embeddings**, one for **analysis**.  
Postgres + pgvector stores documents and chunks. Your topic plugs in via a `DomainAdapter`.

Research notebook you configure — not advice. **Tool-agnostic:** no IDE vendor agent folders or rules packs required.

## Quick start

```bash
# install uv once: curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
cp .env.example .env   # macOS/Linux install + Ollama/DB: docs/SETUP.md
uv run python scripts/init_db.py
# ingest + analyze together (or run the two scripts separately — see docs/CONCEPTS.md)
uv run python scripts/run_entity.py --domain notes --entity demo
uv run pytest -q
```

## Start your project

1. Get the template running (above).
2. Clone/copy into a new folder ([`docs/NEW_PROJECT.md`](docs/NEW_PROJECT.md)).
3. Paste [`docs/prompts/START_NEW_PROJECT.md`](docs/prompts/START_NEW_PROJECT.md) into any coding agent — replace the **IDEA** with what you want; the agent fills the rest.

## Layout

| Path | Role |
|------|------|
| `app/` | Platform (db, ollama, ingest, rag, analysis) |
| `app/domains/` | Topic plugin (`notes` ships as example) |
| `scripts/` | Thin CLIs (`ingest_entity`, `analyze_entity`, `run_entity` = both) |
| `docs/` | Setup, architecture, new-project guide |
| `docs/prompts/` | Copy-paste prompt to bootstrap your product |

## Docs

- [`docs/CONCEPTS.md`](docs/CONCEPTS.md) — domain vs entity; ingest vs analyze (separate or together)
- [`docs/NEW_PROJECT.md`](docs/NEW_PROJECT.md) — specialize this template
- [`docs/prompts/START_NEW_PROJECT.md`](docs/prompts/START_NEW_PROJECT.md) — prompt to start fast
- [`docs/AI_CONTEXT.md`](docs/AI_CONTEXT.md) — short brief for any human or coding agent
- [`docs/SETUP.md`](docs/SETUP.md)
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)

## Commands

```bash
uv run python scripts/init_db.py
uv run python scripts/ingest_entity.py --domain notes --entity demo
uv run python scripts/analyze_entity.py --domain notes --entity demo
uv run python scripts/run_entity.py --domain notes --entity demo   # both
uv run pytest -q
uv run ruff check .
uv run ruff format .
```
