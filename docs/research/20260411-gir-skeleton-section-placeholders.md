# GIR Skeleton: Section-by-Section Placeholder Content and Standards Reference

**Date**: 2026-04-11
**Research question**: For each mandatory and conditional section of a
Geotechnical Interpretive Report (GIR) skeleton, what are the trigger
conditions, structural elements, mandatory tables, applicable NZ standards,
and specific actionable placeholder questions the skeleton must inject for
the author?
**Actor**: A product owner and automation engineer scoping incremental
delivery sub-steps for the Report Skeleton Generator. Each sub-step
releases one section's capability as a standalone artifact.
**Redline domains**: Skeleton Generator (Concept 01), Standards Registry
(Concept 02), execution plan sequencing.

---

## Summary

This research session covers every GIR section from Document Control
through Appendices, providing the exact structural requirements, trigger
conditions, mandatory tables, NZ standards references, and placeholder
prompts the skeleton must inject. The output is directly usable as the
content specification for each incremental delivery sub-step. A companion
open-questions list flags the items requiring engineering SME input before
execution begins.

---

## Findings

### MANDATORY SECTIONS

---

### M1: Document Control Table (front matter)

**Structure**: The Document Control block appears in the front matter,
before the Table of Contents. It contains two elements: a version table
and a distribution matrix.

**Version table -- mandatory columns** [Workflows notebook]:

| Column | Description |
|--------|-------------|
| Date | Date of the revision |
| Version | Revision number (e.g., 0, 1, A) |
| Description | Summary of changes in this version |
| Prepared by | Author name |
| Reviewed by | Technical reviewer name |
| Authorised by | Project Director name |

**Distribution matrix** -- immediately beneath the version table:
placeholders for Client Name, Number of Copies, Output Type (e.g., PDF,
electronic).

**Skeleton placeholder prompts**: None required for the version table
(auto-populated from metadata). The distribution matrix should prompt:
*"Complete the distribution list. Number of copies and output format
must be confirmed with the PM."*

**NZ standards / style rules**: Governed by the company Style Reference
Guide.

---

### M2: Client Summary (front matter)

**Trigger**: Always included by default. An "Executive Summary" heading
is only used if explicitly requested by the client in the LOE; the
default heading is "Client Summary" because executive summaries "carry a
high risk of contradicting the main report or accidentally excluding
critical legal limitations." [Workflows notebook]

**Structure**: Maximum one page, plain non-technical language.

**Mandatory content placeholders** [Workflows notebook]:

- *"Reference the LOE: state the document number and date."*
- *"State the purpose of the report in one sentence."*
- *"Describe the proposed works (what the client intends to build)."*
- *"List any site conditions or construction details that could impact
  cost, programme, or aesthetics."*
- *"Explicitly state the geotechnical risks associated with design
  development, construction, and post-construction operation."*
- *"Include a 'Further work' statement: what additional geotechnical
  input or investigation will be required in the future?"*

---

### M3: Section 1 -- Introduction

**Trigger**: Always included.

**Mandatory sub-headings** [Workflows notebook]:

- 1.0 Introduction (identifies client, site, purpose, superseded
  reports)
- 1.1 Scope of Work -- *conditional*: include unless the Introduction
  already adequately covers the scope. Must never be a copy-paste of
  the LOE.
- 1.2 Site Description
- 1.3 Proposed Development

**Placeholder prompts** [Workflows notebook]:

For 1.0 Introduction: *"Identify the client, the site address, the
purpose of this report, and list any previous reports it supersedes."*

For 1.1 Scope of Work: *"Summarise the scope in your own words --
what work was done and why. This must NOT be copied from the LOE. Group
the client's requirements into themes."*

For 1.2 Site Description: *"Describe location, topography, land use,
access, and any relevant environmental context. Source from the desktop
study."*

For 1.3 Proposed Development: *"Describe what the client intends to
build. Source from the RFP and client communications."*

---

### M4: Section 2.1 -- Ground and Groundwater Conditions

Comprises four sub-sections; all are mandatory.

#### 2.1.1 Geology and Faulting

**Placeholder prompt** [Workflows notebook]: *"List the geological units
which make up the soil/rock profile. Avoid irrelevant technical
geological descriptions. Identify the name and location of known active
faults relative to the site."*

#### 2.1.2 Previous Geotechnical Investigations

