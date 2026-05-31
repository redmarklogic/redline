---
name: task-defer
description: Use when asked to defer an outstanding task, idea, question, or decision to a future date or condition — creates a structured file in docs/deferred/ with a mandatory unfreeze condition and updates the index.
---

# task-defer — Deferred Item Registration

Apply this skill whenever the user or an agent says any of:
- "defer this to [date/quarter]"
- "park this for now"
- "revisit this when [condition]"
- "put this on hold until [event]"
- "we'll come back to this"

**Do not apply proactively.** An explicit instruction to defer is required.

## Boundary Contract

This skill writes to `docs/deferred/` only. It does not write to strategy, product,
or domain documents. The deferred file is a *pointer* — the source artifact stays
where it is; only the deferral record lives here.

## Mandatory Rule: Unfreeze Condition

Every deferred item **must** have a specific unfreeze condition.
"Later" is not an unfreeze condition. "When we have time" is not an unfreeze condition.
An acceptable condition names:
- A specific event ("when NZS XXXX is published")
- A measurable threshold ("when KR1 reaches ≥ 50 signups")
- A decision gate ("when H2 strategy refresh runs")
- An artifact becoming available ("when client X case study is approved")

If no condition can be stated, ask: "What would need to be true for this to be
actionable?" Do not create the file until a condition is agreed.

## File Naming Convention

```
docs/deferred/<ID>-<slug>.md
```

- `ID`: next available ID from `docs/deferred/_index.md` (P-NNN format for strategic;
  use the next sequential number across all types)
- `slug`: 3–5 word lowercase hyphen-separated summary of the topic

## Template

```markdown
---
id: <P-NNN>
type: <strategic | hypothesis | knowledge-gap | content-dependency | design | task | question>
date_deferred: <YYYY-MM-DD>
status: open
deferred_by: <agent-slug or "founder">
owner_at_retrieval: "<who acts when unfrozen>"
unfreeze_condition: >-
  <one-line summary of the unfreeze condition>
revisit_by: <YYYY-MM-DD or quarter e.g. 2026-Q3>    # optional
linked_bet: <Bet N>                                   # optional
problem_statement_ref: <path or one-sentence evidence summary>  # optional
trigger_event: <external event name>                  # optional, for external triggers
stale_after: <YYYY-MM-DD or condition>                # optional, for time-sensitive items
surface: <web | document | taskpane | email>          # optional, for design items
artifact_ref: <path or URL to in-progress artifact>  # optional
---

# <Short descriptive title>

## Why deferred

<1–3 sentences. Enough context to understand without re-reading the original session.>

## Unfreeze condition

<Full unfreeze condition. Be specific. Name the event, threshold, or gate.>

## Owner at retrieval

<Who acts when this is unfrozen.>
```

## Procedure

1. **Agree on the unfreeze condition** before creating the file. If unclear, ask.
2. **Determine the next ID**: read `docs/deferred/_index.md` and use the next P-NNN number.
3. **Determine the type**: use the type that best fits the item's origin.
4. **Create the file** at `docs/deferred/<ID>-<slug>.md` using the template above.
5. **Add a row to `docs/deferred/_index.md`**:
   ```
   | [P-NNN](P-NNN-<slug>.md) | <title> | <status> | <owner> |
   ```
6. **Confirm** to the user: "Deferred as P-NNN. Unfreeze condition: [condition]."

## Retrieval

- **CCE search**: `context_search "deferred [topic keyword]"` — serendipitous discovery.
- **Full enumeration**: read `docs/deferred/_index.md` directly — guaranteed complete list.
- **Quarterly review**: read `_index.md`, filter `status: open`, check each
  `unfreeze_condition` against current state of bets, OKRs, and hypotheses.

## When an Item Is Unfrozen

1. Confirm the unfreeze condition has fired (with evidence — not a feeling).
2. Move the content to the relevant artifact (strategy doc, hypothesis, PRD, etc.).
3. Update `status: done` in the file's frontmatter.
4. Update the row in `_index.md` to show `done`.

## Common Mistakes

**Creating a file without an unfreeze condition**
- Problem: item becomes a dead letter with no retrieval path.
- Fix: agree on condition first; do not create until it exists.

**Setting `revisit_by` as the only unfreeze signal**
- Problem: date arrives, condition hasn't changed, item just renews with a new date.
- Fix: `revisit_by` is a backstop, not a substitute for a condition.

**Forgetting to update `_index.md`**
- Problem: item exists but is invisible at quarterly review.
- Fix: the index update is atomic with file creation — same session, no exceptions.
