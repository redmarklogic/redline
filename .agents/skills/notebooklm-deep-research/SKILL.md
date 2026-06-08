---
name: notebooklm-deep-research
description: Use when running NotebookLM deep research with strict 5 Whys intake, then index the notebook and return a handoff package to the user unless an explicit reviewer is requested.
---

# NotebookLM Deep Research

Use one intake framework only: [5 Whys](../mental-models/root_cause_analysis/five-whys.md).

## Boundary Contract

## 5 Whys Question Template

Question line:
- `Question X of 5: Why [explicit assumption sentence]?`

Helper line:
- `Choose one option, type a custom answer, or choose Skip to start search immediately.`

Ambiguity check:
- Bad: `Why are current assumptions insufficient?`
- Good: `Why must we validate the assumption that Legal Adviser in Microsoft Word has reusable UI patterns for Redline?`

## Notebook Package Format

- Notebook title
- Notebook URL
- notebook_id
- Imported source count
- Imported source list with rationale
- Index confirmation (updated or failed)
- Suggested next actions (options list)

## Completion Gate

Do not declare completion unless all conditions below are true:

1. Notebook creation and source import steps are finished.
2. Index upsert via `notebooklm-index` is confirmed.
3. Notebook package has been returned to the user, and the flow is paused for user decision.


See `procedures/notebooklm-deep-research.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Required correction |
|---|---|
| Reviewer routing assumed by default | Route to reviewer only when explicitly requested earlier. |
| Vague Why questions | Rewrite each question with one explicit assumption sentence. |
| Manual numbering in option labels | Remove numbering; rely on chat UI numbering. |
| Proceeding after package delivery without user instruction | Stop and wait for next user decision. |
| Using `nlm source sync` on a file-upload source | `nlm source sync` only works on Drive-linked sources. Check source type (`nlm source stale`) before syncing. |
