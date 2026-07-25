# Prompt: start a new project

Describe what you want in plain language (a few sentences is enough). Paste everything below the line into any coding agent or chat LLM.

The agent should invent sensible defaults (domain name, entity ids, sources, JSON schema, labels) from your idea. You do **not** need to fill a long form. Optional: skim [`../CONCEPTS.md`](../CONCEPTS.md) if you want the vocabulary (domain / entity / ingest / analyze).

**Replace the `IDEA` block** with your own. Example left in place so you see the shape.

---

```text
You are specializing the rag_analyzer template into a dedicated research analyzer.

## What this template already is (do not rebuild)

Local dual-model RAG on Postgres/pgvector + Ollama:
1. **Ingest** — fetch documents for one subject → chunk → embed → store
2. **Analyze** — retrieve → analysis model → validated JSON research notes
3. Optional **run both**: scripts/run_entity.py
4. Topic logic lives only in a DomainAdapter under app/domains/<slug>/
5. Many subjects (entities) per topic (domain); user picks --entity

Read: docs/AI_CONTEXT.md, docs/CONCEPTS.md, docs/ARCHITECTURE.md, app/domains/base.py, app/domains/notes/__init__.py

## IDEA (user — replace this)

I want a games research notebook. For a game I care about, pull or load notes/reviews,
ingest them, and produce a short JSON note on whether it looks interesting to play —
research notes only, not recommendations-as-advice. Start simple with local markdown
files per game; we can add APIs later.

## What you should decide (fill the gaps)

From the IDEA alone, choose and implement:
- Product name + domain slug
- How one subject is identified (--entity / folder or id rule)
- Document source(s) for v1 (prefer local files under data/<domain>/<entity>/ unless the idea needs an API)
- Analysis labels + Pydantic JSON schema + prompts
- One or two sample entities with demo data
- README / SETUP / AI_CONTEXT updates for THIS product

## Deliverables

1. Specialize branding (README, pyproject description).
2. New DomainAdapter; remove notes only after the new domain has tests + a smoke path.
3. Show ingest, analyze, and run_entity for an example entity.
4. pytest + ruff clean.
5. Keep platform packages domain-neutral.

Platform rules:
- No inventing hard facts in the LLM; facts from sources / deterministic refresh_facts only.
- Empty RAG → sentinel + missing_data; JSON validate + one repair.
- Research notes only — not financial/legal/medical advice framing.
- Tool-agnostic — no IDE vendor agent/rules files unless asked.
- Default loop is per-entity ingest/analyze (see docs/CONCEPTS.md).

End with a short “How to run” blurb for the README.
```
