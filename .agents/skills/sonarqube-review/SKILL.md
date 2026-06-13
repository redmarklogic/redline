---
name: sonarqube-review
description: Use after a successful sonarqube-scan to retrieve open issues for the current branch, triage them, and record false positives so they are not re-surfaced
---

# SonarQube Review

Retrieve open issues for the current branch from a local SonarQube instance,
group them for triage, and record false positives / won't-fix decisions so they
move to RESOLVED and never re-surface.

**Boundary contract:**

- **Input**: a completed `sonarqube-scan` (compute-engine task `SUCCESS`);
  `SONARQUBE_URL`, `SONAR_PROJECT_KEY`, `SONAR_TOKEN` in `.env`.
- **Output**: a triaged issue list grouped by file and severity; false positives
  and won't-fix issues transitioned to RESOLVED in SonarQube.

**Composable.** Called standalone after a successful scan, or as one step in a
larger local quality gate.

## Prerequisites

| # | Requirement |
|---|---|
| P1 | `sonarqube-scan` completed with `SUCCESS` |
| P2 | `SONARQUBE_URL`, `SONAR_PROJECT_KEY`, `SONAR_TOKEN` in `.env` |
| P3 | `mcp/sonarqube` MCP registered in `.mcp.json` (primary path) |

## Guard Conditions

| # | Condition |
|---|---|
| G1 | Instance reachable and UP — recheck before retrieving issues |
| G2 | Never retrieve issues if the CE task has not reached `SUCCESS` — stale/partial results |
| G3 | Record false positives via SonarQube status transition — never by editing local files |

## Python Tool

```python
import os
from sonar_scan import (
    SonarQubeUnavailableError,
    ensure_available,
    current_branch,
    fetch_issues,
    group_issues,
)

# The environment is configured by the caller (the scan scripts export .env; CI
# sets these in the job env). Per AGENTS.md: do NOT load .env from Python and do
# NOT default env vars. sonar_scan applies _normalise_url internally, so
# host.docker.internal is rewritten to localhost for host-side calls.
url     = os.environ["SONARQUBE_URL"]
project = os.environ["SONAR_PROJECT_KEY"]
token   = os.environ["SONAR_TOKEN"]

ensure_available(url)
issues      = fetch_issues(url, project=project, branch=current_branch(), token=token)
by_file     = group_issues(issues, by="file")
by_severity = group_issues(issues, by="severity")
```

Only OPEN / CONFIRMED / REOPENED issues are returned. RESOLVED issues (false
positive / won't-fix) are excluded automatically.

## Recording Transitions

The MCP `change_sonar_issue_status` tool cannot attach rationale comments, so
record dispositions via the web API as a transition + comment pair:

```text
POST {url}/api/issues/do_transition   issue=<key>  transition=accept|falsepositive|reopen
POST {url}/api/issues/add_comment     issue=<key>  text=<rationale: rule ref + why N/A>
```

Auth: HTTP Basic with the token as username and an empty password.

**Token roles (the two `.env` tokens are not interchangeable):**

| Var | Role | Scan | Transition issues |
|---|---|---|---|
| `SONAR_TOKEN` | scanner auth, used by `scan.ps1` / `scan.sh` | yes | no |
| `SONARQUBE_TOKEN` | admin user token for issue administration | -- | yes |

If `do_transition` returns `403 Insufficient privileges`, the repo `.env`
`SONARQUBE_TOKEN` is stale or wrong-typed. The working admin user token lives
in the SonarQube service stack's own `.env` (the `redmark-sonarqube` folder
under the sibling `services/` directory, next to this repo's parent) — copy it
into this repo's `.env` and retry. Do not ask the user to transition manually,
do not grant new SonarQube permissions, and do not create new tokens: the
credential already exists there.

## Procedure

Run: [`procedures/sonarqube-review.md`](procedures/sonarqube-review.md)

Steps: availability recheck → retrieve issues (MCP primary, Python fallback) →
group by file and severity → triage loop → record false positives → re-run to
verify.

## Offline Contract

When SonarQube is unreachable, Step 0 must:

- Exit with code 1 via `SystemExit`.
- Message: `SonarQube is not available at <url>: <reason>. Start the local stack …`
- Never reach issue retrieval or display a triage list.

Verified by:
`tests/.agents/tools/sonar_scan/test_offline_acceptance.py::TestReviewStep0Offline`

## Common Mistakes

| Mistake | Fix |
|---|---|
| Retrieving issues before CE task finishes | Always confirm `SUCCESS` first |
| Marking false positive by editing local files | Transition the issue status in SonarQube (`falsepositive` / `wontfix`) |
| Treating an empty result as "clean" when the instance is down | `ensure_available` must pass before any retrieval |
| Loading `.env` from Python or defaulting env vars | Assume the caller configured the environment (AGENTS.md); use `os.environ["VAR"]` -- no `load_dotenv`, no defaults. `sonar_scan` rewrites `host.docker.internal` -> `localhost` internally |
