# Pre-Review Output: UX Design References

**Status**: Reference note (not a design spec)
**Author**: Matt
**Date**: 2026-05-22
**Domain review**: Graeme (2026-05-22)
**Source**: Ron's competitor profile — [microsoft-legal-agent.md](../../research/competitors/microsoft-legal-agent.md)
**Caveat**: Layout decisions are draft until personas are validated (parked decision P-029).

---

## Purpose

Design reference for when I begin the Pre-Review output format design. Ron flagged four
UX patterns from Microsoft's Legal Agent in Word that are relevant to Redline's Pre-Review
surface. This note records each pattern, my assessment of how it applies, and adaptation
considerations given Redline's web-first delivery.

---

## Pattern 1: Category-First Finding Taxonomy with RAG Severity

**What the Legal Agent does**: After running a playbook review, generates a report with
Green (compliant) and Red (requires changes) colour coding. Users can drill into each
topic to read the AI's analysis and proposed edits.

**Relevance to Pre-Review**: High. Pre-Review needs a scannable summary that lets a
senior reviewer triage quickly — "where do I need to focus?"

**Domain review (Graeme)**: Severity (RAG) is not the primary axis reviewers think in.
They think in **concern categories** first. A Red/Amber/Green severity sort undersells
the real problem — findings with identical severity have completely different
consequences and require different expertise to resolve.

**Adaptation notes**:

- **Primary grouping: four finding categories by consequence type.**
  1. **Liability exposure** — language or missing clauses affecting legal position
     (e.g., missing limitation clause, absolute language like "ensure", "guarantee").
  2. **Technical defensibility** — engineering substance affecting whether conclusions
     are supported (e.g., unsupported conclusions, missing design-type-specific
     parameters).
  3. **Standards compliance** — superseded, withdrawn, or incorrect standard references.
  4. **Mechanical/formatting** — style, structure, presentation issues.
- **Secondary cue: RAG colour within each category.** Red/Amber/Green is a visual
  severity indicator applied within each of the four buckets, not the primary taxonomy.
  This means the summary view has four labelled sections, each containing severity-coded
  findings.
- Colour alone is insufficient — must pair with icon or text label for colour-blind
  accessibility (WCAG 2.1 AA, 1.4.1 Use of Color).
- Web-first advantage: we control the full rendering surface. No dependency on Word's
  limited colour palette or tracked-changes styling constraints.

**Calibration examples (Graeme)**:

| Category | Example finding | Severity |
|---|---|---|
| Liability exposure | Missing limitation clause in Section 1.3 | Red |
| Liability exposure | Absolute language ("ensure") in recommendations | Amber |
| Technical defensibility | Conclusions not supported by presented data | Red |
| Standards compliance | Reference to superseded NZS 4431:2015 (current: 2022) | Amber |
| Mechanical/formatting | Inconsistent figure numbering | Green |

**Resolved question**: The finding taxonomy is now category-first with RAG secondary.
The "Not Applicable" / "Not Reviewed" states are handled by the disposition workflow
(see Pattern 3), not by the colour vocabulary.

---

## Pattern 2: Clickable Source Citations

**What the Legal Agent does**: Numbered citations in AI responses. Clicking a citation
highlights the exact source text in the document. Lets reviewers verify accuracy instantly.

**Relevance to Pre-Review**: Critical. Ron marked this as "non-negotiable for Pre-Review
Sprint 1." Every finding must link to the specific standard clause, house rule, or
structural expectation that triggered it.

**Adaptation notes**:

- The Legal Agent links citation -> source text *within the same Word document*. Redline's
  Pre-Review is web-first, so the citation target is different: it links to a standard
  clause (in the Standards Knowledge Store) or to a location in the uploaded report
  (rendered in-browser or referenced by section/page).
- **Three distinct citation types needed:**
  1. **Source citation** — links to the standard or rule that triggered the finding
     (e.g., "NZS 4431:2022, Clause 4.3.2"). This is a knowledge-store lookup.
  2. **Location citation** — points to where in the user's report the issue was found
     (e.g., "Section 3.1, paragraph 2"). This requires document-position mapping.
  3. **Cross-reference citation** (Graeme) — links two locations within the user's
     report where an internal inconsistency was found (e.g., summary in Section 2
     contradicts conclusions in Section 8). Internal consistency checking is a major
     part of GIR/GBR review.
- **Standard citation format (Graeme)**: all standard citations must include the edition
  year (e.g., "NZS 4431:2022" not "NZS 4431"). Standards get superseded; the year
  disambiguates.
- The interaction on click differs by citation type. Source citation should show the
  standard extract inline (tooltip or expandable panel), not just link to PDF — reviewers
  need the clause text visible without leaving the findings view. Location citation
  should scroll to / highlight the relevant passage in a document preview.
  Cross-reference citation should highlight both locations simultaneously.
- **Provenance indicator (Graeme)**: each finding must indicate whether it was produced
  by deterministic rule checking (word search, clause match — high confidence) or by
  LLM judgment (lower confidence). Reviewers calibrate attention differently for each.
  See also Pattern 5 (Finding Confidence/Provenance).
