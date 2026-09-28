# 📐 HindTrace Architecture Diagram Specification (For Claude)

> **Prompt for Claude**:  
> *"Please review this complete architectural specification of **HindTrace** (an Autonomous Enterprise Incident Commander & Persistent Hindsight Memory Engine). Using this specification, render a comprehensive, publication-ready visual architecture diagram (using Mermaid, SVG, or a React component with Tailwind and Lucide icons) showing the full system flow, component containers, data transitions, memory contracts, and zero-trust security guardrails."*

---

## 1. System Overview & Core Value Proposition

**HindTrace** is an autonomous AI incident response platform built for engineering organizations to investigate outages, resolve recurrent issues, enforce multi-tenant access control, and retain institutional memory.

### Key Architectural Pillars:
1. **Zero-Latency Memory Short-Circuit**: The agent enforces a strict `recall()` before search contract. Known incidents resolve in **0ms** from SQLite Hindsight memory banks without LLM token consumption.
2. **Zero-Trust Squad ACL Guard**: Enforces Role-Based Access Control (RBAC) across 4 engineering squads (`cloud-eng`, `ml-platform`, `backend-core`, `web-dev`). Sensitive documents (finance, HR, restricted postmortems) are excised before the LLM sees them.
3. **Indirect Prompt Injection Neutralizer**: All retrieved texts and user inputs pass through a heuristic and semantic injection detector and are isolated within `<untrusted_content>` XML fences.
4. **Multi-Source Hybrid Synthesis**: Merges dense semantic embeddings (Gemini `models/gemini-embedding-2`) and sparse lexical search (BM25) across Slack threads, Gmail messages, and Google Drive postmortems.
5. **Real-Time Escalation Ladder**: Automatically fires rich Block-Kit alert cards to Slack `#incidents` on **SEV1** and `#<team>` on **SEV2**, assigning on-call personnel.
6. **Continuous Retain Contract**: Every resolved incident is summarized and retained in team-scoped memory banks (`org-shared`, `team-cloud`, `team-ml`, `team-backend`).

<div align="center">

![HindTrace Complete System Architecture Reference](docs/screenshots/architecture_diagram.png)

</div>

---

## 2. High-Level C4 System Context Diagram (Level 1)

```mermaid
graph TD
    User["👨‍💻 SRE / On-Call Engineer<br/>(e.g., Marta Silva, Leo Kim)"]
    AlertSystem["🚨 Alerting Systems<br/>(PagerDuty, Datadog, Prometheus)"]
    
    subgraph HindTracePlatform["🏛️ HindTrace Autonomous Platform"]
        UI["🖥️ Monochrome Studio UI<br/>(FastAPI / Vanilla JS & CSS)"]
        CoreAgent["🤖 HindTrace Agentic Engine<br/>(4-Stage Orchestrator)"]
        MemoryBank["🧠 Hindsight Memory Engine<br/>(SQLite Persistent Banks)"]
    end
    
    subgraph ExternalServices["🌐 External Integrations & Data Sources"]
        Groq["⚡ Groq API<br/>(LLaMA 3.3-70B Versatile)"]
        Slack["💬 Slack API<br/>(Live Webhooks & #incidents channel)"]
        GoogleDrive["📁 Google Drive API<br/>(Incident Postmortems Folder)"]
        Gmail["✉️ Gmail API<br/>(Incident Mail Threads)"]
    end

    User -->|"Submits query / views banks"| UI
    AlertSystem -->|"Fires incident alert payload"| UI
    UI -->|"REST /api/investigate"| CoreAgent
    CoreAgent <-->|"0ms Recall / Post-Investigation Retain"| MemoryBank
    CoreAgent -->|"Synthesize root cause verdict"| Groq
    CoreAgent -->|"SEV1/SEV2 Escalation Webhook"| Slack
    CoreAgent <-->|"Sync runbooks & postmortems"| GoogleDrive
    CoreAgent <-->|"Fetch triage email threads"| Gmail
```

---

## 3. Container & Pipeline Architecture (Level 2)

