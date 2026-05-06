# Information Radiator — Candidate B Design Specification

**Status**: Resolved design. **Owner**: Mark. **Date**: 2026-05-06.
**Strategic bet**: [Bet 2 — Pre-Review Is the Paid Product Day-1](../strategy/strategic-bets.md)
**Feature scope**: Feature D (Pre-Review) — output presentation layer.
**Origin**: [pre-review-state-orientation-gap.md](../problems/pre-review-state-orientation-gap.md)
**Domain input**: [information-radiator-practitioner-feedback.md](../../knowledge/geotechnical/report-writing/information-radiator-practitioner-feedback.md)

## Design Summary

The Pre-Review Coverage Summary is a compact table embedded in the .docx output,
on page 2 (document control page) or page 3 (overflow). It gives the senior reviewer
state orientation in under 60 seconds: what Redline checked, what it found, and
what requires their engineering judgment.

This is an extension of the document control page (Decision 3), not a new surface.
It follows the same provenance logic: the document tells the reviewer what has
happened to it before they begin reviewing.

## Placement Rules

1. **Primary placement**: Page 2, below the revision history table, above the
   signature block. The coverage summary is part of document control.

2. **Overflow rule**: If the coverage summary pushes page 2 beyond one printed page,
   the entire coverage summary moves to a standalone page 3, between the document
   control page and the table of contents. The revision history and signature block
   remain on page 2 undisturbed.

3. **Pipeline responsibility**: The document generation pipeline detects overflow
   dynamically at render time. The number of sections varies per report, so this
   cannot be a static template decision. The pipeline renders on page 2 first,
   measures, and overflows to page 3 if needed.

4. **Table of contents entry**: The TOC includes a "Pre-Review Coverage Summary"
   entry with a bookmark hyperlink to the coverage table. This supports the
   repeat-visit use case (reviewer navigates back to the summary during review).

## Document State Gate

**The coverage summary appears in DRAFT-UNDER-REVIEW versions only.**

It is stripped automatically when the report transitions to "issued" status via
the Finalise Report action (see audit trail design notes, Q3). Rationale: "4
sections not checked" in a contractual document creates litigation exposure.

**Stripping mechanism**:

- The pipeline regenerates the .docx without the coverage summary section on issue.
- The issued version retains: revision history, signature block, audit provenance
  (Level 4 — timestamp, model version, rule library version).
- The coverage summary is archived in the Redline web dashboard as a historical
  record. It leaves the document but not the platform.
- This is automated, not manual. The reviewer must not be responsible for deleting
  the coverage table before issue.

## Coverage Table Specification

### Scope-of-Checking Header

One line above the table, stating what rules and standards Redline checked against.

> **Pre-Review Coverage Summary**
> Checked against: *[Firm X Template v3.2]* + *[NZS 3604:2011]* + *[NZGS Module 2]*

The bracketed items are populated by the pipeline from the rule library metadata.
If multiple standards were applied, list all. This line is essential for reviewer
trust — it answers "what did Redline actually check?" before the reviewer reads
any flags.

### Table Structure

| Section | Status | Flags | Summary |
|---|---|---|---|
| 1. Introduction | Checked | — | Scope statement, project references |
| 2. Site Description | Checked | 2 Fix | Location accuracy, site history completeness |
| 3. Ground Conditions | Not checked | — | *Engineering judgment required* |
| 4. Foundation Design | Checked | 1 Fix, 1 Check | Bearing capacity reference, settlement calc method |
| 5. Recommendations | Checked | 1 Note | Terminology consistency |
| 6. Limitations | Checked | — | Standard limitations clause present |

### Column Definitions

**Section**: Report section name from the skeleton template. Top-level sections
only (e.g., "3. Ground Conditions", not "3.1 Geology"). Exception: if the report
has fewer than 6 top-level sections, go one level deeper. The pipeline counts
top-level sections at generation time and applies this rule automatically.

**Status**: One of three values:
- **Checked** — Redline's rule library covers this section and rules were applied.
- **Not checked** — Redline does not have rules covering this section.
  Always displayed as: "Not checked" with the Summary showing
  "*Engineering judgment required*". Never softened to "Outside scope" or similar.
- **Checked (no rules matched)** — Rules exist but none fired. Distinct from
  "Not checked" because Redline did examine the section.

**Flags**: Count of flags by severity, using reviewer-native labels:
- **Fix** — Must be corrected. Maps to internal "critical."
- **Check** — Should be verified by the reviewer. Maps to internal "advisory."
- **Note** — FYI, no action required. Maps to internal "informational."

