---
doc_id: "DOC-ML-025"
doc_type: "postmortem"
title: "PM-052"
date: "2024-06-10"
author: "Asha Rao"
author_role: "lead"
services: ["training-jobs"]
versions: ["torch-2.1.0", "torch-2.2.1"]
status: "current"
supersedes: []
acl_teams: ["ml-eng"]
tier: "team"
source_node: "PM-052"
---

# PM-052

### Postmortem record
Postmortem: PM-052
Incident: INC-313
Date: 2024-06-10
Status: final
Finding: RB-14 step-8 advice made things worse when applied without matching torch version and environment: increasing workers worsened the torch-2.1.0 staging worker failures, while universal num_workers=0 advice harmed the torch-2.2.1 prod throughput target. Keep the two fixes separate.
Supersedes runbooks: RB-14
