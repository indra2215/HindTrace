"""
Stage 4: Evidence Synthesis & Root Cause Determination
"""
from typing import Dict, Any, List

def synthesize_investigation(query: str, chunks: List[Dict[str, Any]], user_name: str, sev_level: int) -> Dict[str, Any]:
    from agents.pipeline import stage4_synthesizer
    return stage4_synthesizer(query, chunks, user_name, sev_level)
