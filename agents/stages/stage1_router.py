"""
Stage 1: Incident Router & Triage
"""
from typing import Dict, Any

def route_incident(query: str, user_name: str) -> Dict[str, Any]:
    from agents.pipeline import stage1_router
    return stage1_router(query, user_name)
