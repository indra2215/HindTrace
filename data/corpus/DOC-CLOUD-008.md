---
doc_id: "DOC-CLOUD-008"
doc_type: "kb_howto"
title: "Kubernetes image-pull triage"
date: "2024-02-21"
author: "Eli Brooks"
author_role: "junior"
services: ["k8s-cluster"]
versions: ["k8s-1.29"]
status: "current"
supersedes: []
acl_teams: ["cloud-eng"]
tier: "team"
source_node: "RB-16"
---

# Kubernetes image-pull triage

### Knowledge-base entry
Runbook: RB-16 — Kubernetes image-pull triage
Status: active.
Step 1: Record the namespace, node image, and image reference.
Step 2: Check whether the private registry trust bundle is present.
