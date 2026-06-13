# Data Model: Office.js Spike — Scan, Mark, Replace in Script Lab

**Date**: 2026-06-13 | **Plan**: [plan.md](plan.md)

No persistent storage and no Python models exist in this spike. The "data model" is
the set of in-snippet shapes and in-document artifacts that the acceptance scenarios
read off.

## Entities

### WordListEntry (snippet constant)

| Field | Type | Rules |
|---|---|---|
| `word` | string | Lowercase single word; 3-5 entries total (placeholder until #195) |
| `replacement` | string | Non-empty; shown as mark metadata and used by Replace |

### SeedText (in-document)

| Property | Value | Rules |
|---|---|---|
| occurrences of listed words | exactly 3 | One word twice + a second word once (spec FR-002) — repetition is part of the baseline so US1 scenario 3 reads off the standard seed |
| content | plain prose paragraph | No punctuation adjacent to seeded words that could perturb search (risk register) |

### FoundOccurrence (transient, per Find run)

| Field | Source | Rules |
|---|---|---|
| `text` | found range's text after load/sync | Logged verbatim per occurrence |
| `word` | the WordListEntry that matched | Used to derive the mark tag |

### Mark (in-document content control)

| Field | Value | Rules |
|---|---|---|
| `appearance` | `"BoundingBox"` | Visible bounded highlight (spec FR-005) |
| `color` | one distinct color (e.g., red) | Distinct from normal text |
| `title` | the occurrence's `replacement` | Inspectable metadata (spec FR-006) |
| `tag` | `redline-taboo:<word>` | Machine marker; idempotency key (plan D4); persists in OOXML `<w:sdtPr><w:tag>` |

State transitions: unmarked range → marked (Mark stage); marked → replaced text
(Replace stage; control state afterwards is observed and reported, not prescribed).

### ConsoleReport (transient, per stage)

See [contracts/console-output.md](contracts/console-output.md) — the read-off
interface. Counts in reports MUST equal in-document reality (that equality IS the
spike evidence).

### EvidenceLog (committed file)

`docs/research/20260622-185-officejs-spike/evidence.md` — one section per child
issue (#186, #187, #188), each holding the pasted console transcript and the
observations the issue's acceptance criteria name.
