# Procedure: pre-pr-checks

Orchestrates the full local quality gate for the current branch. See
`pre-pr-checks/SKILL.md` for the triage schema, gates table, and Common Mistakes.
Each sub-skill carries its own guard conditions — surface failures verbatim; do
not swallow them here.

## Step 0 — Scan-script health (fail loud, fail early)

The orchestrator runs `scan.ps1` / `scan.sh`; validate them before the scan so a
broken script fails here, not mid-run (`scan.ps1` once parse-failed on a stray
non-ASCII character under Windows PowerShell 5.1).

- Encoding / 5.1-safety: `uv run prek run check-script-encoding --all-files`.
- PowerShell parse (no execution):

  ```powershell
  $e = $null
  [System.Management.Automation.Language.Parser]::ParseFile(
      (Resolve-Path ./scan.ps1).Path, [ref]$null, [ref]$e) | Out-Null
  if ($e) { $e; throw 'scan.ps1 has parse errors' }
  ```

- Shell parse (no execution): `bash -n scan.sh`.

Any failure is a hard stop — fix the script before scanning.

## Step 1 — Scan

Load and run `sonarqube-scan`. Stop on any failure.

## Step 2 — Retrieve

Load and run `sonarqube-review` to fetch and group issues (by file, by severity).
Stop on any failure.

## Step 3 — Triage gate

Tag every issue Decision × Priority × Type (schema in `SKILL.md`). Present the
table. Do not edit any file until all issues are tagged.

## Step 4 — Reproduce gate (`behavioral` only)

Demonstrate the finding in the current code before fixing. Cannot reproduce →
reclassify `disagree` → false positive (Step 6).

## Step 5 — Fix gate

- `behavioral`: write a fail-first test, confirm it fails for the right reason,
  then apply the minimal fix.
- `maintainability` / `hotspot`: minimal fix, no unrelated refactors.
- Re-run the fast local gate before continuing:

  ```powershell
  .\.venv\Scripts\activate; uv run prek run -a
  .\.venv\Scripts\activate; python -m pytest <impacted test files> -x
  ```

## Step 6 — Record false positives (class vs instance)

First decide whether the finding is one *instance* or a whole *class*:

- **Whole out-of-scope class** (test fixtures, captured third-party assets,
  generated code): do NOT flag issues one by one. Exclude the class at the SSOT
  scan scope — `[tool.usethis]` in `pyproject.toml`: `sonar.exclusions` for main
  sources, `sonar.test.exclusions` for test-scope files. Scope exclusion removes
  the whole class at the root, survives re-scans, and prevents recurrence on new
  files. (Example: 27 findings in `tests/assets/**` HTML fixtures cleared with one
  `sonar.test.exclusions` entry, not 27 transitions.)
- **Genuine one-off**: transition the issue in SonarQube via `sonarqube-review`
  (`falsepositive` / `wontfix`) with a **mandatory justification** (rule
  reference and why it does not apply here). Per `sonarqube-review` guard G3,
  disposition is recorded in SonarQube, never by editing local files. A bare
  transition is a defect — the next run must not re-triage from scratch.

**Verify persistence (FR-025).** Issue keys can churn between scans, so a
false-positive transition is not guaranteed to suppress the equivalent finding on
the next scan. After any disposition, re-scan (Step 8) and confirm the finding
does not re-surface; if it does, prefer scope exclusion.

## Step 7 — Prevent gate (critical / repeat findings)

Capture the durable fix:

- Automation candidate per the shift-left ladder below.
- For critical or repeat-type defects, record a lesson in `docs/lessons/`
  (`lesson_template.md`) with a 5-Whys.

### Automation Capture Priority (shift-left)

The durable fix is the rule, not the one-off edit. Record as a follow-up;
implement mid-cycle only if critical and under 15 minutes without touching
application code.

1. **Enable a ruff rule** — `ruff rule <CODE>`; add to `extend-select` in `pyproject.toml`.
2. **Add a community pre-commit hook** — pre-commit hook catalog (`https://pre-commit.com/hooks.html`).
3. **Extend an existing `hooks/` script** — add a case to a domain-specific hook.
4. **Write a new local hook** — last resort.

## Step 8 — Verify

Re-run `sonarqube-scan`. Confirm fixed issues are gone and recorded false
positives do not re-surface.

## Step 9 — Closure (all must be true)

- [ ] No unresolved BLOCKER or CRITICAL
- [ ] Behavioral findings fixed with a fail-first test
- [ ] False positives transitioned with rationale
- [ ] Re-scan clean
- [ ] Prevention candidates captured for critical/repeat findings
