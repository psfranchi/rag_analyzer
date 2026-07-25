# Setup

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- PostgreSQL + [pgvector](https://github.com/pgvector/pgvector)
- [Ollama](https://ollama.com/) with an embedding model and an analysis model  
  Defaults: `nomic-embed-text`, `qwen3:8b`

## Install

```bash
cd /path/to/rag_analyzer
uv sync
cp .env.example .env
```

Create a database (example):

```sql
CREATE USER rag WITH PASSWORD 'rag';
CREATE DATABASE rag_analyzer OWNER rag;
\c rag_analyzer
CREATE EXTENSION IF NOT EXISTS vector;
```

Set `DATABASE_URL` in `.env` to match (see `.env.example`). Pull models if needed:

```bash
ollama pull nomic-embed-text
ollama pull qwen3:8b
```

```bash
uv run python scripts/init_db.py
```

## Smoke (notes domain)

Demo markdown lives at `data/notes/demo/`.

```bash
uv run python scripts/ingest_entity.py --domain notes --entity demo
uv run python scripts/analyze_entity.py --domain notes --entity demo
uv run pytest -q
uv run ruff check .
```

## Next: your topic

- New project / fork: [`NEW_PROJECT.md`](NEW_PROJECT.md)
- New domain only: [`ADDING_A_DOMAIN.md`](ADDING_A_DOMAIN.md)
- Copy-paste AI prompts: [`prompts/`](prompts/)

## Lint / format

```bash
uv run ruff check .
uv run ruff format .
```
