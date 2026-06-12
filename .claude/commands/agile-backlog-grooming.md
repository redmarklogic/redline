# Agile — Backlog Grooming

Audit the GitHub Projects backlog and produce a per-row decision table for the
founder. Executes only founder-approved rows (verbal per row in session).

## What to do

Load and follow the `agile-backlog-grooming` skill at
`.agents/skills/agile-backlog-grooming/SKILL.md`.

Run the full workflow (Phases A–H). Present the decision table to the founder
before executing anything.

## Preflight checks (abort with a clear error if any fails)

1. `gh auth status` — must list `project` in scopes
2. `.agents/tools/github_projects/project_config.json` must exist and be ≤ 24 h old
3. `docs/product/strategy/strategic-bets.md` must have ≥ 1 active bet

## Critical rule

No issue is dropped, merged, re-parented, or updated until the founder explicitly
approves that row in session. No default-approval, no silence-as-consent.
