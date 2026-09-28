"""
FastAPI Request and Response Models
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class InvestigateRequest(BaseModel):
    query: str
    user_name: str = "Marta Silva"
    sev_level: int = 3
    force_search: bool = False

class MemoryRecallRequest(BaseModel):
    query: str
    bank: Optional[str] = None
    limit: int = 5

class MemoryRetainRequest(BaseModel):
    bank: str
    incident_id: str
    root_cause: str
    resolution: str
    context: Optional[str] = None

class FeedbackRequest(BaseModel):
    incident_id: str
    user_name: str
    verdict_correct: bool
    notes: Optional[str] = None
