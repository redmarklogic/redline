# Acceptance Criteria for the GIR Skeleton Generator

**Date**: 2026-04-11
**Research question**: What must a well-formed GIR skeleton contain, and what
acceptance criteria ensure structural completeness, standards compliance,
traceability, and liability risk mitigation?
**Actor**: A product owner and automation engineer designing acceptance criteria
for an AI-generated Geotechnical Interpretive Report (GIR) skeleton, to be
reviewed by intermediate/senior engineers before fieldwork begins.
**Redline domains**: Skeleton Generator (Concept 01), Standards Registry
(Concept 02), incumbent report-writing process.

---

## Summary

Research across five knowledge bases reveals that the current acceptance criteria
in the skeleton-generator concept document are directionally correct but
insufficiently specific in three areas: (1) the mandatory legal boilerplate
clauses and their liability consequences are not enumerated; (2) the structural
formatting requirements (heading case, bullet hierarchy, table placement rules)
are missing as testable criteria; and (3) the placeholder questions for
incomplete sections should follow domain-specific prompts rather than generic
TODOs. This document synthesises findings into a refined, research-backed
acceptance criteria set.

## Findings

### 1. Mandatory structural elements and section ordering

The Geotechnical Engineering Report Workflows notebook establishes that a
well-formed GIR must follow a "logical, story-like flow" and contains both
mandatory and conditional sections.

**Front matter** (always required):

- Document Control and Table of Contents.
- **Client Summary** (not "Executive Summary") -- a maximum one-page
  plain-language summary of purpose, proposed works, geotechnical risks, and
  cost/programme impacts. An "Executive Summary" heading should only appear
  if explicitly requested by the client in the LOE; otherwise the default
  is "Client Summary" because executive summaries "carry a high risk of
  contradicting the main report or accidentally excluding critical legal
  limitations."

**Core sections** (always required for GIR):

- Section 1: Introduction (client, site, purpose, superseded reports).
- Section 1.1: Scope of Work -- conditional (required unless the Introduction
  adequately covers the scope); must never be a copy-paste of the LOE.
- Section 1.2: Site Description -- mandatory.
- Section 1.3: Proposed Development -- mandatory.
- Section 2: Assessment and Interpretation -- mandatory.
- Section 2.1: Ground and groundwater conditions -- mandatory, including
  geology, previous/current investigations, and groundwater.
