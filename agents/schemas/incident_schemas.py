"""
Incident Investigation Pydantic Schemas
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class IncidentQuery(BaseModel):
    query: str = Field(..., description="The incident description or error message")
    user_name: str = Field(default="Marta Silva", description="Name of the investigating engineer")
    user_role: str = Field(default="Staff SRE", description="Role of the engineer")
    user_team: str = Field(default="cloud-eng", description="Team of the engineer")
    sev_level: int = Field(default=3, description="Severity level: 1 (Critical) to 4 (Low)")
    force_search: bool = Field(default=False, description="Bypass memory recall cache")

class MemoryHit(BaseModel):
    bank: str
    incident_id: str
    root_cause: str
    resolution: str
    confidence: float
    retrieved_at: str

class RoutingDecision(BaseModel):
    is_safe: bool
    requires_retrieval: bool
    detected_incident_id: Optional[str] = None
    target_banks: List[str] = []
    risk_assessment: str = "nominal"

class InvestigationResponse(BaseModel):
    incident_id: str
    sev_level: int
    user: str
    verdict: str
    answer: str
    root_cause: Optional[str] = None
    steps_taken: List[str] = []
    sources_consulted: List[Dict[str, Any]] = []
    memory_hit: bool = False
    escalation_fired: bool = False
    execution_time_ms: float
