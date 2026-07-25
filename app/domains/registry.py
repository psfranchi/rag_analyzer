"""Domain name → factory registry with package auto-discovery."""

from __future__ import annotations

import importlib
import pkgutil
from collections.abc import Callable

from app.domains.base import DomainAdapter

_REGISTRY: dict[str, Callable[[], DomainAdapter]] = {}
_DISCOVERED = False


def register_domain(name: str, factory: Callable[[], DomainAdapter]) -> None:
    _REGISTRY[name.strip().lower()] = factory


def _discover_domains() -> None:
    """Import every subpackage under app.domains so register_domain() runs."""
    global _DISCOVERED
    if _DISCOVERED:
        return
    _DISCOVERED = True
    import app.domains as domains_pkg

    for mod in pkgutil.iter_modules(domains_pkg.__path__, domains_pkg.__name__ + "."):
        if mod.ispkg:
            importlib.import_module(mod.name)


def get_domain(name: str) -> DomainAdapter:
    _discover_domains()
    key = name.strip().lower()
    if key not in _REGISTRY:
        known = ", ".join(sorted(_REGISTRY)) or "(none)"
        raise KeyError(f"unknown domain {name!r}; registered: {known}")
    return _REGISTRY[key]()


def list_domains() -> list[str]:
    _discover_domains()
    return sorted(_REGISTRY)
