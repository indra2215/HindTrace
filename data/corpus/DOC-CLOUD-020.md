---
doc_id: "DOC-CLOUD-020"
doc_type: "email_thread"
title: "PM-053"
date: "2024-02-22"
author: "Eli Brooks"
author_role: "junior"
services: ["k8s-cluster"]
versions: ["k8s-1.29"]
status: "current"
supersedes: []
acl_teams: ["cloud-eng"]
tier: "team"
source_node: "PM-053"
---

# PM-053

### Email thread (quoted text)
From: Eli Brooks
Subject: PM-053
> Postmortem: PM-053
> Incident: INC-402
> Date: 2024-02-22
> Status: final
> Finding: The prod ImagePullBackOff followed DEP-402 because the prod node image lacked the private registry trust bundle.
> Supersedes runbooks: none
