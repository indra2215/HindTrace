---
doc_id: "DOC-CLOUD-012"
doc_type: "ticket"
title: "INC-401"
date: "2024-02-09"
author: "Eli Brooks"
author_role: "junior"
services: ["ci-runner"]
versions: ["runner-3.9"]
status: "current"
supersedes: []
acl_teams: ["cloud-eng"]
tier: "team"
source_node: "INC-401"
---

# INC-401

### Ticket record
Ticket status: current
Reporter: Eli Brooks
Description:
- Incident: INC-401
- Service: ci-runner
- Version: runner-3.9
- Date: 2024-02-09
- Severity: SEV2
- Symptom: CrashLoopBackOff
- Trigger: DEP-401
- Root cause: The runner deployment referenced a base image tag that was not present in the internal registry.
- Resolution: Restored the published runner base image tag.
- Status: confirmed
- Confirmed by: Ben Okafor
