# Session Handover — Full Procedure

**See:** `session-handover/SKILL.md` for boundary contract, out-of-scope rules, and common mistakes.

> **Provisional note (2026-06-03):** The four footgun categories below are sourced from the initial shaping pitch. They are subject to principal engineer review before being marked stable. Do not add or remove categories without a new shaping session.

---

## Prerequisites

- VS Code `SessionStart` hook has run and `.session/session-start.md` exists (written by `hooks/session-start-anchor.ps1`).
- Token budget: this procedure must complete within **8k tokens**. No historical trawling.
- Platform: **Windows / PowerShell only**. All commands use the `rtk` prefix.

---

## Step-by-Step

### Step 1 — Verify session bounds

```powershell
Get-Content .session/session-start.md
```

Extract the `HEAD_SHA` value. If the file is absent (hook didn't fire) → **go to Fallback now. Do not proceed.**

---

### Step 2 — Scope the session

```powershell
rtk git log <HEAD_SHA>..HEAD --name-only
```

This is the **only** source of truth for what changed this session. Do not expand scope beyond this log.

---

### Step 3 — Recall in-session CCE decisions

Call `mcp_context-engin_session_recall` with a topic matching the current branch or feature. This surfaces any `record_decision` calls already made during this session. These inform the "What shipped" and "In flight" sections — they do not replace the procedure.

---

### Step 4 — Check footgun categories

Before drafting the note, explicitly audit each category:

| Category | What breaks | Status |
|---|---|---|
| Pandera schema changes without fixture updates | Test suite fails; fixtures out of sync with schema | Check now |
| Pydantic model changes without test regeneration | Serialization tests fail; generated test data stale | Check now |
| ADR references broken | `check-hook-adr-reference.py` fails pre-commit; ADR links dead | Check now |
| CCE index stale after new file creation | Context search returns incomplete results; new files invisible | Check now |

For each category: write "Not triggered" if confirmed clear, or describe the specific risk if triggered. **Silent omission is a failure.**

---

### Step 5 — Produce the four-section handover note

Use this template verbatim. Do not rename sections. Do not add sections.

```
## What Shipped
<!-- Completed items with file paths from the bounded git log. -->
<!-- Example: feat(ingestion): added Pandera schema for CPT data — src/rl/ingestion/cpt_schema.py -->

## In Flight
<!-- Partial work not yet complete. MUST name which agent picks up next. -->
<!-- Example: "ADR-009 draft 60% complete — next agent (the invoking agent's successor) to finalise." -->
<!-- If nothing in flight: write "Nothing in flight." -->

## Watch-outs
<!-- ONLY entries from the four footgun categories. No free-form risk entries. -->
<!-- Example: "Pandera schema changed in cpt_schema.py — fixture tests/assets/cpt_fixture.py not yet updated." -->
<!-- If all categories clear: write "All footgun categories checked. None triggered." -->

## Open Questions
<!-- Unresolved decisions the next agent must answer before proceeding. -->
<!-- Example: "Should the CPT schema enforce strict column order? Deferred — needs domain expert input." -->
<!-- If none: write "No open questions." -->
```

---

### Step 6 — Write to CCE (primary output)

For each item that qualifies as a **scope change, architectural choice, or deferred decision**, call:

```
mcp_context-engin_record_decision(
    decision = "<concise decision statement>",
    reason = "<rationale — one sentence>"
)
```

Call this once per qualifying item. The printed note (Step 5) is human-readable confirmation. CCE is the durable record. Both are required.

---

### Step 7 — Flag uncommitted changes and stop

```powershell
rtk git status --short
```

If uncommitted changes exist, print them. Stop. Do not stage or commit. The invoking agent or the founder decides whether to commit.

---

### Step 8 — `/memories/` writes (conditional, confirmation required)

If the session-start file needs updating (e.g., new SHA for a continued session), display the proposed write:

```
"I will write the following to .session/session-start.md:
---
HEAD_SHA: <value>
written: <timestamp>
---
May I proceed? (yes/no)"
```

Wait for explicit user confirmation. Do not write without it.

---

## Fallback — `session-start.md` absent

If `.session/session-start.md` does not exist:

1. **STOP immediately.** Do not approximate with `--since=today` or any other heuristic.
2. Report verbatim:

   > `session-start.md` not found at `.session/session-start.md`. The VS Code `SessionStart` hook did not fire this session. Cannot bound the session window safely. Do not proceed with the handover. **Founder action required:** verify the hook at `.github/hooks/handover.json` is registered and firing on session start.

3. Do not produce a partial handover note.
4. Do not call `record_decision` with an unbounded scope.

---

## Rationalization Red Flags

Stop and restart from Step 1 if you catch yourself thinking:

| Thought | Why it is wrong |
|---|---|
| "CCE already has most of the decisions" | CCE record_decision is the output of this skill, not a bypass condition |
| "A quick verbal summary is good enough" | Not a substitute; four sections mandatory |
| "Exploratory work doesn't need a handover" | Spikes trigger footgun categories (CCE index stale, ADR drift) |
| "`--since=today` is close enough" | Approximation is prohibited; the SHA boundary is the contract |
| "The spirit is continuity — I'm achieving that differently" | The procedure is the spirit; shortcuts undermine cross-session consistency |
| "This footgun category doesn't apply" | State "Not triggered" explicitly; never omit silently |
| "The note captures everything; skip record_decision" | CCE is the durable record; the note is confirmation only |

---

## Hook Reference

The `SessionStart` hook that writes `session-start.md` is configured at:

```
.github/hooks/handover.json
```

This file is infrastructure — the invoking agent must not create or modify it. If the hook is missing or not firing, flag to the founder.
