# Problem Statement: Pre-Review State Orientation Gap

**Status**: Resolved. **Owner**: Mark. **Date**: 2026-05-06.
**Strategic bet**: [Bet 2 — Pre-Review Is the Paid Product Day-1](../strategy/strategic-bets.md)
**Feature scope**: Feature D (Inline Annotation Engine / Pre-Review) — output
presentation layer.
**Related**: [audit-trail-design-notes.md](../prds/audit-trail-design-notes.md),
[maker-checker-ux-concept.md](../initiatives/maker-checker-ux-concept.md)

## Problem Statement

**Who**: The senior reviewer (Technical Reviewer or Practice Director) at an
engineering consultancy, reviewing an AI-assisted geotechnical report produced
through Redline's Pre-Review pipeline.

**Pain**: When a reviewer opens a report for review today, they spend 20-30 minutes
*orienting* before they begin *reviewing*. Orientation means: what sections exist,
what state is the document in, has anyone looked at it yet, what needs my attention.
A templated report (structural orientation) cuts this in half because the reviewer
knows what sections exist and where to find them. But even with structural
orientation, the reviewer still lacks *state orientation* — they do not know, at a
glance, what Redline has already checked, what it found, and what state the report
is in before they open a single section. They must walk through the document
sequentially to discover this.

**Desired outcome**: The reviewer can determine the report's Pre-Review state — what
was checked, what was flagged, what is unexamined — in under 60 seconds, before
beginning section-level review. This compresses orientation time and directs
reviewer attention to flagged sections first.

**Strategic link**: Bet 2 assumes intermediate engineers will pay for Pre-Review
because it attacks the reviewer-bottleneck. The information radiator amplifies that
value by making the *reviewer's* experience faster — not just the author's. If the
reviewer's orientation time drops measurably, the bottleneck loosens from both ends.

## Insight: Structural Orientation vs State Orientation

Graeme's observation (2026-05-06): a templated report takes half the review time
because the reviewer doesn't spend 20-30 minutes working out where everything is.
The template provides **structural orientation** — the reviewer knows what sections
exist and what order they appear in.

The information radiator provides **state orientation** — a layer above structural
orientation. Before the reviewer walks through any section, they know:

