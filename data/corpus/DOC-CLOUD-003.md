---
doc_id: "DOC-CLOUD-003"
doc_type: "slack_thread"
title: "INC-403"
date: "2024-02-23"
author: "Jules Chen"
author_role: "mid"
services: ["k8s-cluster"]
versions: ["k8s-1.29"]
status: "current"
supersedes: []
acl_teams: ["cloud-eng"]
tier: "team"
source_node: "INC-403"
---

# INC-403

### Slack export (thread excerpt)
@JulesChen: Incident: INC-403
> Service: k8s-cluster
> Version: k8s-1.29
> Date: 2024-02-23
> Severity: SEV2
> Symptom: kubelet eviction notice; pod evicted under node memory pressure.
> Trigger: DEP-403
> Root cause: The staging node memory reservation was lower than the workload request during the image-cache warmup.
> Resolution: Restored the previous node memory reservation for the staging pool.
> Status: confirmed
> Confirmed by: Jules Chen
