---
doc_id: "DOC-WEB-024"
doc_type: "ticket"
title: "PM-051"
date: "2024-03-14"
author: "Leo Kim"
author_role: "junior"
services: ["checkout-api"]
versions: ["v2.3"]
status: "current"
supersedes: []
acl_teams: ["web-dev"]
tier: "team"
source_node: "PM-051"
---

# PM-051

### Ticket record
Ticket status: current
Reporter: Leo Kim
Description:
- Postmortem: PM-051
- Incident: INC-201
- Date: 2024-03-14
- Status: final
- Finding: The Hikari timeout followed DEP-101 and was caused by pool exhaustion after the concurrency increase; it was not the missing-index failure later recorded for INC-202.
- Supersedes runbooks: none
