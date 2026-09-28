---
doc_id: "DOC-ML-014"
doc_type: "kb_howto"
title: "ML service quick reference"
date: "2024-06-10"
author: "Victor Chen"
author_role: "senior"
services: ["training-jobs", "model-serve-api"]
versions: ["torch-2.1.0", "release-23"]
status: "current"
supersedes: []
acl_teams: ["ml-eng"]
tier: "team"
source_node: "KB-ML"
---

# ML service quick reference

### Knowledge-base entry
Service: training-jobs.
Stack: Python / PyTorch / CUDA / DataLoader.
Environments: prod, staging.
The confirmed GPU training incident is INC-311; the serving OOM incident is INC-310 and is a different service and failure.
