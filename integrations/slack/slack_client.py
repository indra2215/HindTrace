"""
Live Slack Integration Connector
=================================
Connects HindTrace to real Slack workspaces.
Supports:
1. Incoming Webhook alerts for SEV1/SEV2 incident escalation.
2. Slack Bolt App for answering `/investigate` slash command queries.
"""

import os
import json
import urllib.request
from typing import Optional

SLACK_WEBHOOK_URL  = os.getenv("SLACK_WEBHOOK_URL", "")
SLACK_CLIENT_SECRET = os.getenv("SLACK_CLIENT_SECRET", "669b9efaba109e289b1ed2d550e292da")
SLACK_APP_ID       = "A0C5WVDTF16"  # https://api.slack.com/apps/A0C5WVDTF16

def post_slack_alert(
    channel: str,
    incident_id: str,
    sev_level: int,
    verdict: str,
    summary: str,
    on_call: str,
    webhook_url: Optional[str] = None,
) -> bool:
    """
    Sends an escalation alert card to a live Slack channel.
    Requires SLACK_WEBHOOK_URL configured in .env.
    """
    url = webhook_url or SLACK_WEBHOOK_URL
    if not url:
        # Dry-run mode for testing / hackathon
        print(f"[SLACK DRY-RUN] Alert to {channel}: SEV{sev_level} {incident_id} — {verdict}")
        return False

    payload = {
        "channel": channel,
        "text": f"🚨 *SEV{sev_level} Incident Alert: {incident_id}*",
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": f"🚨 SEV{sev_level} Incident: {incident_id}"}
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Verdict:* `{verdict}`"},
                    {"type": "mrkdwn", "text": f"*On-Call:* <@{on_call}>"}
                ]
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*Summary:*\n{summary[:500]}"}
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Acknowledge Alert"},
                        "style": "primary",
                        "value": f"ack_{incident_id}"
                    }
                ]
            }
        ]
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status == 200
    except Exception as e:
        print(f"[SLACK ERROR] Failed to send webhook: {e}")
        return False

