---
doc_id: "DOC-WEB-001"
doc_type: "incident_report"
title: "INC-201"
date: "2024-03-12"
author: "Nina Park"
author_role: "lead"
services: ["checkout-api"]
versions: ["v2.3"]
status: "current"
supersedes: []
acl_teams: ["web-dev"]
tier: "team"
source_node: "INC-201"
---

# INC-201

Incident: INC-201
Service: checkout-api
Version: v2.3
Date: 2024-03-12
Severity: SEV2
Symptom: HikariPool-1 - Connection is not available, request timed out after 30000ms
Trigger: DEP-101
Root cause: The increased checkout concurrency exhausted the configured Hikari connection pool; checkout transactions held connections longer than the pool could replenish them.
Resolution: Rolled back the concurrency increase and returned the pool to its prior configuration.
Status: confirmed
Confirmed by: Omar Reed
