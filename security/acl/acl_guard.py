"""
Security Subsystem: ACL Guardrail
=================================
Enforces Role-Based Access Control (RBAC) and squad boundaries.
Prevents data leaks for restricted HR/finance documents (Trap T6).
"""

from typing import Optional

def check_acl(
    doc_tier: str,
    doc_acl_teams: list[str],
    doc_acl_users: list[str],
    user_team: str,
    user_name: str,
) -> bool:
    """
    Returns True if user_name / user_team is authorized to read the document.
    
    Tiers:
    - public-internal: accessible by all 4 squads (default)
    - team: restricted to squads in doc_acl_teams
    - restricted: restricted to explicit users in doc_acl_users
    """
    if doc_tier == "public-internal" or not doc_tier:
        return True

    if doc_tier == "team":
        if not doc_acl_teams:
            return True
        return user_team in doc_acl_teams

    if doc_tier == "restricted":
        return user_name in doc_acl_users

    # Deny by default
    return False


def filter_allowed_chunks(chunks: list[dict], user_team: str, user_name: str) -> list[dict]:
    """Filter candidate chunks against user identity and squad."""
    allowed = []
    for chunk in chunks:
        tier = chunk.get("tier", "public-internal")
        teams = chunk.get("acl_teams", [])
        users = chunk.get("acl_users", [])
        if check_acl(tier, teams, users, user_team, user_name):
            allowed.append(chunk)
    return allowed