Displayed as: "2 Fix", "1 Fix, 1 Check", "1 Note", or "—" (no flags).
No rule IDs. Rule IDs (e.g., "GBR-LANG-01") belong in Level 4 (audit trail) only.

**Summary**: One-line description of what was checked or what flags were raised.
For checked sections with no flags: what Redline verified (e.g., "Scope statement,
project references"). For flagged sections: brief description of the flags. For
unchecked sections: always "*Engineering judgment required*" (italicised).

### Ordering

**Primary ordering**: Section number (matching document structure).

**Visual severity distinction**: Rows with Fix flags are visually distinguished:

- In digital .docx: bold text and/or a subtle row background colour.
- In printed/PDF: bold text on the Flag and Summary cells.

This gives the reviewer both spatial navigation (section order matches document)
and severity orientation (Fix items are visually prominent) in one scan.

**Open question for KR2 interviews** *(resolved 2026-05-06)*: Founder confirmed
section-number ordering with visual severity distinction (Mark's position).
Graeme's flag-severity preference is recorded in P-036 and will be tested in
KR2 interviews. If interview data contradicts the founder's decision, re-evaluate.

### Flag Totals Line

Below the table, a single summary line:

> Pre-Review checked 8 of 12 sections. 3 flags raised (1 Fix, 1 Check, 1 Note).
> 4 sections require reviewer judgment.

### Disclaimer

Below the totals line:

> Pre-Review checks are limited to the rules in Redline's current library.
> The reviewing engineer is responsible for all engineering judgment.

## Information Hierarchy Mapping

| Level | What | Where |
|---|---|---|
| Level 1 — Report state | Totals line ("checked 8 of 12, 3 flags") | Coverage summary, below table |
| Level 2 — Section coverage | Coverage table (section, status, flags, summary) | Coverage summary |
| Level 3 — Flag detail | Individual flag descriptions, expected content, what is missing | Word comments (inline annotations) |
| Level 4 — Audit provenance | Timestamp, model version, rule library version, rule IDs | Document control page (existing) |

## What the Radiator Must Never Show

1. "All clear" or "Report approved" — no green-light-means-done signal.
2. Confidence scores — no "85% compliant."
3. Reviewer performance metrics — no "you resolved flags 30% faster."
4. Rule IDs — these are Level 4 only.

## Deferred to v1.1

These elements are acknowledged as valuable but deferred due to engineering
complexity or dependency on P-024 (Word task pane).

| Element | Why deferred | Dependency |
|---|---|---|
| Reviewer's note column | Requires structured input in Word (content controls or task pane). A read-only coverage table in v1.0 is sufficient; the reviewer's working tool is Word comments. | P-024 unfreeze |
| Revision delta context | Requires pipeline to diff two revisions and summarise per-section changes. High engineering cost. Existing revision history table provides coarse context. | Pipeline revision comparison capability |
| Trust calibration feedback | Flag accuracy tracking (agreed/dismissed) is a feedback loop, not a radiator feature. Requires structured flag resolution capture. | Task pane or web review interface |

## KR2 Interview Stimulus

Candidate B is the primary interview stimulus for the information radiator question.
Present as a static mockup:

1. Show a standard page 2 (status quo) alongside the enhanced page 2 with coverage
   summary.
2. Ask: "Before you read any section, you can see what was machine-checked and what
   has flags. Would you use this? Would it change the order you review sections?"
3. Test ordering preference: show section-number version and flag-severity version.
   Ask which the reviewer prefers and why.

## Engineering Handoff Notes

When this design moves to spec-kit for implementation:

1. **Overflow detection**: The pipeline must measure whether the coverage summary
   fits on page 2 and overflow to page 3 dynamically.
2. **Conditional section**: The coverage summary is gated on document status
   (draft vs issued). The Finalise Report action triggers regeneration without it.
3. **Scope-of-checking population**: The header line is populated from rule library
   metadata — which standards and templates were applied.
4. **Granularity rule**: Pipeline counts top-level sections; if < 6, includes one
   level deeper.
5. **Label mapping**: Internal critical/advisory/informational maps to
   Fix/Check/Note in the presentation layer only.
6. **TOC bookmark**: Coverage summary gets a TOC entry with a working hyperlink.
7. **Web dashboard archive**: On issue, the coverage summary is archived in the
   web dashboard for the PD's historical view.
