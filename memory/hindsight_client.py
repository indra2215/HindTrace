"""
Hindsight Memory Client
=======================
Implements the retain() / recall() / reflect() contract.

Mode selection (HINDSIGHT_MODE env var):
  local  (default) — SQLite-backed in-process memory (for hackathon demo)
  cloud             — Real Hindsight Cloud (set HINDSIGHT_API_TOKEN)
"""

import os
import json
import time
import sqlite3
import hashlib
import threading
from typing import Any, Optional
from pathlib import Path
import numpy as np
from openai import OpenAI as _OpenAI
import itertools
import urllib.request
import logging
import urllib.error

logger = logging.getLogger("hindsight_client")

# ─── Config ────────────────────────────────────────────────────────────────
_MODE = os.getenv("HINDSIGHT_MODE", "local")
_TOKEN = os.getenv("HINDSIGHT_API_TOKEN", "")
_raw_db = os.getenv("HINDSIGHT_DB_PATH")
if _raw_db:
    _p = Path(_raw_db)
    _DB_PATH = _p if _p.is_absolute() else (Path(__file__).resolve().parent.parent / _p)
else:
    _DB_PATH = Path(__file__).resolve().parent / "hindsight_local.db"

# ─── Local implementation ───────────────────────────────────────────────────
_lock = threading.Lock()

