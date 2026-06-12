# Procedure: Commit (shared backbone — both modes end here)

Selection → out-of-scope → sequencing → risks → board materialization → plan document → this-week. Internal file of `agile-sprint-planning` — not independently dispatchable. **The ceremony is open until Hard Gate 4 (SKILL.md) passes.**

All board operations use `github-projects` procedures by name; their guards (G1–G7) apply. State each write to the founder before executing it (Hard Gate 1).

## 1 — Select committed tasks (≤ capacity)

Order: dependencies of the primary goal task → the primary goal task → secondary tasks sharing the goal's bet → foundational tasks that unblock future sprints → stop at capacity. Write a "done when" for any selected task missing one (INVEST-Testable).

## 2 — Out-of-scope (Hard Gate 3)

Name ≥ 3 backlog tasks NOT committed, each with a one-sentence reason. Scope grows like grass (*Shape Up*); requirements are immutable once the iteration begins (*Clean Agile*) — unnamed tasks are implicitly "maybe this sprint". The table doubles as the ranked pull-order: if the sprint clears early, pull the top row — never inflate the committed count up front. If the founder explicitly says "defer X", apply `task-defer` (its rule: never proactively).

## 3 — Sequencing view

Identify the dependency chain and parallel-safe tasks across committed work. If real dependencies exist, render a dependency diagram per `mermaid-diagrams` (flowchart LR); if all tasks are independent, say so and skip the diagram.

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

**5b — Create/update items (WBS mirror rule — founder ruling 2026-06-12).** The board mirrors the WBS exactly. Every **level-1** WBS row is a parent board item: `github-projects` → create-task / update-task. Title = WBS task name; body = agent, description, done-criteria; exactly one type label from the canonical set in `github-projects` (retrieve the set there — never recall it). Every **level-2** WBS row becomes a native sub-issue of its parent: `github-projects` → set-parent. Ceremony WBS rows are exempt from the Structuring Doctrine's promote/keep test — see that doctrine's sprint-planning exception.

**5c — Sprint field.** `github-projects` → update-task: Sprint = "Sprint N - [dates]" on every committed item.

**5d — Dependencies.** For every committed task with a predecessor: `github-projects` → **set-dependencies** (native issue dependencies — the legacy `depends_on`/`blocked_by` text fields are deprecated there; leave them blank). The standup's dependency diagram reads the board, not the plan doc — dependencies identified but not written = incomplete ceremony.

**5e — Close gate (Hard Gate 4, blocking).** Verify via `github-projects` → list-tasks:

1. items for Sprint N == WBS level-1 row count — if not, create the missing rows now;
2. Sprint field set on all;
3. every identified predecessor written (5d);
4. every level-2 WBS row exists as a sub-issue linked to its parent (mirror rule).

## 6 — Plan document

Write `docs/product/tasks/sprint-<N>-goal.md` per `reference/plan-format.md`, including the kickoff checklist with gate confirmations and the failure tripwire verbatim.

## 7 — Regenerate this-week

`github-projects` → sync-this-week (procedure 10). Then state to the founder: ceremony closed, gates passed, next action and owner.
