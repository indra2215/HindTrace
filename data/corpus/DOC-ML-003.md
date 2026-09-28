---
doc_id: "DOC-ML-003"
doc_type: "slack_thread"
title: "INC-312"
date: "2024-05-21"
author: "Noor Haddad"
author_role: "mid"
services: ["training-jobs"]
versions: ["train-24.05"]
status: "current"
supersedes: []
acl_teams: ["ml-eng"]
tier: "team"
source_node: "INC-312"
---

# INC-312

### Slack export (thread excerpt)
@NoorHaddad: Incident: INC-312
> Service: training-jobs
> Version: train-24.05
> Date: 2024-05-21
> Severity: SEV2
> Symptom: nan loss
> Trigger: Training run with the train-24.05 configuration.
> Root cause: The normalization input contained a zero-variance feature and the training path divided by its standard deviation without a guard.
> Resolution: Added a zero-variance guard to the normalization path.
> Status: confirmed
> Confirmed by: Noor Haddad
