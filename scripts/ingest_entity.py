#!/usr/bin/env python3
"""Ingest documents for one entity in a domain."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from app.config import get_settings
from app.db.database import create_db_engine, session_scope
from app.domains.registry import get_domain, list_domains
from app.ingestion.pipeline import ingest_entity
from app.ollama.client import OllamaClient, OllamaConnectionError

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Ingest documents for one entity")
    parser.add_argument("--domain", required=True, help=f"Domain name, e.g. {list_domains()}")
    parser.add_argument("--entity", required=True, help="Entity key, e.g. demo")
    args = parser.parse_args(argv)

    try:
        settings = get_settings()
        adapter = get_domain(args.domain)
    except Exception as exc:
        logger.error("%s", exc)
        return 1

    engine = create_db_engine(settings)
    ollama = OllamaClient(settings)
    try:
        with session_scope(engine) as session:
            counts = ingest_entity(
                session,
                adapter=adapter,
                entity_key=args.entity,
                ollama=ollama,
                progress=lambda m: logger.info("%s", m),
            )
        print(counts)
        return 0
    except OllamaConnectionError as exc:
        logger.error("Ollama unreachable: %s", exc)
        return 1
    except Exception as exc:
        logger.error("ingest failed: %s", exc)
        return 1
    finally:
        engine.dispose()


if __name__ == "__main__":
    raise SystemExit(main())
