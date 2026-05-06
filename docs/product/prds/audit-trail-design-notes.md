# Audit Trail UX: Design Notes and Open Questions

**Status**: Design exploration. **Owner**: Mark. **Date**: 2026-05-05.
**Related PRD**: [audit-trail-day1-requirement.md](audit-trail-day1-requirement.md)
**Mockups**: `output/mockups/audit-trail-*.html` (not version-controlled)

## Design Decisions (Confirmed)

### 1. Document-level sign-off, not section-level

**Decision**: The audit trail sign-off is at the report level (Author + Reviewer).
Section-level sign-off is deferred until user interviews confirm demand.

**Rationale** (Graeme): Standard single-discipline reports (GIR, GIntR) use
document-level sign-off. Section-level review was only observed in large
multi-disciplinary design reports where different Technical Directors reviewed
their discipline sections. That is an edge case.

**Null hypothesis**: Users will wait until the entire document is complete and then
sign, even if section-level sign-off is available. Validate with user interviews
before building section-level.

### 2. Two-tier signature block (minimum)

**Decision**: Model Author ("Prepared by") and Reviewer ("Reviewed by") as two
signature roles. Support an optional third tier (Technical Reviewer separate from
Practice Director) for large firms.

**Rationale** (Graeme):
- Large firms (100+ staff): three-tier (Author, TR, PD) -- genuinely separate people.
- Medium firms (20-50): two-tier, PD often doubles as TR.
- Small firms (5-15): effectively single-signer (the principal).

### 3. Audit trail lives on page 2 (document control page)

**Decision**: The provenance summary and Pre-Review results appear on the standard
document control page (page after cover page), alongside the revision history table
and signature block. Not a separate certificate or appendix.

**Rationale** (Graeme): This is where document control information already lives in
every engineering report. The revision history table (Rev | Date | Description |
Author | Approved) is the natural anchor point.

### 4. Two interaction surfaces: Word taskpane + web dashboard

**Decision**: The engineer interacts with Pre-Review inside Word (taskpane/sidebar).
The PD/QA manager gets a web dashboard showing portfolio-level report status.

**Rationale** (Graeme): These are two different personas doing two different jobs.
Engineers live in Word -- forcing them into a browser breaks adoption. PDs need
portfolio visibility -- they should not need to open each Word document.

### 5. Capture Pre-Review events only (not manual edits)

**Decision**: The audit trail records: Pre-Review ran, flags raised, flags resolved,
sign-off. It does not capture manual Word edits.

**Rationale** (Graeme):
- Signal-to-noise: most Word edits are formatting and typos.
- Legal relevance: insurers need "was there a structured review?" not "what did
  the engineer type?"
- Adoption risk: surveillance perception kills adoption.

**Phase 2 candidates**:
- Track Changes summary ("TR made 14 changes across 6 sections").
- Re-run deltas ("First Pre-Review: 12 flags. Second run after review: 2 flags").
- Deliberate section markers ("I have reviewed Section 4" in the taskpane).

## Open Questions (Require User Interviews)

### Q1. Section-level sign-off demand

Will engineers find value in marking individual sections as reviewed while working
through a report? Or will they complete the entire document and sign once at the end?

**Hypothesis**: Engineers will not use section-level sign-off. They review
sequentially and sign at the end. Section markers add friction without value.

**Test**: Show the document control page mockup (C-revised) to 3-5 engineers.
Ask: "Would you want to sign off each section individually, or just sign the
whole report at the end?"

### Q2. Word taskpane vs. web app for Pre-Review

Is a Word taskpane the right surface for the engineer's Pre-Review interaction?
Or would they accept a separate web interface?

**Hypothesis**: Word taskpane is strongly preferred. Engineers will resist
switching to a browser mid-review.

**Test**: Show both Mockup D (web UI) and a Word taskpane wireframe. Ask which
feels natural during a report review session.

### Q3. What constitutes a "Finalise" action?

For firms without formal PD sign-off checklists (medium and small firms), what
triggers the transition from "draft under review" to "issued"?

**Graeme's input**: Large firms have a PD checklist (Section B). Medium firms
email the PDF plus update an Excel register. Small firms just send the email.

**Design implication**: Redline needs a "Finalise Report" action that creates
the definitive end-event. For larger firms this maps to PD sign-off. For
smaller firms it replaces the implicit "I sent the email" trigger.

### Q4. PD dashboard: what status granularity?

The PD wants to see where each report is. What stages matter?

**Candidate stages**: Draft generated, Pre-Review complete, Author review in
progress, Author review complete, TR review in progress, TR review complete,
PD sign-off pending, Issued.

**Test**: Show Mockup E to a Practice Director. Ask: "Which of these stages
do you actually need to see? Which are noise?"

### Q5. Three-tier sign-off adoption

For large firms, is the TR role always separate from the PD, or do firms
sometimes collapse them even when they have the headcount?

**Test**: Interview 2-3 people from firms with 50+ staff. Do they actually
use three separate signatories, or is it aspirational?

### Q6. Information radiator surface and content for reviewer state orientation

*(Added 2026-05-06. Origin: strategy session — Graeme's structural orientation
insight + founder's information radiator idea. Framing: Ron.)*
*(Resolved 2026-05-06. Graeme practitioner feedback confirmed Candidate B.)*

**RESOLVED — Candidate B (Enhanced Document Control Page).**

Graeme's practitioner feedback confirmed that reviewers open the document first,
page 2 is the first substantive stop, and the coverage summary extends existing
provenance rather than introducing a new concept.

Candidate A demoted to supplement (PD dashboard can show coverage summary).
Candidate C deferred to P-024 unfreeze.

Full resolved design: `docs/product/prds/information-radiator-candidate-b-design.md`.
Practitioner feedback: `docs/knowledge/geotechnical/report-writing/information-radiator-practitioner-feedback.md`.

**One open sub-question for KR2 interviews**: coverage table ordering (section
number vs flag severity). Mark recommends section number with visual distinction;
Graeme recommends flag severity. Testable.

## Mockup Index

| Mockup | File | Status |
|---|---|---|
| A -- Appendix Table | `audit-trail-A-appendix-table.html` | Exploratory |
| B -- Inline Badges | `audit-trail-B-inline-badges.html` | Exploratory |
| C -- QA Certificate (original) | `audit-trail-C-qa-certificate.html` | Superseded |
| C -- Document Control Page (revised) | `audit-trail-C-doc-control-page.html` | **Active** |
| D -- Web UI Pre-Review | `audit-trail-D-web-ui-prereview.html` | Parked -- redesign as Word taskpane after Q2 |
| E -- Firm Dashboard | `audit-trail-E-firm-dashboard.html` | Parked -- validate stages with PD (Q4) |
