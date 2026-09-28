"""
Google Drive & Runbook Parser
=============================
Parses standard operating procedures and runbooks (doc_type: runbook / postmortem).
Splits procedures at step-level to maintain conditional execution branches
(e.g., PyTorch 2.1.0 staging vs PyTorch 2.2.1 production in RB-14).
"""

import re

def parse_runbook_steps(body: str, doc_id: str) -> list[dict]:
    """Extract step-level sections from runbooks preserving version/environment contexts."""
    # Split on markdown headings e.g. ## Step 1, ### Step 8
    sections = re.split(r"(?m)^(?=#{1,3}\s+(?:Step\s+\d+|Context|Phase\s+\d+))", body)
    chunks = []

    for idx, sec in enumerate(sections):
        sec = sec.strip()
        if not sec:
            continue
        
        # Check if this step contains version branches
        has_staging = bool(re.search(r"staging|torch-2\.1\.0|workaround", sec, re.IGNORECASE))
        has_prod = bool(re.search(r"prod|torch-2\.2\.1|permanent", sec, re.IGNORECASE))

        chunks.append({
            "doc_id": doc_id,
            "step_index": idx,
            "text": sec,
            "is_branch": has_staging or has_prod,
            "branch_type": "staging" if (has_staging and not has_prod) else ("prod" if (has_prod and not has_staging) else "mixed"),
        })

    return chunks
