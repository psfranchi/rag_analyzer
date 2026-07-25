#!/usr/bin/env python3
"""Initialize database schema (pgvector + tables)."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from app.config import get_settings
from app.db.database import create_db_engine, init_schema

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main() -> int:
    try:
        settings = get_settings()
    except Exception as exc:
        logger.error("Missing or invalid settings: %s", exc)
        return 1
    engine = create_db_engine(settings)
    try:
        logger.info("Creating extension and tables…")
        init_schema(engine)
        logger.info("init_db OK")
        return 0
    except Exception as exc:
        logger.error("init_db failed: %s", exc)
        return 1
    finally:
        engine.dispose()


if __name__ == "__main__":
    raise SystemExit(main())
