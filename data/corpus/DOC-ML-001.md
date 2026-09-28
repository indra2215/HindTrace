---
doc_id: "DOC-ML-001"
doc_type: "incident_report"
title: "INC-310"
date: "2024-05-03"
author: "Asha Rao"
author_role: "lead"
services: ["model-serve-api"]
versions: ["release-23"]
status: "current"
supersedes: []
acl_teams: ["ml-eng"]
tier: "team"
source_node: "INC-310"
---

# INC-310

Incident: INC-310
Service: model-serve-api
Version: release-23
Date: 2024-05-03
Severity: SEV2
Symptom: OOMKilled
Trigger: DEP-301
Root cause: The larger default inference batch exceeded the serving container memory limit for a high-size request.
Resolution: Restored the earlier default batch size and bounded per-request batch size.
Status: confirmed
Confirmed by: Victor Chen
