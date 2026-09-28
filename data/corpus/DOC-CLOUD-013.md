---
doc_id: "DOC-CLOUD-013"
doc_type: "slack_thread"
title: "INC-402"
date: "2024-02-20"
author: "Marta Silva"
author_role: "lead"
services: ["k8s-cluster"]
versions: ["k8s-1.29"]
status: "current"
supersedes: []
acl_teams: ["cloud-eng"]
tier: "team"
source_node: "INC-402"
---

# INC-402

### Slack export (thread excerpt)
@MartaSilva: Incident: INC-402
> Service: k8s-cluster
> Version: k8s-1.29
> Date: 2024-02-20
> Severity: SEV2
> Symptom: ImagePullBackOff
> Trigger: DEP-402
> Root cause: The prod node image lacked the registry trust bundle required by the private image endpoint.
> Resolution: Installed the registry trust bundle on the prod node image and retried the pull.
> Status: confirmed
> Confirmed by: Marta Silva
