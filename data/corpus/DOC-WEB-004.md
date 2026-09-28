---
doc_id: "DOC-WEB-004"
doc_type: "email_thread"
title: "INC-204"
date: "2024-04-10"
author: "Leo Kim"
author_role: "junior"
services: ["checkout-api"]
versions: ["v2.4"]
status: "current"
supersedes: []
acl_teams: ["web-dev"]
tier: "team"
source_node: "INC-204"
---

# INC-204

### Email thread (quoted text)
From: Leo Kim
Subject: INC-204
> Incident: INC-204
> Service: checkout-api
> Version: v2.4
> Date: 2024-04-10
> Severity: SEV3
> Symptom: bind: address already in use
> Trigger: DEP-104
> Root cause: The staging callback listener attempted to bind a port already held by the prior local process.
> Resolution: Stopped the prior process before restarting the staging service.
> Status: confirmed
> Confirmed by: Priya Shah
