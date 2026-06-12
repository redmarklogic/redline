# Procedure: Suggest

Agent drafts the goal from project state; founder confirms. Internal file of `agile-sprint-planning` — not independently dispatchable. On completion, continue to `procedures/commit.md`.

## 1 — Capacity (yesterday's weather)

Count last sprint's Done tasks (`github-projects` → list-tasks, sprint = N−1, status Done; or read `this-week.md` if current). Capacity = that count, exactly — the best predictor of this iteration is the last one (*Clean Agile*). Sprint 1 with no history: default 5 (Redline convention).

State it: "Last sprint you completed X tasks. Planning for X." Do not inflate for optimism, deflate for pessimism, or split the difference when pushed — a number in between is still optimism.

## 2 — Read the backlog

`github-projects` → list-tasks (status Backlog). Consider tasks with no sprint assigned plus any already marked for Sprint N.

## 3 — Strategic context

Read `strategic-bets.md` (active bets) and `okrs/2026-h2.md` (active KRs). Map each candidate task to a bet/KR. No link → flag as misaligned; selectable only as a dependency of a bet-linked task, with the link stated.

## 4 — Readiness filter

Apply the INVEST table in SKILL.md to every candidate. Estimable or Testable failures do not enter the sprint unfixed. State which tasks were excluded and why.

## 5 — Draft the sprint goal

One sentence. One goal per sprint (*Sprint*, Knapp — the goal is the measuring stick). It must:

- name what is **deployable or demonstrable** at sprint end (a state, not an activity)
- link to an active bet by name
- be falsifiable — true or false on the last day, no partial credit (bar per `pm-hypothesis-builder`)

Bad: "Continue working on the infra chain." Good: "Skeleton API deployed to Cloud Run staging with green CI, proving Bet 1 is deployable."

If no single sentence covers all candidate tasks, the sprint is over-scoped — drop tasks until it does.

**Hard Gate 1:** present goal + candidate list; founder confirms before anything is written. Then → `procedures/commit.md`.