- Section 2.1.4: Geotechnical Model Table -- mandatory as a structured table
  (text-only soil profile descriptions are "strictly prohibited because they
  are difficult to read"). The skeleton must include empty table headers.
- Section 2.2: Seismic shaking hazard -- mandatory for NZ sites.
- Section 2.3: Liquefaction assessment -- mandatory for most NZ sites.
- Section 4: Residual Geotechnical Risk -- mandatory. "Failing to report
  [residual risks] exposes the company to legal claims."
- Section 5: Further Work -- mandatory.
- Section 6: Applicability (legal boilerplate) -- mandatory.

**Conditional sections** (included based on scope):

- Section 2.4: Other geotechnical hazards (slope stability, fault rupture) --
  only when relevant to the site.
- Section 2.5: Geotechnical issues identified -- optional summary table.
- Section 3: Foundation Assessment -- only when the LOE specifically requires
  foundation design or engineering parameters.
- Section 3.X: Ground Improvement -- when natural ground is inadequate.

**Appendices** -- must appear in the order first referenced in the text:

- Appendix A: Figures (always).
- Appendices B/C/D: Investigation logs and lab results -- conditional. If a
  separate GFR is being produced, the GIR appendices should cross-reference
  the GFR rather than duplicating the raw data.

### 2. Quality gates before drafting begins

The Workflows notebook identifies two mandatory gates:

**Gate 1: The "Touchstone" (Scope of Works definition).** Before any other
section is written, the skeleton must contain a completed extraction of the
client's requirements, pain points, deliverables, timeframes, and wider goals
from the RFP/LOE. This acts as the "master checklist the engineer will
constantly refer back to while populating the draft."

**Gate 2: PD/PM Skeleton "Sense Check".** The Project Director or Project
Manager must verify that the AI has "successfully translated the client's
specific questions into customized sub-headings, ensuring that all required
points are captured and that the proposed structure correctly solves the
client's problem."

### 3. Formatting and style compliance

The Workflows notebook provides unambiguous formatting rules that the skeleton
must satisfy:

- **Font**: Calibri 11pt body; Calibri Bold headings sized by level.
- **Heading case**: Sentence case only (first word + proper nouns). Exception:
  legal Act documents are fully capitalised.
- **Numbering**: Flush left, no indentation.
- **Bullet hierarchy**: Level 1: solid bullet; Level 2: dash; Level 3: hollow
  circle.
- **Spacing**: One space after comma, colon, semi-colon, full stop. One space
  before unit abbreviations (e.g., "12 ha", "59 m2").
- **Spelling**: NZ English (e.g., "programme" not "program"). Maori macrons
  included where applicable.
- **Table/figure labels**: Labels above tables, below figures.
- **Document naming**: `[Job Number]-[Doc Type]-[Discipline]-[Element]-[Sequence]`
  (e.g., `1001234.1-RPT-GT-NRT-001`).

### 4. Legal boilerplate and liability exposure

The Risk Assessment notebook, analysed via Document Lifecycle Mapping,
identifies three mandatory legal clauses and one mandatory risk section, each
with specific liability consequences if omitted:

**Clause 1: Exclusive Use and Applicability.** Must state that the report
pertains only to the specific project and is not applicable to any other
project or site. Must establish a temporal boundary (e.g., if the project is
not initiated within eighteen months, the firm must re-confirm recommendations).
*Omission risk*: Courts have held professionals liable to "anyone they knew,
or should have known, would rely on their professional opinion." Without this
clause, the firm faces claims from unknown third parties (subsequent purchasers,
banks, bonding companies).

**Clause 2: Inferred Conditions.** Must state that "subsurface conditions
between boreholes are inferred and may vary significantly from conditions
encountered at the borings." *Omission risk*: A client could argue the report
implied uniform ground conditions, leading to negligence claims when adverse
conditions are found between investigation points.

**Clause 3: Observation Disclaimer.** Must state that conditions "refer only
to those observed at the place and time of observation" and can be
"significantly altered by construction activities" or seasonal changes.
*Omission risk*: Claims arising from changed site conditions over time.

**Clause 4 (conditional): Council/Regulatory Authority use.** Required when
the RFP indicates the report supports a consent application.

**Residual Geotechnical Risk section**: Must document risks remaining after
mitigation to ensure "the client retains ownership of those risks." Without
this, the client may assume hazards have been entirely eliminated and transfer
liability to the consultant.

### 5. NZ standards references for residential GIR

The Engineering Standards notebook identifies specific standard sections the
skeleton must reference:

- **NZS 3604:2011** -- Section 3.1.2 (Good Ground definition: 300 kPa
  bearing capacity); Section 3.2/3.3.7 (exclusions from good ground);
  Section 3.3.1/3.3.4 (Scala Penetrometer testing to 2m depth minimum);
  Section 17 (expansive soils -- liquid limit >50% or linear shrinkage >15%).
- **NZS 1170.5:2004** -- Section 3.1.3 (Site Subsoil Classification,
  Classes A-E).
- **NZGS Field Description of Soil and Rock (2005)** -- mandatory format for
  borehole and test pit log appendices.
- **NZGS Module 3** -- liquefaction hazard identification, assessment, and
  mitigation.
- **Council-specific** (Canterbury): MBIE Part D guidelines; CCC IDS Part 4;
  Port Hills hazard assessment (GNS Stage 1); Producer Statements (PS1, PS2a,
  PS4); HAIL site assessment; Statements of Professional Opinion
  (Appendix I/II).

### 6. Geotechnical Model Table structure

The skeleton must include an empty Geotechnical Model Table with the following
mandatory column headers:

| Column | Description |
|--------|-------------|
| Layer / Unit | e.g., Holocene Marine, Uncontrolled Fill |
| Description | Brief soil/rock composition |
| Top of Layer (m) / Depth | Depth from ground surface |
| Top of Layer (RL) | Elevation relative to datum |
| Layer Thickness (m) | Vertical extent |
| Typical Test Values | SPT N-values and/or CPT qc values |

### 7. Section-specific placeholder prompts

The Workflows notebook provides explicit prompts for sections that cannot be
completed before fieldwork. The skeleton should include these domain-specific
questions rather than generic `[TODO]` markers:

- **2.1.1 Geology**: "List the geological units which make up the soil/rock
  profile. Avoid irrelevant technical geological descriptions. Identify the
  name and location of known active faults relative to the site."
- **2.1.2/2.1.3 Investigations**: "Provide a bullet-point list of the
  investigation scope. Ensure cross-references to the location plan in
  Appendix A, and the logs/lab results in Appendices B, C, and D."
- **2.1.5 Groundwater**: "Outline the available groundwater information.
  Present conclusions in terms of RL. What are the anticipated effects of
  seasonal/tidal changes and climate change sea-level rise? State the design
  groundwater level for basement and foundation design."
- **2.2.1 Seismic site subsoil class**: "What is the assessed seismic site
  subsoil class? What is the basis for this assessment? Could further
  investigation modify this assessment?"
- **2.2.2 Ground shaking hazard**: "Present the Earthquake Magnitude (M) and
  Peak Ground Acceleration (PGA) for SLS, ULS, and any intermediate design
  cases."
- **3.1 Foundation options**: "Insert a simple options and relative merits
  table. State which foundation option the client/project team has formally
  selected. Do not present detailed designs for unselected options."
- **3.2 Foundation design parameters**: "State the information received from
  others that you relied upon (e.g., foundation loads, settlement tolerances).
  Provide design parameters for the selected option only."

### 8. Technical writing structural quality

The Engineers' Guide to Technical Communication notebook identifies common
structural defects that the skeleton should prevent by design:

- **Stacked headings**: Two consecutive headings with no text between them.
- **Lone headings**: A single subdivision (e.g., subsection A without B).
- **Widowed headings**: A heading at the bottom of a page without at least
  two lines of body text following it.
- **Missing introduction framework**: The introduction must contain
  placeholders for purpose, problem, scope, and document format.
- **Undefined acronyms**: Every acronym must be spelled out on first use.

### 9. Acceptance criteria format

The Writing Painless Product and Functional Specifications notebook recommends
against rigid Given/When/Then templates for product specifications, favouring
narrative scenarios with specific examples. However, for document generation
acceptance criteria, the notebook advises separating **feasibility risk**
("Can we build this?") from **value risk** ("Will the user use this?").
Structural correctness should be tested via automated checks; content
usefulness requires qualitative testing with real engineers.

---

## Implications for the Skeleton Generator

Based on these findings, the acceptance criteria in
[skeleton-generator.md](../concepts/01-skeleton-generator/skeleton-generator.md)
should be revised as follows:

### Revised acceptance criteria

| #   | Criterion | Category | Verification | Step |
|-----|-----------|----------|--------------|------|
| AC1 | **Client Summary (default) or Executive Summary (only if LOE requests it)** is present as front matter. Client Summary is max 1 page, plain language, with placeholders for: LOE reference, report purpose, proposed works, cost/programme impacts, geotechnical risks, and further work statement. | Structure | Automated check on heading name; manual review of placeholder prompts. | 1 |
| AC2 | **All mandatory GIR sections** are present, correctly numbered, in the standard order: Document Control, ToC, Client Summary, Sections 1-6, References, Appendices A-D. No mandatory section is missing. | Structure | Diff against the canonical section list. | 1 |
| AC3 | **Conditional sections** (liquefaction, slope stability, fault rupture, ground improvement, foundation assessment) are included or excluded based on explicit rules tied to project scope, location, and infrastructure type. The inclusion decision is logged. | Structure | Review processing log for inclusion/exclusion rationale. | 1 |
| AC4 | **Geotechnical Model Table** in Section 2.1.4 is present as an empty table with mandatory column headers (Layer/Unit, Description, Depth, RL, Thickness, Typical Test Values). No text-only soil profile placeholder is used. | Structure | Automated check for table presence and header names. | 1 |
| AC5 | **Project metadata** (project number, client name, site address, date, document naming per `[JobNo]-RPT-GT-[Element]-[Seq]`) is populated from the RFP/LOE. No `[INSERT X]` remains for data that existed in the inputs. | Metadata | Spot-check against source documents. | 2 |
| AC6 | **Traceability matrix** maps every RFP/LOE deliverable to a report section. Unmapped deliverables are flagged. This matrix acts as the "touchstone" for the PD/PM skeleton review gate. | Traceability | Review matrix; verify no orphaned deliverables. | 3 |
| AC7 | **Legal boilerplate** (Applicability section) contains all mandatory clauses: Exclusive Use (with client name, project scope, temporal boundary), Inferred Conditions, Observation Disclaimer. Council/Regulatory Authority clause is included when the RFP indicates a consent application. | Liability | Automated check for clause presence; manual review of tailoring. | 7 |
| AC8 | **Residual Geotechnical Risk** section (Section 4) is present with a domain-specific placeholder prompt requiring the author to explicitly evaluate and articulate site-specific residual risks. No generic boilerplate is used for this section. | Liability | Read placeholder; confirm it requires project-specific risk articulation. | 8 |
| AC9 | **Section-specific placeholder questions** are present in every incomplete section. Questions are domain-specific (sourced from the standards registry and industry guidance), not generic `[TODO]`. Each question names the relevant standard and clause. | Content quality | Read placeholders in Sections 2 and 3; confirm they match the domain prompts from the Workflows notebook. | 8 |
| AC10 | **Standards references** per section are present, citing specific clause numbers from NZS 3604, NZS 1170.5, NZGS guidelines, and applicable council requirements. Standards are sourced from the Standards Registry. | Compliance | Cross-check per-section standards against the registry. | 6 |
| AC11 | **Formatting compliance**: Calibri 11pt body, Calibri Bold headings, sentence case headings, flush-left numbering, three-level bullet hierarchy (bullet/dash/hollow circle), NZ English spelling, one-space-before-units, labels above tables and below figures. | Style | Automated style check or manual "20 Checkpoints" review (structural items: Checkpoints 1, 3, 4, 5, 13, 19). | 0 |
| AC12 | **No structural defects**: No stacked headings (two consecutive headings without intervening text), no lone subdivisions, no widowed headings, no undefined acronyms. | Style | Automated or manual structural review. | 1 |
| AC13 | **Appendix ordering** matches the order of first reference in the main text. If a separate GFR exists, appendices cross-reference the GFR rather than duplicating raw data. | Structure | Manual check of cross-references. | 1 |
| AC14 | **Company Word template** (`.dotx`) is used as the base. Cover page, styles, and brand identity come from the template, not from generic formatting. | Template | Visual inspection. | 0 |
| AC15 | **The author's first action is editing, not writing.** The skeleton provides enough structure, metadata, standards references, and actionable questions that an intermediate engineer can begin refining immediately without needing to add sections or research which standards apply. | Value | Qualitative feedback from at least one practising engineer. | All |

### Changes from the original acceptance criteria

| Original | Change | Rationale |
|----------|--------|-----------|
| AC1 (sections present) | Split into AC2 (mandatory sections), AC3 (conditional sections with logged rationale), AC4 (Geotechnical Model Table structure). | The original was too coarse. The table structure and conditional logic are independently testable. |
| AC2 (metadata populated) | Retained as AC5 with document naming convention added. | Document naming was implicit; now explicit and testable. |
| AC3 (traceability matrix) | Retained as AC6 with "touchstone" quality gate language added. | Connects to the PD/PM review gate from the Workflows notebook. |
| AC4 (actionable placeholders) | Split into AC9 (domain-specific questions per section) and AC8 (Residual Risk section). | The Residual Risk section has specific liability implications that warrant a separate criterion. |
| AC5 (standards per section) | Retained as AC10. | No change needed. |
| AC6 (boilerplate) | Expanded into AC7 (enumerates all four clause types with liability rationale) and AC1 (Client Summary vs Executive Summary distinction). | The original did not distinguish the specific mandatory clauses or the Client Summary requirement. |
| AC7 (company template) | Retained as AC14. | No change needed. |
| AC8 (author edits not writes) | Retained as AC15 with explicit value-testing requirement. | Added qualitative testing requirement per Product Specs notebook. |
| *New* AC11 | Added: formatting compliance. | Was entirely absent from original; these are testable, automatable requirements. |
| *New* AC12 | Added: no structural defects. | Common rework causes identified by the Technical Writing notebook. |
| *New* AC13 | Added: appendix ordering. | Domain-specific requirement from the Workflows notebook. |

---

## Open Questions

| # | Question | Source |
|---|----------|--------|
| Q1 | Should the Client Summary placeholder include a maximum word count (vs. "one page") since page length depends on formatting? | Workflows notebook |
| Q2 | How should the skeleton handle the Canterbury-specific requirements (MBIE Part D, CCC Appendix I/II) -- as conditional sections triggered by location, or as a separate Canterbury GIR variant? | Engineering Standards notebook |
| Q3 | The Workflows notebook states that Section 1.1 (Scope of Work) is conditional -- "required unless the Introduction adequately covers the scope." How should the AI decide this? Default to including it? | Workflows notebook |
| Q4 | Should formatting compliance (AC11) be checked by the skeleton generator itself, or deferred to a separate "Faultless" QA tool? | Architecture decision |
| Q5 | The Risk Assessment notebook asks: how will the Residual Geotechnical Risk placeholder prevent the engineer from relying on generic automated text? Should there be a "this section requires site-specific content" watermark? | Risk Assessment notebook |

---

## Glossary

| Term | Definition |
|------|------------|
| GIR | Geotechnical Interpretive Report -- the primary engineering deliverable interpreting ground conditions and providing design recommendations. |
| GFR | Geotechnical Factual Report -- an objective record of field and lab data with no interpretation. |
| LOE | Letter of Engagement -- the binding contract between the engineering firm and the client. |
| RFP | Request for Proposal -- the client's formal invitation defining requirements. |
| Client Summary | A max-one-page, plain-language front matter section summarising key findings for non-technical readers. Preferred over "Executive Summary." |
| Touchstone | The extracted scope-of-works requirements used as a master checklist throughout drafting to verify the report addresses every client requirement. |
| Geotechnical Model Table | A structured table (not narrative text) presenting the soil/rock profile with standardised columns. |
| Residual risk | The level of geotechnical risk remaining after the engineer has applied mitigations and design recommendations. |
| RL (Reduced Level) | An elevation relative to a specified standard datum. |
| SPT | Standard Penetration Test -- measures blow count (N-value) to infer soil density and strength. |
| CPT | Cone Penetration Test -- measures tip resistance to infer soil stratigraphy and properties. |
| NZS 3604 | NZ standard for timber-framed buildings -- defines "good ground" criteria. |
| NZS 1170.5 | NZ standard for earthquake loading -- defines site subsoil classification. |
| NZGS | New Zealand Geotechnical Society -- provides professional practice guidelines. |
| SLS / ULS | Serviceability Limit State / Ultimate Limit State -- structural design criteria for normal use vs. extreme loads. |
| Scala Penetrometer | A field testing device driven into the ground to measure soil resistance; mandatory under NZS 3604. |

---

## Sources Consulted

| Notebook | Queries asked | Key citations |
|----------|--------------|---------------|
| Geotechnical Engineering Report Workflows and Standard Procedures | 4 | Mandatory sections, Client Summary vs Executive Summary distinction, Geotechnical Model Table format, section-specific placeholder prompts, 20 Checkpoints checklist, PD/PM skeleton review gate. |
| Engineers' Guide to Technical Communication and Writing | 1 | Front matter configuration, appendix ordering, cross-referencing best practices, structural defects (stacked/lone/widowed headings), introduction framework requirements. |
| Engineering Standards (NZ) | 1 | NZS 3604 sections 3.1.2/3.2/3.3/17, NZS 1170.5 section 3.1.3, NZGS Field Description guidelines, NZGS Module 3, Canterbury council requirements (MBIE Part D, CCC IDS Part 4, Producer Statements). |
| Risk Assessment in Engineering | 3 | Exclusive Use clause purpose and liability, Inferred Conditions disclaimer, Observation Disclaimer, Residual Geotechnical Risk section role in liability mitigation, Document Lifecycle Mapping analysis. |
| Writing Painless Product and Functional Specifications | 1 | Acceptance criteria format (narrative over Given/When/Then), feasibility vs value risk separation, vertical slice decomposition, edge case documentation. |
