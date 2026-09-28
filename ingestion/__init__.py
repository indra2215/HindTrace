"""
Ingestion Subsystem for HindTrace
"""

from .indexers.corpus_loader import (
    load_corpus,
    retrieve,
    sanitise_query,
    is_loaded,
)
from .parsers.slack_parser import parse_slack_thread
from .parsers.email_parser import parse_email_thread
from .parsers.gdrive_parser import parse_runbook_steps

# Alias for backwards compatibility
hybrid_search = retrieve

__all__ = [
    "load_corpus",
    "retrieve",
    "hybrid_search",
    "sanitise_query",
    "is_loaded",
    "parse_slack_thread",
    "parse_email_thread",
    "parse_runbook_steps",
]