**Placeholder prompt** [Workflows notebook]: *"Provide a bullet-point
list of the investigation scope. Avoid long descriptions. Ensure
cross-references to the location plan in Appendix A and the logs/lab
results in Appendices B, C, and D."*

#### 2.1.3 Current Geotechnical Investigations

**Placeholder prompt** [Workflows notebook]: *"Describe the scope of
investigations you conducted (test types, number, depth). Reference the
GFR. Ensure cross-references to Appendix A (location plan) and Appendix
C (investigation logs)."*

#### 2.1.4 Geotechnical Model

**Critical formatting rule** [Workflows notebook]: Text-only soil profile
descriptions are *"strictly prohibited because they are difficult to
read."* The skeleton must inject an empty Geotechnical Model Table --
not a prose paragraph.

**Empty Geotechnical Model Table -- mandatory column headers**:

| Column | Description |
|--------|-------------|
| Layer / Unit | e.g., Holocene Marine, Uncontrolled Fill |
| Description | Brief soil/rock composition |
| Top of Layer (m) | Depth from ground surface |
| Top of Layer (RL) | Elevation relative to datum |
| Layer Thickness (m) | Vertical extent |
| Typical Test Values | SPT N-values and/or CPT qc values |

**Placeholder prompt**: *"Populate from borehole logs, CPT profiles, and
lab results. Site variances must be noted in table footnotes or shown
on cross-sections in Appendix A -- not described in prose."*

#### 2.1.5 Groundwater

**Placeholder prompt** [Workflows notebook]: *"Outline available
groundwater information. Present conclusions in terms of RL (Reduced
Level). What are the anticipated effects of seasonal/tidal fluctuations
and climate-change sea-level rise? State the design groundwater level
to be assumed for basement and foundation design."*

---

### M5: Section 2.2 -- Seismic Hazard

**Trigger**: Mandatory for NZ sites.

**Sub-sections**:

- 2.2.1 Seismic site subsoil class
- 2.2.2 Ground shaking hazard

**Governing standard**: NZS 1170.5:2004, Section 3.1.3 (Site Subsoil
Classification; Classes A-E).

**Placeholder prompts** [Workflows notebook]:

For 2.2.1: *"What is the assessed seismic site subsoil class (Class A
through E per NZS 1170.5:2004 Cl. 3.1.3)? What is the basis for this
classification? Could further investigation modify this assessment?"*

For 2.2.2: *"Present the Earthquake Magnitude (M) and Peak Ground
Acceleration (PGA) for the Serviceability Limit State (SLS), Ultimate
Limit State (ULS), and any intermediate design cases specified in the
brief."*

---

### M6: Section 4 -- Residual Geotechnical Risk

**Trigger**: Always included. Its omission creates direct professional
liability exposure: *"Any risks that remain unmitigated by the design
must be explicitly stated here. If these are not reported, the company
risks liability for failing to identify them."* [Workflows notebook;
Risk Assessment notebook]

**Placeholder prompt**: *"Brainstorm all geotechnical risks relevant to
this site. For each risk deemed greater than minor, state the mitigation
recommended. For each risk that remains unmitigated after the design
response, explicitly document it here so the client retains ownership of
that residual risk. Do not use generic text -- this section must be
project-specific."*

---

### M7: Section 5 -- Further Work

**Trigger**: Always included. Manages professional liability by setting
client expectations about future required investigations.

**Placeholder prompt** [Workflows notebook]: *"Explicitly state the
intended limits of this report to prevent someone from using this
information for a purpose it was not intended for (e.g., using
preliminary design information for detailed design). Detail the specific
future geotechnical input or physical investigations the client must
plan and budget for."*

---

### M8: Section 6 -- Applicability

**Trigger**: Always included.

**Mandatory clauses** (insert boilerplate, then prompt to customise)
[Workflows notebook; Risk Assessment notebook]:

1. **Exclusive Use clause**: Pre-populate with client name extracted
   from LOE. Prompt: *"Mandatory -- verify the client name below is
   the full legal entity name and update if needed."* Insert temporal
   boundary: if project not initiated within 18 months, the firm must
   re-confirm recommendations.
2. **Inferred Conditions clause**: Static boilerplate -- no
   customisation required, but author must not delete it.
3. **Observation Disclaimer clause**: Static boilerplate -- no
   customisation required.