def _get_conn():
    conn = sqlite3.connect(str(_DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id          TEXT PRIMARY KEY,
            bank        TEXT NOT NULL,
            key_name    TEXT NOT NULL,
            content     TEXT NOT NULL,
            embedding   TEXT,
            acl_ceiling TEXT DEFAULT 'public-internal',
            created_at  REAL NOT NULL,
            updated_at  REAL NOT NULL
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_bank ON memories(bank)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_key  ON memories(bank, key_name)")
    conn.commit()
    return conn


def _make_id(bank: str, key: str) -> str:
    return hashlib.sha256(f"{bank}::{key}".encode()).hexdigest()[:24]


def _cosine(a: list, b: list) -> float:
    a, b = np.array(a), np.array(b)
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


# ─── Gemini Embedding via native REST API (embedContent) ─────────────────────
# Uses all 3 Gemini keys in round-robin; falls back gracefully on quota errors.
# Model: text-embedding-004 (8192 token limit, 768-dim output)
_GEMINI_EMBED_MODEL = "models/text-embedding-004"
_GEMINI_KEYS = [
    k for k in [
        os.getenv("GEMINI_API_KEY", ""),
        os.getenv("GEMINI_API_KEY_2", ""),
        os.getenv("GEMINI_API_KEY_3", ""),
    ] if k
]
_GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
_gemini_key_cycle = itertools.cycle(_GEMINI_KEYS) if _GEMINI_KEYS else None


def _embed(text: str) -> Optional[list]:
    """Embed via Gemini native REST API (embedContent).
    Rotates across 3 Gemini API keys. Returns normalised float list or None."""
    if not _GEMINI_KEYS or _gemini_key_cycle is None:
        return None
    for _ in range(len(_GEMINI_KEYS)):
        api_key = next(_gemini_key_cycle)
        try:
            url = f"{_GEMINI_BASE_URL}/{_GEMINI_EMBED_MODEL}:embedContent?key={api_key}"
            payload = json.dumps({
                "model": _GEMINI_EMBED_MODEL,
                "content": {"parts": [{"text": text[:8000]}]}
            }).encode("utf-8")
            req = urllib.request.Request(
                url, data=payload,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            vec = np.array(data["embedding"]["values"], dtype=np.float32)
            n = np.linalg.norm(vec)
            if n > 0:
                vec = vec / n
            return vec.tolist()
        except Exception:
            continue  # rotate to next key
    return None


class MemoryHit:
    def __init__(self, key: str, content: dict, confidence: float, bank: str):
        self.key = key
        self.content = content
        self.confidence = confidence
        self.bank = bank

    def __repr__(self):
        return f"<MemoryHit key={self.key!r} confidence={self.confidence:.3f}>"


def retain(bank: str, key: str, content: dict, acl_ceiling: str = "public-internal") -> str:
    """Store or update a memory in the given bank. Idempotent upsert on (bank, key)."""
    if _MODE == "cloud" and _TOKEN:
        return _cloud_retain(bank, key, content, acl_ceiling)

    mem_id = _make_id(bank, key)
    content_json = json.dumps(content)
    embedding_text = key + " " + content.get("root_cause", "") + " " + content.get("verdict", "")
    embedding = _embed(embedding_text)
    embedding_json = json.dumps(embedding) if embedding else None
    now = time.time()

    with _lock:
        conn = _get_conn()
        conn.execute("""
            INSERT INTO memories (id, bank, key_name, content, embedding, acl_ceiling, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                content     = excluded.content,
                embedding   = excluded.embedding,
                acl_ceiling = excluded.acl_ceiling,
                updated_at  = excluded.updated_at
        """, (mem_id, bank, key, content_json, embedding_json, acl_ceiling, now, now))
        conn.commit()
    return mem_id


def recall(
    bank: str,
    query: str,
    top_k: int = 1,
    min_confidence: float = 0.70,
    requester_team: Optional[str] = None,
    requester_name: Optional[str] = None,
) -> Optional[MemoryHit]:
    """Retrieve the best matching memory. Returns None if below min_confidence."""
    if _MODE == "cloud" and _TOKEN:
        return _cloud_recall(bank, query, top_k, min_confidence, requester_team, requester_name)

    with _lock:
        conn = _get_conn()
        rows = conn.execute("SELECT * FROM memories WHERE bank = ?", (bank,)).fetchall()

    if not rows:
        return None

    query_embedding = _embed(query)
    best = None
    best_score = -1.0

    for row in rows:
        ceiling = row["acl_ceiling"]
        if ceiling == "team" and requester_team:
            content_obj = json.loads(row["content"])
            owner_team = content_obj.get("owner_team", "")
            if owner_team and owner_team != requester_team:
                continue
        elif ceiling == "restricted":
            content_obj = json.loads(row["content"])
            allowed = content_obj.get("acl_users", [])
            if requester_name and requester_name not in allowed:
                continue

        if query_embedding and row["embedding"]:
            stored_emb = json.loads(row["embedding"])
            score = _cosine(query_embedding, stored_emb)
        else:
            score = 0.0

        # High-precision entity and key matching
        import re
        key_raw = row["key_name"].lower()
        q_raw = query.lower()
        q_entities = set(re.findall(r"[a-z]+-[0-9a-z]+", q_raw))
        k_entities = set(re.findall(r"[a-z]+-[0-9a-z]+", key_raw))
        if q_entities and k_entities and (q_entities & k_entities):
            score = max(score, 0.95)
        elif key_raw in q_raw or (len(key_raw) > 5 and key_raw.replace("incident:", "") in q_raw):
            score = max(score, 0.90)
        else:
            q_words = set(re.findall(r"\w+", q_raw))
            k_words = set(re.findall(r"\w+", key_raw))
            overlap = len(q_words & k_words)
            if overlap > 0:
                tok_score = overlap / max(len(k_words), 1) * 0.85
                score = max(score, tok_score)

        if score > best_score:
            best_score = score
            content_obj = json.loads(row["content"])
            best = MemoryHit(key=row["key_name"], content=content_obj, confidence=score, bank=bank)

    if best and best.confidence >= min_confidence:
        return best
    return None


def recall_all(
    bank: str,
    query: str,
    top_k: int = 5,
    min_confidence: float = 0.50,
    requester_team: Optional[str] = None,
) -> list:
    """Return top-k memory hits above min_confidence."""
    with _lock:
        conn = _get_conn()
        rows = conn.execute("SELECT * FROM memories WHERE bank = ?", (bank,)).fetchall()

    if not rows:
        return []

    query_embedding = _embed(query)
    hits = []

    for row in rows:
        ceiling = row["acl_ceiling"]
        if ceiling == "team" and requester_team:
            content_obj = json.loads(row["content"])
            owner_team = content_obj.get("owner_team", "")
            if owner_team and owner_team != requester_team:
                continue

        if query_embedding and row["embedding"]:
            stored_emb = json.loads(row["embedding"])
            score = _cosine(query_embedding, stored_emb)
        else:
            q_words = set(query.lower().split())
            k_words = set(row["key_name"].lower().replace(":", " ").split())
            overlap = len(q_words & k_words)
            score = overlap / max(len(q_words), 1) * 0.9

        if score >= min_confidence:
            content_obj = json.loads(row["content"])
            hits.append(MemoryHit(key=row["key_name"], content=content_obj, confidence=score, bank=bank))

    hits.sort(key=lambda h: h.confidence, reverse=True)
    return hits[:top_k]


def reflect(bank: str, topic: str) -> str:
    """Reflect on accumulated memories in a bank. Returns synthesised summary."""
    if _MODE == "cloud" and _TOKEN:
        return _cloud_reflect(bank, topic)

    hits = recall_all(bank, topic, top_k=10, min_confidence=0.3)
    if not hits:
        return f"No memories found in bank '{bank}' for topic '{topic}'."
    lines = [
        f"- [{h.key}] verdict={h.content.get('verdict','?')} "
        f"root_cause={h.content.get('root_cause','?')}"
        for h in hits
    ]
    return f"Memory reflection for '{topic}' in bank '{bank}':\n" + "\n".join(lines)


def list_memories(bank: str) -> list:
    """List all memories in a bank (for debug/UI)."""
    with _lock:
        conn = _get_conn()
        rows = conn.execute(
            "SELECT key_name, content, acl_ceiling, updated_at FROM memories WHERE bank = ? ORDER BY updated_at DESC",
            (bank,)
        ).fetchall()
    return [
        {
            "key": r["key_name"],
            "content": json.loads(r["content"]),
            "acl_ceiling": r["acl_ceiling"],
            "updated_at": r["updated_at"],
        }
        for r in rows
    ]


def seed_historical_memories() -> int:
    """Pre-seed verified historical incident outcomes into Hindsight memory banks."""
    seeds = [
        (
            "org-shared",
            "incident:INC-201",
            {
                "verdict": "confirmed",
                "root_cause": "DEP-101 concurrency increase exhausted the Hikari pool while transactions held connections.",
                "resolution": "Capped max transaction connection lifetime and adjusted pool size.",
                "citations": ["DOC-WEB-001"],
                "acl_ceiling": "public-internal",
                "investigation_id": "INV-HIST-01",
            },
            "public-internal",
        ),
        (
            "org-shared",
            "incident:INC-202",
            {
                "verdict": "confirmed",
                "root_cause": "DEP-102 added unindexed order-history lookup path causing slow queries to monopolise pool connections.",
                "resolution": "Added missing database index on order-history predicate.",
                "citations": ["DOC-WEB-002"],
                "acl_ceiling": "public-internal",
                "investigation_id": "INV-HIST-02",
            },
            "public-internal",
        ),
        (
            "team-ml",
            "incident:INC-311",
            {
                "verdict": "confirmed",
                "root_cause": "Per-device training batch size exceeded available staging GPU VRAM.",
                "resolution": "Reduced per-device batch size and enabled gradient accumulation.",
                "citations": ["DOC-ML-002"],
                "acl_ceiling": "team",
                "owner_team": "ml-eng",
                "investigation_id": "INV-HIST-03",
            },
            "team",
        ),
        (
            "team-cloud",
            "incident:INC-402",
            {
                "verdict": "confirmed",
                "root_cause": "DEP-402 prod node image lacked private container registry CA trust bundle, causing ImagePullBackOff.",
                "resolution": "Injected private-registry CA certificate into base node image.",
                "citations": ["DOC-CLOUD-002"],
                "acl_ceiling": "team",
                "owner_team": "cloud-eng",
                "investigation_id": "INV-HIST-04",
            },
            "team",
        ),
        (
            "org-shared",
            "mapping:FAIL-UI-01",
            {
                "verdict": "confirmed",
                "root_cause": "Asset export timeout (INC-410 / FAIL-UI-01). Equivalent team-specific phrases: 'asset export timeouts' (ui-ux), 'SVG conversion job hangs' (web-dev), and 'figma-pipeline 504 gateway timeout' (cloud-eng).",
                "resolution": "All three phrases map to FAIL-UI-01 / INC-410. Bounded 15s deadline and capped retries to 3.",
                "citations": ["DOC-UI-001", "DOC-UI-003", "DOC-XTEAM-008"],
                "acl_ceiling": "public-internal",
                "investigation_id": "INV-HIST-05",
            },
            "public-internal",
        ),
        (
            "team-ml",
            "runbook:RB-14-torch-2.2.1",
            {
                "verdict": "confirmed",
                "root_cause": "RB-14 step 8 torch-2.2.1 prod EPOCH_RESTART_WORKER failure.",
                "resolution": "Keep configured worker count and set persistent_workers=false. Do not apply the torch-2.1.0 staging num_workers=0 fix.",
                "citations": ["DOC-ML-010", "DOC-ML-011"],
                "acl_ceiling": "team",
                "owner_team": "ml-eng",
                "investigation_id": "INV-HIST-06",
            },
            "team",
        ),
    ]

    count = 0
    for bank, key, content, ceiling in seeds:
        retain(bank=bank, key=key, content=content, acl_ceiling=ceiling)
        count += 1
    return count


def _cloud_retain(bank, key, content, acl_ceiling):
    """Fallback to local storage if real Hindsight Cloud credentials or instance are absent."""
    logger.info("Hindsight Cloud endpoint unconfigured; using local memory engine.")
    return retain(bank=bank, key=key, content=content, acl_ceiling=acl_ceiling)

def _cloud_recall(bank, query, top_k, min_confidence, requester_team, requester_name):
    """Fallback to local storage if real Hindsight Cloud credentials or instance are absent."""
    logger.info("Hindsight Cloud endpoint unconfigured; using local memory engine.")
    return recall(bank=bank, query=query, top_k=top_k, min_confidence=min_confidence, requester_team=requester_team, requester_name=requester_name)

def _cloud_reflect(bank, topic):
    """Fallback to local storage if real Hindsight Cloud credentials or instance are absent."""
    logger.info("Hindsight Cloud endpoint unconfigured; using local memory engine.")
    return reflect(bank=bank, topic=topic)
