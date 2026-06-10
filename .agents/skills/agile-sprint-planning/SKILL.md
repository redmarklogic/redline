---
name: agile-sprint-planning
description: Use at the start of each new sprint to set a sprint goal, select tasks from the backlog, sequence them by risk, identify dependencies and parallelism, and output a sprint plan. Reads the GitHub Projects board and strategic bets. Writes sprint goal to docs/product/tasks/ and assigns sprint field on selected tasks.
---

# Agile Sprint Planning

## What This Is

A sprint planning ceremony for a solo founder. Runs at the beginning of each sprint
(Monday morning, before any work starts). Takes 20-30 minutes.

**Output**: a sprint goal, a committed task list, an explicit out-of-scope list, and
the sprint plan written to `docs/product/tasks/sprint-<N>-goal.md`. Selected tasks
have their Sprint field updated on the GitHub Projects board.

## Why Sprint Planning Matters

*Written for someone unfamiliar with agile planning — skip if you already know
the literature.*

Without a sprint goal, every task feels equally important and you start everything
at once, finishing nothing. Sprint planning forces three decisions that make the week
tractable:

1. **What does success look like on Sunday?** — A one-sentence goal makes "done"
   unambiguous. Without it, you can work all week and still feel behind.

2. **What are we NOT doing this sprint?** — Explicitly naming out-of-scope items
   prevents creep. Work that is not named as out-of-scope will get pulled in.

3. **What must happen before what?** — Dependencies determine the execution order.
   Starting a task whose prerequisite isn't done yet is wasted effort.

**Yesterday's Weather (XP)**: The best predictor of how much work you can finish
this sprint is how much you finished last sprint. Do not plan based on optimism —
plan based on your actual recent throughput.

**INVEST criteria**: Before a task can enter a sprint, it should be:
- **I**ndependent — can be worked without waiting for another task (except known deps)
- **N**egotiable — scope can flex; it is not a contract
- **V**aluable — delivers something the product or bet needs
- **E**stimable — clear enough to judge if it fits in one sprint
- **S**mall — one person, one sprint. If it can't fit, split it.
- **T**estable — you can describe what "done" looks like

**Feasibility before planning (Inspired by Marty Cagan)**: Tasks that no one has
thought through technically should not enter sprint planning. They belong in a design
or spike session first. Bringing an unresearched task to planning produces
conservative estimates and wastes the session. If a task in the backlog has not been
shaped (no Peter Pitch, no spec), flag it and push it back to shaping.

## Boundary Contract

### Inputs

