---
doc_id: "DOC-ML-011"
doc_type: "email_thread"
title: "PM-052"
date: "2024-06-10"
author: "Noor Haddad"
author_role: "mid"
services: ["training-jobs"]
versions: ["torch-2.1.0", "torch-2.2.1"]
status: "current"
supersedes: ["DOC-ML-010"]
acl_teams: ["ml-eng"]
tier: "team"
source_node: "PM-052"
---


# PM-052

### Email thread (quoted text)
From: Noor Haddad
Subject: PM-052
> Postmortem: PM-052
> Incident: INC-313
> Date: 2024-06-10
> Status: final
> Finding: RB-14 step-8 advice made things worse when applied without matching torch version and environment: increasing workers worsened the torch-2.1.0 staging worker failures, while universal num_workers=0 advice harmed the torch-2.2.1 prod throughput target. Keep the two fixes separate.
> Supersedes runbooks: RB-14