4. **Council/Regulatory Authority clause**: *Conditional* -- include
   only when the RFP indicates the report supports a consent
   application. Placeholder prompt: *"Insert the name of the
   regulatory authority relying on this report."*

---

### M9: References

**Location**: Immediately after the Applicability section, before
Appendices [Workflows notebook].

**Format**: APA referencing system (standard for NZ and Australia).

**Placeholder prompt** [Workflows notebook]: *"List all external
reference materials, published geological information, and guidelines
using the APA referencing system. Note: Internal company reports must
NOT be listed here -- reference them using footnotes within the main
body text."*

---

### CONDITIONAL SECTIONS

---

### C1: Section 2.3 -- Liquefaction Assessment

**Trigger**: Mandatory by default for NZ sites [Workflows notebook].
Elevated specificity required if: site is in a liquefaction-prone area
per the Vulnerability to Liquefaction map (replacing MBIE Technical
Categories); or project is a Canterbury subdivision (triggers MBIE
Part D compliance).

**Governing standards** [Engineering Standards notebook]:
- NZGS Geotechnical Earthquake Engineering Practice Module 3 --
  Guideline for the identification, assessment and mitigation of
  liquefaction hazards.
- MBIE Part D Guidelines (Canterbury subdivisions only).
- Vulnerability to Liquefaction map (national guidance document
  *Planning and engineering guidance for potentially
  liquefaction-prone land*).

**Three-path placeholder** [Workflows notebook]: The skeleton must force
the author to select one of three reporting paths based on hazard
severity:

*"Assess the site in accordance with NZGS/MBIE Module 3 guidelines.
State whether liquefaction for this site:*
*(1) Does not dictate the design -- keep the section simple.*
*(2) Has limited impact on the design -- describe briefly.*
*(3) Is an important issue for the design -- provide full analysis.*

*If path (3) applies: carefully explain the uncertainty in seismic
design loadings. Detail any potential step-change behaviour in the soil
at levels of shaking either between SLS and ULS, or beyond ULS."*

---

### C2: Section 2.4.X -- Slope Stability Assessment

**Trigger**: When the RFP/LOE scope requires assessing natural or
engineered slopes (landfills, coastal revetments, earthworks), or when
the preliminary desktop study identifies steep terrain or slope
instability risks [Workflows notebook].

**Heading rule**: The AI must dynamically name this section to reflect
the specific hazard (e.g., "2.4.1 Slope stability assessment"), not a
generic "Hazard Assessment" heading [Workflows notebook].

**Governing standards** [Engineering Standards notebook]:
- NZS 4431 (Code of Practice for Earth Fill for Residential
  Development) -- applies to residential earthfills only; explicitly
  does NOT cover natural slopes.
- NZGS *Geotechnical Issues in Land Development* -- primary guidance
  for natural slopes in NZ residential context.
- NZGS/MBIE guidelines for factor-of-safety targets (must be
  confirmed with engineering SME -- see Open Questions).

**Structural elements**:

1. Prose describing the analysis approach and software.
2. Mandatory Slope Stability Results Table.

**Slope Stability Results Table -- mandatory columns** [Workflows
notebook]:

| Design Case | Assessed FoS | Seismic Displacement (mm) | Design Criteria |
|-------------|--------------|--------------------------|-----------------|

**Placeholder prompt** [Workflows notebook + Ground Engineering notebook]:

*"State the analysis approach used (limit equilibrium or finite
element) and the software (e.g., GeoStudio Slope/W, PLAXIS, Oasys).
Present the FoS for: static long-term, static temporary/construction,
seismic SLS, and seismic ULS design cases. Populate the results table
above.*

*State the assumed groundwater/piezometric conditions explicitly,
including worst-credible groundwater levels during prolonged rainfall.
State any allowances for sea-level rise or extreme leachate levels.*

*Provide estimated seismic displacements using an appropriate method
(e.g., Newmark Sliding Block approach).*

*Are drainage interventions required during construction to prevent
groundwater-induced instability?"*

**Industry FoS guidance** (general -- NZ-specific values to be
confirmed) [Ground Engineering notebook]:
- Static long-term: minimum FoS ≥ 1.5
- Static temporary/construction: minimum FoS ≥ 1.2–1.3
- Seismic SLS: minimum FoS ≥ 1.2
- Seismic ULS: minimum FoS ≥ 1.0

---

