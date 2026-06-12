---
name: agile-sprint-planning
description: Use at the start of a new sprint, when the previous sprint has ended, or when the founder asks to plan, scope, or commit the coming sprint's work. Also use when a sprint is running with no sprint goal on record.
---

# Agile Sprint Planning

## Overview

Start-of-sprint ceremony for a solo founder (20–30 min — Redline convention). Output: a falsifiable sprint goal, committed tasks materialized on the GitHub Projects board (issues, sub-issues, Sprint field, dependencies), an explicit out-of-scope list, and `docs/product/tasks/sprint-<N>-goal.md`.

**REQUIRED SUB-SKILL:** `github-projects` — every board read/write in this ceremony uses its procedures and guards. No board mechanics are restated here.

## Mode Routing (first action, before anything else)

Ask:

> "Which sprint planning mode?
> **Suggest** — I read the project docs and backlog, draft a falsifiable goal, present it for your confirmation.
> **Lead** — You tell me what you want to prove this sprint. I ask questions until the goal is clear, then reconcile with the backlog."

Wait for the answer. Do not read the backlog, query the board, or draft anything first — and do not start either procedure ahead of the answer: no interview questions, no capacity figure, no goal sketch. Asking ahead IS starting the procedure ("the rule only prohibits reading and drafting, not asking" is a rationalization — it prohibits all pre-work). The founder stating intent up front means Lead — still ask the mode question (one line), and your first reply ends with it or, at most, with that procedure's opening questions.

**Time pressure compresses narration, never turns.** "We only have 10 minutes" does not license collapsing the ceremony into one reply: presenting a goal draft, task plan, or backlog mapping in the first reply — even framed as "a proposal pending your confirmation" — is running the ceremony without the founder, and it lets the backlog anchor the goal (the exact failure Lead mode exists to prevent). The gates are turn boundaries, not proposal framing.

Then: Suggest → `procedures/suggest.md` · Lead → `procedures/lead.md`. **Both end in `procedures/commit.md` — mandatory.** A session that confirms a goal but does not complete the commit procedure is an incomplete ceremony, not a shorter one.

## Boundary Contract

**Inputs:** board backlog (via `github-projects`); last sprint's Done count; `docs/product/strategy/strategic-bets.md`; `docs/product/strategy/okrs/2026-h2.md`; `docs/product/operations/cadences.md` (sprint-boundary convention); open `specs/NNN-*/spec.md`; `docs/product/tasks/this-week.md` if present.
**Outputs:** `docs/product/tasks/sprint-<N>-goal.md` (per `reference/plan-format.md`); board updated (issues, sub-issues, Sprint field, dependencies); regenerated `this-week.md`.
**Does not cover:** ad-hoc task creation (`github-projects`); shaping unrefined tasks (`shaping`); retrospectives (`/session-retro` command); bet-level risk stress-tests (`strategy-pre-mortem`).

**Steward:** PM. Principal Engineer consulted on any unshaped candidate task. Founder decides goal and scope — nothing enters the sprint without founder confirmation.

## Prerequisites (run immediately after the mode answer; abort with a clear error if any fails)

- G1: `gh auth status` lists `project` scope (per `github-projects` guards)
- G2: `project_config.json` exists and is ≤ 24 h old (path per `github-projects`)
- G3: strategic-bets file exists **and has at least one active bet**
- Sprint numbering: next sprint = current + 1, detected from the Sprint field options in `project_config.json` or the live board. `cadences.md` defines the boundary convention only — it has no sprint date table.

## INVEST — task readiness (single authoritative statement)

Source: *Clean Agile* (Martin); also *Continuous Delivery*. Applied to any sprint task, not only user stories.

| Criterion | Question | Fail signal → action |
|---|---|---|
| Independent | Workable without waiting on an unfinished task? | Unmet predecessor → sequence it or defer it |
| Negotiable | Scope can flex? | Reads as a fixed contract → renegotiate wording |
| Valuable | Linked to an active bet/OKR? | No link → flag; allowed only if it unblocks a bet-linked task (state the link) |
| Estimable | Spec, Pitch, or prior art exists? | None → **push to `shaping`; never commit** |
| Small | Fits one sprint, one person? | Uncertain → split; tasks MUST NOT cross sprint boundaries (cadences.md) |
| Testable | Observable "done when" (browser/CLI-visible, not "code merged")? | Missing → write one before committing |

No prior art in this codebase → mark high-risk, allow extra time.

## Hard Gates (blocking — no step may override)

1. **Goal confirmation:** founder confirms the goal before any document or board write.
2. **Goal-first, backlog-second (Lead):** the backlog is read only after the goal and failure tripwire are confirmed. The founder asking to "peek at the board first" is not a waiver — the answer is the next goal question.
3. **Out-of-scope list:** ≥ 3 named items with reasons (Redline convention; principle per *Shape Up* scope hammering / *Clean Agile* immutable iteration). Draft them yourself if the founder won't.
4. **Board completeness (close gate):** board items for Sprint N == committed level-1 count; Sprint field set on every item; every identified predecessor written to the board via `github-projects` → set-dependencies; every level-2 WBS row exists as a sub-issue linked to its parent (WBS mirror rule — founder ruling 2026-06-12). Until all four hold, the ceremony is open.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Plan doc written, board never updated | **Sprint 2 failure: 8 of 10 planned tasks never reached the board.** Run the close gate; a GitHub issue is not a board item until verified via list-tasks. |
| Dependencies named in prose but not written to the board | The daily standup reads board dependency data, not the plan doc. Write them via `github-projects` → set-dependencies before closing. |
| Planning above last sprint's Done count | Yesterday's weather is the ceiling (*Clean Agile*). A "compromise" above it is still optimism. |
| Committing a task with no spec/Pitch | Estimable fail → `shaping`. Offer the shaping session a sprint slot instead. |
| Goal that can't be falsified ("work on X") | Goal = a state at sprint end, linked to a bet, with a failure tripwire (see `procedures/lead.md`). |
| Reading the backlog before goal confirmation (Lead) | Hard Gate 2. Never before, never during the interview. |
| Skipping out-of-scope | Every unnamed task is implicitly "maybe this sprint". Hard Gate 3. |
| Board writes without founder confirmation | Hard Gate 1. Present, don't decide. |
| Inventing labels or board fields | Label set and field mechanics live in `github-projects` — retrieve, never recall. |
| Collapsing the ceremony into one turn under time pressure ("here's the full plan, just confirm") | First reply ends with the mode question or the opening questions. Compress narration, never turns. |
