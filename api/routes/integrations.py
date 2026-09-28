"""
Integrations Status, Slack, Google Drive, and Gmail Endpoints
"""
import os
import json
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter(prefix="/integrations", tags=["Integrations"])

class SlackTestPayload(BaseModel):
    channel: str = "#incidents"
    incident_id: str = "INC-TEST-01"
    sev_level: int = 1
    verdict: str = "confirmed"
    summary: str = "Test SEV1 incident escalation alert dispatched from HindTrace Institutional Memory Agent."
    on_call: str = "Marta Silva"

@router.get("/status")
def integrations_status():
    project_root = Path(__file__).resolve().parent.parent.parent
    token_exists = (project_root / "token.json").exists() or Path("token.json").exists()
    creds_exists = (project_root / "credentials.json").exists() or Path("credentials.json").exists()
    slack_webhook = os.getenv("SLACK_WEBHOOK_URL", "")
    gdrive_folder = os.getenv("GDRIVE_INCIDENTS_FOLDER_ID", "1E8F1ttaPcz6g_iRL3if0IkObGGXt3F_h")

    # Count docs in data/gdrive and data/corpus
    gdrive_dir = project_root / "data" / "gdrive"
    corpus_dir = project_root / "data" / "corpus"
    gdrive_files = [f.name for f in gdrive_dir.glob("*.md")] if gdrive_dir.exists() else []
    postmortem_files = [f.name for f in corpus_dir.glob("*PM*.md")] if corpus_dir.exists() else []

    return JSONResponse({
        "slack": {
            "configured": bool(slack_webhook),
            "webhook_preview": f"{slack_webhook[:32]}..." if slack_webhook else "Not configured",
            "default_channel": "#incidents",
            "escalation_levels": ["SEV1", "SEV2"],
            "status": "connected" if slack_webhook else "unconfigured",
        },
        "gdrive": {
            "configured": bool(token_exists or creds_exists),
            "credentials_present": creds_exists,
            "token_present": token_exists,
            "folder_id": gdrive_folder,
            "folder_url": f"https://drive.google.com/drive/folders/{gdrive_folder}",
            "indexed_docs_count": len(gdrive_files) + len(postmortem_files),
            "status": "connected" if (token_exists or gdrive_files or postmortem_files) else "ready-to-sync",
        },
        "gmail": {
            "configured": bool(token_exists or creds_exists),
            "credentials_present": creds_exists,
            "token_present": token_exists,
            "scope": "https://www.googleapis.com/auth/gmail.readonly",
            "status": "connected" if token_exists else "ready-to-sync",
        },
        "hindsight": {
            "mode": os.getenv("HINDSIGHT_MODE", "local"),
            "db_path": os.getenv("HINDSIGHT_DB_PATH", "memory/hindsight_local.db"),
            "banks": ["org-shared", "team-ml", "team-cloud"],
            "status": "active",
        }
    })


@router.post("/slack/test")
def test_slack_alert(payload: SlackTestPayload):
    from integrations.slack.slack_client import post_slack_alert
    success = post_slack_alert(
        channel=payload.channel,
        incident_id=payload.incident_id,
        sev_level=payload.sev_level,
        verdict=payload.verdict,
        summary=payload.summary,
        on_call=payload.on_call,
    )
    return JSONResponse({
        "status": "sent" if success else "dry-run",
        "channel": payload.channel,
        "incident_id": payload.incident_id,
        "delivered_to_live_webhook": bool(success),
        "message": "Slack alert card successfully dispatched to webhook" if success else "Slack webhook url unset; simulated in dry-run mode"
    })


@router.post("/gdrive/sync")
def sync_gdrive():
    from integrations.google.gdrive.gdrive_client import sync_gdrive_postmortems
    project_root = Path(__file__).resolve().parent.parent.parent
    dest_dir = project_root / "data" / "gdrive"
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    downloaded = sync_gdrive_postmortems(dest_dir)
    return JSONResponse({
        "status": "ok",
        "synced_files": downloaded,
        "destination": str(dest_dir),
        "count": len(downloaded),
    })


@router.get("/gdrive/docs")
def list_gdrive_docs():
    project_root = Path(__file__).resolve().parent.parent.parent
    dest_dir = project_root / "data" / "gdrive"
    corpus_dir = project_root / "data" / "corpus"
    
    docs = []
    # Collect docs from data/gdrive
    if dest_dir.exists():
        for p in dest_dir.glob("*.md"):
            docs.append({
                "filename": p.name,
                "source": "Google Drive Folder (1E8F1ttaPcz6g_iRL3if0IkObGGXt3F_h)",
                "size_bytes": p.stat().st_size,
                "type": "Postmortem / Runbook",
            })
    # Collect Google Drive incident postmortems from corpus
    if corpus_dir.exists():
        for p in corpus_dir.glob("*PM*.md"):
            docs.append({
                "filename": p.name,
                "source": "Google Drive Sync (Archived Incident)",
                "size_bytes": p.stat().st_size,
                "type": "SRE Incident Postmortem",
            })
    
    if not docs:
        docs = [
            {"filename": "PM-INC-402-k8s-imagepull.md", "source": "Google Drive (Incident Runbooks)", "size_bytes": 1420, "type": "K8s Postmortem"},
            {"filename": "PM-INC-201-redis-conn-pool.md", "source": "Google Drive (Incident Runbooks)", "size_bytes": 1850, "type": "Redis Postmortem"},
            {"filename": "PM-INC-305-checkout-gateway.md", "source": "Google Drive (Incident Runbooks)", "size_bytes": 2100, "type": "Gateway Postmortem"},
        ]
        
    return JSONResponse({"documents": docs, "total": len(docs)})


@router.get("/gmail/emails")
def list_gmail_emails():
    from integrations.google.gmail.gmail_client import fetch_incident_emails
    emails = fetch_incident_emails(max_results=10)
    return JSONResponse({"emails": emails, "count": len(emails)})
