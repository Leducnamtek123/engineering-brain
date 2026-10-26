---
name: backend-authz-review
description: Review backend endpoints for missing authorization and ownership checks (IDOR). Use when reviewing an API diff, a new endpoint, or when asked "check access control", "is this endpoint safe", "review authz".
---

# Backend authorization review

## Steps
1. List every endpoint in scope that reads an id from the request (path, query, body).
2. For each, apply the rules below. Read the rule file before judging.
3. Report only what you can point to: `file:line`, which rule, why, suggested fix. If the check happens somewhere you cannot see (middleware, policy layer), say "not verified" instead of guessing.
4. Do not flag endpoints that serve public data or already constrain the query by the authenticated owner.

## Rules
- `knowledge/backend/BE-AUTHZ-001.md`: ownership check on id-based endpoints

## Output
| Severity | file:line | Rule | Problem | Fix |
|---|---|---|---|---|

End with: endpoints checked, findings count, anything not verified.
