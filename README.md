# RAG Analyzer

Local **dual-model RAG** template: one Ollama model for **embeddings**, one for **analysis**.  
Postgres + pgvector stores documents and chunks. Domains (notes, laws, …) plug in via a `DomainAdapter`.

Research notebook you configure — not advice. **Tool-agnostic:** no IDE vendor agent folders or rules packs required.

## Quick start

```bash
# install uv once: curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync
cp .env.example .env   # set DATABASE_URL; create DB + pgvector (see docs/SETUP.md)
uv run python scripts/init_db.py
uv run python scripts/ingest_entity.py --domain notes --entity demo
uv run python scripts/analyze_entity.py --domain notes --entity demo
uv run pytest -q
```

## Start a project for your topic

1. Get the template running (above).
2. Choose a path:
   - **Add a domain** here → [`docs/ADDING_A_DOMAIN.md`](docs/ADDING_A_DOMAIN.md)
   - **Specialize the whole repo** → [`docs/NEW_PROJECT.md`](docs/NEW_PROJECT.md)
3. Paste a filled prompt from [`docs/prompts/`](docs/prompts/) into any coding agent or chat LLM to scaffold sources, labels, and schema.

## Layout

| Path | Role |
|------|------|
| `app/` | Platform (db, ollama, ingest, rag, analysis) |
| `app/domains/` | Pluggable domains (`notes` ships as example) |
| `scripts/` | Thin CLIs |
| `docs/` | Setup, architecture, new-project guide |
| `docs/prompts/` | Copy-paste prompts to bootstrap a domain or product |

## Docs

- [`docs/NEW_PROJECT.md`](docs/NEW_PROJECT.md) — fork or add a topic
- [`docs/prompts/`](docs/prompts/) — AI prompts to start fast
- [`docs/AI_CONTEXT.md`](docs/AI_CONTEXT.md) — short brief for any human or coding agent
- [`docs/SETUP.md`](docs/SETUP.md)
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- [`docs/ADDING_A_DOMAIN.md`](docs/ADDING_A_DOMAIN.md)

## Commands

```bash
uv run python scripts/init_db.py
uv run python scripts/ingest_entity.py --domain notes --entity demo
uv run python scripts/analyze_entity.py --domain notes --entity demo
uv run pytest -q
uv run ruff check .
uv run ruff format .
```
