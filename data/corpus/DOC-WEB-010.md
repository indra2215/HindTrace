---
doc_id: "DOC-WEB-010"
doc_type: "runbook"
title: "Checkout connection timeout triage"
date: "2024-03-20"
author: "Omar Reed"
author_role: "senior"
services: ["checkout-api"]
versions: ["v2.3", "2.3.0", "release-23"]
status: "current"
supersedes: []
acl_teams: ["web-dev"]
tier: "team"
source_node: "RB-15"
---

# Checkout connection timeout triage

### Runbook extract
Runbook: RB-15 — Checkout connection timeout triage
Status: active.
Step 1: Capture the exact Hikari timeout and deployment ID.
Step 2: Check pool saturation and query latency separately; distinguish pool pressure from slow queries.
Step 3: Compare the version and deployment with the matching confirmed incident.
