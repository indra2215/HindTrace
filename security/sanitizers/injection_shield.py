"""
Security Subsystem: Prompt Injection Shield
===========================================
Detects and neutralizes malicious instruction overrides embedded in incident notes,
bug reports, and customer payloads (e.g., NOTE-INJECT in DOC-WEB-013).
"""

import re
from typing import Tuple

INJECTION_PATTERNS = [
    r"ignore\s+(?:all\s+)?(?:previous|prior)\s+instructions",
    r"disregard\s+(?:all\s+)?(?:previous|prior)\s+instructions",
    r"system\s*prompt",
    r"you\s+are\s+now\s+(?:a|an)\s+",
    r"act\s+as\s+(?:a|an|DAN|developer\s+mode)",
    r"print\s+(?:your\s+)?instructions",
    r"reveal\s+(?:your\s+)?prompt",
    r"<script[\s>]",
]

def detect_injection(text: str) -> bool:
    """Returns True if any prompt injection signature is detected."""
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def sanitise_and_wrap(text: str) -> Tuple[str, bool]:
    """
    Neutralises prompt injection.
    Wraps content inside strict XML data boundaries to enforce passive interpretation.
    """
    was_injected = detect_injection(text)
    clean_text = text
    if was_injected:
        for pattern in INJECTION_PATTERNS:
            clean_text = re.sub(pattern, "[FILTERED_INSTRUCTION_OVERRIDE]", clean_text, flags=re.IGNORECASE)
    
    # Enclose within passive data tags
    wrapped = f"<untrusted_document_content>\n{clean_text}\n</untrusted_document_content>"
    return wrapped, was_injected
