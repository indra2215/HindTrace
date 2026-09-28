"""
Email Thread & Postmortem Parser
================================
Parses simulated email thread exports from corpus documents (doc_type: email_thread).
Extracts sender, recipients, subject, and chain of replies.
"""

import re

def parse_email_thread(content: str) -> dict:
    """Parse simulated email postmortems into structured headers and body."""
    headers = {}
    body_lines = []
    in_headers = True

    for line in content.split("\n"):
        if in_headers:
            header_match = re.match(r"^(From|To|Subject|Date|Cc):\s*(.*)", line, re.IGNORECASE)
            if header_match:
                headers[header_match.group(1).lower()] = header_match.group(2).strip()
                continue
            elif line.strip() == "":
                in_headers = False
                continue
        body_lines.append(line)

    return {
        "type": "email_thread",
        "headers": headers,
        "from": headers.get("from", "unknown"),
        "subject": headers.get("subject", ""),
        "body": "\n".join(body_lines).strip(),
    }
