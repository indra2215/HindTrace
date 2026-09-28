"""
Chunking Utilities for Markdown Runbooks, Slack Threads, and Incident Reports
"""
import re
from typing import List, Dict, Any

def chunk_markdown_by_headings(content: str, source_id: str = "") -> List[Dict[str, Any]]:
    """Splits markdown documents into step-level semantic chunks based on headings."""
    sections = re.split(r'\n(?=#{1,4}\s)', content)
    chunks = []
    for idx, sec in enumerate(sections):
        cleaned = sec.strip()
        if not cleaned:
            continue
        first_line = cleaned.splitlines()[0].strip("# ")
        chunks.append({
            "chunk_id": f"{source_id}_chunk_{idx}",
            "heading": first_line,
            "text": cleaned,
            "char_count": len(cleaned)
        })
    return chunks
