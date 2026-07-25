#!/usr/bin/env python3
"""Analyze one entity: RAG + Ollama JSON → stdout."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from app.analysis.runner import AnalysisError, analyze_entity
from app.config import get_settings
from app.db.database import create_db_engine, session_scope
from app.domains.registry import get_domain, list_domains
from app.ollama.client import OllamaClient, OllamaConnectionError

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s", stream=sys.stderr)
logger = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze one entity using RAG + Ollama")
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
            result = analyze_entity(session, adapter=adapter, entity_key=args.entity, ollama=ollama)
        print(result.model_dump_json(indent=2))
        return 0
    except AnalysisError as exc:
        logger.error("%s", exc)
        return 1
    except OllamaConnectionError as exc:
        logger.error("Ollama unreachable: %s", exc)
        return 1
    except Exception as exc:
        logger.error("analyze failed: %s", exc)
        return 1
    finally:
        engine.dispose()


if __name__ == "__main__":
    raise SystemExit(main())
