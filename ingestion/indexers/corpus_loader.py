"""
Corpus Ingestion Pipeline
=========================
Parses all markdown docs in corpus/, extracts YAML front-matter,
chunks runbooks at step level, embeds, and stores in a vector index.
Also builds an in-memory BM25 index for hybrid retrieval.
Embeddings: Google Gemini text-embedding-004 (3-key rotation, OpenAI-compatible endpoint).
"""

import os
import re
import json
import yaml
import hashlib
import numpy as np
from pathlib import Path
from typing import Optional
import threading
import itertools
import urllib.request
import urllib.error
from openai import OpenAI as _OpenAI

# ─── Config ────────────────────────────────────────────────────────────────
CORPUS_DIR = Path(os.getenv("CORPUS_PATH", "data/corpus"))

# ─── Chunk store (in-memory) ────────────────────────────────────────────────
_chunks: list[dict] = []
_chunk_embeddings: list = []  # parallel list of np.array
_loaded = False
_lock = threading.Lock()

# ─── Gemini Embedding via native REST (embedContent) ─────────────────────────
# Model: text-embedding-004 (native REST, no extra packages)
_GEMINI_EMBED_MODEL = "models/text-embedding-004"
_GEMINI_KEYS = [
    k for k in [
        os.getenv("GEMINI_API_KEY", ""),
        os.getenv("GEMINI_API_KEY_2", ""),
        os.getenv("GEMINI_API_KEY_3", ""),
    ] if k
]
_GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"
_gemini_cycle = itertools.cycle(_GEMINI_KEYS) if _GEMINI_KEYS else None


def _embed_one(text: str) -> Optional[np.ndarray]:
    """Embed a single text via Gemini native REST embedContent API.
    Rotates Gemini API keys. Returns normalised np.ndarray or None."""
    if not _GEMINI_KEYS or _gemini_cycle is None:
        return None
    for _ in range(len(_GEMINI_KEYS)):
        api_key = next(_gemini_cycle)
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
            return vec
        except Exception:
            continue
    return None


# ─── YAML front-matter parser ───────────────────────────────────────────────

def _parse_doc(path: Path) -> Optional[dict]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", text, re.DOTALL)
    if not fm_match:
        return None
    try:
        meta = yaml.safe_load(fm_match.group(1)) or {}
    except Exception:
        meta = {}
    body = fm_match.group(2).strip()
    meta["_body"] = body
    meta["_path"] = str(path)
    meta["_hash"] = hashlib.md5(text.encode()).hexdigest()
    return meta


# ─── Chunker ────────────────────────────────────────────────────────────────

def _chunk_doc(meta: dict) -> list[dict]:
    doc_id = meta.get("doc_id", "UNKNOWN")
    doc_type = meta.get("doc_type", "")
    acl_teams = meta.get("acl_teams", [])
    acl_users = meta.get("acl_users", [])
    tier = meta.get("tier", "public-internal")
    body = meta.get("_body", "")

    base = {
        "doc_id": doc_id,
        "doc_type": doc_type,
        "acl_teams": acl_teams,
        "acl_users": acl_users,
        "tier": tier,
        "source_node": meta.get("source_node", ""),
        "title": meta.get("title", ""),
        "date": meta.get("date", ""),
        "author": meta.get("author", ""),
        "status": meta.get("status", "current"),
    }

    if doc_type == "runbook":
        return _chunk_runbook(body, base)

    # All other types: one chunk per doc
    return [{**base, "chunk_id": f"{doc_id}::body", "text": body}]


def _chunk_runbook(body: str, base: dict) -> list[dict]:
    """Split runbook at step headings. Step 8 sub-contexts split further."""
    chunks = []
    # Split on lines starting with "Step" or "## Step" or numbered steps
    step_pattern = re.compile(r"(?m)^(?:#+\s*)?[Ss]tep[\s\-]*(\d+)", re.MULTILINE)
    positions = [(m.start(), m.group(1)) for m in step_pattern.finditer(body)]

    if not positions:
        # fallback: one chunk
        return [{**base, "chunk_id": f"{base['doc_id']}::body", "text": body}]

    for i, (start, step_num) in enumerate(positions):
        end = positions[i + 1][0] if i + 1 < len(positions) else len(body)
        step_text = body[start:end].strip()

        if step_num == "8" or step_num == 8:
            # Try to split into context-A and context-B
            ctx_split = re.split(r"(?i)(context[- ][AB]|torch[-\s]2\.[12])", step_text)
            if len(ctx_split) > 2:
                chunks.append({**base, "chunk_id": f"{base['doc_id']}::step-8::context-A",
                                "text": (ctx_split[0] + ctx_split[1] + ctx_split[2]).strip()})
                if len(ctx_split) > 4:
                    chunks.append({**base, "chunk_id": f"{base['doc_id']}::step-8::context-B",
                                    "text": (ctx_split[3] + ctx_split[4] + "".join(ctx_split[5:])).strip()})
                continue

        chunks.append({**base, "chunk_id": f"{base['doc_id']}::step-{step_num}",
                        "text": step_text})

    return chunks


# ─── Injection sanitiser ─────────────────────────────────────────────────────

_INJECTION_PATTERNS = [
    re.compile(r"ignore\s+(previous\s+)?instructions?", re.IGNORECASE),
    re.compile(r"reveal\s+.*(secret|token|password|key|restricted)", re.IGNORECASE),
    re.compile(r"you\s+are\s+now", re.IGNORECASE),
    re.compile(r"act\s+as", re.IGNORECASE),
    re.compile(r"disregard\s+", re.IGNORECASE),
    re.compile(r"forget\s+(your|previous)", re.IGNORECASE),
]

