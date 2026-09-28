---
doc_id: "DOC-ML-002"
doc_type: "ticket"
title: "INC-311"
date: "2024-05-05"
author: "Victor Chen"
author_role: "senior"
services: ["training-jobs"]
versions: ["torch-2.1.0"]
status: "current"
supersedes: []
acl_teams: ["ml-eng"]
tier: "team"
source_node: "INC-311"
---

# INC-311

### Ticket record
Ticket status: current
Reporter: Victor Chen
Description:
- Incident: INC-311
- Service: training-jobs
- Version: torch-2.1.0
- Date: 2024-05-05
- Severity: SEV2
- Symptom: CUDA out of memory
- Trigger: DEP-302
- Root cause: The per-device training batch exceeded available GPU memory on the staging training worker.
- Resolution: Reduced the per-device batch size for the affected training configuration.
- Status: confirmed
- Confirmed by: Asha Rao
