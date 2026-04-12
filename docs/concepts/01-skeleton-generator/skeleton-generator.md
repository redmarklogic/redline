# Concept: Report Skeleton Generator

> **Audience**: Product owners, automation engineers, and domain engineers.
> This document describes an automated pipeline that ingests pre-field
> contractual documents (RFP, LOE, client communications) and produces a
> structured Word document skeleton -- ready for an author to refine,
> not write from scratch.

---

## Table of Contents

1. [Problem Statement](#1-problem-statement)
2. [Vision](#2-vision)
3. [Acceptance Criteria](#3-acceptance-criteria)
4. [Inputs and Outputs](#4-inputs-and-outputs)
5. [Incremental Delivery Steps](#5-incremental-delivery-steps)
6. [Architecture Overview](#6-architecture-overview)
7. [Dependencies](#7-dependencies)
8. [Deferred Work](#8-deferred-work)
9. [Relationship to Incumbent Process](#9-relationship-to-incumbent-process)
10. [Open Questions](#10-open-questions)

---

## 1. Problem Statement

Today, authors start report drafting with a near-blank template
(see [incumbent-process.md](./incumbent-process.md),
Phase 2 and Gap G2). The decision of which sections to include is
experience-dependent rather than rule-driven, and there is no formal
traceability from the client brief to report sections (Gap G3).
This leads to:

- Structural misalignment with the brief discovered late in the review cycle.
- Skilled engineers spending time on low-value formatting work (Gap G4).
- Inconsistent skeletons across authors and projects.

---

## 2. Vision

An AI-powered pipeline that takes contractual inputs available **before**
the desktop study begins and produces a Word document skeleton that an
intermediate or senior engineer can open and immediately start editing.

The author's first action is **editing and validating**, not writing.
The skeleton replaces the blank canvas.

### Scope boundary

This tool produces a **Phase 2 artifact** (skeleton creation) -- not a
Phase 4 artifact (drafted report). It slots into the existing PD/PM
skeleton approval gate. It does not bypass human review.

### Anti-goals

- The skeleton must **not** contain speculative engineering content.
- No guessed ground models, assumed foundation types, or fabricated
  parameters.
- Anything requiring field data or desktop study outputs appears as a
  placeholder with specific questions -- never as filled-in content.

---

## 3. Acceptance Criteria

The skeleton is "done" when an intermediate or senior engineer can open
the Word document and confirm:

| #   | Criterion | Category | Verification | Step |
|-----|-----------|----------|--------------|------|
| AC1 | **Client Summary (default) or Executive Summary (only if LOE requests it)** is present as front matter. Client Summary is max 1 page, plain language, with placeholders for: LOE reference, report purpose, proposed works, cost/programme impacts, geotechnical risks, and further work statement. | Structure | Automated check on heading name; manual review of placeholder prompts. | 1 |
| AC2 | **All mandatory GIR sections** are present, correctly numbered, in the standard order: Document Control, ToC, Client Summary, Sections 1--6, References, Appendices A--D. No mandatory section is missing. | Structure | Diff against the canonical section list. | 1 |
| AC3 | **Conditional sections** (slope stability, fault rupture, ground improvement, foundation assessment) are included or excluded based on explicit rules tied to project scope, location, and infrastructure type. Liquefaction Assessment is mandatory for all NZ sites and is always included. The inclusion decision is logged. | Structure | Review processing log for inclusion/exclusion rationale. | 1 |
| AC4 | **Geotechnical Model Table** in Section 2.1.4 is present as an empty table with mandatory column headers (Layer/Unit, Description, Depth, RL, Thickness, Typical Test Values). No text-only soil profile placeholder is used. | Structure | Automated check for table presence and header names. | 1 |
| AC5 | **Project metadata** (project number, client name, site address, date, document naming per `[JobNo]-RPT-GT-[Element]-[Seq]`) is populated from the RFP/LOE. No `[INSERT X]` remains for data that existed in the inputs. | Metadata | Spot-check against source documents. | 2 |
| AC6 | **Traceability matrix** maps every RFP/LOE deliverable to a report section. Unmapped deliverables are flagged. This matrix acts as the "touchstone" for the PD/PM skeleton review gate. | Traceability | Review matrix; verify no orphaned deliverables. | 3 |
| AC7 | **Legal boilerplate** (Applicability section) contains all mandatory clauses: Exclusive Use (with client name, project scope, temporal boundary), Inferred Conditions, Observation Disclaimer. Council/Regulatory Authority clause is included when the RFP indicates a consent application. | Liability | Automated check for clause presence; manual review of tailoring. | 7 |
| AC8 | **Residual Geotechnical Risk** section (Section 4) is present with a domain-specific placeholder prompt requiring the author to explicitly evaluate and articulate site-specific residual risks. No generic boilerplate is used for this section. | Liability | Read placeholder; confirm it requires project-specific risk articulation. | 8 |
| AC9 | **Section-specific placeholder questions** are present in every incomplete section. Questions are domain-specific (sourced from the standards registry and industry guidance), not generic `[TODO]`. Each question names the relevant standard and clause. | Content quality | Read placeholders in Sections 2 and 3; confirm they match the domain prompts from the Workflows notebook. | 8 |
| AC10 | **Standards references** per section are present, citing specific clause numbers from NZS 3604, NZS 1170.5, NZGS guidelines, and applicable council requirements. Standards are sourced from the Standards Registry. | Compliance | Cross-check per-section standards against the registry. | 6 |
| AC11 | **Formatting compliance**: Calibri 11pt body, Calibri Bold headings, sentence case headings, flush-left numbering, three-level bullet hierarchy (bullet/dash/hollow circle), NZ English spelling, one-space-before-units, labels above tables and below figures. | Style | Automated style check or manual review against structural checkpoints. | 0 |
| AC12 | **No structural defects**: No stacked headings (two consecutive headings without intervening text), no lone subdivisions, no widowed headings, no undefined acronyms. | Style | Automated or manual structural review. | 1 |
| AC13 | **Appendix ordering** matches the order of first reference in the main text. If a separate GFR exists, appendices cross-reference the GFR rather than duplicating raw data. | Structure | Manual check of cross-references. | 1 |
| AC14 | **Company Word template** (`.dotx`) is used as the base. Cover page, styles, and brand identity come from the template, not from generic formatting. | Template | Visual inspection. | 0 |
| AC15 | **The author's first action is editing, not writing.** The skeleton provides enough structure, metadata, standards references, and actionable questions that an intermediate engineer can begin refining immediately without needing to add sections or research which standards apply. | Value | Qualitative feedback from at least one practising engineer. | All |

---

## 4. Inputs and Outputs

### Inputs

| Input | Format | Required? | Content |
|-------|--------|-----------|---------|
| RFP / Client Brief | PDF, DOCX | At least one of RFP or LOE | Scope, deliverables, timeframes, terms. |
| LOE / Contract | PDF, DOCX | At least one of RFP or LOE | Agreed scope, fee, programme, T&Cs. |
| Client communications | MSG, EML | Optional | Post-sign-off clarifications, additional instructions. |
| Company Word template | DOTX | Required (can use a default) | Corporate formatting, styles, logos. |
| Standards registry | Structured data | Required | Rules dispatched per section category (see [02-standards-registry](../02-standards-registry/standards-registry.md)). |

### Outputs

| Output | Format | Description |
|--------|--------|-------------|
| Report skeleton | DOCX | Word document with sections, metadata, placeholders, traceability matrix, standards notes, boilerplate. |
| Traceability matrix | Table within the DOCX (and optionally a separate artifact) | Maps each RFP/LOE deliverable to the report section that addresses it. |
| Processing log | Structured text / JSON | What was extracted, what was not found, confidence indicators. |

---

## 5. Incremental Delivery Steps

Each step produces a standalone useful artifact. Steps are cumulative --
each builds on the output of the previous one.

| Step | Name | Description | Output after this step |
|------|------|-------------|----------------------|
| 0 | **Template ingestion** | Ingest the company Word template (`.dotx`) as the base for all output. All subsequent steps cast content into this template. | Empty DOCX in company style. |
| 1 | **Mandatory sections** | Insert all mandatory GIR sections and subsections (headings, document control table, version control table, table of contents placeholder). Define explicitly which sections are always included vs. conditional. | DOCX with correct section structure, no content. |
| 2 | **Project metadata** | Extract and populate project number, client name, address, date, document naming convention from the RFP/LOE. | DOCX with sections + populated metadata. |
| 3 | **Traceability matrix** | Parse RFP/LOE deliverables; generate a table mapping each to a report section. Flag unmapped items. | DOCX with sections + metadata + traceability table. |
| 4 | **Abstract and introduction** | Draft the abstract/executive summary and introduction sections from contractual materials. | DOCX with sections + metadata + traceability + intro draft. |
| 5 | **Scope extraction** | Extract project scope, client drivers, deliverables, timeframes, contractual terms. Populate relevant sections or generate a structured checklist. | DOCX with richer content in scope-related sections. |
| 6 | **Standards and guidelines** | Query the standards registry for rules applicable to this project type, jurisdiction, and infrastructure category. Insert standard references and specific clause notes into each relevant section. | DOCX with standards notes per section. |
| 7 | **Applicability clauses** | Select and insert the correct combination of boilerplate clauses based on project type, client, and regulatory context. | DOCX with legal boilerplate tailored to the project. |
| 8 | **Actionable placeholders** | For every section that cannot be completed without field data or desktop study, insert specific questions the author must answer. Emphasise relevant standards and industry guidelines. | Complete skeleton meeting all acceptance criteria. |

### Section inclusion rules (Step 1 detail)

For the GIR document type, the following sections are **always included**:

```
Document Control
Table of Contents
Client Summary  (use "Executive Summary" only if the LOE explicitly requests it)

1   Introduction
    1.1  Scope of Work  (always included by default)
    1.2  Site Description
    1.3  Proposed Development

2   Assessment and Interpretation of Site Conditions
    2.1  Ground and Groundwater Conditions
        2.1.1  Geology
        2.1.2  Previous Investigations
        2.1.3  Current Investigations
        2.1.4  Geotechnical Model  [empty table: Layer/Unit | Description | Depth | RL | Thickness | Typical Test Values]
        2.1.5  Groundwater
    2.2  Seismic Hazard
        2.2.1  Seismic Site Subsoil Class
        2.2.2  Ground Shaking Hazard
    2.3  Liquefaction Assessment  (mandatory -- included for all NZ sites by default)

4   Residual Geotechnical Risk
5   Further Work
6   Applicability

References

Appendices  (ordered by first reference in main text)
    Appendix A  Figures
    Appendix B  Previous Investigations
    Appendix C  Investigation Logs
    Appendix D  Geotechnical Laboratory Test Results
```

**Conditional sections** (included based on scope/project type -- inclusion decision logged):

- **Section 2.4: Other Geotechnical Hazards** -- auto-created as a parent H2 heading
  when any of its child sections are enabled. Sub-sections inserted as H3 headings:
  - 2.4.1  Slope Stability (when `slope_stability=True`)
  - 2.4.2  Fault Rupture Hazard (when `fault_rupture=True`)
  If neither child is enabled, the parent heading is omitted entirely.
- **Section 2.5: Geotechnical Issues Identified** -- optional summary table.
- **Section 3: Foundation Assessment** -- only when the LOE specifically requires foundation
  design or engineering parameters (when `foundation_assessment=True`).
  - 3.1  Foundation Options
  - 3.2  Foundation Design Parameters
  - 3.X  Ground Improvement (only when `ground_improvement=True` AND
    `foundation_assessment=True` -- `ground_improvement` is ignored when
    `foundation_assessment=False` because it is a child of Foundation Assessment)

---

## 6. Architecture Overview

```
                    +------------------+
                    |  Input Documents |
                    |  (RFP, LOE, MSG) |
                    +--------+---------+
                             |
                             v
                   +---------+----------+
                   |  Document Parser   |
                   |  (PDF/DOCX/MSG     |
                   |   extraction)      |
                   +---------+----------+
                             |
                             v
                   +---------+----------+
                   |  CrewAI Pipeline   |
                   |  (Steps 1-8)       |
                   |                    |
                   |  Agents:           |
                   |  - Extractor       |
                   |  - Section Builder |
                   |  - Standards Mapper|
                   |  - Formatter       |
                   +---------+----------+
                             |
                             |  queries
                             v
                   +---------+----------+
                   |  Standards Registry|
                   |  (see concept 02)  |
                   +--------------------+
                             |
                             v
                   +---------+----------+
                   |  marker package    |
                   |  (DocumentFacade)  |
                   |   |               |
                   |   +- python-docx   |
                   |   +- (future       |
                   |      engines)      |
                   +---------+----------+
                             |
                             v
                   +---------+----------+
                   |  Report Skeleton   |
                   |  (.docx)           |
                   +--------------------+
```

### Key technical considerations

- **Document parsing is the hard part.** Reliable extraction from messy
  contractual PDFs is where most debugging time will be spent. The LLM
  calls are comparatively straightforward.
- **python-docx** for Word generation, accessed through a `DocumentFacade`
  protocol in the `marker` sibling package. The facade decouples business
  logic from engine specifics, allowing future engine swaps (e.g.,
  ONLYOFFICE document-builder for post-processing). See
  [ADR-001](../../adr/adr-001-docx-generation-engine-facade.md).
- **CrewAI** orchestrates the multi-step pipeline with specialised agents
  for extraction, section building, and formatting. Note: CrewAI is
  deferred for the initial phases (0-3) which use pure DOCX generation
  with no LLM. CrewAI enters when LLM agents are introduced in Phase 4+.

---

## 7. Dependencies

| Dependency | Type | Notes |
|------------|------|-------|
| Standards Registry | Concept | See [02-standards-registry](../02-standards-registry/standards-registry.md). The skeleton generator consumes the registry but does not build it. Start with a hand-curated rule set. |
| Company Word template | Artifact | Must be provided by the client organisation. |
| Incumbent process documentation | Reference | See [incumbent-process.md](./incumbent-process.md). |

---

## 8. Deferred Work

The following items are out of scope for the initial concept but are
noted for future consideration.

| Item | Rationale for deferral |
|------|----------------------|
| **Feedback mechanism** | Design the feedback loop (diffing skeleton vs. author's edited version, or structured feedback table) after real skeletons are being used by real authors. Learn from observation, not speculation. |
| **GFR skeleton** | Start with GIR only. Extend to GFR and other document types after the GIR skeleton is validated. |
| **Multi-jurisdiction support** | Start with NZ standards and a single council. Expand jurisdiction coverage via the standards registry. |
| **Automated template learning** | Automatically learning company template structure from examples rather than manual template configuration. |

---

## 9. Relationship to Incumbent Process

This concept addresses:

- **Gap G2** (ad-hoc skeleton creation) -- replaces experience-dependent
  section selection with rule-driven generation.
- **Gap G3** (no brief-to-section traceability) -- the traceability matrix
  makes deliverable coverage explicit and auditable.
- **Gap G4** (formatting consumes author time) -- the skeleton arrives
  pre-formatted in the company template.
- **Gap G7** (manual boilerplate insertion) -- Applicability clauses are
  selected and inserted automatically.

It implements automation opportunities:

- **A1** (skeleton generation from LOE) -- the core capability.
- **A2** (brief-to-section traceability matrix) -- Step 3.
- **A5** (boilerplate and disclaimer management) -- Step 7.

---

## 10. Open Questions

| #  | Question | Impact |
|----|----------|--------|
| Q1 | Should the Client Summary placeholder include a maximum word count (vs. "one page") since page length depends on formatting? | Affects AC1 verification. |
| Q2 | How should the skeleton handle Canterbury-specific requirements (MBIE Part D, CCC Appendix I/II) -- as conditional sections triggered by location, or as a separate Canterbury GIR variant? | Affects Step 1 section rules and Standards Registry scope. |
| Q3 | ~~Section 1.1 (Scope of Work) is conditional -- "required unless the Introduction adequately covers the scope." How should the AI decide this? Default to including it?~~ **Resolved**: Always include Section 1.1 by default. The AI cannot reliably judge whether the Introduction "adequately covers" scope. The author can remove it during editing if redundant. | ~~Affects Step 1 section rules.~~ |
| Q4 | Should formatting compliance (AC11) be checked by the skeleton generator itself, or deferred to a separate QA tool? | Architecture decision affecting Step 0 scope. |
| Q5 | How will the Residual Geotechnical Risk placeholder prevent the engineer from relying on generic automated text? Should there be a "this section requires site-specific content" watermark? | Affects AC8 design and liability exposure. |
| Q6 | How should confidence be communicated to the author? (e.g., "AI-extracted -- verify" vs. "Confirmed from contract") | Affects trust and adoption. |
| Q7 | What MSG/EML parsing quality is achievable? Are client emails structured enough to extract useful scope clarifications? | Affects Step 5 reliability. |
| Q8 | Should the traceability matrix be a separate document or embedded in the skeleton? | Affects PD/PM review workflow. |
