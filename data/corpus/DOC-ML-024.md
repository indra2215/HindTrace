---
doc_id: "DOC-ML-024"
doc_type: "email_thread"
title: "Training worker recovery and step-8 decision"
date: "2024-05-06"
author: "Sam Patel"
author_role: "junior"
services: ["training-jobs"]
versions: ["torch-2.1.0", "torch-2.2.1"]
status: "superseded"
supersedes: []
acl_teams: ["ml-eng"]
tier: "team"
source_node: "RB-14"
---

# Training worker recovery and step-8 decision

### Email thread (quoted text)
From: Sam Patel
Subject: Training worker recovery and step-8 decision
> Runbook: RB-14 — Training worker recovery and step-8 decision
> Status: superseded by PM-052.
> Step 8 is context-specific; the fixes must not be merged.
> Step 8 context A: torch-2.1.0, staging, error WORKER_EXIT_137; raising workers to 8 increased shared-memory pressure and worsened worker crashes. Fix: set num_workers=0.
> Step 8 context B: torch-2.2.1, prod, error EPOCH_RESTART_WORKER; universal num_workers=0 advice removed the crash but made the established throughput target fail. Fix: keep the configured worker count and set persistent_workers=false.
> Do not transfer either context-specific step-8 fix to the other context.
