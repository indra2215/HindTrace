---
doc_id: "DOC-CLOUD-002"
doc_type: "ticket"
title: "INC-402"
date: "2024-02-20"
author: "Ben Okafor"
author_role: "senior"
services: ["k8s-cluster"]
versions: ["k8s-1.29"]
status: "current"
supersedes: []
acl_teams: ["cloud-eng"]
tier: "team"
source_node: "INC-402"
---

# INC-402

### Ticket record
Ticket status: current
Reporter: Ben Okafor
Description:
- Incident: INC-402
- Service: k8s-cluster
- Version: k8s-1.29
- Date: 2024-02-20
- Severity: SEV2
- Symptom: ImagePullBackOff
- Trigger: DEP-402
- Root cause: The prod node image lacked the registry trust bundle required by the private image endpoint.
- Resolution: Installed the registry trust bundle on the prod node image and retried the pull.
- Status: confirmed
- Confirmed by: Marta Silva
