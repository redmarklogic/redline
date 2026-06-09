Run the three-phase code review sequence below. Do not advance to the next phase until the current phase exits clean.

## Phase 1 — prek (static checks gate)

Load and apply the skill at `.agents/skills/prek-find-and-fix/SKILL.md`.

`rtk uv run prek run -a` must exit 0 before proceeding to Phase 2.

## Phase 2 — Tests (test-suite gate)

Load and apply the skill at `.agents/skills/test-find-and-fix/SKILL.md`.

`rtk uv run pytest` must exit 0 before proceeding to Phase 3.

## Phase 3 — SonarQube (deep analysis gate)

Load and apply the skill at `.agents/skills/sonarqube-find-and-fix/SKILL.md`.

## End-of-run Report

After all phases complete, output two tables.

### Violations found

One row per violation encountered across all phases, regardless of outcome.

| Phase | Hook / Rule | File | Line | Description | Decision |
|---|---|---|---|---|---|
| prek / tests / sonarqube | hook id, rule key, or test id | path | line or — | what the tool flagged | Fixed / Suppressed / xfail |

### Suppressed violations (calibration log)

One row per finding that was justified (not fixed). This table is the primary signal for linter calibration — false positives here indicate rules that are too aggressive or need scope exclusions.

| Phase | Hook / Rule | File | Rationale | Calibration signal |
|---|---|---|---|---|
| prek / tests / sonarqube | hook id, rule key, or test id | path | why the finding is inapplicable | Rule too broad / Out-of-scope path / Needs prek.toml exclusion / Needs sonar.exclusions / Genuine FP / xfail justified |

If all tables are empty, state: "No violations found in any phase."
