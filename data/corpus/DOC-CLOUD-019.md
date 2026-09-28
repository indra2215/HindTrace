---
doc_id: "DOC-CLOUD-019"
doc_type: "runbook"
title: "Kubernetes image-pull triage"
date: "2024-02-21"
author: "Jules Chen"
author_role: "mid"
services: ["k8s-cluster"]
versions: ["k8s-1.29"]
status: "current"
supersedes: []
acl_teams: ["cloud-eng"]
tier: "team"
source_node: "RB-16"
---

# Kubernetes image-pull triage

### Runbook extract
Runbook: RB-16 — Kubernetes image-pull triage
Status: active.
Step 1: Record the namespace, node image, and image reference.
Step 2: Check whether the private registry trust bundle is present.
