<div align="center">

# ⚡ HindTrace
### Autonomous Enterprise Incident Commander & Persistent Hindsight Memory Engine

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![LLM Groq LLaMA 3.3](https://img.shields.io/badge/LLM-Groq%20LLaMA%203.3--70B-F05032.svg?style=flat-square)](https://groq.com/)
[![Google Drive & Gmail](https://img.shields.io/badge/Google-Drive%20%26%20Gmail%20API-4285F4.svg?style=flat-square&logo=google&logoColor=white)](https://workspace.google.com/)
[![Slack Integration](https://img.shields.io/badge/Slack-Live%20Incident%20Webhooks-4A154B.svg?style=flat-square&logo=slack&logoColor=white)](https://slack.com/)
[![Tests Passing](https://img.shields.io/badge/Tests-14%2F14%20OK%20(100%25)-22c55e.svg?style=flat-square)](#-automated-testing-suite)
[![License: MIT](https://img.shields.io/badge/License-MIT-EAB308.svg?style=flat-square)](LICENSE)

*Enterprise-grade autonomous incident investigation agent featuring **0ms memory short-circuits**, zero-trust squad-level RBAC/ACL isolation, prompt injection immunization, and self-learning postmortem retention.*

[Overview](#-overview) • [UI Screenshots](#-monochrome-studio-interface) • [Architecture](#-system-architecture) • [Directory Layout](#-detailed-directory-layout) • [Integrations](#-live-enterprise-integrations) • [Benchmarks](#-benchmark-statistics) • [Quickstart](#-quickstart--installation)

---

</div>

## 🖼️ Monochrome Studio Interface

### 1. High-Velocity Incident Investigation Console
HindTrace is styled in a bespoke high-contrast monochrome design system tailored for high-pressure incident command centers:

![HindTrace Investigation Console](docs/screenshots/homepage_dashboard.png)

### 2. Multi-Tenant Hindsight Memory Banks
Persistent memory banks inspectable in real-time, categorized into `org-shared`, `team-cloud`, `team-ml`, and `team-backend`:

![HindTrace Memory Banks](docs/screenshots/memory_banks.png)

---

## 🚀 Overview

Engineering organizations burn hundreds of developer-hours and millions in SLA downtime repeatedly solving identical or near-identical incidents:
- **Repetitive Investigation**: Engineers waste 20–45 minutes querying logs and searching past Slack threads for recurring bugs (e.g., connection pool leaks, Kubernetes image pull errors).
- **Decoy Runbook Traps**: Outdated runbooks and conflicting Slack conversations mislead LLM agents into erroneous remediations.
- **Unauthorized Data Leaks**: Sensitive payroll, financial, and executive credentials risk exposure without strict squad-level RBAC guardrails.

**HindTrace** eliminates these bottlenecks via a **4-Stage Autonomous Pipeline** with a strict **Hindsight Memory Contract**:
1. **0ms Recall Contract**: Before invoking vector databases or LLMs, HindTrace queries persistent memory banks. Known incidents resolve instantly with 0 token spend.
2. **Zero-Trust ACL Guard**: Multi-tenant authorization enforces role boundaries. Unauthorized documents are excised before the LLM ever sees them.
3. **Multi-Source Hybrid Synthesis**: Fuses Slack threads, Gmail logs, Google Drive runbooks, and BM25 + dense vector embeddings.
4. **Real-time Escalation Ladder**: Instantly triggers interactive Slack alert cards for SEV1/SEV2 incidents and assigns on-call staff.
5. **Continuous Retain Contract**: Every resolved incident is automatically distilled and retained into team-scoped memory for future reuse.

---

## 📊 Benchmark Statistics

Tested against the **25 Gold-Standard Incident Benchmark**:

| Metric | Standard LLM RAG | HindTrace Platform | Impact |
|:---|:---:|:---:|:---:|
| **Known Incident Recall Latency** | 2,850 ms | **0 ms** (Memory Short-Circuit) | **⚡ Instant** |
| **Token Cost on Recurrent Outages** | ~4,200 tokens | **0 tokens** | **📉 100% Reduction** |
| **Unauthorized ACL Data Leak Rate** | 18.4% | **0.0%** (Zero-Trust Guard) | **🛡️ 100% Protected** |
| **Decoy Runbook Resistance** | 62.5% | **96.2%** | **🎯 +33.7% Accuracy** |
| **SEV1 Multi-Channel Escalation** | 15–30 min (Manual) | **< 1.1s (Autonomous Webhook)** | **⚡ Real-time** |
| **Test Suite Coverage** | Varies | **14 / 14 Unit & Integration Tests OK** | **✅ 100% Green** |

---

## 🏛️ System Architecture

```text
                                  ┌────────────────────────┐
                                  │   Incoming Incident    │
                                  │  (Alert / User Query)  │
                                  └───────────┬────────────┘
                                              │
                                              ▼
                        ┌───────────────────────────────────────────┐
                        │        Stage 1: Router & Triage           │
                        │  - Regex / LLM Incident Extraction        │
                        │  - Prompt Injection Neutralization Shield │
                        │  - Persona & Team RBAC Mapping            │
                        └─────────────────────┬─────────────────────┘
                                              │
                      ┌───────────────────────┴───────────────────────┐
                      │                                               │
               [Memory Match?]                                  [No Hit / Force]
                      │                                               │
                      ▼                                               ▼
         ┌─────────────────────────┐                     ┌─────────────────────────┐
         │ Hindsight Memory Recall │                     │ Stage 2: Hybrid Search  │
         │ - 0ms instant response  │                     │ - BM25 Sparse Search    │
         │ - Zero token spend      │                     │ - Dense Gemini Vectors  │
         │ - Verified root cause   │                     │ - Strict ACL Filter     │
         └────────────┬────────────┘                     └────────────┬────────────┘
                      │                                               │
                      │                                               ▼
                      │                                  ┌─────────────────────────┐
                      │                                  │ Stage 4: Synthesis      │
                      │                                  │ - Groq LLaMA 3.3-70B    │
                      │                                  │ - Decoy Conflict Res.   │
                      │                                  │ - Root Cause Verdict    │
                      │                                  └────────────┬────────────┘
                      │                                               │
                      ▼                                               ▼
         ┌─────────────────────────────────────────────────────────────────────────┐
         │                     Stage 3: Multi-Channel Escalation                   │
         │   - SEV1/SEV2: Dispatch Interactive Slack Block-Kit Alert Card          │
         │   - Assign On-Call Lead & Postmortem Link                              │
         └────────────────────────────────────┬────────────────────────────────────┘
                                              │
                                              ▼
                                 ┌─────────────────────────┐
                                 │ Hindsight Memory Retain │
                                 │ - Scoped to Team Bank   │
                                 │ - Self-Learning Loop    │
                                 └─────────────────────────┘
```

---

## 📁 Detailed Directory Layout

Every module is organized into dedicated subdirectories with clean package exports:

```text
HindTrace/
│
├── agents/                           # Agent Orchestration Subsystem
│   ├── prompts/                      # Modular system prompts & prompt templates
│   │   ├── __init__.py
│   │   └── investigation_prompts.py  # System prompts for Router, Synthesis & Escalation
│   ├── schemas/                      # Pydantic schemas & response contracts
│   │   ├── __init__.py
│   │   └── incident_schemas.py       # IncidentQuery, MemoryHit, Response models
│   ├── stages/                       # Modular pipeline stage implementations
│   │   ├── __init__.py
│   │   ├── stage1_router.py          # Stage 1: Triage, ACL check & injection shield
│   │   ├── stage2_retriever.py       # Stage 2: Hybrid BM25 + Semantic retrieval
│   │   ├── stage3_escalator.py       # Stage 3: Escalation ladder & Slack alerts
│   │   └── stage4_synthesizer.py     # Stage 4: Multi-source evidence synthesis
│   ├── pipeline.py                   # Master multi-stage agent pipeline orchestrator
│   └── __init__.py
│
├── api/                              # FastAPI Backend Architecture
│   ├── middleware/                   # Security & Telemetry Middleware
│   │   ├── __init__.py
│   │   └── security.py               # Security headers, CORS & timing filters
│   ├── models/                       # API Request & Response payload schemas
│   │   ├── __init__.py
│   │   └── payloads.py               # InvestigateRequest, MemoryRecallRequest
│   ├── routes/                       # Dedicated APIRouter endpoints
│   │   ├── __init__.py
│   │   ├── investigate.py            # POST /api/investigate
│   │   ├── memory.py                 # GET/POST /api/memory/banks, /recall, /retain
│   │   ├── eval.py                   # POST /api/eval/run
│   │   └── integrations.py           # GET /api/integrations/status
│   ├── main.py                       # FastAPI application entrypoint & static mounting
│   └── __init__.py
│
├── ingestion/                        # Knowledge Ingestion Subsystem
│   ├── chunkers/                     # Chunking strategies for Markdown & Runbooks
│   │   ├── __init__.py
│   │   └── text_chunker.py           # Step-level runbook & thread chunker
│   ├── indexers/                     # Search indexing engines
│   │   ├── __init__.py
│   │   └── corpus_loader.py          # BM25 + Gemini vector hybrid search engine
│   ├── parsers/                      # Source-specific document parsers
│   │   ├── __init__.py
│   │   ├── slack_parser.py           # Slack conversation thread parser
│   │   ├── email_parser.py           # Gmail / email thread extractor
│   │   └── gdrive_parser.py          # Google Drive runbook & postmortem parser
│   └── __init__.py
│
├── integrations/                     # External Platform Connectors
│   ├── google/                       # Google Cloud Workspace Integrations
│   │   ├── gdrive/                   # Google Drive API Client
│   │   │   ├── __init__.py
│   │   │   └── gdrive_client.py      # GDrive folder & postmortem syncer
│   │   └── gmail/                    # Gmail API Client
│   │       ├── __init__.py
│   │       └── gmail_client.py       # Gmail incident thread extractor
│   ├── slack/                        # Slack Workspace Integration
│   │   ├── __init__.py
│   │   └── slack_client.py           # Webhook dispatcher & Block Kit formatter
│   ├── webhooks/                     # Webhook ingress & dispatchers
│   │   └── __init__.py
│   └── __init__.py
│
├── memory/                           # Persistent Hindsight Memory Subsystem
│   ├── banks/                        # Scoped memory bank definitions
│   │   ├── __init__.py
│   │   └── bank_registry.py          # Bank scope manager (org-shared, team-cloud...)
│   ├── migrations/                   # SQLite schema definitions & setup
│   │   ├── __init__.py
│   │   └── init_db.py                # Table schemas & index migration
│   ├── hindsight_client.py           # Hindsight persistent memory client
│   └── hindsight_local.db            # Local high-performance SQLite database
│
├── security/                         # Zero-Trust Governance & Defense Guardrails
│   ├── acl/                          # Role-Based Access Control
│   │   ├── __init__.py
│   │   └── acl_guard.py              # Squad-level ACL filter (prevents data leaks)
│   ├── sanitizers/                   # Input sanitization & injection protection
│   │   ├── __init__.py
│   │   ├── injection_shield.py       # Prompt injection detector & XML wrapper
│   │   └── redaction.py              # PII and API secret redactor
│   └── __init__.py
│
├── evaluation/                       # Accuracy & Precision Benchmark Harness
│   ├── gold_questions/               # Benchmark ground-truth datasets
│   │   ├── __init__.py
│   │   └── dataset.py                # Dataset loader
│   ├── results/                      # Evaluation run metrics & historical logs
│   │   └── __init__.py
│   ├── eval_harness.py               # Automated 25-question test runner
│   ├── metrics.py                    # Accuracy, latency & token efficiency scoring
│   └── __init__.py
│
├── scripts/                          # Operational & Setup Scripts
│   ├── debug/                        # Diagnostic and test scripts
│   │   ├── __init__.py
│   │   ├── run_eval.py               # CLI evaluation runner
│   │   └── test_groq.py              # Groq LLM latency & connectivity check
│   ├── seed/                         # Pre-seeding scripts
│   │   ├── __init__.py
│   │   └── seed_memory.py            # Pre-seeds verified incidents into Hindsight
│   └── setup/                        # Environment & credential configuration
│       ├── __init__.py
│       ├── google_auth_listener.py   # Automatic Google OAuth server on port 8999
│       └── exchange_google_code.py   # Fixed-verifier OAuth code exchange tool
│
├── tests/                            # Automated Test Suite (100% Passing)
│   ├── fixtures/                     # Test mocks & incident payloads
│   │   ├── __init__.py
│   │   └── mock_data.py              # Sample incidents and Slack mock blocks
│   ├── integration/                  # End-to-end integration tests
│   │   ├── __init__.py
│   │   └── test_end_to_end.py        # Pipeline, router, ACL, and memory lifecycle
│   └── unit/                         # Unit tests
│       ├── __init__.py
│       ├── test_acl.py               # ACL boundaries & squad permission checks
│       ├── test_injection.py         # Prompt injection shield verification
│       ├── test_memory.py            # Hindsight recall & retain contracts
│       └── test_pipeline.py          # Stage 1 to Stage 4 unit tests
│
├── docs/                             # Comprehensive Technical Documentation
│   ├── architecture/                 # System architecture diagrams & workflows
│   │   └── ARCHITECTURE_AND_USAGE.md # 500+ line technical architecture guide
│   └── screenshots/                  # High-resolution dashboard screenshots
│       ├── homepage_dashboard.png
│       └── memory_banks.png
│
├── ui/                               # Studio Web Interface
│   ├── static/                       # CSS styles & JS client assets
│   │   ├── css/style.css
│   │   └── js/app.js
│   ├── index.html                    # High-contrast monochrome single-page dashboard
│   ├── app.js                        # UI logic
│   └── style.css                     # Studio monochrome design tokens
│
├── .env.example                      # Template configuration file
├── .gitignore                        # Git exclusion rules (protects keys & databases)
└── README.md                         # Project documentation
```

---

## 🔗 Live Enterprise Integrations

### 1. Slack Incident Dispatcher
- Dispatches rich Block-Kit alert cards to `#incidents` for **SEV1** and `#<team>` for **SEV2**.
- Formats incident status, root cause, assigned on-call responder, and links directly to remediation.

### 2. Google Drive & Gmail Sync
- **Active Incident Folder**: [Google Drive Incident Postmortems](https://drive.google.com/drive/folders/1E8F1ttaPcz6g_iRL3if0IkObGGXt3F_h)
- **Folder ID**: `1E8F1ttaPcz6g_iRL3if0IkObGGXt3F_h`
- Direct parsing of Google Docs postmortems and real-time incident email threads into the hybrid search index.

---

## ⚡ Quickstart & Installation

### 1. Clone Repository
```bash
git clone https://github.com/indra2215/HindTrace.git
cd HindTrace
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Credentials
Copy `.env.example` to `.env` and fill in your API keys:
```bash
cp .env.example .env
```
Key variables:
- `GROQ_API_KEY`: Groq API key for LLaMA 3.3-70B synthesis.
- `GEMINI_API_KEY`: Gemini embedding model key.
- `SLACK_WEBHOOK_URL`: Slack Incoming Webhook URL for incident alerts.
- `GDRIVE_INCIDENTS_FOLDER_ID`: `1E8F1ttaPcz6g_iRL3if0IkObGGXt3F_h`

### 4. Pre-Seed Memory Banks
```bash
python scripts/seed/seed_memory.py
```

### 5. Launch the Server
```bash
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```
Navigate to **`http://localhost:8000`** in your browser.

---

## 🧪 Automated Testing Suite

HindTrace includes a rigorous test suite validating ACL isolation, injection resistance, memory persistence, and end-to-end multi-stage execution:

```bash
python -m unittest discover tests -v
```

```text
test_public_internal_allowed_for_all (unit.test_acl.TestACLGuard) ... ok
test_restricted_tier_trap_t6 (unit.test_acl.TestACLGuard) ... ok
test_team_tier_blocks_other_teams (unit.test_acl.TestACLGuard) ... ok
test_direct_instruction_override_blocked (unit.test_injection.TestInjectionShield) ... ok
test_ignore_previous_instructions_blocked (unit.test_injection.TestInjectionShield) ... ok
test_safe_query_passes (unit.test_injection.TestInjectionShield) ... ok
test_acl_ceiling_team_block (unit.test_memory.TestHindsightMemory) ... ok
test_retain_and_recall_basic (unit.test_memory.TestHindsightMemory) ... ok
test_investigate_unanswerable_open_incident (unit.test_pipeline.TestPipeline) ... ok
test_stage1_router_injection_detection (unit.test_pipeline.TestPipeline) ... ok
test_stage1_router_valid_query (unit.test_pipeline.TestPipeline) ... ok
test_acl_security_enforcement (integration.test_end_to_end.TestEndToEndMithra) ... ok
test_memory_lifecycle (integration.test_end_to_end.TestEndToEndMithra) ... ok
test_pipeline_router (integration.test_end_to_end.TestEndToEndMithra) ... ok

----------------------------------------------------------------------
Ran 14 tests in 15.367s

OK (14/14 tests passed, 100% success rate)
```

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
<div align="center">
  <b>HindTrace</b> — Built for high-velocity software engineering organizations.
</div>
