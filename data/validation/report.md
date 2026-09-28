# Validation report — Northbeam Studio synthetic corpus

## Summary

- Corpus documents: **100**
- Gold questions: **25**
- The question-category totals in the prompt sum to 24; one extra single-document answerable question was added to reach 25. The prompt-injection case is included within the 9 single-document questions, and the 2 contradiction questions are included within the 4 multi-hop questions.
- The source-of-truth graph includes a document catalog and evidence_text on source nodes. Document factual body text is rendered from those graph nodes; no free-form factual filler was added.
- The synthetic schedule includes no real secrets. The only key-shaped string is redacted.

## Checklist results

- **PASS — V1 Fact-leak check:** Every document body normalizes exactly to evidence_text on its source graph node; every front-matter field matches its graph documents-catalog record. No non-graph factual body claims detected.
- **PASS — V2 Gold evidence coverage:** All non-empty gold_doc_ids resolve to corpus documents; each question answer point is represented in its source-node evidence. Missing: []
- **PASS — V3 Trap discoverability:** All T1-T9 have explicit graph nodes/edges and tagged gold questions; restricted-record allowlists match corpus acl_users and all T6 users are unauthorized. {"T1": "INC-201, INC-202, INC-203 (same Hikari symptom; three distinct confirmed causes); GQ-14..GQ-16", "T2": "RB-14 superseded by PM-052; GQ-10", "T3": "CON-501 vs CON-502; CON-503 vs CON-504; GQ-12, GQ-13", "T4": "VOC-UI, VOC-WEB, VOC-CLOUD; GQ-11 (and INC-410)", "T5": "RB-14 step 8 context A/B, distinct fixes; GQ-20..GQ-22", "T6": "RET-001, RET-002, RET-003; GQ-23..GQ-25; restricted ACL allowlists verified", "T7": "Open incidents INC-205, INC-314, INC-404; GQ-17..GQ-19", "T8": "RB-14 missing-context partials GQ-20, GQ-21; distinct context-specific answers represented", "T9": "Checkout decoy pairs: INC-201/202, INC-201/203, INC-202/203; GQ-14..GQ-16"}
- **PASS — V4 ID integrity:** All graph edge endpoints and postmortem incident references resolve. Unresolved: []
- **PASS — V5 Date sanity:** All document dates parse; every postmortem date is on/after its incident. Low-confidence wrong author-extracted date is explicitly flagged in NOTE-LOWDATE (author-entered 2024-04-05; graph incident date 2024-05-05). Issues: []
- **PASS — V6 Answerability labels:** answer_labels.csv matches expected_verdict for all 25 questions; counts: {"answerable": 17, "partial": 2, "unanswerable": 6}
- **PASS — V7 Counts and coverage:** Corpus=100; questions=25; user-team coverage={'web-dev': 10, 'cloud-eng': 5, 'ml-eng': 7, 'ui-ux': 3}; trap tags=['T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9', 'none']; question-user roles=['junior', 'lead', 'mid', 'senior'].

## Spot-check sample: five complete documents

### DOC-WEB-001

```markdown
---
doc_id: "DOC-WEB-001"
doc_type: "incident_report"
title: "INC-201"
date: "2024-03-12"
author: "Nina Park"
author_role: "lead"
services: ["checkout-api"]
versions: ["v2.3"]
status: "current"
supersedes: []
acl_teams: ["web-dev"]
tier: "team"
source_node: "INC-201"
---

# INC-201

Incident: INC-201
Service: checkout-api
Version: v2.3
Date: 2024-03-12
Severity: SEV2
Symptom: HikariPool-1 - Connection is not available, request timed out after 30000ms
Trigger: DEP-101
Root cause: The increased checkout concurrency exhausted the configured Hikari connection pool; checkout transactions held connections longer than the pool could replenish them.
Resolution: Rolled back the concurrency increase and returned the pool to its prior configuration.
Status: confirmed
Confirmed by: Omar Reed
```
### DOC-ML-001

```markdown
---
doc_id: "DOC-ML-001"
doc_type: "incident_report"
title: "INC-310"
date: "2024-05-03"
author: "Asha Rao"
author_role: "lead"
services: ["model-serve-api"]
versions: ["release-23"]
status: "current"
supersedes: []
acl_teams: ["ml-eng"]
tier: "team"
source_node: "INC-310"
---

# INC-310

Incident: INC-310
Service: model-serve-api
Version: release-23
Date: 2024-05-03
Severity: SEV2
Symptom: OOMKilled
Trigger: DEP-301
Root cause: The larger default inference batch exceeded the serving container memory limit for a high-size request.
Resolution: Restored the earlier default batch size and bounded per-request batch size.
Status: confirmed
Confirmed by: Victor Chen
```
### DOC-CLOUD-002

```markdown
---
doc_id: "DOC-CLOUD-002"
doc_type: "ticket"
title: "INC-402"
date: "2024-02-20"
author: "Ben Okafor"
author_role: "senior"
services: ["k8s-cluster"]
versions: ["k8s-1.29"]
status: "current"
supersedes: []
acl_teams: ["cloud-eng"]
tier: "team"
source_node: "INC-402"
---

# INC-402

### Ticket record
Ticket status: current
Reporter: Ben Okafor
Description:
- Incident: INC-402
- Service: k8s-cluster
- Version: k8s-1.29
- Date: 2024-02-20
- Severity: SEV2
- Symptom: ImagePullBackOff
- Trigger: DEP-402
- Root cause: The prod node image lacked the registry trust bundle required by the private image endpoint.
- Resolution: Installed the registry trust bundle on the prod node image and retried the pull.
- Status: confirmed
- Confirmed by: Marta Silva
```
### DOC-UI-003

```markdown
---
doc_id: "DOC-UI-003"
doc_type: "email_thread"
title: "UI wording for FAIL-UI-01"
date: "2024-07-13"
author: "Ana Costa"
author_role: "mid"
services: ["design-pipeline", "figma-api"]
versions: ["design-5.2", "figma-client-2.7"]
status: "current"
supersedes: []
acl_teams: ["ui-ux"]
tier: "team"
source_node: "VOC-UI"
---

# UI wording for FAIL-UI-01

### Email thread (quoted text)
From: Ana Costa
Subject: UI wording for FAIL-UI-01
> Failure vocabulary: “asset export timeouts”.
> Failure ID: FAIL-UI-01.
> The wording refers to the same design-pipeline/Figma upstream-timeout failure recorded as INC-410.
```
### DOC-XTEAM-004

```markdown
---
doc_id: "DOC-XTEAM-004"
doc_type: "email_thread"
title: "Contemporaneous DEP-103 note A"
date: "2024-04-01"
author: "Leo Kim"
author_role: "junior"
services: ["checkout-api"]
versions: ["release-23"]
status: "current"
supersedes: []
acl_teams: []
tier: "public-internal"
source_node: "CON-501"
---

# Contemporaneous DEP-103 note A

### Email thread (quoted text)
From: Leo Kim
Subject: Contemporaneous DEP-103 note A
> Entity: DEP-103 / checkout-api, prod, 2024-04-01 window.
> Assertion in note A: DEP-103 included the order-history database index.
> Conflict status: unresolved; this note does not establish which assertion is correct.
```
