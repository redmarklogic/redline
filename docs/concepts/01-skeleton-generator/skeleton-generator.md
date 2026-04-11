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

| #  | Criterion | Verification |
|----|-----------|--------------|
| AC1 | Every mandatory section and subsection for the target document type (starting with GIR) is present, correctly numbered, in the right order. | Compare against the standard skeleton headings in the incumbent process. |
| AC2 | Project metadata (number, client name, address, date, document naming) is populated from the contract/RFP -- no `[INSERT X]` for information that existed in the inputs. | Spot-check against source documents. |
| AC3 | A traceability matrix maps every RFP/LOE deliverable to a report section. No deliverable is orphaned. | Review the matrix; flag any unmapped items. |
| AC4 | Each incomplete section has **specific, actionable questions** the author needs to answer -- not generic `[TODO]`. Example: Section 2.4 should ask *"What is the site subsoil class per NZS 1170.5? What is the design PGA for the return period specified in the brief?"* | Read placeholders; confirm they are section-specific and answerable. |
| AC5 | Each section names the applicable standards and highlights the specific clauses relevant to this project type and location. | Cross-check against the standards registry (see [02-standards-registry](../02-standards-registry/standards-registry.md)). |
| AC6 | Boilerplate clauses (Applicability, disclaimers, document control, version table) are present and tailored to the project type. | Compare against the Style Reference Guide requirements. |
| AC7 | The output uses the company Word template (`.dotx`), not a generic style. | Visual inspection. |
| AC8 | The author's first action is editing, not writing. They refine existing content, answer specific questions, and delete irrelevant sections. | Author feedback. |

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

### Section inclusion rules (Step 1 detail -- to be refined)

For the GIR document type, the following sections are **always included**:

```
Document Control
Table of Contents
Executive Summary

1   Introduction
    1.1  Scope of Work
    1.2  Site Description
    1.3  Proposed Development

2   Assessment and Interpretation of Site Conditions
    2.1  Ground and Groundwater Conditions
    2.2  Geotechnical Model
    2.3  Groundwater
    2.4  Seismic Hazard
    2.5  Geotechnical Issues Identified

3   Foundation Assessment
    3.1  Foundation Options
    3.2  Foundation Design Parameters

4   Residual Geotechnical Risk
5   Further Work
6   Applicability

References

Appendices
    Appendix A  Figures
    Appendix B  Previous Investigations
    Appendix C  Investigation Logs
    Appendix D  Geotechnical Laboratory Test Results
```

**Conditional sections** (included based on scope/project type):

- 2.X Liquefaction Assessment -- when site is in a liquefaction-prone area
- 2.X Slope Stability -- when slopes are within the project footprint
- 2.X Fault Rupture Hazard -- when active faults are mapped near the site
- 3.X Ground Improvement -- when natural ground is inadequate for the proposed loads

The conditions for including or excluding these sections will be refined
through research and author feedback.

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
                   |  DOCX Generator    |
                   |  (python-docx /    |
                   |   docxtpl)         |
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
- **python-docx or docxtpl** for Word generation -- must support company
  template styles, not just content insertion.
- **CrewAI** orchestrates the multi-step pipeline with specialised agents
  for extraction, section building, and formatting.

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
| Q1 | Which conditional sections should be included/excluded by default for a standard residential GIR? | Affects Step 1 section rules. |
| Q2 | What is the minimum viable set of standards for the initial registry? NZS 3604, NZS 1170.5, and what else? | Affects Step 6 quality. |
| Q3 | How should confidence be communicated to the author? (e.g., "AI-extracted -- verify" vs. "Confirmed from contract") | Affects trust and adoption. |
| Q4 | What MSG/EML parsing quality is achievable? Are client emails structured enough to extract useful scope clarifications? | Affects Step 5 reliability. |
| Q5 | Should the traceability matrix be a separate document or embedded in the skeleton? | Affects PD/PM review workflow. |