1. What Redline checked (coverage).
2. What Redline found (flags).
3. What Redline did not check (the reviewer's judgment domain).

This is the distinction between "I know where the rooms are" (structural) and "I
know which rooms have been inspected and which have open issues" (state).

## Clarity Check

| Check | Status | Detail |
|---|---|---|
| Target user | Identified | Senior reviewer (TR or PD) |
| Core pain | Identified | No quick-glance summary of report Pre-Review state before section-level review |
| Desired outcome | Measurable | Orientation time < 60 seconds; reviewer can name flagged sections before opening any |
| Strategic link | Linked | Bet 2 — Pre-Review as paid product |
| Constraints | Identified | See below |

## Constraints

1. **Switzerland-neutral positioning** (from Ron): The radiator must frame coverage
   as "Here is what Redline checked. Here is what it found. Your engineering judgment
   covers everything else." It must never imply "everything green, you're done!" That
   framing would undermine the professional liability posture that makes Redline
   trustworthy.

2. **Not a standalone feature**: This is a UX design decision within Feature D
   (Pre-Review), specifically the output presentation layer. It does not get its own
   bet, its own PRD, or its own backlog item. It is an open question (Q6) in the
   audit trail design notes.

3. **Word task pane is parked** (P-024): The H2 delivery surface is web-only for
   Pre-Review. Any candidate design that requires a Word task pane must be flagged as
   dependent on P-024 unfreezing.

4. **Document control page is locked** (Decision 3): The provenance summary and
   Pre-Review results already live on page 2 (document control page). The radiator
   must complement this, not duplicate it.

5. **Two existing surfaces** (Decision 4): Word for the author during authoring, web
   dashboard for the PD. The reviewer's quick-glance surface is the identified gap.

## What the Radiator Is NOT

- It is not a replacement for section-level Word comments (those are the Checker's
  output per the Maker-Checker concept).
- It is not a compliance certificate or sign-off mechanism (that is the audit trail).
- It is not a portfolio dashboard (that is the PD's Mockup E surface).
- It is not an approval gateway — it never says "this report is ready."

---

## Candidate Designs

Three candidate designs for how the information radiator could work. Each describes
what it shows, where it lives, and what interaction model it uses. No HTML mockups
yet — these are conceptual descriptions for Graeme to react to.

### Candidate A: Web Pre-Review Summary Page (before opening the document)

**Where it lives**: In the Redline web app. After Pre-Review completes, the reviewer
receives a link (email or dashboard). Clicking the link opens a summary page *before*
the reviewer opens the .docx.

**What it shows**:

- **Report header**: Project name, report type (GIR/GBR), author, date, revision.
- **Coverage map**: A list of report sections (from the skeleton template), each
  showing one of three states:
  - *Checked, no flags* — Redline reviewed this section and found nothing to flag.
    Shows what was checked (e.g., "Checked against NZS 3910 s4.2, NZGS Module 2
    Clause 3.4").
  - *Checked, flags raised* — Redline found issues. Shows count and severity
    (e.g., "3 flags: 1 critical, 2 advisory"). Brief one-line summary of each flag.
  - *Not checked* — Redline does not have rules covering this section. Explicitly
    labelled: "This section requires your engineering judgment."
- **Flag summary**: Total flags by severity (critical / advisory / informational),
  with the most severe at the top.
- **Action**: "Open Report in Word" button that opens or downloads the .docx with
  Word comments already embedded.

**Interaction model**: Read-then-open. The reviewer reads the summary, forms a mental
model of where to focus, then opens the document. The summary page is a *launch pad*,
not a working surface.

**Strength**: Clean separation of orientation (web) from review (Word). Does not
require Word integration. Ships on the web surface that already exists for H2.

**Risk**: The reviewer may skip the summary and go straight to the .docx, making the
radiator invisible. If the .docx arrives by email (as reports do today), the web
summary is an extra step.

### Candidate B: Enhanced Document Control Page (inside the document)

**Where it lives**: On page 2 of the .docx output — the document control page where
the audit trail already lives (Decision 3). The radiator is a new section on this
page, below the revision history table and above the signature block.

**What it shows**:

- **Pre-Review Coverage Summary** (compact table):

  | Section | Status | Flags | What Was Checked |
  |---|---|---|---|
  | 1. Introduction | Checked | 0 | Scope statement, project references |
  | 2. Site Description | Checked | 2 (1 critical) | Location accuracy, site history |
  | 3. Ground Conditions | Not checked | — | *Requires engineering judgment* |
  | ... | ... | ... | ... |

- **Flag totals**: Single line: "Pre-Review checked 8 of 12 sections. 5 flags raised
  (2 critical, 3 advisory). 4 sections require reviewer judgment."

- **Disclaimer**: "Pre-Review checks are limited to the rules in Redline's current
  library. The reviewing engineer is responsible for all engineering judgment."

**Interaction model**: The reviewer opens the .docx and the first substantive page
they see (after the cover) is the document control page with the coverage summary.
They scan the table, note which sections have critical flags, then navigate to those
sections where Word comments provide the detail.

**Strength**: Zero extra steps — the radiator is in the document the reviewer already
opens. It follows the engineering convention that document control information lives
on page 2. No web app dependency for the reviewer.

**Risk**: Page 2 may become crowded (revision history + signature block + provenance
summary + coverage table). The table must remain compact. Also, a static table in
a .docx cannot link to the flagged sections (no interactive navigation).

### Candidate C: Web Overlay Panel (inside the web review interface)

**Where it lives**: In the Redline web app, as a persistent side panel alongside the
document preview. Visible during the review session, not just before it.

**What it shows**:

- **Section navigator**: A vertical list of report sections, each with a status
  indicator (checked/flagged/unchecked). Clicking a section scrolls the document
  preview to that section.
- **Flag detail panel**: When a flagged section is selected, the panel expands to
  show each flag with its severity, what rule triggered it, and what was checked.
- **Progress tracker**: As the reviewer resolves flags (accepts, dismisses, or
  modifies), the status updates in real time. "5 of 8 flags resolved."
- **Coverage footer**: Persistent reminder: "Redline checked 8 of 12 sections.
  4 sections require your engineering judgment."

**Interaction model**: The radiator is a *companion* throughout the review session,
not a launch pad. The reviewer uses it to navigate, track progress, and ensure they
have addressed every flag before signing off.

**Strength**: Interactive, persistent, and navigable. Gives the reviewer a working
tool, not just a summary. The progress tracker makes resolution status visible.

**Risk**: Requires the reviewer to use the web app for review — which conflicts with
the assumption that engineers review in Word (Decision 4, Q2). This candidate only
works if the review surface is web-based, or if it coexists with Word review via a
task pane (P-024, currently parked). Most ambitious to build.

---

## Information Hierarchy

Regardless of which candidate surface delivers it, the radiator should present
information in a consistent hierarchy. The reviewer drills from high-level to detail:

**Level 1 — Report state (one glance)**:
"Pre-Review checked 8 of 12 sections. 5 flags raised (2 critical, 3 advisory)."

This is the single sentence the reviewer reads first. It answers: "How much of this
report has been machine-reviewed, and how much needs my attention?"

**Level 2 — Section-level coverage (scan the list)**:
Each section shows: checked with no flags, checked with flags (count + severity), or
not checked (requires judgment). The reviewer identifies which sections to examine
first.

**Level 3 — Flag detail (on demand)**:
For each flag: what rule fired, what standard or checklist item was checked, what the
expected content is, and what is missing or incorrect. This level exists in the Word
comments (Maker-Checker output). The radiator at Level 2 points the reviewer to the
right sections; the Word comments at Level 3 provide the detail.

**Level 4 — Audit provenance (reference)**:
Timestamp, model version, rule library version, which rules were applied. This is the
document control page content (Decision 3). The reviewer rarely needs this during
review — it is for the audit record.

### What the Radiator Must Always Show

1. **Coverage scope**: What sections Redline checked and what it did not check.
2. **Flag count by severity**: How many issues were found, ranked by severity.
3. **Unchecked sections**: Explicitly named — never implied by omission.
4. **Disclaimer**: Redline's checks are bounded by its rule library. Engineering
   judgment is the reviewer's responsibility.

### What the Radiator Must Never Show

1. **"All clear" or "Report approved"**: No green-light-means-done signal.
2. **Confidence scores**: No "85% compliant" — this implies a completeness claim
   Redline cannot make.
3. **Reviewer performance metrics**: No "you resolved flags 30% faster than average."
   This is surveillance, not orientation.

---

## Design Tensions

| Tension | Candidate A (Web Summary) | Candidate B (Doc Control Page) | Candidate C (Web Overlay) |
|---|---|---|---|
| **Matches reviewer workflow** | Extra step before opening .docx | Inside the document they already open | Requires web-based review |
| **Interactivity** | Static (read-then-open) | Static (printed table) | Interactive (click-to-navigate, live progress) |
| **Build complexity** | Low (web page rendering Pre-Review results) | Low (template modification in .docx generation) | High (web review surface + real-time state) |
| **P-024 dependency** | None | None | Yes (or requires web-only review, conflicting with Decision 4) |
| **Works for printed reports** | No (web only) | Yes (in the document) | No (web only) |
| **Crowding risk** | None (own page) | High (page 2 is already dense) | None (side panel) |
| **Adoption risk** | Reviewer skips summary, goes straight to .docx | None (unavoidable — it's on page 2) | Reviewer must use web app for review |

**Recommendation for KR2 interviews**: Test Candidates A and B as primary stimuli.
Candidate C is the most powerful but depends on the reviewer accepting a web-based
review surface (which Q2 already tests). If Q2 interviews show strong Word preference,
Candidate C is deferred. If Q2 shows web acceptance, Candidate C becomes the leading
option.

Candidate B has the unique advantage of working for printed/PDF reports — which matters
because many firms still issue reports as PDFs to clients. The coverage summary table
on page 2 becomes part of the permanent record.

---

## KR2 Interview Stimulus Design

The candidates should be presented to reviewers as concrete stimuli during KR2
discovery interviews. Suggested interview approach:

1. **Prime with the insight**: "We've heard that a templated report cuts your review
   time because you know where everything is. We call that structural orientation.
   Now imagine you also knew, before opening any section, what an AI had already
   checked and what it found. Would that change how you start a review?"

2. **Show Candidate B first** (document control page with coverage table): "Imagine
   this table appeared on page 2 of every report you review. Before you read any
   section, you can see which sections were machine-checked and which have flags.
   Would you use this? Would it change the order you review sections?"

3. **Show Candidate A** (web summary page): "Now imagine the same information was
   available in your browser before you even open the Word document. You click a link,
   see the summary, then open the report. Better or worse than having it on page 2?"

4. **Probe for Candidate C** (if the reviewer shows web openness): "What if this
   summary stayed visible alongside the document while you reviewed — like a
   checklist you could tick off as you work through each section?"

5. **Key question**: "Where would you want to see this — in your browser before
   opening the document, on page 2 inside the document, or as a sidebar while you
   review? Or somewhere else we haven't thought of?"

---

## Questions for Graeme

1. **Coverage table on page 2 — too crowded?** Decision 3 already places provenance
   and Pre-Review results on the document control page. Adding a section-by-section
   coverage table may push page 2 to two pages. Is that acceptable in engineering
   report conventions, or does page 2 have an implicit length constraint?

2. **"Not checked" framing**: When Redline's rule library does not cover a section
   (e.g., geotechnical interpretation, engineering judgment sections), the radiator
   shows "Not checked — requires engineering judgment." Is this framing clear and
   acceptable to a senior reviewer, or does it read as an excuse? Would "Outside
   Redline's current scope" be better?

3. **Section granularity**: Should the coverage map use the top-level sections from the
   skeleton template (e.g., "3. Ground Conditions"), or should it go one level deeper
   (e.g., "3.1 Geology", "3.2 Groundwater", "3.3 Geotechnical Properties")? What
   level matches how a reviewer thinks about their review?

4. **Flag severity labels**: The Maker-Checker concept uses critical / advisory /
   informational. Do these map to how a reviewer thinks about markup? Or would
   different labels (e.g., "must address" / "consider" / "note") be more natural?

5. **Printed report value**: Some firms issue final reports as PDFs. Does a coverage
   summary table on page 2 add value in the issued document (as evidence of QA
   process), or should it only appear in the draft-under-review version and be
   removed before issue?

6. **Review order**: Does a reviewer always review sequentially (Section 1, 2, 3...),
   or do they jump to high-risk sections first? If the latter, the radiator's value
   is higher — it tells them which sections to jump to.

---

## Resolved Design (2026-05-06)

Graeme's practitioner feedback confirmed **Candidate B (Enhanced Document Control
Page)** as the winner. See
`docs/knowledge/geotechnical/report-writing/information-radiator-practitioner-feedback.md`
for the full feedback and
`docs/product/prds/information-radiator-candidate-b-design.md` for the resolved
design specification.

### Key Resolutions

| Question | Resolution |
|---|---|
| Candidate selection | Candidate B. Candidate A demoted to supplement (PD dashboard). Candidate C deferred to P-024 unfreeze. |
| Page 2 length | Coverage summary on page 2 if it fits; overflow to standalone page 3 between document control and TOC. Never displace revision history or signature block. |
| "Not checked" framing | "Not checked — engineering judgment required." No softened alternatives. |
| Section granularity | Top-level sections only. One level deeper if fewer than 6 top-level sections. Pipeline decides at generation time. |
| Flag severity labels | Fix / Check / Note (presentation layer). Internal system retains critical / advisory / informational. |
| Draft vs issued | Coverage summary in DRAFT-UNDER-REVIEW only. Stripped automatically on issue. Archived in web dashboard. |
| Ordering | Section number with visual severity distinction (Fix rows visually marked). **Founder confirmed 2026-05-06** (Mark's position). Graeme's preference recorded in P-036; will be tested in KR2 interviews. |
| Scope-of-checking header | v1.0 — one line above coverage table stating rules/standards checked. |
| Reviewer's note column | Deferred to v1.1 / P-024 unfreeze. |
| Revision delta context | Deferred to v1.1. |
| Trust calibration feedback | Deferred to v1.1. Rule ID suppression in v1.0. |
| Navigation | TOC entry with bookmark link to coverage summary. v1.0. |
| Document control page as radiator surface | **Founder confirmed 2026-05-06.** Page 2 is acceptable as the radiator surface — extends provenance, does not break it. |

### ~~Remaining Decision for Founder~~

**Resolved 2026-05-06.** Founder confirmed:
1. Document control page (page 2) is confirmed as the radiator surface.
2. Section-number ordering with visual severity distinction (Mark's position).
Both decisions are recorded in P-036 and the Candidate B design spec.

## Next Step

Mark produces the Candidate B design specification
(`docs/product/prds/information-radiator-candidate-b-design.md`). That document
is the engineering handoff artifact for spec-kit when Feature D reaches
implementation.
