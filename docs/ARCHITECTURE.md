# Architecture

## Domain vs entity

| | Role | CLI |
|--|------|-----|
| Domain | Topic plugin (`app/domains/<slug>/`) | `--domain notes` |
| Entity | One subject; many per domain | `--entity demo` |

See [`CONCEPTS.md`](CONCEPTS.md). Pipeline below always runs for **one** `(domain, entity)` pair.

## Pipeline

Two faces for each `(domain, entity)`:

1. **Ingest** — fetch → chunk → embed → store  
2. **Analyze** — retrieve → prompt → JSON report  

CLI: `ingest_entity.py` and `analyze_entity.py` separately, or `run_entity.py` for both. See [`CONCEPTS.md`](CONCEPTS.md).

```text
Document sources (domain, for one entity)
    → chunk + embed (platform, Ollama embedding model)
    → Postgres / pgvector
    → retrieve + context (platform; domain supplies queries)
    → analysis prompt (domain)
    → Ollama analysis model → JSON
    → Pydantic validate (+ one repair)
    → analysis_reports
```

## Layers

| Layer | Package | Responsibility |
|-------|---------|----------------|
| Config | `app/config.py` | `DATABASE_URL`, `OLLAMA_URL`, models |
| DB | `app/db/` | Engine, `Entity`, `Document`, `DocumentChunk`, `AnalysisReport` |
| Ollama | `app/ollama/` | Dual HTTP client: `/api/embeddings` + `/api/generate` |
| Ingest | `app/ingestion/` | Chunk, hash, quality, store, `ingest_entity` |
| RAG | `app/rag/` | Cosine retrieve, context blocks, empty sentinel |
| Analysis | `app/analysis/` | JSON extract, `analyze_entity` orchestration |
| Domains | `app/domains/` | Adapter protocol + plugins (`notes`, …) |

## Dual models

| Role | Env | Default |
|------|-----|---------|
| Embed | `EMBEDDING_MODEL` | `nomic-embed-text` (768-d) |
| Analyze | `ANALYSIS_MODEL` | `qwen3:8b` |

## DomainAdapter

See `app/domains/base.py`. Platform code only talks to the adapter interface.

Registration: each `app/domains/<slug>/` package calls `register_domain` on import. `get_domain` / `list_domains` auto-import those subpackages.

Specialize via [`NEW_PROJECT.md`](NEW_PROJECT.md) and [`prompts/START_NEW_PROJECT.md`](prompts/START_NEW_PROJECT.md).