- Web-first opportunity: we can render richer citation previews (hover tooltips, side-by-
  side view) than a Word side panel allows. This is a potential UX advantage over the
  Legal Agent.

**Open question**: Does the user's uploaded document get rendered in-browser for
location citations, or do we reference by section/page number only? This is an
architecture question (Peter) with major UX implications. Flag early.

---

## Pattern 3: Disposition Workflow

**What the Legal Agent does**: Users can accept suggestions individually or click
"Accept All" to apply all playbook-aligned edits at once. Everything remains advisory —
human oversight required before finalising.

**Relevance to Pre-Review**: High. The disposition workflow is the core reviewer
interaction — how the engineer records their judgment on each finding.

**Adaptation notes**:

- Phase 1 Pre-Review is a *review* tool, not an *editing* tool. The output is a report
  of findings, not a set of tracked changes to accept. The accept/reject metaphor does
  not directly apply to "here are 12 issues I found in your GIR."
- **Six disposition options required (Graeme):**
  1. **Will Fix** — finding valid, report will be amended. (Renamed from "Agree" to
     signal active commitment rather than passive agreement.)
  2. **Disagree** — false positive, the tool got it wrong.
  3. **Not Applicable** — finding correct in general but does not apply to this project
     context.
  4. **Accepted Risk** — deviation is intentional and documented. This is the most
     important addition (Graeme). Engineering practice commonly and legitimately
     deviates from standards with documented justification. Has PI implications.
     Distinct from Disagree (tool wrong) and Not Applicable (rule does not apply).
  5. **Requires Discussion** — cannot be resolved by one reviewer alone; needs dialogue
     with design engineer, project director, or specialist.
  6. **Deferred** — acknowledged, will be addressed in a later revision.
- **Mandatory free-text annotation field** on every disposition. The reviewer's
  justification or commentary is part of the QA record. "Accepted Risk" without a
  written rationale is meaningless. All other dispositions benefit from annotation
  (e.g., Disagree: explain why the tool is wrong; Requires Discussion: who and what).
- **Dispositions must be exportable** for the project QA file. See Pattern 8 (Exportable
  QA Record) for format requirements.
- Phase 2 (Pre-Review with inline annotations, parked P-024 for Word taskpane): the
  accept/reject flow becomes directly relevant when Redline proposes edits or
  annotations in the document itself.
- **"Accept All" removed** (Graeme). Engineering findings are issues to investigate,
  not edits to accept. A reviewer who bulk-accepts without reading is in a worse
  position than having no tool at all — they have created a false record of review.
  If ever reintroduced, gate behind a confirmation that lists every single finding
  being accepted, forcing the reviewer to read what they are accepting.

**Design principle**: The Legal Agent optimises for speed (lawyers reviewing hundreds of
contracts). Pre-Review optimises for thoroughness (engineers reviewing one critical
report). The interaction tempo is different. The disposition workflow must support
deliberate, documented judgment — not rapid throughput.

---

## Pattern 4: Side Panel Interaction

**What the Legal Agent does**: Operates from a dedicated side panel in Word. Users type
questions or instructions, get streamed answers with citations, and review proposed
redline edits.

**Relevance to Pre-Review**: Low for Phase 1 (web-first), High for deferred Word
taskpane surface.

**Adaptation notes**:

- Phase 1 is web-first. The Pre-Review output is a standalone web view, not a Word side
  panel. This gives us more screen real estate and richer interaction options than a
  constrained 320-400px panel.
- The conversational interaction model (type a question, get a streamed answer) conflicts
  with Redline's design principle: "Do not use chatbot popups or conversational UI
  patterns. Redline is not a chatbot. The interaction model is annotation and review, not
  conversation." The Legal Agent is explicitly conversational; Pre-Review is explicitly
  not.
- When the Word taskpane surface is eventually designed (post-P-024 unfreeze), the side
  panel constraint (320-400px width) will force significant layout adaptation. Design
  the web-first output format with a content hierarchy that can degrade gracefully into
  a narrow panel — do not design a wide-screen layout that cannot be reflowed.
- Record this as a forward-compatibility concern: every web-first layout decision should
  be checked against "could this work in a 380px-wide panel?"

---

## Patterns 5-8: Missing Review Workflow Patterns (Graeme)

Four patterns that Graeme identified as fundamental to how senior reviewers actually work.
These were absent from the initial design reference and must be addressed in the
Pre-Review design.

### Pattern 5: Section-Anchored Findings

The primary view must be organised by report section, not a flat severity-sorted list.
Reviewers work through a report section by section. A flat list sorted by severity forces
jumping between Section 2, Section 8, Section 3 — destroying the reviewer's mental model
of the document.

The section-anchored view uses the document's own section structure as the navigation
frame. Within each section, findings are grouped by category (Pattern 1) and colour-coded
by severity.

A secondary "all findings" view sorted by category or severity may exist for summary
purposes, but the section-anchored view is the default working view.

