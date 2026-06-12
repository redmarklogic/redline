# Reference: plan and table formats

Internal file of `agile-sprint-planning`. Formats only — rules live in SKILL.md and the procedures.

## WBS table (the single task-table format — used in-session and in the plan document)

```text
| #   | Task / Sub-task        | Agent    | Done when / Description                          | Risk |
|-----|------------------------|----------|--------------------------------------------------|------|
| 1   | **Parent task name**   | DevOps   | One-line parent outcome                          | Med  |
| 1.1 | — Sub-task name        | DevOps   | What it produces — done when curl returns 200    | Low  |
| 1.2 | — Sub-task name        | PrincEng | What it produces — [agent] implements            | High |
```

Rules: parents bold, sub-tasks plain with leading dash and dot numbering; every parent has ≥ 1 row whose description ends in an observable done-when (browser/CLI-visible); Risk = High/Med/Low; no Days column (sequencing lives in the Gantt); same task numbers in Gantt and table.

## Gantt block (sequencing confirmation, Lead mode)

```text
          Mon            Tue            Wed            Thu            Fri
──────────────────────────────────────────────────────────────────────────────
  1       [Task name] ── [Task name] ── ...

  2       [Task name] ─────────────────────────────────────────────────────────
                                            │
  3                                         └──────── [Task name] ── [Task name]
```

Task names 2–3 words so they fit the blocks; single-day tasks name the day once (not "Thu – Thu"); parallel tracks on separate rows; blank line between the Gantt block and the task table. Rendered Mermaid diagrams (plan document only) follow `mermaid-diagrams`.

## `sprint-<N>-goal.md` template

```markdown
# Sprint [N] Plan — [date range]

**Status**: Active. **Owner**: Founder.
**Generated**: [date]

---

## Sprint Goal

> [One sentence. Deployable or demonstrable. Linked to a bet. Falsifiable.]

**Success looks like**: [2–3 concrete sentences]
**Failure looks like**: [the specific signal the goal was not met]
**Failure tripwire (verbatim)**: "If by [day N] we have not seen [X], we will [stop / change course]."

**Bet**: [name from strategic-bets.md]
**OKR**: [KR this sprint feeds]

---

## Capacity

Last sprint completed: [N] tasks (yesterday's weather)
This sprint planning for: [N] tasks [+ reason if held below ceiling]

---

## Committed Tasks — WBS

[WBS table, execution order]

**Dependency order**: [one-sentence execution sequence, or "all tasks are independent"]

[Dependency diagram per mermaid-diagrams — only if real dependencies exist]

---

## Explicitly Out of Scope

| Task | Deferred to | Reason |
|---|---|---|
| [title] | Sprint [N+1] / Backlog | [one sentence] |
[≥ 3 rows]

---

## Sprint Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|

---

## Kickoff Checklist

- [ ] Goal + task list confirmed by founder (Hard Gate 1)
- [ ] **[BLOCKING]** Close gate passed (Hard Gate 4): item count == WBS level-1 count; Sprint field on all; dependencies written via set-dependencies; every level-2 row linked as a sub-issue (mirror rule)
- [ ] Out-of-scope list ≥ 3 (Hard Gate 3)
- [ ] this-week.md regenerated
- [ ] Every prerequisite task Done or committed this sprint
- [ ] Shaping session scheduled for any task flagged unestimable
```
