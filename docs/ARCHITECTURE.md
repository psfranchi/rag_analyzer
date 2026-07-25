# Architecture

```text
Document sources (domain)
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

Specialize via [`NEW_PROJECT.md`](NEW_PROJECT.md) or [`ADDING_A_DOMAIN.md`](ADDING_A_DOMAIN.md).
