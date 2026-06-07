---
name: sonarqube-scan
description: Use to trigger a SonarQube static analysis scan on the current branch and wait for the compute-engine task to succeed before retrieving results
---

# SonarQube Scan

Trigger a static analysis scan of the currently checked-out branch against the
local SonarQube instance and wait until the background task completes.

**Boundary contract:**

- **Input**: `SONAR_TOKEN` in untracked `.env` (only mandatory secret); scan
  scope and exclusions from `pyproject.toml` `[tool.usethis]` (SSOT — do not
  edit `sonar-project.properties` directly; it is generated at scan time).
- **Output**: confirmed `SUCCESS` status from the SonarQube compute-engine task,
  or a typed `SonarQubeUnavailableError` / `TimeoutError` surfaced with
  remediation.

**Composable.** Called standalone, or as one step in a larger local quality gate.

## Inputs

| Input | Source | Required |
|---|---|---|
| `SONAR_TOKEN` | `.env` | **Yes** |
| `SONAR_HOST_URL` | `.env` | No — defaults to `http://host.docker.internal:9000` |
| `SONAR_PROJECT_KEY` | `.env` | No — defaults to `redline` |
| Scan scope / exclusions | `pyproject.toml` `[tool.usethis]` | Configured in repo |
| Current branch | `git rev-parse --abbrev-ref HEAD` | Derived automatically |

## Prerequisites

| # | Requirement | Check |
|---|---|---|
| P1 | Local stack running | `curl http://localhost:9000/api/system/status` → `{"status":"UP"}` |
| P2 | `.env` present with `SONAR_TOKEN` | `Test-Path .env`; token non-empty |
| P3 | Branch is not detached `HEAD` | `git rev-parse --abbrev-ref HEAD` → not `HEAD` |

## Guard Conditions

| # | Condition |
|---|---|
| G1 | Instance reachable and UP — checked before running scanner |
| G2 | `SONAR_TOKEN` non-empty — checked before running scanner |
| G3 | Branch is not detached `HEAD` |
| G4 | Any availability failure → `SonarQubeUnavailableError` surfaced; never a silent pass |

## Procedure

Run: [`procedures/sonarqube-scan.md`](procedures/sonarqube-scan.md)

Steps: availability check → run `scan.ps1` / `scan.sh` → poll compute-engine
task (bounded, max ~60 s) → confirm `SUCCESS`.

## Offline Contract

When SonarQube is unreachable, `scan.ps1` must:

- Exit with code 1.
- Print to stderr: `SonarQube is not available at <url>: <reason>. Start the local stack …`
- Never proceed to run the scanner container or poll the CE task.

`scan.ps1` delegates its availability gate to `sonar_scan.healthcheck` (line 51), so this
contract is verified by:
`tests/.agents/tools/sonar_scan/test_offline_acceptance.py::TestHealthcheckCliOffline`

## Common Mistakes

| Mistake | Fix |
|---|---|
| Skipping availability check | Always call `ensure_available` first; let the error propagate |
| Polling with no timeout | Bounded wait only (max ~60 s); on timeout surface the task URL and stop |
| Proceeding when task status is not `SUCCESS` | Only advance to the review step after confirmed `SUCCESS` |
| Ruff report has Windows paths, scanner runs in Linux container | `WARN Failed to resolve 1 file path(s) in Ruff report` — ruff issues silently not imported | Known cross-platform limitation; scan succeeds but ruff findings are absent from SonarQube |
