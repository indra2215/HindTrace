"""
Integrations Status and Webhook Routes
"""
import os
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/integrations", tags=["Integrations"])

class SlackTestPayload(BaseModel):
    channel: str = "#incidents"
    message: str = "Test alert from HindTrace"

@router.get("/status")
def integrations_status():
    return {
        "slack": {
            "configured": bool(os.getenv("SLACK_WEBHOOK_URL")),
            "webhook_set": bool(os.getenv("SLACK_WEBHOOK_URL")),
        },
        "google": {
            "credentials_present": os.path.exists("credentials.json"),
            "token_present": os.path.exists("token.json"),
            "gdrive_folder_id": os.getenv("GDRIVE_INCIDENTS_FOLDER_ID", "1E8F1ttaPcz6g_iRL3if0IkObGGXt3F_h"),
        },
        "llm": {
            "provider": "Groq",
            "model": "llama-3.3-70b-versatile",
            "configured": bool(os.getenv("GROQ_API_KEY")),
        }
    }

