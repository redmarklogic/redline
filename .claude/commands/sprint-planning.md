# Sprint Planning

Run a sprint planning ceremony for the next sprint using the GitHub Projects backlog
and strategic bets.

## What to do

Load and follow the `agile-sprint-planning` skill at
`.agents/skills/agile-sprint-planning/SKILL.md`.

Run the full workflow (Steps 1–12) and present results before writing anything.

## Sequence

1. Run Steps 1–8 (capacity, backlog, context, INVEST filter, goal draft,
   task selection, out-of-scope, dependency view, risks).
2. Present the full draft sprint plan to the founder — goal, committed tasks,
   out-of-scope, risks.
3. **Wait for explicit confirmation before proceeding.**
4. On confirmation: write `docs/product/tasks/sprint-<N>-goal.md`, update board
   Sprint fields, regenerate `this-week.md`.

## Preflight checks (abort with clear error if either fails)

1. `gh auth status` — must list `project` in scopes
2. `.agents/tools/github_projects/project_config.json` must exist and be <= 24 h old
3. `docs/product/strategy/strategic-bets.md` must exist

## Sprint numbering

Detect the current sprint from `docs/product/operations/cadences.md` or from the
Sprint options in `project_config.json`. The next sprint is current + 1.

## Critical rule

Do not write files or update the board until the founder explicitly confirms the plan.
The sprint goal and committed task list are founder decisions — present, do not decide.
