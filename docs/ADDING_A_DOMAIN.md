# Adding a domain

Add a research domain **without** changing platform packages (`app/db`, `app/ollama`, `app/ingestion`, `app/rag`, `app/analysis`).

Prefer the prompt in [`prompts/START_NEW_DOMAIN.md`](prompts/START_NEW_DOMAIN.md) if you want a coding agent to do the scaffolding. Manual steps below.

## Checklist

1. **Copy** `app/domains/notes/` → `app/domains/<slug>/` (e.g. `laws`).
2. **Register** with `register_domain("<slug>", factory)` at import time in that package.  
   Subpackages under `app/domains/` are **auto-discovered** — do not edit `registry.py`.
3. **Entity identity** — stable keys (e.g. `USC-42-1983`), not free-form titles alone.
4. **DocumentSource(s)** — each `fetch(entity_key)` returns dicts:
   ```python
   {
     "source_type": "statute",   # your types
     "source_url": "...",
     "title": "...",
     "published_at": None,       # or datetime
     "raw_text": "...",
   }
   ```
5. **`source_quality`** — map `source_type` → 0.0–1.0 (official > commentary).
6. **`refresh_facts`** — deterministic metadata only. Never invent from the LLM.
7. **`build_queries` / `score_chunk`** — bias retrieval for your corpus.
8. **Labels + schema** — replace notes labels; update Pydantic model, `schema_text`, and system prompt together.
9. **`persist_report`** — write into generic `analysis_reports` (or extend later with domain columns).
10. **Sample data** — e.g. `data/<slug>/<entity>/…` if you use local files.
11. **Tests** — registry, source fetch, prompt/schema smoke.
12. **Env** — document new keys in `.env.example` and [`SETUP.md`](SETUP.md).

## CLI

```bash
uv run python scripts/ingest_entity.py --domain <slug> --entity <key>
uv run python scripts/analyze_entity.py --domain <slug> --entity <key>
```

List registered domains (Python):

```bash
uv run python -c "from app.domains import list_domains; print(list_domains())"
```

## Do not

- Import topic-specific code into `app/rag` or `app/ollama`
- Let the model invent citations, prices, statutes, or other hard facts
- Add IDE-/vendor-specific agent or rules files to the template unless you intentionally want them
