"""
Stage 2: Hybrid Multi-Source Retriever & ACL Enforcement
"""
from typing import Dict, Any, List

def retrieve_evidence(query: str, user_name: str, top_k: int = 6) -> List[Dict[str, Any]]:
    from agents.pipeline import stage2_retriever
    return stage2_retriever(query, user_name, top_k=top_k)
