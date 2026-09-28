---
doc_id: "DOC-WEB-003"
doc_type: "slack_thread"
title: "INC-203"
date: "2024-04-02"
author: "Priya Shah"
author_role: "mid"
services: ["checkout-api"]
versions: ["release-23"]
status: "current"
supersedes: []
acl_teams: ["web-dev"]
tier: "team"
source_node: "INC-203"
---

# INC-203

### Slack export (thread excerpt)
@PriyaShah: Incident: INC-203
> Service: checkout-api
> Version: release-23
> Date: 2024-04-02
> Severity: SEV2
> Symptom: HikariPool-1 - Connection is not available, request timed out after 30000ms
> Trigger: DEP-103
> Root cause: The new connection-return path failed to close connections after a retryable database exception.
> Resolution: Patched the retry cleanup path and drained the affected application instances.
> Status: confirmed
> Confirmed by: Omar Reed
