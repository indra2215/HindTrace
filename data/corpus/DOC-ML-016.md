---
doc_id: "DOC-ML-016"
doc_type: "incident_report"
title: "INC-311"
date: "2024-05-05"
author: "Sam Patel"
author_role: "junior"
services: ["training-jobs"]
versions: ["torch-2.1.0"]
status: "current"
supersedes: []
acl_teams: ["ml-eng"]
tier: "team"
source_node: "INC-311"
---

# INC-311

Incident: INC-311
Service: training-jobs
Version: torch-2.1.0
Date: 2024-05-05
Severity: SEV2
Symptom: CUDA out of memory
Trigger: DEP-302
Root cause: The per-device training batch exceeded available GPU memory on the staging training worker.
Resolution: Reduced the per-device batch size for the affected training configuration.
Status: confirmed
Confirmed by: Asha Rao
