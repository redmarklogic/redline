---
name: sonarqube-find-and-fix
description: Use when running the end-to-end SonarQube find-and-fix cycle for the current branch — from scan trigger through triage, fix, false-positive recording, shift-left prevention, and re-scan verification.
---

# SonarQube Find and Fix

Orchestrates the SonarQube quality-gate sequence for the current branch. Wraps
the scan sub-skills in a triage → reproduce → fix → prevent loop so findings are
fixed at the root, false positives are recorded with rationale, and detection
shifts left over time.

**Boundary contract:**

- **Input**: a checked-out branch; all sub-skill prerequisites met.
- **Output**: branch confirmed clean — every finding fixed, or transitioned to
  RESOLVED (false positive / won't fix) with rationale; re-scan verified;
  prevention candidates captured for critical/repeat findings.
- **Out of scope**: linting, type-check, and coverage-threshold gates; PR review
  (`resolving-pr-issues`); merge/branch decisions.

## Gates (in order)

| # | Gate | Purpose |
|---|---|---|
| 0 | scan-script health | Parse/lint `scan.ps1` / `scan.sh` before relying on them — `check-script-encoding` + a parse check |
| 1 | `sonarqube-scan` | Static analysis — trigger scan, wait for `SUCCESS` |
| 2 | `sonarqube-review` | Retrieve issues, group, transition false positives |

Each sub-skill owns its guards and error handling — surface failures verbatim;
never swallow them here.

## Triage schema (quick reference)

Tag every retrieved issue before editing any file. Tags scope which gates are
mandatory.

| Tag | Values (SonarQube → tag) |
|---|---|
| **Decision** | `agree` (fix) · `disagree` (false positive / won't fix) |
| **Priority** | `critical` (BLOCKER, CRITICAL) · `standard` (MAJOR) · `low` (MINOR, INFO) |
| **Type** | `behavioral` (BUG, VULNERABILITY) · `maintainability` (CODE_SMELL, complexity, duplication) · `hotspot` (SECURITY_HOTSPOT) |

Reproduce gate and fail-first test apply to **`behavioral` Type only**.
Maintainability findings are self-evident static facts — fix directly.

**Class vs instance.** A finding that belongs to a whole out-of-scope *class*
(test fixtures, captured third-party assets, generated code) is excluded at the
SSOT scan scope (`sonar.exclusions` / `sonar.test.exclusions` in
`[tool.usethis]`), not marked false positive one issue at a time. Reserve
per-issue `falsepositive` / `wontfix` for genuine one-offs (procedure Step 6).

## Procedure

Steps: script-health → scan → retrieve → triage → reproduce (behavioral) → fix →
record false positives with rationale → prevent (shift-left) → re-scan verify →
closure.

## Common Mistakes

| Mistake | Correct behaviour |
|---|---|
| Fixing a `behavioral` finding without reproducing it | Reproduce locally first — unreproducible is a false-positive signal, not a fix target |
| Writing a fail-first test for every finding | Tests scope to `behavioral` Type only; smells / complexity / duplication are self-evident — fix directly |
| Marking a false positive with no rationale | Attach a justification to the SonarQube transition (rule ref + why N/A) — never a bare transition, never a local-file edit |
| Marking each finding in an out-of-scope class as a false positive | Exclude the class at the SSOT scan scope (`sonar.exclusions` / `sonar.test.exclusions`) — per-issue FP recurs on new files and does not survive key churn |
| Trusting an FP transition without re-scanning | FP-persistence (FR-025) is not guaranteed across issue-key churn — re-scan and confirm the finding does not re-surface |
| One-off fixing what a linter could catch | Push left — record a ruff-rule / hook candidate so it never reaches the scan again |
| Treating the re-scan as optional | Re-scan after fixes; confirm fixed issues are gone and false positives do not re-surface |
| "No BLOCKER/CRITICAL" = ready | Ready = behavioral fixed + tested, false positives recorded with rationale, re-scan clean, prevention captured |
