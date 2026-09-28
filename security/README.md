# HindTrace — Security & Guardrails Subsystem

This directory implements defense-in-depth security layers protecting corporate incident intelligence.

## Components

1. **`acl_guard.py`**:
   - Implements squad and identity-based access control.
   - Enforces `public-internal`, `team`, and `restricted` document tiers.
   - Blocks unauthorized team members (e.g. Leo Kim from web-dev attempting to query restricted finance doc `RET-001`).

2. **`injection_shield.py`**:
   - Sanitizes prompt injection attacks embedded inside untrusted incident logs or documents.
   - Replaces override directives (e.g. "ignore previous instructions") with `[FILTERED_INSTRUCTION_OVERRIDE]`.
   - Wraps document context in passive XML boundaries.

3. **`redaction.py`**:
   - Automatically redacts API keys, runner tokens (`sk-***REDACTED***`), and sensitive employee PII before responses leave the pipeline.

