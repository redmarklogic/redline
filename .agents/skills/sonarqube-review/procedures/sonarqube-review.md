# Procedure: sonarqube-review

Retrieve issues for the current branch, triage them, and record dispositions in
SonarQube. Prerequisite: `sonarqube-scan` completed with `SUCCESS`.

## Step 0 — Setup and availability recheck

```python
import os
from sonar_scan import ensure_available, current_branch, fetch_issues, fetch_metrics, group_issues

# Environment is configured by the caller (scan scripts export .env; CI sets the
# job env). Per AGENTS.md: no Python .env loaders, no env-var defaults.
# _normalise_url runs inside every sonar_scan function, so pass SONARQUBE_URL raw.
url     = os.environ["SONARQUBE_URL"]
project = os.environ["SONAR_PROJECT_KEY"]
token   = os.environ["SONAR_TOKEN"]

try:
    ensure_available(url)
except SonarQubeUnavailableError as exc:
    raise SystemExit(str(exc)) from None
```

## Step 1 — Retrieve issues

Primary path — `mcp/sonarqube` MCP (registered in `.mcp.json`): ask for
issues filtered by `project=$SONAR_PROJECT_KEY` and the current branch.

Fallback (no MCP runtime, e.g. CI or tests):

```python
from sonar_scan import current_branch, fetch_issues
issues = fetch_issues(url, project=project, branch=current_branch(), token=token)
```

Both return the same open set (rule, severity, file, line, message, status).

## Step 2 — Group for triage

```python
from sonar_scan import group_issues
by_file     = group_issues(issues, by="file")
by_severity = group_issues(issues, by="severity")
```

Present both: per-file list (fix one file at a time) and severity rollup
(BLOCKER / CRITICAL / MAJOR / MINOR / INFO counts).

## Step 3 — Triage loop

For each issue decide:

1. **Fix** — real defect; note file:line for the developer.
2. **False positive** — not a real problem in this context; record (Step 4).
3. **Won't fix** — real but accepted; record (Step 4).

## Step 4 — Record false positives

Transition the issue status **in SonarQube** — never by editing local files.

Use the MCP issue-status tool, or:

```http
POST /api/issues/do_transition
  issue=<issueKey>
  transition=falsepositive   # or: wontfix
```

The issue moves to RESOLVED and is excluded from all future retrievals.

## Step 5 — Retrieve and review metrics

```python
metrics = fetch_metrics(url, project=project, branch=current_branch(), token=token)
```

Present the following gates. Flag any that warrant attention before the PR:

| Metric | Key | Gate |
| --- | --- | --- |
| Coverage | `coverage` | Drop vs main? Below team threshold? |
| Cyclomatic complexity | `complexity` | Spike in new code? |
| Cognitive complexity | `cognitive_complexity` | Unusually high for the branch? |
| Duplication density | `duplicated_lines_density` | > 0 on new code is a smell |
| Bugs / Vulnerabilities | `bugs`, `vulnerabilities` | Must be 0 before merge |
| Code smells | `code_smells` | Review alongside issues — same findings |
| Security hotspots | `security_hotspots` | Any > 0 requires review |

Metrics are informational — they do not block the triage loop, but a coverage
drop or duplication spike should be raised to the developer before the PR is
opened.

## Step 6 — Re-run to verify

After fixes and false-positive marking, trigger `sonarqube-scan` again.
Confirm:

- Fixed issues no longer appear.
- Issues marked false-positive / won't-fix do not re-surface.
- Remaining issues are genuinely new or still-open.
