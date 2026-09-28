"""
Database Module for HindTrace
======================================
Stores persistent audit logs and investigation records as specified in
the 3-stage architecture (Stage 3 Escalator: Update investigations DB table).
"""

import sqlite3
import json
import time
from pathlib import Path
from typing import Optional, Any

DB_PATH = Path(__file__).parent / "investigations.db"

def get_db():
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS investigations (
            investigation_id    TEXT PRIMARY KEY,
            query               TEXT NOT NULL,
            user_name           TEXT NOT NULL,
            user_team           TEXT NOT NULL,
            sev_level           INTEGER NOT NULL,
            verdict             TEXT NOT NULL,
            status              TEXT NOT NULL, -- confirmed, rejected, unverified
            root_cause          TEXT,
            resolution          TEXT,
            citations           TEXT,          -- JSON list
            memory_used         INTEGER DEFAULT 0,
            memory_key          TEXT,
            memory_confidence   REAL,
            was_injected        INTEGER DEFAULT 0,
            escalation_fired    INTEGER DEFAULT 0,
            escalation_channel  TEXT,
            timestamp           REAL NOT NULL
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_inv_user ON investigations(user_name)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_inv_team ON investigations(user_team)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_inv_status ON investigations(status)")
    conn.commit()
    return conn

def record_investigation(
    investigation_id: str,
    query: str,
    user_name: str,
    user_team: str,
    sev_level: int,
    verdict: str,
    root_cause: Optional[str] = None,
    resolution: Optional[str] = None,
    citations: Optional[list] = None,
    memory_used: bool = False,
    memory_key: Optional[str] = None,
    memory_confidence: Optional[float] = None,
    was_injected: bool = False,
    escalation_fired: bool = False,
    escalation_channel: Optional[str] = None,
) -> None:
    """Record a completed investigation into the investigations table."""
    conn = get_db()
    status = "confirmed" if verdict == "confirmed" else ("unverified" if verdict == "insufficient-evidence" else "rejected")
    conn.execute("""
        INSERT OR REPLACE INTO investigations (
            investigation_id, query, user_name, user_team, sev_level, verdict,
            status, root_cause, resolution, citations, memory_used, memory_key,
            memory_confidence, was_injected, escalation_fired, escalation_channel,
            timestamp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        investigation_id,
        query,
        user_name,
        user_team,
        sev_level,
        verdict,
        status,
        root_cause,
        resolution,
        json.dumps(citations or []),
        1 if memory_used else 0,
        memory_key,
        memory_confidence,
        1 if was_injected else 0,
        1 if escalation_fired else 0,
        escalation_channel,
        time.time()
    ))
    conn.commit()

def list_investigations(limit: int = 50) -> list[dict]:
    """Retrieve recent investigation records."""
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM investigations ORDER BY timestamp DESC LIMIT ?",
        (limit,)
    ).fetchall()
    results = []
    for r in rows:
        item = dict(r)
        item["citations"] = json.loads(item["citations"] or "[]")
        item["memory_used"] = bool(item["memory_used"])
        item["was_injected"] = bool(item["was_injected"])
        item["escalation_fired"] = bool(item["escalation_fired"])
        results.append(item)
    return results

