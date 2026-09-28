"""
Integrations Package for HindTrace
"""

from .slack.slack_client import post_slack_alert
from .google.gmail.gmail_client import fetch_incident_emails
from .google.gdrive.gdrive_client import sync_gdrive_postmortems

__all__ = [
    "post_slack_alert",
    "fetch_incident_emails",
    "sync_gdrive_postmortems",
]

