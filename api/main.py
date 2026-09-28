"""
FastAPI Backend
===============
Serves the investigation API and static UI.
"""

import os
import sys
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
load_dotenv(project_root / ".env")

app = FastAPI(
    title="HindTrace",
    description="Autonomous Enterprise Incident Investigation & Memory Platform",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Startup: load corpus (BM25 instant, embeddings in background) ────────────
@app.on_event("startup")
async def startup_event():
    import threading
    from ingestion.indexers.corpus_loader import load_corpus
    raw_path = os.getenv("CORPUS_PATH", "../output_extracted/corpus")
    p = Path(raw_path)
    if not p.is_absolute():
        if (project_root / p).exists():
            corpus_path = project_root / p
        elif (Path.cwd() / p).exists():
            corpus_path = Path.cwd() / p
        elif Path("d:/hack/output_extracted/corpus").exists():
            corpus_path = Path("d:/hack/output_extracted/corpus")
        else:
            corpus_path = project_root / p
    else:
        corpus_path = p

    def _load():
        n = load_corpus(corpus_path)
        print(f">> Corpus loaded: {n} chunks indexed from {corpus_path}")

    # Run in background thread — BM25 indexes fast; Gemini embeddings stream in
    t = threading.Thread(target=_load, daemon=True)
    t.start()
    print(f">> Corpus loading started in background from {corpus_path}")



# ─── Models ─────────────────────────────────────────────────────────────────
class InvestigateRequest(BaseModel):
    query: str
    user_name: str
    sev_level: int = 3


class FeedbackRequest(BaseModel):
    investigation_id: str
    verdict_correct: bool
    notes: str = ""


# ─── Routes ─────────────────────────────────────────────────────────────────

ui_dir = project_root / "ui"
if not ui_dir.exists():
    ui_dir = Path("d:/hack/HindTrace/ui")

if (ui_dir / "static").exists():
    app.mount("/static", StaticFiles(directory=str(ui_dir / "static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    index_file = ui_dir / "index.html"
    if index_file.exists():
        return HTMLResponse(content=index_file.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>HindTrace API</h1><p>UI not found.</p>")

@app.get("/style.css")
async def get_css():
    for p in [ui_dir / "style.css", ui_dir / "static" / "css" / "style.css"]:
        if p.exists():
            return FileResponse(str(p), media_type="text/css")
    raise HTTPException(status_code=404, detail="CSS not found")

@app.get("/app.js")
async def get_js():
    for p in [ui_dir / "app.js", ui_dir / "static" / "js" / "app.js"]:
        if p.exists():
            return FileResponse(str(p), media_type="application/javascript")
    raise HTTPException(status_code=404, detail="JS not found")


@app.post("/api/investigate")
async def investigate_endpoint(req: InvestigateRequest):
    from agents.pipeline import investigate
    result = investigate(
        query=req.query,
        user_name=req.user_name,
        sev_level=req.sev_level,
    )
    return JSONResponse(content=result)


@app.get("/api/memory/{bank}")
async def get_memory(bank: str):
    from memory.hindsight_client import list_memories
    memories = list_memories(bank)
    return JSONResponse(content=memories)


@app.get("/api/memory")
async def get_all_memory():
    from memory.hindsight_client import list_memories
    result = {}
    for bank in ["org-shared", "team-ml", "team-cloud"]:
        result[bank] = list_memories(bank)
    return JSONResponse(content=result)


@app.post("/api/memory/seed")
async def seed_memory_endpoint():
    from memory.hindsight_client import seed_historical_memories
    count = seed_historical_memories()
    return JSONResponse(content={"status": "ok", "seeded": count})


@app.post("/api/feedback")
async def submit_feedback(req: FeedbackRequest):
    from memory.hindsight_client import retain
    retain(
        bank="org-shared",
        key=f"feedback:{req.investigation_id}",
        content={
            "investigation_id": req.investigation_id,
            "verdict_correct": req.verdict_correct,
            "notes": req.notes,
        },
        acl_ceiling="public-internal",
    )
@app.get("/api/investigations")
async def get_investigations(limit: int = 50):
    from database.db import list_investigations
    return JSONResponse(content=list_investigations(limit=limit))


@app.get("/api/personas")
async def get_personas():
    from agents.pipeline import PERSONAS
    return JSONResponse(content=PERSONAS)


def _get_gt_path() -> Path:
    raw_gt = os.getenv("GROUND_TRUTH_PATH", "../output_extracted/ground_truth")
    p = Path(raw_gt)
    if p.is_absolute() and p.exists():
        return p
    for candidate in [project_root / p, Path.cwd() / p, Path("d:/hack/output_extracted/ground_truth")]:
        if candidate.exists():
            return candidate
    return project_root / p


@app.get("/api/gold-questions")
async def get_gold_questions():
    gt_path = _get_gt_path()
    csv_path = gt_path / "gold_questions.csv"
    if not csv_path.exists():
        raise HTTPException(404, "Gold questions not found")
    import csv
    rows = []
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(dict(row))
    return JSONResponse(content=rows)


@app.get("/api/eval/run")
async def run_eval():
    """Run a quick eval against gold questions."""
    from agents.pipeline import investigate
    import csv
    gt_path = _get_gt_path()
    csv_path = gt_path / "gold_questions.csv"
    if not csv_path.exists():
        return JSONResponse({"error": "gold_questions.csv not found"})

    results = []
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            result = investigate(
                query=row["question"],
                user_name=row["user"],
                sev_level=3,
            )
            correct = result["verdict"].lower() == row["expected_verdict"].lower()
            results.append({
                "question_id": row["question_id"],
                "expected": row["expected_verdict"],
                "got": result["verdict"],
                "correct": correct,
                "memory_used": result.get("memory_used", False),
            })

    total = len(results)
    correct = sum(1 for r in results if r["correct"])
    return JSONResponse({
        "total": total,
        "correct": correct,
        "accuracy": correct / total if total else 0,
        "results": results,
    })


@app.get("/api/health")
async def health():
    from ingestion.indexers.corpus_loader import is_loaded
    return {"status": "ok", "corpus_loaded": is_loaded()}


# ─── Static files ────────────────────────────────────────────────────────────
if ui_dir.exists():
    app.mount("/static", StaticFiles(directory=str(ui_dir)), name="static")

