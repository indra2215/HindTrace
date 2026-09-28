---
doc_id: "DOC-WEB-002"
doc_type: "ticket"
title: "INC-202"
date: "2024-03-18"
author: "Omar Reed"
author_role: "senior"
services: ["checkout-api"]
versions: ["2.3.0"]
status: "current"
supersedes: []
acl_teams: ["web-dev"]
tier: "team"
source_node: "INC-202"
---

# INC-202

### Ticket record
Ticket status: current
Reporter: Omar Reed
Description:
- Incident: INC-202
- Service: checkout-api
- Version: 2.3.0
- Date: 2024-03-18
- Severity: SEV2
- Symptom: HikariPool-1 - Connection is not available, request timed out after 30000ms
- Trigger: DEP-102
- Root cause: The order-history lookup introduced by the deployment used an unindexed database predicate; slow queries occupied otherwise healthy pool connections.
- Resolution: Added the order-history lookup index and verified the query plan.
- Status: confirmed
- Confirmed by: Nina Park
