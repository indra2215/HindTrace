"""
Memory Banks API Routes
"""
from fastapi import APIRouter, HTTPException
from api.models.payloads import MemoryRecallRequest, MemoryRetainRequest
from memory.hindsight_client import recall, retain, get_all_memories, get_memory_stats

router = APIRouter(prefix="/memory", tags=["Memory"])

@router.get("/banks")
def list_memory_banks():
    return get_all_memories()

@router.get("/stats")
def memory_statistics():
    return get_memory_stats()

@router.post("/recall")
def memory_recall(req: MemoryRecallRequest):
    return recall(req.query, bank=req.bank, limit=req.limit)

@router.post("/retain")
def memory_retain(req: MemoryRetainRequest):
    return retain(
        bank=req.bank,
        incident_id=req.incident_id,
        root_cause=req.root_cause,
        resolution=req.resolution,
        context=req.context or ""
    )
