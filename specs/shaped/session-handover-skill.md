---
title: "Pitch: session-handover skill"
status: shaped
shaped-by: Peter (Principal Engineer)
shaped-date: 2026-06-03
handed-to: Harriet (Agent Development)
appetite: S
---

# Pitch: `session-handover` Skill

## Problem

When a VS Code session ends, the in-session reasoning — decisions made, scope changes agreed, risks surfaced — evaporates. The next agent (Kabilan resuming, or Mark picking up a thread) re-discovers context that was already established, repeating work and risking contradictory decisions. CCE `record_decision` partially mitigates this, but only if it was called during the session; under time pressure, agents skip it. The gap is worst at the Kabilan/Peter/Mark boundary: work is "in flight" between agents and there is no structured handoff note. Without a forcing function at session close, context loss is the default.

## Appetite

**Small.** Deliverables are one `SKILL.md`, one `procedures/session-handover.md`, and one hook JSON (`.github/hooks/handover.json`). No new infrastructure, no new dependencies. This is a documentation and procedure artifact, not a feature. Harriet should be able to draft both files in a single session.

Rationale for Small: the mechanism is already decided (git log bounded by SHA, four-section note, CCE as primary output). Harriet's job is to encode it correctly, not to design it.

## Solution

The skill is a procedure invoked explicitly at session end by Kabilan, Peter, or Mark. It does three things in order:

**1. Bound the session window.**
Read `/memories/session/session-start.md` (written by the VS Code `SessionStart` hook) to get the HEAD SHA at session open. Run `rtk git log <sha>..HEAD --name-only` to get the files changed this session. This is the scope — nothing outside it is considered.

**2. Produce the four-section handover note.**
Using only the bounded git log and any decisions recalled from CCE, generate a structured note with exactly four sections:
- **What shipped** — completed items with file paths
- **In flight** — partial work; must name which agent picks up next
- **Watch-outs** — only from the pre-defined footgun categories (listed in the procedures file); no free-form risk entries
- **Open questions** — unresolved decisions that the next agent needs to answer before proceeding

**3. Write decisions to CCE.**
Call `record_decision` for each item that qualifies (scope change, architectural choice, deferred item). The printed note is secondary confirmation. CCE is the durable record.

The `/memories/` write (if the session-start file needs updating) requires explicit user confirmation before executing.

## Breadboard

```
[SessionStart hook] --> writes HEAD SHA --> /memories/session/session-start.md
                                                        |
[User invokes skill] --> reads SHA --> git log bounded to session
                                                        |
                              --> four-section note (stdout)
                                                        |
                              --> record_decision (CCE) [primary output]
                                                        |
                              --> flag uncommitted changes and stop
```

Connections that are NOT in scope: CCE reindex, auto-commit, scratchpad.md filing, cross-session trend analysis.

## Rabbit Holes

| Hole | Why to avoid |
|---|---|
| Inferring decisions from diff content | Diffs show what changed, not why. Inference is unreliable and expensive. Decisions must be stated, not reverse-engineered. |
| Auto-commit at session end | Introduces git state side-effects the user hasn't reviewed. Deferred to V2. |
| Free-form Watch-outs | Creates inconsistency across sessions. Pre-defined footgun categories enforce shared vocabulary. |
| CCE reindex call at session end | Slow, non-deterministic, and the skill has an 8k token budget. Reindex is a separate maintenance action. |
| `scratchpad.md` lessons filing | Out of scope. Lessons filing is a separate skill invocation, not a session-close side-effect. |
| Cross-session trend analysis | Requires historical trawling. Exceeds the 8k token budget. Deferred. |
| Making the hook JSON writable by the skill | The hook JSON is infrastructure. Harriet documents it; she does not own or modify it. |

## No-Gos

Hard constraints Harriet must not violate in the SKILL.md or procedures file:

1. **No auto-commit.** The skill flags uncommitted changes and stops. It does not stage or commit.
2. **No `/memories/` writes without explicit user confirmation.** This is a platform safety constraint, not a convention.
3. **No free-form footgun categories.** The pre-defined categories are: Pandera schema changes without fixture updates; Pydantic model changes without test regeneration; ADR references broken; CCE index stale after new file creation. Harriet may format these but must not add or remove categories without a new shaping session.
4. **≤8k token budget.** No historical trawling. The skill reads the bounded git log and CCE for the current session only.
5. **Windows/PowerShell only.** All terminal commands use `rtk` prefix and PowerShell syntax.
6. **Skill body must not name agents.** Per writing-skills convention: skills are agent-agnostic. Write "the invoking agent" not "Kabilan". The skill description and routing table in agent JDs handles routing.
7. **Hook JSON path is fixed.** `.github/hooks/handover.json`. Harriet references it; she does not create or move it.
8. **CCE `record_decision` is primary output.** The printed note is human-readable confirmation only. The skill must treat CCE writes as the durable artifact.

## Handover to Harriet

**What Harriet is writing:**
- `SKILL.md` — the loadable agent instruction file
- `procedures/session-handover.md` — the step-by-step procedure including the four-section template and the pre-defined footgun category list

**What Harriet is NOT writing:**
- The VS Code hook JSON (`.github/hooks/handover.json`) — infrastructure, owned separately
- The git commands — these are specified in this Pitch and should appear verbatim in the procedures file

**Key formatting decisions:**
- The four-section template belongs in `procedures/session-handover.md`, not inline in `SKILL.md`. SKILL.md cross-references it.
- The footgun categories are a fixed enumeration in the procedures file. Present them as a table: Category / What breaks.
- The `SKILL.md` description field must follow the `"Use when..."` convention and mention "session end" and "handover note" so Claude routes to it correctly.

**Skill name:** `session-handover` (not `session-close`, not `kabilan-handover`).

**Trigger condition for the description field (suggestion):**
> "Use when ending a development session and needing to produce a structured handover note, write in-session decisions to CCE, and flag uncommitted work before the next agent begins."

**What Harriet should ask Peter before writing:**
- If the pre-defined footgun category list needs domain review from Graeme (it may, for Pandera/Pydantic items — this is a judgment call Harriet should flag, not decide unilaterally).
- If a procedures file for `session-handover` already exists that should be merged rather than replaced.

**Acceptance test (informal):**
After drafting, Harriet should ask: "If an agent loads this SKILL.md cold, with no prior session context, can they produce a valid four-section note and at least one CCE `record_decision` call from a real session's git log?" If yes, the skill is complete.
