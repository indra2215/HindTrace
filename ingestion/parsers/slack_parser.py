"""
Slack Channel & Thread Parser
==============================
Parses simulated Slack thread exports from corpus documents (doc_type: slack_thread).
Extracts participating squad members, message timestamps, and key snippets.
"""

import re
from typing import Optional

def parse_slack_thread(content: str) -> dict:
    """Parse a simulated Slack thread body into structured messages."""
    lines = content.strip().split("\n")
    messages = []
    current_msg = None

    for line in lines:
        # Match pattern: [HH:MM] Author: Message
        match = re.match(r"^\[(\d{1,2}:\d{2}(?::\d{2})?)\]\s*([^:]+):\s*(.*)", line)
        if match:
            if current_msg:
                messages.append(current_msg)
            current_msg = {
                "timestamp": match.group(1),
                "author": match.group(2).strip(),
                "text": match.group(3).strip(),
            }
        elif current_msg:
            current_msg["text"] += "\n" + line

    if current_msg:
        messages.append(current_msg)

    participants = list(dict.fromkeys(m["author"] for m in messages))
    return {
        "type": "slack_thread",
        "message_count": len(messages),
        "participants": participants,
        "messages": messages,
    }