- GitHub Projects board backlog (live, via `github-projects` → `list-tasks`)
- Last sprint's Done count (yesterday's weather capacity estimate)
- `docs/product/strategy/strategic-bets.md` (active bets — the goal must link to one)
- `docs/product/strategy/okrs/2026-h2.md` (OKR ladder — which KR does this sprint feed?)
- `docs/product/operations/cadences.md` (sprint dates, conventions)
- All open specs in `specs/NNN-*/spec.md` (for task descriptions and done criteria)
- `docs/product/tasks/this-week.md` if it exists (last sprint's state)

### Outputs

- `docs/product/tasks/sprint-<N>-goal.md` — sprint goal, committed tasks, out-of-scope,
  risks, and dependency diagram
- GitHub Projects board: Sprint field set on all committed tasks
- `docs/product/tasks/this-week.md` — regenerated for the new sprint

### Does Not Cover

- Creating new tasks (use `github-projects` → `create-task`)
- Shaping unrefined tasks (use `shaping` skill + Peter)
- Retrospective on the previous sprint (use `session-retro`)

## Steward

Mark (PM), with Peter consulted for feasibility on any task that hasn't been shaped.
Founder makes the final call on goal and scope. No task enters the sprint without
founder confirmation.

## Prerequisites

- G1: `gh auth status` lists `project` scope
- G2: `project_config.json` exists and is <= 24 h old
- G3: Strategic bets file exists and has at least one active bet

## Workflow

### Step 1 — Determine capacity (yesterday's weather)

Read `docs/product/tasks/this-week.md` or query Done tasks from the previous sprint:

```python
done_last_sprint = list_tasks(config, sprint="Sprint N-1 ...", status="Done")
capacity = len(done_last_sprint)  # tasks completed last sprint
```

If this is Sprint 1 (no prior sprint), use a conservative default of 5 tasks.
State the capacity figure explicitly: "Last sprint you completed X tasks. Planning
for X tasks this sprint."

Do not inflate capacity based on optimism. Do not deflate it based on pessimism.
Use the number.

### Step 2 — Read the backlog

```python
backlog = list_tasks(config, status="Backlog")
```

Filter to tasks with no sprint assigned (unscheduled backlog) plus any tasks
explicitly marked for this sprint already.

### Step 3 — Read strategic context

- Read `docs/product/strategy/strategic-bets.md` → identify active bets
- Read `docs/product/strategy/okrs/2026-h2.md` → identify which KRs are active
- Identify which backlog tasks connect to active bets and KRs

Flag any backlog task with no bet link as misaligned. It can still be selected if
it is a dependency for a bet-linked task (infra, tooling, etc.) but the lack of
direct bet link should be stated.

### Step 4 — Check task readiness (INVEST filter)

For each backlog task being considered, apply the INVEST check:

| Criterion | Check |
|---|---|
| Independent | Does it have `depends_on` pointing to an unfinished task? If yes, sequence it correctly or defer it. |
| Valuable | Does it link to an active bet or OKR? If not, flag. |
| Estimable | Is there a spec or design? If the task has no `source` field and no spec, it is likely unestimable — push to shaping. |
| Small | Can it fit in one sprint? If uncertain, split it. Per cadences.md: tasks MUST NOT cross sprint boundaries. |
| Testable | Is there a "done when" field or clear acceptance condition? If not, write one before committing. |

Tasks that fail Small or Testable should not enter the sprint without being fixed first.
State which tasks were excluded and why.

### Step 5 — Draft the sprint goal

The sprint goal is one sentence. It must:
- Name what will be *deployable or demonstrable* by sprint end (not "work on X")
- Link to an active strategic bet by name
- Be falsifiable: at sprint end, it is either true or false — no partial credit

Bad: "Continue working on the infra chain and make progress on Cloud Run"
Good: "Deploy the skeleton API to Cloud Run staging with a green CI pipeline,
       proving Bet 1 is deployable"

If no single sentence covers all committed tasks, the sprint is over-scoped — remove
tasks until the goal is coherent.

Ask the founder to confirm the goal before proceeding. Do not write the plan document
without confirmation.

### Step 6 — Select committed tasks

Select tasks from the backlog up to the capacity number. Apply this ordering:

1. Dependencies of the primary goal task first (nothing else can move without them)
2. The primary goal task
3. Secondary tasks that share the sprint goal's bet
4. Foundational tasks (infra, tooling) that unblock future sprints
5. Stop at capacity

Name the tasks explicitly. For each selected task, write a "done when" statement if
one is missing.

### Step 7 — Name out-of-scope tasks

List at least 3 backlog tasks that are NOT being committed to this sprint. Name them
explicitly with one sentence explaining why each is deferred.

This step is mandatory. Unnamed out-of-scope items get pulled in during the sprint.

### Step 8 — Build the dependency and sequencing view

Identify the dependency chain across committed tasks. Identify which tasks can run
in parallel (no shared dependency). This informs the execution order for daily standups.

Generate a dependency diagram using `mermaid-diagrams` → flowchart LR only if there
are actual dependencies. If all tasks are independent, state that and skip the diagram.

### Step 9 — Identify sprint risks

For each committed task with a `depends_on` pointing to another committed task,
assess: what happens if the dependency slips?

| Risk pattern | Mitigation |
|---|---|
| Critical path with no buffer | Schedule the riskiest task first, not last |
| Task has no prior art (novel) | Allow extra time; note it as high-risk in the plan |
| Task depends on external gate (approval, third party) | Identify a parallel task to run while waiting |
| Task was not shaped (no spec, no Pitch) | Remove from sprint; send to shaping |

### Step 10 — Write the plan document

Write `docs/product/tasks/sprint-<N>-goal.md`. See Output Format below.

### Step 11 — Update the board

For each committed task:
```python
update = TaskUpdate(item_id="...", sprint="Sprint N - [dates]")
result = update_task(update, config)
```

Confirm updates with the founder before writing. Log any failures.

### Step 12 — Regenerate this-week.md

Run `sync-this-week` (procedure 10 in `github-projects`) to write the fresh
`docs/product/tasks/this-week.md` for the new sprint.

---

## Output Format — sprint-<N>-goal.md

```markdown
# Sprint [N] Plan — [date range]

**Status**: Active. **Owner**: Founder.
**Generated**: [date]

---

## Sprint Goal

> [One sentence. Deployable or demonstrable. Linked to a bet. Falsifiable.]

**Success looks like**: [Two or three sentences — what a passing sprint looks like concretely]
**Failure looks like**: [One sentence — the specific signal that the goal was not met]

**Bet**: [bet name from strategic-bets.md]
**OKR**: [KR this sprint feeds — e.g. KR1: 50 verified signups by Sep 1]

---

## Capacity

Last sprint completed: [N] tasks (yesterday's weather)
This sprint planning for: [N] tasks

---

## Committed Tasks

Tasks the founder is committing to complete this sprint. Ordered by execution sequence.

| # | Title | Done when | Risk | Agent |
|---|---|---|---|---|
| 1 | [title] | [done criteria] | High / Med / Low | [agent] |
| ... |

**Dependency order**: [text description of the execution sequence, or "all tasks are independent"]

[Dependency diagram if applicable — flowchart LR, Mermaid <= 8.8.0]

---

## Explicitly Out of Scope

These tasks are NOT being done this sprint. Named to protect the sprint from creep.

| Task | Deferred to | Reason |
|---|---|---|
| [title] | Sprint [N+1] / Backlog | [one sentence why not now] |
| ... |

---

## Sprint Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| [what could derail this sprint] | High / Med / Low | High / Med / Low | [specific action] |

---

## Kickoff Checklist

- [ ] Sprint goal confirmed with founder
- [ ] Board sprint field updated for all committed tasks
- [ ] this-week.md regenerated
- [ ] Dependencies verified: all prerequisite tasks either Done or committed this sprint
- [ ] At least one shaping session scheduled for any task flagged as unestimable
```

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| Sprint goal that cannot be falsified ("work on Cloud Run") | Goal must be a state at sprint end — "API deployed to staging" not "work on deployment" |
| Planning more tasks than last sprint's capacity | Yesterday's weather is the ceiling. Optimism is not velocity. |
| Bringing an unresearched task to planning | Tasks without a spec or Pitch belong in shaping, not planning. Flag and defer. |
| Skipping the out-of-scope list | Every unnamed task is implicitly "maybe this sprint." Name them out. |
| Setting sprint field without founder confirmation | Board changes are visible to the project. Confirm before writing. |
| Sprint goal that doesn't link to a bet | No bet link = no strategic rationale. Stop and ask which bet this serves. |
| Tasks that cross sprint boundary | Split before committing. A task that cannot fit in one sprint must become two tasks. |
