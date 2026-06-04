---
name: session-handover
description: Use when ending a development session before a context switch, long pause, or handoff to a new agent.
---

## Boundary Contract

### Inputs
- `.session/session-start.md` — HEAD SHA written by the VS Code `SessionStart` hook (`hooks/session-start-anchor.ps1`)
- `rtk git log <sha>..HEAD --name-only` — bounded file list for this session only
- CCE `session_recall` — in-session decisions already recorded

### Outputs
- Four-section handover note (stdout) — human-readable confirmation
- `record_decision` calls to CCE — one per qualifying decision
- `record_code_area` calls to CCE — one per meaningfully-changed file from the git log
- Both are **primary durable output**; the note is secondary
- Uncommitted-change flag (stdout) — stops without committing

### Out of Scope
- Auto-commit or staging changes
- `/memories/` writes without explicit user confirmation
- CCE reindex at session end
- Diff content analysis or decision inference from diffs
- Cross-session trend analysis
- Scratchpad filing
- Creating or modifying `.github/hooks/handover.json` (infrastructure — not this skill)

## Session Context

**Anchor file:**
```!
cat .session/session-start.md 2>/dev/null || echo "ABSENT"
```

**Files changed this session:**
```!
SHA=$(cat .session/session-start.md 2>/dev/null | tr -d '[:space:]') && git log "$SHA..HEAD" --name-only --pretty=format: 2>/dev/null | grep -v '^$' || echo "Cannot run — anchor SHA unavailable."
```

## Core Steps

1. Check the **Anchor file** block above. If it shows `ABSENT` → **fail loudly** (see `procedures/session-handover.md` Fallback). Do not proceed.
2. Use the **Files changed this session** block above as the bounded file list.
3. Recall CCE: call `session_recall` for in-session decisions.
4. Produce four-section note: **What shipped / In flight / Watch-outs / Open questions**.
5. Check each of the four footgun categories explicitly; write "Not triggered" if clear.
6. Write to CCE — `record_decision` per qualifying item (scope change, architectural choice, deferred item); `record_code_area` per file in the bounded git log where meaningful work was done.
7. Flag uncommitted changes. Stop. Do not commit.

See `procedures/session-handover.md` for the full procedure, four-section template, footgun categories table, and fallback rules.

## Common Mistakes

| Mistake | Fix |
|---|---|
| "CCE already has most of the decisions — skip the procedure." | `record_decision` is the *output* of this skill, not a reason to bypass it. Prior calls cover earlier work; the procedure captures the full session. |
| "A quick verbal summary is good enough." | Verbal summary is not a handover. Four-section structure is mandatory; no section may be omitted. |
| "Exploratory sessions / spikes don't need a handover." | No session type is exempt. Spikes surface watch-outs (e.g., CCE index stale after new file creation). |
| "`session-start.md` is missing — I'll approximate with `--since=today`." | Approximation prohibited. Fail loudly and stop. See Fallback in `procedures/session-handover.md`. |
| "The note captures everything — I'll skip the `record_decision` calls." | The note is human-readable confirmation only. CCE writes are the durable record. Both required; neither substitutes for the other. |
| "This footgun category doesn't apply to today's session." | Each category must be explicitly checked and marked "Not triggered" or described. Silent omission is a failure. |
| "I'll call `record_decision` once with a summary to save time." | One call per qualifying item — scope change, architectural choice, deferred decision. Bulk calls break CCE topic-search granularity. |