def sanitise_query(query: str) -> tuple[str, bool]:
    """Strip prompt-injection attempts. Returns (cleaned_query, was_injected)."""
    injected = False
    for pattern in _INJECTION_PATTERNS:
        if pattern.search(query):
            injected = True
            query = pattern.sub("[REDACTED]", query)
    return query.strip(), injected


# ─── BM25 helper ─────────────────────────────────────────────────────────────

def _tokenise(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


def _bm25_score(query_tokens: list[str], doc_tokens: list[str], avgdl: float,
                k1: float = 1.5, b: float = 0.75) -> float:
    doc_len = len(doc_tokens)
    freq = {}
    for t in doc_tokens:
        freq[t] = freq.get(t, 0) + 1
    score = 0.0
    N = len(_chunks) + 1
    for token in query_tokens:
        tf = freq.get(token, 0)
        df = sum(1 for c in _chunks if token in c.get("_tokens", []))
        idf = np.log((N - df + 0.5) / (df + 0.5) + 1)
        numerator = tf * (k1 + 1)
        denominator = tf + k1 * (1 - b + b * doc_len / (avgdl + 1e-6))
        score += idf * numerator / (denominator + 1e-6)
    return score


# ─── Load / index ────────────────────────────────────────────────────────────

def load_corpus(corpus_dir: Optional[Path] = None) -> int:
    global _chunks, _chunk_embeddings, _loaded

    if corpus_dir is None:
        corpus_dir = CORPUS_DIR

    corpus_dir = Path(corpus_dir)
    if not corpus_dir.exists():
        # Try relative from this file
        corpus_dir = Path(__file__).parent / corpus_dir

    with _lock:
        _chunks = []
        _chunk_embeddings = []

        for md_file in sorted(corpus_dir.glob("*.md")):
            meta = _parse_doc(md_file)
            if meta is None:
                continue
            for chunk in _chunk_doc(meta):
                chunk["_tokens"] = _tokenise(chunk["text"])
                _chunks.append(chunk)

        # Batch embed via Gemini native REST API (one call per text)
        if _GEMINI_KEYS and _chunks:
            print(f">> Embedding {len(_chunks)} chunks via Gemini {_GEMINI_EMBED_MODEL}...")
            all_vecs = []
            for i, chunk in enumerate(_chunks):
                vec = _embed_one(chunk["text"])
                all_vecs.append(vec)
                if i % 20 == 0 and i > 0:
                    print(f"   Embedded {i}/{len(_chunks)} chunks...")
            ok = sum(1 for v in all_vecs if v is not None)
            print(f">> Embedding complete: {ok}/{len(_chunks)} chunks embedded successfully")
            _chunk_embeddings = all_vecs
        else:
            _chunk_embeddings = [None] * len(_chunks)

        _loaded = True

    return len(_chunks)


def is_loaded() -> bool:
    return _loaded


# ─── ACL filter (delegates to security subsystem) ───────────────────────────
from security.acl.acl_guard import check_acl, filter_allowed_chunks

def _acl_allowed(chunk: dict, user_team: str, user_name: str) -> bool:
    tier = chunk.get("tier", "public-internal")
    acl_teams = chunk.get("acl_teams", [])
    acl_users = chunk.get("acl_users", [])
    return check_acl(tier, acl_teams, acl_users, user_team, user_name)


# ─── Hybrid retrieval ────────────────────────────────────────────────────────

def retrieve(
    query: str,
    user_team: str,
    user_name: str,
    top_k: int = 8,
    vector_weight: float = 0.7,
) -> list[dict]:
    """
    Hybrid retrieval: vector cosine + BM25.
    Applies ACL filter twice (before scoring and before returning).
    Returns top_k chunks sorted by combined score.
    """
    if not _loaded:
        load_corpus()

    query_tokens = _tokenise(query)
    avg_dl = sum(len(c.get("_tokens", [])) for c in _chunks) / (len(_chunks) + 1e-6)

    results = []
    query_vec = None
    if _GEMINI_KEYS:
        query_vec = _embed_one(query)

    for i, chunk in enumerate(_chunks):
        # ACL pre-filter
        if not _acl_allowed(chunk, user_team, user_name):
            continue

        # Vector score
        v_score = 0.0
        if query_vec is not None and _chunk_embeddings[i] is not None:
            v_score = float(np.dot(query_vec, _chunk_embeddings[i]))

        # BM25 score (normalised roughly)
        bm_raw = _bm25_score(query_tokens, chunk.get("_tokens", []), avg_dl)
        bm_norm = min(bm_raw / 10.0, 1.0)  # rough normalisation

        combined = vector_weight * v_score + (1 - vector_weight) * bm_norm

        results.append({**chunk, "_score": combined})

    results.sort(key=lambda x: x["_score"], reverse=True)

    # ACL re-check (post-retrieval citation verifier pass)
    verified = [r for r in results if _acl_allowed(r, user_team, user_name)]
    return verified[:top_k]


def verify_citation(doc_id: str, quote: str, user_team: str, user_name: str) -> dict:
    """
    Citation verifier:
    (a) doc exists in corpus
    (b) quote is literal substring of doc text
    (c) ACL re-check passes
    """
    matching = [c for c in _chunks if c["doc_id"] == doc_id]
    if not matching:
        return {"valid": False, "reason": f"doc_id {doc_id} not found in corpus"}

    # ACL re-check
    for chunk in matching:
        if not _acl_allowed(chunk, user_team, user_name):
            return {"valid": False, "reason": f"access denied to {doc_id} for user {user_name}"}

    # Quote check
    full_text = " ".join(c["text"] for c in matching)
    if quote and quote not in full_text:
        return {"valid": False, "reason": f"quoted text not found as literal substring in {doc_id}"}

    return {"valid": True, "doc_id": doc_id}
