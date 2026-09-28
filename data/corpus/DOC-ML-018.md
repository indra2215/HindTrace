---
doc_id: "DOC-ML-018"
doc_type: "slack_thread"
title: "INC-313"
date: "2024-06-04"
author: "Victor Chen"
author_role: "senior"
services: ["training-jobs"]
versions: ["torch-2.2.1"]
status: "current"
supersedes: []
acl_teams: ["ml-eng"]
tier: "team"
source_node: "INC-313"
---

# INC-313

### Slack export (thread excerpt)
@VictorChen: Incident: INC-313
> Service: training-jobs
> Version: torch-2.2.1
> Date: 2024-06-04
> Severity: SEV2
> Symptom: DataLoader worker exited unexpectedly; worker process crashed.
> Trigger: DEP-303
> Root cause: The updated worker image used persistent workers with a dataset iterator that was not safe to reuse after an epoch restart.
> Resolution: Disabled persistent workers for the affected dataset iterator.
> Status: confirmed
> Confirmed by: Victor Chen
