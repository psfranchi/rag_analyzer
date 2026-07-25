# Setup

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- PostgreSQL + [pgvector](https://github.com/pgvector/pgvector)
- [Ollama](https://ollama.com/) with an embedding model and an analysis model  
  Defaults: `nomic-embed-text`, `qwen3:8b`

## 1. Install uv + project

**macOS / Linux** (same):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
cd /path/to/rag_analyzer
uv sync
cp .env.example .env
```

Edit `.env` — see [Configuration](#configuration) below.

## 2. Ollama

App talks to Ollama over HTTP (`OLLAMA_URL`, default `http://localhost:11434`).

### macOS

1. Install from [ollama.com](https://ollama.com/download) (or `brew install ollama`).
2. Start the app (menu bar) or run `ollama serve`.
3. Pull models:

```bash
ollama pull nomic-embed-text
ollama pull qwen3:8b
```

4. Check:

```bash
curl -s http://localhost:11434/api/tags | head
ollama list
```

### Linux

1. Install:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

2. Service usually starts automatically. If not:

```bash
ollama serve
# or, with systemd:
# sudo systemctl enable --now ollama
```

3. Pull models:

```bash
ollama pull nomic-embed-text
ollama pull qwen3:8b
```

4. Check:

```bash
curl -s http://localhost:11434/api/tags | head
ollama list
systemctl status ollama   # if using systemd
```

### Notes

- Analysis model needs enough RAM/VRAM; smaller tags (e.g. `qwen3:4b`) work if `qwen3:8b` is too heavy — set `ANALYSIS_MODEL` in `.env`.
- If Ollama runs on another host/port, set `OLLAMA_URL` (e.g. `http://192.168.1.10:11434`).
- Embedding dimension is fixed at **768** for `nomic-embed-text`. Changing `EMBEDDING_MODEL` to a different size requires a matching DB vector column (advanced).

## 3. PostgreSQL + pgvector

### macOS (Homebrew)

```bash
brew install postgresql@16 pgvector
brew services start postgresql@16
```

Create role + DB (adjust if your Homebrew Postgres user differs — often your macOS username has superuser access):

```bash
createuser -s rag 2>/dev/null || true
psql postgres -c "ALTER USER rag WITH PASSWORD 'rag';" 2>/dev/null || \
  psql postgres -c "CREATE USER rag WITH PASSWORD 'rag' SUPERUSER;"
createdb -O rag rag_analyzer
psql -d rag_analyzer -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

If `pgvector` is not found as an extension, install/link per [pgvector](https://github.com/pgvector/pgvector#installation) for your Postgres version, then re-run the `CREATE EXTENSION` line.

### Linux (Debian/Ubuntu example)

```bash
sudo apt update
sudo apt install -y postgresql postgresql-contrib
sudo systemctl enable --now postgresql
```

Install pgvector for your Postgres major version (package name varies by distro). Examples:

```bash
# Ubuntu 24.04+ often has:
sudo apt install -y postgresql-16-pgvector
# or build from https://github.com/pgvector/pgvector
```

Then:

```bash
sudo -u postgres psql <<'SQL'
CREATE USER rag WITH PASSWORD 'rag';
CREATE DATABASE rag_analyzer OWNER rag;
\c rag_analyzer
CREATE EXTENSION IF NOT EXISTS vector;
SQL
```

On some setups you must allow password auth in `pg_hba.conf` for local TCP (`localhost:5432`), then `sudo systemctl reload postgresql`.

### Verify DB

```bash
psql "postgresql://rag:rag@localhost:5432/rag_analyzer" -c "SELECT extname FROM pg_extension WHERE extname = 'vector';"
```

## Smoke (notes domain)

`--domain notes` is the topic. `--entity demo` is **one** subject (folder `data/notes/demo/`).  
Add another subject anytime as `data/notes/<other_id>/` and pass `--entity <other_id>`. See [`CONCEPTS.md`](CONCEPTS.md).

Two faces: **ingest** (docs → embeddings) and **analyze** (RAG → JSON). Run them separately or together:

```bash
uv run python scripts/init_db.py
uv run python scripts/ingest_entity.py --domain notes --entity demo
uv run python scripts/analyze_entity.py --domain notes --entity demo
# same as both steps:
uv run python scripts/run_entity.py --domain notes --entity demo
uv run pytest -q
```

## Configuration

Copy `.env.example` → `.env`. All values below are required for CLI flows.

| Variable | Purpose | Default / example |
|----------|---------|-------------------|
| `DATABASE_URL` | Postgres connection | `postgresql://rag:rag@localhost:5432/rag_analyzer` |
| `OLLAMA_URL` | Ollama HTTP base (no trailing path) | `http://localhost:11434` |
| `EMBEDDING_MODEL` | Ollama embed model (768-d with nomic) | `nomic-embed-text` |
| `ANALYSIS_MODEL` | Ollama generate model | `qwen3:8b` |

Same `.env` shape on **macOS and Linux**. OS differences are only how you install Postgres/Ollama; the app config does not change.

Optional checks:

```bash
# Ollama up?
curl -s "$OLLAMA_URL/api/tags"   # or http://localhost:11434/api/tags

# Models present?
ollama list
```

Loaded by `app/config.py` (pydantic-settings) from the process cwd `.env`.

## Next: your topic

- What the template does + specialize: [`NEW_PROJECT.md`](NEW_PROJECT.md)
- Short IDEA prompt: [`prompts/START_NEW_PROJECT.md`](prompts/START_NEW_PROJECT.md)
- Vocabulary: [`CONCEPTS.md`](CONCEPTS.md)

## Lint / format

```bash
uv run ruff check .
uv run ruff format .
```
