# Procedure: Commit (shared backbone — both modes end here)

Selection → out-of-scope → sequencing → risks → board materialization → plan document → this-week. Internal file of `agile-sprint-planning` — not independently dispatchable. **The ceremony is open until Hard Gate 4 (SKILL.md) passes.**

All board operations use `github-projects` procedures by name; their guards (G1–G7) apply. State each write to the founder before executing it (Hard Gate 1).

## 1 — Select committed tasks (≤ capacity)

Order: dependencies of the primary goal task → the primary goal task → secondary tasks sharing the goal's bet → foundational tasks that unblock future sprints → stop at capacity. Write a "done when" for any selected task missing one (INVEST-Testable).

## 2 — Out-of-scope (Hard Gate 3)

Name ≥ 3 backlog tasks NOT committed, each with a one-sentence reason. Scope grows like grass (*Shape Up*); requirements are immutable once the iteration begins (*Clean Agile*) — unnamed tasks are implicitly "maybe this sprint". The table doubles as the ranked pull-order: if the sprint clears early, pull the top row — never inflate the committed count up front. If the founder explicitly says "defer X", apply `task-defer` (its rule: never proactively).

## 3 — Sequencing & schedule

Identify the dependency chain and parallel-safe tasks across committed work. If real dependencies exist, render a dependency diagram per `mermaid-diagrams` (flowchart LR); if all tasks are independent, say so and skip the diagram.

Then lay the work on the sprint calendar — this drives the roadmap, so it is mandatory, not decorative:

- **Duration.** Give every committed task a duration in **working days** (risk-weighted: Low/Med = 1 day, High = 2; anything > 2 fails INVEST-Small — split it). The board has no estimate field — duration is expressed only as the Start→Target span, so the roadmap bar width *is* the estimate.
- **Dates.** Walk the dependency order and assign `start_date` / `target_date` inside the sprint's working window (Mon–Fri; weekend = buffer): a successor's `start_date` ≥ every predecessor's `target_date`; parallel-safe tasks overlap (same days, a different track); a single-day task has `start_date == target_date`; keep any tripwire task's `target_date` on the tripwire day. A parent spans its children (min start → max target).
- **Never leave tasks at the full sprint span.** Uniform dates render every roadmap bar the full week wide — the exact failure this step exists to prevent. Distinct, dependency-ordered dates are what let the founder read execution order (left→right), duration (bar width), and parallelism (stacked rows) straight off the roadmap.

Record the result as the Schedule table (`reference/plan-format.md`); the Gantt block is its ASCII preview. These dates are written to the board in 5c.

## 4 — Sprint risks

For each committed task, assess: what if its predecessor slips?

| Pattern | Mitigation |
|---|---|
| Critical path, no buffer | Riskiest task first, not last |
| No prior art (novel) | Extra time; mark high-risk in the plan |
| External gate (approval, third party) | Name a parallel task to run while waiting |
| Unshaped (no spec/Pitch) | Remove; route to `shaping` (INVEST-Estimable) |

## 5 — Board materialization

**5a — Reconcile against existing items.** For each WBS level-1 row, scan the backlog for an existing non-Done issue covering the same problem. Match → update its title, body, done-criteria to the agreed scope (board cultivation — history and links are preserved; stale scope is not). No match → create.

**5b — Create/update items (WBS mirror rule — founder ruling 2026-06-12).** The board mirrors the WBS exactly. Every **level-1** WBS row is a parent board item: `github-projects` → create-task / update-task. Title = WBS task name; **body = the full template in `reference/task-content.md`** (problem/context, solution outline, Given/When/Then acceptance criteria — agent-verifiable where possible, appetite, rabbit holes, no-gos, agents, source) — the auto-generated create-task body is the floor, not the standard; exactly one type label from the canonical set in `github-projects` (retrieve the set there — never recall it). Every **level-2** WBS row becomes a native sub-issue of its parent: `github-projects` → set-parent. Ceremony WBS rows are exempt from the Structuring Doctrine's promote/keep test — see that doctrine's sprint-planning exception.

**5c — Sprint field + schedule dates.** `github-projects` → update-task on every committed item: Sprint = "Sprint N - [dates]"; **Start date / Target date = the per-task values from the schedule (step 3)** — never the uniform sprint span. The roadmap positions and sizes each bar from these two date fields; the Sprint iteration field alone renders every bar the full week. Items created in 5b already carry their schedule dates via `create-task` (both are mandatory on `TaskCreate`); this step sets the dates on reconciled/existing items and the Sprint field on all.

**5d — Dependencies.** For every committed task with a predecessor: `github-projects` → **set-dependencies** (native issue dependencies — the legacy `depends_on`/`blocked_by` text fields are deprecated there; leave them blank). The standup's dependency diagram reads the board, not the plan doc — dependencies identified but not written = incomplete ceremony.

**5e — Close gate (Hard Gate 4, blocking).** Verify via `github-projects` → list-tasks:

1. items for Sprint N == WBS level-1 row count — if not, create the missing rows now;
2. Sprint field set on all;
3. every identified predecessor written (5d);
4. every level-2 WBS row exists as a sub-issue linked to its parent (mirror rule);
5. Start date / Target date set on every item from the schedule (5c), `start ≤ target`, and **not all identical to the sprint window** — uniform dates are the bar-spans-the-whole-week bug.

If, with dates set, the roadmap still renders full-week bars, the Roadmap **view** is positioned by the Sprint iteration field — reconfigure it once to **Start date → Target date** per `github-projects` (Roadmap view setup; not API-scriptable).

## 6 — Plan document

Write `docs/product/tasks/sprint-<N>-goal.md` per `reference/plan-format.md`, including the kickoff checklist with gate confirmations and the failure tripwire verbatim.

## 7 — Regenerate this-week

`github-projects` → sync-this-week (procedure 10). Then state to the founder: ceremony closed, gates passed, next action and owner.
