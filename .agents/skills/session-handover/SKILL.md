---
name: session-handover
description: Use when ending a development session and needing to produce a structured handover note, write in-session decisions to CCE, and flag uncommitted work before the next agent begins.
---

## Boundary Contract

### Inputs
- `.session/session-start.md` — HEAD SHA written by the VS Code `SessionStart` hook (`hooks/session-start-anchor.ps1`)
- `rtk git log <sha>..HEAD --name-only` — bounded file list for this session only
- CCE `session_recall` — in-session decisions already recorded

### Outputs
- Four-section handover note (stdout) — human-readable confirmation
- `record_decision` calls to CCE — **primary durable output**; the note is secondary
- Uncommitted-change flag (stdout) — stops without committing

### Out of Scope
- Auto-commit or staging changes
- `/memories/` writes without explicit user confirmation
- CCE reindex at session end
- Diff content analysis or decision inference from diffs
- Cross-session trend analysis
- Scratchpad filing
- Creating or modifying `.github/hooks/handover.json` (infrastructure — not this skill)

## Core Steps

1. Read `.session/session-start.md` → extract HEAD SHA. If absent → **fail loudly** (see `procedures/session-handover.md` Fallback).
2. Run `rtk git log <sha>..HEAD --name-only` → session-bounded file list.
3. Recall CCE: call `session_recall` for in-session decisions.
4. Produce four-section note: **What shipped / In flight / Watch-outs / Open questions**.
5. Check each of the four footgun categories explicitly; write "Not triggered" if clear.
6. Call `record_decision` for each qualifying item (scope change, architectural choice, deferred item).
7. Flag uncommitted changes. Stop. Do not commit.

See `procedures/session-handover.md` for the full procedure, four-section template, footgun categories table, and fallback rules.

## Common Mistakes

**"CCE already has most of the decisions — skip the procedure."**
CCE `record_decision` is the *output* of this skill, not a reason to bypass it. Prior calls cover the morning; the procedure captures the afternoon. There is no "most of it" exemption.

**"A quick verbal summary is good enough."**
A verbal summary is not a handover. The four-section structure is mandatory. No section may be omitted.

**"Exploratory sessions / spikes don't need a handover."**
No session type is exempt. Spikes surface watch-outs (e.g., CCE index stale after new file creation). The footgun check runs regardless.

**"`session-start.md` is missing — I'll approximate with `--since=today`."**
Approximation is prohibited. If `session-start.md` is absent, fail loudly and stop. See Fallback in `procedures/session-handover.md`.

**"The note captures everything — I'll skip the `record_decision` calls."**
The note is human-readable confirmation only. CCE writes are the durable record. Both are required; neither substitutes for the other.

**"This footgun category doesn't apply to today's session."**
Each category must be explicitly checked and marked "Not triggered" or described. Silent omission is a failure.

**"I'll call `record_decision` once with a summary to save time."**
One call per qualifying item — scope change, architectural choice, deferred decision. A single bulk call is not a valid substitute; CCE search depends on granular, topic-specific entries.