```mermaid
flowchart TD
    subgraph ClientLayer["1. Client & Presentation Layer"]
        Browser["Studio Dashboard (Vanilla JS, CSS Tokens)"]
        RESTClient["External Webhook Clients (cURL / Python SDK)"]
    end

    subgraph APILayer["2. API & Ingress Gateway (FastAPI)"]
        SecurityMW["Security Headers & Timing Middleware"]
        RouterGateway["FastAPI Router Gateway (/api/investigate, /api/memory)"]
    end

    subgraph AgentPipeline["3. HindTrace 4-Stage Agentic Pipeline"]
        direction TB
        S1["Stage 1: Intake Router & Triage<br/>• Incident ID Extraction (INC-xxx)<br/>• Prompt Injection Shield<br/>• User Role & Squad Persona Mapping"]
        
        Decision1{"Known Incident<br/>in Memory?"}
        
        S1Mem["⚡ 0ms Short-Circuit<br/>• Return Verified Root Cause<br/>• Bypass Search & LLM<br/>• Zero Token Spend"]
        
        S2["Stage 2: Hybrid Multi-Source Retriever<br/>• BM25 Lexical Keyword Search<br/>• Gemini Dense Vector Embeddings<br/>• Squad-Level ACL Filtering (RBAC)"]
        
        S4["Stage 4: Synthesis & Reasoning<br/>• Decoy Runbook Neutralization<br/>• Groq LLaMA 3.3-70B Synthesis<br/>• Root Cause & Remediation Steps"]
        
        S3["Stage 3: Escalation Ladder<br/>• SEV1/SEV2 Slack Dispatch<br/>• On-Call Assignment<br/>• Postmortem Linkage"]
    end

    subgraph StorageLayer["4. Memory & Knowledge Subsystems"]
        HindsightDB[("SQLite Hindsight Local DB<br/>• org-shared<br/>• team-cloud<br/>• team-ml<br/>• team-backend")]
        CorpusStorage[("Enterprise Knowledge Corpus<br/>• Slack threads<br/>• Google Drive Postmortems<br/>• Gmail threads")]
    end

    ClientLayer --> APILayer
    APILayer --> S1
    S1 --> Decision1
    Decision1 -- "YES (Memory Hit)" --> S1Mem
    Decision1 -- "NO (New Issue)" --> S2
    S2 <--> CorpusStorage
    S2 --> S4
    S4 --> S3
    S1Mem --> S3
    S3 -->|"retain() verified outcome"| HindsightDB
    S1Mem <-->|"recall() query"| HindsightDB
```

---

## 4. Component Sequence Diagram (Level 3)

```mermaid
sequenceDiagram
    autonumber
    actor Engineer as SRE Engineer
    participant UI as HindTrace UI / API
    participant Router as Stage 1 Router
    participant Memory as Hindsight Client
    participant Retriever as Stage 2 Hybrid Search
    participant ACL as Security ACL Guard
    participant LLM as Groq LLaMA 3.3-70B
    participant Escalator as Stage 3 Escalator
    participant Slack as Slack Webhook

    Engineer->>UI: POST /api/investigate (query, user_name="Marta Silva", sev=1)
    UI->>Router: Intake analysis & sanitization
    Router->>Router: Detect prompt injection & extract incident ID
    
    alt Memory Bank Contains Pre-existing Solution
        Router->>Memory: recall(bank="team-cloud", query="INC-402")
        Memory-->>Router: MemoryHit (Root cause: ECR rate limit, Resolution: VPC endpoint)
        Router-->>UI: ⚡ Return instant resolution (0ms, 0 tokens)
    else Unresolved / Novel Incident
        Router->>Retriever: retrieve(query, top_k=6)
        Retriever->>Retriever: BM25 score + Gemini embedding dot product
        Retriever->>ACL: filter_allowed_chunks(chunks, user_team="cloud-eng")
        ACL-->>Retriever: Stripped of unauthorized confidential chunks
        Retriever->>LLM: synthesize(evidence_chunks, system_prompt)
        LLM-->>Router: InvestigationResult (verdict, root_cause, steps)
        Router->>Memory: retain(bank="team-cloud", key="INC-402", outcome)
        Memory-->>Router: Persisted to SQLite
    end

    opt Severity is SEV1 or SEV2
        Router->>Escalator: trigger_escalation(sev=1, incident_id, verdict)
        Escalator->>Slack: POST Block-Kit Card to #incidents
        Slack-->>Escalator: 200 OK
    end

    Router-->>UI: Complete Investigation Response JSON
    UI-->>Engineer: Render Investigation Card + Sources + Action Buttons
```

---

## 5. Security & Isolation Matrix

| Layer | Mechanism | Protection Scope |
|:---|:---|:---|
| **Query Input** | `injection_shield.py` | Neutralizes direct/indirect prompt overrides & jailbreaks |
| **Ingress** | `security.py` | Sets `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, CORS |
| **Corpus Retrieval** | `acl_guard.py` | Enforces `public-internal`, `team`, and `restricted` visibility tiers |
| **Synthesis Prompt** | `<untrusted_content>` tags | Sandboxes retrieved text so LLM does not execute external instructions |
| **Credential Scrubbing** | `redaction.py` | Replaces Bearer tokens, passwords, and private keys with `[REDACTED]` |
| **Memory Access** | `bank_registry.py` | Engineers cannot query private team banks outside their squad |

---

## 6. Prompt for Claude (How to use this file)

Copy and paste the following into Claude:

```markdown
Hi Claude! Please generate a set of clean, visually stunning architecture diagrams for the **HindTrace** Autonomous Incident Response Platform based on this specification file.

Specifically, I would like:
1. An Executive-Level Architecture Diagram (high-level visual containers with icons).
2. A Data Flow & Triage Decision Tree (explaining the 0ms memory short-circuit vs hybrid retrieval).
3. A Security Isolation & ACL Enforcement Diagram showing how unauthorized documents are filtered out before reaching the LLM.
4. A component interaction table showing latency, inputs, and outputs of each of the 4 stages.

Please format your response with clean Mermaid diagrams and accompanying structured explanations!
```
