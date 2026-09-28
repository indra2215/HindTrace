# HindTrace — Database Subsystem

This directory manages persistent storage for HindTrace.

## Databases

1. **`investigations.db`** (in `database/`):
   - Created and managed by `database/db.py`.
   - Stores the structured audit log table: `investigations`.
   - Tracks `investigation_id`, `user_name`, `user_team`, `sev_level`, `verdict`, `status`, `citations`, `memory_used`, and Slack escalation records.

2. **`hindsight_local.db`** (in `memory/`):
   - Created and managed by `memory/hindsight_client.py`.
   - Stores the persistent Hindsight memory banks:
     - `org-shared`: Studio-wide shared incident resolutions and vocabulary mappings.
     - `team-ml`: Machine Learning squad specific knowledge.
     - `team-cloud`: Cloud infrastructure squad specific knowledge.
   - Enforces `acl_ceiling` (`public-internal`, `team`, `restricted`).

