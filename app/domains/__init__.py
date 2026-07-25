"""Domain plugins."""

from app.domains.base import DocumentSource, DomainAdapter
from app.domains.registry import get_domain, list_domains, register_domain

__all__ = [
    "DomainAdapter",
    "DocumentSource",
    "get_domain",
    "list_domains",
    "register_domain",
]