### C3: Section 2.4.X -- Fault Rupture Hazard Assessment

**Trigger**: When the desktop study identifies faulted terrain, site
within 20 km of a major fault listed in NZS 1170.5:2004 Table 3.6
(e.g., Wellington Fault), or critical containment infrastructure
requiring strict seismic resilience [Workflows notebook].

**Heading rule**: Dynamically named (e.g., "2.4.2 Fault rupture hazard
assessment") [Workflows notebook].

**Governing standards** [Engineering Standards notebook]:
- NZS 1170.5:2004 -- Site Subsoil Classification (Classes A-E) and
  seismic demand. Table 3.6 lists major active faults and setback
  guidance.
- GNS Active Faults Database -- for fault location, distance, and
  geometry.
- GNS Science Stage 1 Report -- Port Hills specific hazards (rockfall,
  cliff collapse, mass movement).

**Placeholder prompt** [Workflows notebook]:

*"Identify the name and location of known active faults relative to the
site (reference NZS 1170.5:2004 Table 3.6 and the GNS Active Faults
Database). Detail the fault geometry, distance to the site, and
inferred rupture mechanisms based on existing or newly mapped fault
traces. Assess the hazard for both operational and long-term/post-
closure scenarios. Where risks are greater than minor, provide clear,
practical mitigation recommendations."*

*[Canterbury/Port Hills only]: "Include assessment of rockfall, cliff
collapse, and mass movement per the GNS Science Stage 1 Report. Include
placeholders for Producer Statements: PS1 (Design), PS2a (Peer Review),
PS4 (Construction Review)."*

---

### C4: Section 2.5 -- Geotechnical Issues Identified

**Trigger**: Include by default if the report proceeds to a foundation
assessment or detailed design phase [Workflows notebook]. Acts as the
bridge between hazard analysis (Section 2) and engineering design
(Section 3).

**Structural elements**:

- Brief introductory statement.
- Mandatory summary table.

**Pre-table prompt** [Workflows notebook]: *"Brainstorm with experienced
engineers to identify all key geotechnical issues and constraints for
the site. Populate the table below and cross-reference each issue to
the specific report section that addresses it."*

**Geotechnical Issues Table -- mandatory columns** [Workflows notebook]:

| Geotechnical Issue | Cross-reference to subsequent report section |
|-------------------|----------------------------------------------|

---

### C5: Section 3.1 -- Foundation Options

**Trigger**: When the LOE specifically requires evaluation of multiple
foundation types before a preferred option is recommended [Workflows notebook].

**Structural elements**: Introductory statement + options table.

**Placeholder prompt** [Workflows notebook]: *"Insert a simple options
and relative merits table. State which foundation option the
client/project team has formally selected. Do NOT present detailed
designs for unselected options."*

**Foundation Options Table -- mandatory columns** [Workflows notebook]:

| Foundation Option | Relative Merits | Geotechnical Issues Addressed (cross-ref to Section 2.5) |
|-------------------|----------------|----------------------------------------------------------|

---

### C6: Section 3.2 -- Foundation Design Parameters (or renamed to match method)

**Trigger**: When the LOE requires foundation design parameters.
Dynamically rename to reflect the selected method (e.g., "3.2 CFA
ground improvement design parameters", "3.2 Shallow foundation design
parameters") [Workflows notebook].

**Placeholder prompt** [Workflows notebook]: *"State the information
received from others that you relied upon (e.g., foundation loads,
settlement tolerances). Provide design parameters for the SELECTED
option only -- not unselected alternatives. Challenge whether the
detailed basis of these parameters needs to be in the report body; if
not, document in internal calculation files to keep the report
concise."*

---

### C7: Section 3.X -- Ground Improvement

**Trigger**: When preliminary desktop study or RFP indicates natural
ground conditions are insufficient to support the proposed development
[Workflows notebook].

**Governing standards** [Engineering Standards notebook]:
- NZS 4431 -- earthfill compaction for residential development.
- Good Ground acceptance: 300 kPa ultimate bearing capacity; verified
  via Scala Penetrometer (>5 blows per 100 mm to 2× footing width
  depth; >3 blows per 100 mm below that).
- Granular compaction acceptance: dry density ≥ 2,150 kg/m³ per the
  NZ Vibrating Hammer Compaction Test (NZS 4402.4.1.3).
- Settlement criterion: site must not experience ≥ 25 mm settlement
  from subsidence, instability, creep, or compressible soils.

**Placeholder prompt** [Workflows notebook]: *"Present the design
parameters for the selected ground improvement option ONLY. Detail the
information received from others (foundation loads, settlement
tolerances). Provide specific design parameters (bearing capacity,
strength reduction factor, stiffness). Exclude detailed calculation
bases from the report body -- document in internal files instead."*

---

### APPENDICES

**Ordering rule**: Appendices must appear in the exact order they are
first referenced in the main text [Workflows notebook; Technical
Writing notebook].

**Mandatory appendix structure** [Workflows notebook]:

| Appendix | Content | Always/Conditional |
|----------|---------|-------------------|
| A | Figures (location plans, site plans, cross-sections) | Always |
| B | Previous Investigations | Conditional (if referenced in 2.1.2) |
| C | Investigation Logs (borehole logs, test pit logs per NZGS 2005 Field Description guidelines) | Conditional (if separate GFR not produced) |
| D | Geotechnical Laboratory Test Results | Conditional (if separate GFR not produced) |

**GFR handling**: If a separate GFR is being produced alongside the
GIR, Appendices B/C/D must contain cross-references to the GFR rather
than duplicating raw data [Workflows notebook].

**Log table format**: Borehole and test pit log appendices must follow
the NZGS Field Description of Soil and Rock (2005) column format:
Soil Type, Colour, Strength (Cohesive Soil Consistency), Density
(Non-Cohesive Soil), Moisture, Grading, Organic Content [Engineering
Standards notebook].

---

## Implications for the Skeleton Generator Execution Plan

This research enables the following sub-step decomposition for
incremental delivery. Each sub-step produces a DOCX artifact that can
be put in front of an engineer for feedback.

| Sub-step | Capability built | Sections covered | Validated on | Release artifact |
|----------|----------------|-----------------|-------------|-----------------|
| 0 | Word Template ingestion | All (base) | Any GIR | Empty DOCX in company style |
| 1a | Mandatory section structure | Document Control, ToC, Section headers 1-6, Appendix stubs | GIR skeleton for a sample project | DOCX with correct headings, no content |
| 1b | Mandatory tables (empty) | Document Control table, Geotechnical Model Table, Issues table | Same | DOCX with empty structured tables |
| 2 | Metadata extraction | Client name, project number, document naming, date | RFP/LOE input | DOCX with populated front matter |
| 3 | Client Summary / intro draft | Client Summary, Section 1.0/1.2/1.3 | RFP/LOE input | DOCX with intro sections drafted |
| 4 | Traceability matrix | Scope extraction, deliverable-to-section mapping | RFP/LOE input | DOCX with traceability table |
| 5 | Mandatory boilerplate | Applicability clauses (Sections 6, References, Further Work prompts) | Project type + client name | DOCX with legal sections inserted |
| 6 | Standards references per section | Sections 2.2 (seismic), 2.3 (liquefaction), 3.x (foundations) | Standards registry query | DOCX with clause notes per section |
| 7 | Actionable placeholder questions | All sections (M3-M9, C1-C7 prompts from this document) | Validated section-by-section | Complete skeleton (all AC met) |
| 8 | Conditional section logic | C1-C7 inclusion/exclusion based on RFP/location triggers | Canterbury residential project | Skeleton with correct conditionals |

---

## Open Questions

| # | Question | Impact | Who resolves |
|---|----------|--------|-------------|
| OQ1 | What are the exact minimum FoS values mandated by NZGS/MBIE guidance for NZ residential slope stability (static long-term, static temporary, seismic SLS, seismic ULS)? The Ground Engineering notebook provided international norms (1.5/1.2-1.3/1.2/1.0) but noted these require NZ-specific verification. | Affects AC10 and slope stability placeholder prompt accuracy. | Engineering SME / NZGS guidelines direct review. |
| OQ2 | Does the GNS Active Faults Database have publicly accessible API or structured data for automated fault proximity checking, or does the skeleton trigger fault rupture sections purely from RFP/LOE text? | Affects C3 trigger logic. | Architecture / data access investigation. |
| OQ3 | For Section 1.1 (Scope of Work), should the default be to always include it, or should the AI attempt to judge whether the Introduction already covers it? | Affects section inclusion logic for sub-step 1a. | Product decision -- recommend defaulting to always include. |
| OQ4 | Canterbury-specific sections (MBIE Part D, CCC Appendix I/II, Port Hills, HAIL site assessment): should these be a separate "Canterbury GIR" configuration, or conditional flags within the standard template? | Major architecture decision. | Product + engineering SME. |
| OQ5 | Section 2.3 (Liquefaction) is described as mandatory by default for NZ. Should it always appear as a full section, or can the skeleton insert a one-line statement ("Liquefaction does not dictate the design") when the scope clearly excludes it? | Affects sub-step 8 conditional logic. | Engineering SME. |
| OQ6 | For the Distribution matrix (Document Control), can client name and output type be auto-populated from metadata, or does this always require manual completion? | Affects sub-step 2 scope. | Product decision. |

---

## Glossary

| Term | Definition |
|------|------------|
| GIR | Geotechnical Interpretive Report -- the primary engineering deliverable interpreting ground conditions and providing design recommendations. |
| GFR | Geotechnical Factual Report -- an objective record of field and lab data, no interpretation. |
| Client Summary | Max-one-page plain-language front matter summarising key findings for non-technical readers. Preferred over "Executive Summary." |
| Geotechnical Model Table | Structured table presenting the soil/rock profile with standardised columns. Text-only descriptions are prohibited. |
| Touchstone | Extracted scope-of-works used as a master checklist throughout drafting. |
| FoS | Factor of Safety -- ratio of resisting to driving forces; >1.0 indicates stability. |
| SLS | Serviceability Limit State -- structure remains functional under normal loads. |
| ULS | Ultimate Limit State -- structure does not collapse under extreme loads. |
| Limit Equilibrium | Analysis method computing FoS by comparing driving and resisting forces along a potential failure surface. |
| Finite Element | Numerical method evaluating stability via strength reduction; does not require pre-assumed failure surface shape. |
| Scala Penetrometer | Field device driven into ground to verify bearing capacity compliance under NZS 3604. |
| RL | Reduced Level -- elevation relative to a standard datum. |
| SPT | Standard Penetration Test -- blow count (N-value) per 300 mm drive; measures soil density and strength. |
| CPT | Cone Penetration Test -- tip resistance (qc); infers soil stratigraphy and properties. |
| NZGS Module 3 | NZ Geotechnical Society guideline for liquefaction hazard identification, assessment, and mitigation. |
| MBIE Part D | Ministry of Business, Innovation and Employment guidelines for Canterbury subdivision geotechnical investigations. |
| NZS 4431 | NZ Code of Practice for Earth Fill for Residential Development. Does not cover natural slopes. |
| NZS 1170.5 | NZ Earthquake Actions standard. Governs site subsoil classification and seismic demand. |
| CFA | Continuous Flight Auger -- drilling method used for ground improvement piling. |
| APA | American Psychological Association referencing style -- mandatory for external citations in NZ engineering reports. |
| GNS | GNS Science (NZ Crown Research Institute) -- publishes the Active Faults Database and seismic hazard data. |
| Producer Statements | Formal council certification documents: PS1 (Design), PS2a (Peer Review), PS4 (Construction Review). |
| HAIL | Hazardous Activities and Industries List -- used to flag potential site contamination. |

---

## Sources Consulted

| Notebook | Queries asked | Key citations |
|----------|--------------|---------------|
| Geotechnical Engineering Report Workflows and Standard Procedures | 4 | Mandatory/conditional section triggers; placeholder prompts for all 13 sections; Document Control table columns; Geotechnical Model Table headers; slope stability results table; foundation options table; Geotechnical Issues table; Client Summary vs Executive Summary; Further Work prompts; Applicability customisation; References location and format. |
| Engineering Standards (NZ) | 1 | Liquefaction triggers and standards (NZGS Module 3, MBIE Part D, Vulnerability to Liquefaction map); slope stability NZS 4431 scope limitation; fault rupture NZS 1170.5 Table 3.6; ground improvement acceptance criteria (NZS 4431, 300 kPa bearing, Scala Penetrometer, NZ Vibrating Hammer Test, 25 mm settlement limit). |
| Ground Engineering Magazine | 1 | Slope stability FoS targets (general industry norms); limit equilibrium vs finite element methods; standard analysis software (GeoStudio, PLAXIS, LimitState:GEO, Oasys, GEO5); worst-credible groundwater level requirement; Newmark Sliding Block displacement approach. |
