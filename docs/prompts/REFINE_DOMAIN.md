# Prompt: refine an existing domain

Use after a first domain draft exists. Fill the blanks, paste below the line into any coding agent or chat LLM.

---

```text
Refine the DomainAdapter for domain YOUR_DOMAIN_SLUG in this rag_analyzer repo.

Read: docs/AI_CONTEXT.md, app/domains/base.py, app/domains/YOUR_DOMAIN_SLUG/, and the current tests.

Problems to fix / improve:
- YOUR_ISSUES (e.g. weak retrieval queries, vague labels, thin system prompt, bad source quality weights, invented fields in schema)

Goals:
- Clearer decision labels and when each applies
- Stronger build_queries / score_chunk for this corpus
- System + user prompts that forbid inventing YOUR_FACTS
- Schema fields that match what a human actually uses in the report
- Tests covering the changed behavior

Do not change platform packages unless there is a clear bug. Keep CLI scripts thin.
When done: uv run pytest -q && uv run ruff check .
```
