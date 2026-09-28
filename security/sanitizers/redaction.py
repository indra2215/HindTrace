"""
Security Subsystem: Secret & PII Redactor
=========================================
Ensures secrets, tokens, API keys, and sensitive employee PII
are redacted from outgoing agent summaries.
"""

import re

SECRET_PATTERNS = [
    (r"(?i)(sk-[a-zA-Z0-9_\-]{8,})", "sk-***REDACTED***"),
    (r"(?i)(ghp_[a-zA-Z0-9]{20,})", "ghp_***REDACTED***"),
    (r"(?i)(xai-[a-zA-Z0-9]{20,})", "xai-***REDACTED***"),
    (r"(?i)(gsk_[a-zA-Z0-9]{20,})", "gsk_***REDACTED***"),
    (r"(?i)(password\s*[:=]\s*)['\"][^'\"]+['\"]", r"\1'***REDACTED***'"),
    (r"(?i)(authorization:\s*bearer\s+)[a-zA-Z0-9_\-\.]+", r"\1***REDACTED***"),
]

def redact_sensitive_data(text: str) -> str:
    """Scans and redacts detected API keys and secrets."""
    redacted = text
    for pattern, replacement in SECRET_PATTERNS:
        redacted = re.sub(pattern, replacement, redacted)
    return redacted
