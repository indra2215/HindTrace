# HindTrace — Ingestion Subsystem

This directory contains the multi-source data ingestion pipeline for corporate engineering artifacts.

## Components

1. **`corpus_loader.py`**:
   - Primary corpus ingestion pipeline.
   - Parses YAML frontmatter headers from all 100 documents in `corpus/`.
   - Builds in-memory BM25 sparse index and entity index for sub-millisecond retrieval.
   - Enforces RBAC/ACL boundaries (`tier`, `acl_teams`, `acl_users`).
   - Implements prompt injection detection and neutralization.

2. **`slack_parser.py`**:
   - Parses simulated Slack channel exports (`doc_type: slack_thread`).
   - Extracts timestamps, author personas, and threaded conversational turns.

3. **`email_parser.py`**:
   - Parses simulated email postmortems and chains (`doc_type: email_thread`).
   - Separates headers (`From`, `To`, `Subject`) from discussion body.

4. **`gdrive_parser.py`**:
   - Parses Google Drive SOPs, runbooks, and postmortems (`doc_type: runbook`).
   - Performs step-level chunking preserving environment branches (e.g. PyTorch 2.1.0 staging vs PyTorch 2.2.1 production in `RB-14`).

