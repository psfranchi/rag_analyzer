# Domain vs entity (read this first)

This template analyzes **one subject at a time**. Two words matter:

| Term | Meaning | Example (games) | Example (ships with template) |
|------|---------|-----------------|-------------------------------|
| **Domain** | The *kind* of research (one plugin / product topic) | `games` | `notes` |
| **Entity** | *One* thing you run ingest/analyze on | `hades`, `celeste` | `demo` |

```text
domain  = games          →  app/domains/games/ , data/games/
entity  = hades          →  data/games/hades/  ,  --entity hades
entity  = celeste        →  data/games/celeste/
```

## Two faces: ingest and analyze

Every entity run has two steps. You can run them **separately** or **together**.

| Face | Script | What it does |
|------|--------|----------------|
| **Ingest** | `scripts/ingest_entity.py` | Fetch docs for the entity → chunk → embed → store in Postgres/pgvector |
| **Analyze** | `scripts/analyze_entity.py` | Retrieve chunks → prompt the analysis model → validate JSON → save a report |

```text
ingest   = get documents into the DB (embeddings)
analyze  = RAG + LLM JSON note for that entity
```

**Separately** (re-analyze without re-fetching, or ingest only while iterating on sources):

```bash
uv run python scripts/ingest_entity.py --domain notes --entity demo
uv run python scripts/analyze_entity.py --domain notes --entity demo
```

**Together** (usual happy path — ingest then analyze in one go):

```bash
uv run python scripts/run_entity.py --domain notes --entity demo
```

Analyze needs prior ingest (or an earlier ingest) so there is something to retrieve. Empty RAG still runs, but the report will usually flag missing data.

## You choose the entity; sources fetch for it

You do **not** wait for a data source to invent the id.

1. Decide what you’re researching → pick a short id (`hades`).
2. Put docs where the source expects them (e.g. `data/games/hades/*.md`), **or** point an API source at that id.
3. Run ingest and/or analyze (see above).

Same domain, **many** entities: repeat with `--entity celeste`, etc. Each gets its own documents and reports in the DB.

## What to put in the new-project IDEA

You only need a plain-language goal. Example: “games notebook — local notes per game, JSON on whether it looks interesting.”  
The agent picks domain slug, entity id rules, sources, and schema. Use this doc when you (or the agent) need the vocabulary.

## What this template is not (yet)

A single query like “find interesting games” across an unknown catalog is **discovery/search**. The default loop is: **you already care about this entity → ingest its docs → analyze it.**  
“Interesting” usually belongs in the **JSON labels** (e.g. worth_playing / skip) or in *which* entities you choose to run — not in skipping `--entity`.
