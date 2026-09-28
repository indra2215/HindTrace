"""
Investigation API Routes
"""
from fastapi import APIRouter, HTTPException
from api.models.payloads import InvestigateRequest
from agents.pipeline import investigate

router = APIRouter(prefix="/investigate", tags=["Investigation"])

@router.post("")
def run_investigation(req: InvestigateRequest):
    try:
        return investigate(
            query=req.query,
            user_name=req.user_name,
            sev_level=req.sev_level,
            force_search=req.force_search,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