### Pattern 6: Progress Tracking

GIR review is a 2-4 hour session with interruptions (phone calls, site queries, other
projects). The tool must provide persistent session state:

- "7 of 12 sections reviewed, 4 findings undispositioned."
- Visual indicator per section: not started / in progress / complete.
- Resume capability — the reviewer returns to exactly where they left off.

This is not a nice-to-have. Without it, the reviewer must manually track where they
stopped, which negates the efficiency gain the tool provides.

### Pattern 7: Finding Confidence and Provenance

Every finding must carry a provenance indicator distinguishing:

- **Deterministic findings** — produced by rule-based checking (word search, clause
  match, section presence check). High confidence. Low false positive rate.
- **LLM-based findings** — produced by language model judgment (e.g., "conclusions may
  not be fully supported by data"). Variable confidence. Higher false positive rate.

Reviewers calibrate attention completely differently for each type. A deterministic
finding ("NZS 4431:2015 is superseded") can be verified in seconds. An LLM finding
("recommendations may contain absolute language") requires careful reading.

Mixing the two without distinction erodes trust in both. The provenance indicator
should be visible in the finding card/row — not hidden behind a detail expansion.

### Pattern 8: Exportable QA Record

All findings, dispositions, annotations, and session metadata must be exportable as a
structured document to attach to the project QA file alongside the Section B Review
Checklist.

Supported export formats: PDF (for formal record), DOCX (for editing), CSV (for
spreadsheet analysis). The export must be format-agnostic enough to attach to any
firm's document control platform (Aconex, ProjectWise, SharePoint).

If findings are trapped in a web interface with no export path, the tool is disconnected
from real QA workflows and will not be adopted.

---

## Cross-Cutting Observations

### Web-First Advantages Over Word-Native

Redline's web-first delivery is not a limitation — it is a UX opportunity:

- **Richer citation previews**: hover tooltips, side-by-side standard text, expandable
  context. A Word side panel cannot do this well.
- **Full colour and typography control**: no dependency on Word's theme engine.
- **Responsive layout**: can optimise for desktop review (primary) while supporting
  tablet viewport for site visits.
- **Interactive filtering and sorting**: findings can be filtered by severity, standard,
  section — impossible in a static Word panel.

### AI Language Policy Compliance

All four Legal Agent patterns use first-person AI voice ("I found", "I recommend").
Redline's AI Language Policy prohibits this. Every pattern adopted must be reframed:

- Not "I found 3 issues in Section 4" -> "3 issues identified in Section 4"
- Not "I recommend changing..." -> "Suggested revision: ..."

### Switzerland-Neutral Alignment

The Legal Agent's "advisory only, human oversight required" posture matches Redline's
positioning. The UI patterns that enforce this (nothing auto-applied, everything requires
explicit user action) are the right foundation. Pre-Review should feel like a review
checklist the engineer works through, not an AI that has already decided.

### Tool Boundary: Completeness vs Correctness (Graeme)

The tool should check "is this item present?" (legitimate completeness check) but must
not check "is this item correct?" (engineering judgment). Example: "No Factor of Safety
stated" is legitimate. "Factor of Safety = 1.2 may be insufficient" is overstepping.

High false positive rate is the primary adoption killer. Precision matters more than
recall for senior reviewer time. A reviewer who must dismiss 30 false alarms to find
3 real issues will stop using the tool after the second report.

### Adoption Criteria (Graeme)

**Use it if**:
- Catches mechanical issues faster than manual pass (60 seconds vs 20-30 minutes).
- Section-anchored view matches how reviewers actually work.
- Exportable QA record integrates with existing project file workflows.
- Clear provenance — reviewer knows which findings are deterministic vs LLM-based.
- Honest about limitations — explicitly states "Not checked — engineering judgment
  required" rather than implying comprehensive coverage.

**Dismiss it if**:
- False positive rate exceeds 20% — reviewer time wasted on noise.
- Flat severity-sorted lists force jumping around the document.
- No export path — findings trapped in a web interface.
- Deterministic and LLM-based findings mixed without distinction.
- AI voice used in findings ("I found", "I recommend").

---

## Next Actions

- When Mark's Pre-Review PRD is ready, revisit this note and map each pattern (including
  Patterns 5-8) to specific PRD requirements.
- Flag the document-rendering question (Pattern 2, location citations) to Peter early —
  it has architecture implications.
- Flag the cross-reference citation type (Pattern 2) to Peter — internal consistency
  checking requires document-position mapping between two locations.
- Flag the export format requirements (Pattern 8) to Peter — architecture must support
  PDF/DOCX/CSV export of the full QA record.
- Define the provenance classification rules (Pattern 7): which specific checks are
  deterministic vs LLM-based. This is an engineering question with UX implications.
- Route the section-anchored view question (Pattern 5) to Peter: should the view use the
  document's actual section numbering (varies by firm template) or a normalised
  structure?
- Route disposition workflow (Pattern 3) through John for micro-copy review — the six
  disposition labels and their free-text prompts are conversion-relevant copy.
