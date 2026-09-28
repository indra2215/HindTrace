"""
Memory Bank Definitions and Scopes for HindTrace
"""
from typing import Dict, List

STANDARD_BANKS: Dict[str, Dict[str, str]] = {
    "org-shared": {
        "description": "Enterprise-wide common outages, platform incidents, and global runbooks",
        "access": "all_teams"
    },
    "team-cloud": {
        "description": "Kubernetes, AWS/GCP infrastructure, networking, and deployment incidents",
        "access": "cloud-eng"
    },
    "team-ml": {
        "description": "Model serving, CUDA out of memory, Triton inference server incidents",
        "access": "ml-platform"
    },
    "team-backend": {
        "description": "Database locks, connection pool exhaustion, Redis caching, microservices",
        "access": "backend-core"
    }
}

def get_allowed_banks_for_team(team: str) -> List[str]:
    """Returns memory banks accessible to an engineer based on their team."""
    banks = ["org-shared"]
    for bank_name, bank_meta in STANDARD_BANKS.items():
        if bank_meta["access"] == team and bank_name not in banks:
            banks.append(bank_name)
    return banks

