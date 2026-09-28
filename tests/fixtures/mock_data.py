"""
Test Fixtures and Mock Data for HindTrace Test Suite
"""

MOCK_INCIDENTS = [
    {
        "id": "INC-402",
        "title": "ImagePullBackOff on production kubernetes cluster",
        "team": "cloud-eng",
        "sev": 1,
        "root_cause": "ECR rate limiting caused kubelet image pull failure",
        "resolution": "Enabled AWS VPC endpoint for ECR and bumped node pool image cache TTL"
    },
    {
        "id": "INC-109",
        "title": "Postgres connection pool exhaustion in checkout service",
        "team": "backend-core",
        "sev": 2,
        "root_cause": "Abandoned connection leak in order reservation transaction",
        "resolution": "Applied pool timeout patch and recycled idle connections"
    }
]

MOCK_SLACK_WEBHOOK_PAYLOAD = {
    "channel": "#incidents",
    "text": "CRITICAL INC-402 Alert",
    "blocks": [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": "SEV1 INCIDENT ALERT"}
        }
    ]
}

