---
doc_id: "DOC-UI-001"
doc_type: "incident_report"
title: "INC-410"
date: "2024-07-13"
author: "Iris Wong"
author_role: "lead"
services: ["design-pipeline"]
versions: ["design-5.2"]
status: "current"
supersedes: []
acl_teams: ["ui-ux"]
tier: "team"
source_node: "INC-410"
---

# INC-410

Incident: INC-410
Service: design-pipeline
Version: design-5.2
Date: 2024-07-13
Severity: SEV2
Symptom: SVG conversion job hangs; asset export timeouts.
Trigger: DEP-501
Root cause: The Figma API client retried a timed-out upstream request without a bounded deadline, occupying SVG conversion workers.
Resolution: Applied a bounded request deadline and capped retries in the Figma API client.
Status: confirmed
Confirmed by: Iris Wong
