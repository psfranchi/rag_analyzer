#!/usr/bin/env python3
"""Ingest then analyze one entity (both faces in one command)."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts.analyze_entity import main as analyze_main
from scripts.ingest_entity import main as ingest_main

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Ingest documents then run analysis for one entity"
    )
    parser.add_argument("--domain", required=True, help="Domain name, e.g. notes")
    parser.add_argument("--entity", required=True, help="Entity key, e.g. demo")
    args = parser.parse_args(argv)
    pair = ["--domain", args.domain, "--entity", args.entity]

    logger.info("step 1/2 ingest domain=%s entity=%s", args.domain, args.entity)
    code = ingest_main(pair)
    if code != 0:
        return code

    logger.info("step 2/2 analyze domain=%s entity=%s", args.domain, args.entity)
    return analyze_main(pair)


if __name__ == "__main__":
    raise SystemExit(main())
