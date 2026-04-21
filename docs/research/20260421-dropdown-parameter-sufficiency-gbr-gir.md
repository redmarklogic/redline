# Dropdown-Based Parameter Sufficiency for NZ GBR/GIR Skeleton Generation

**Date**: 2026-04-21
**Research question**: Is dropdown-based parameter selection sufficient for NZ GBR/GIR jurisdiction mapping, and what are the specific parameter sets required?
**Actor**: A product designer building a dropdown-based form for Sprint 1 of the skeleton generator.
**Redline domains**: Skeleton Generator (Concept 01), Standards Registry (Concept 02), Sprint 1 form design.

---

## Summary

Dropdown-based parameter selection is **sufficient for Sprint 1** to generate structurally correct GBR and GIR skeletons with the right sections included/excluded and generic domain-specific placeholder prompts. However, five parameters fundamentally require free text to produce a *useful* skeleton (project name, client name, site address, job number, and LOE deliverable extraction). A hybrid form (dropdowns + targeted free-text fields) is the correct design.

---

## Findings

### 1. GBR Parameter Set (NZ Jurisdiction)

The GBR (Geotechnical Baseline Report) is a contract document that provides a single, measurable interpretation of anticipated subsurface conditions to fairly allocate financial risk between the project owner and the contractor. Its structure follows the ASCE 10-chapter framework, adapted by the NZTS (New Zealand Tunnelling Society) guide for NZ jurisdiction.

#### 1.1 Parameters That Drive GBR Section Selection

| # | Parameter | Input Type | Options / Values | Sections Affected |
|---|-----------|-----------|------------------|-------------------|
| P1 | **Contract form** | Dropdown | NZS 3910, FIDIC Emerald Book, NEC4, Other | Ch 1 (Introduction) -- determines how GBR is invoked contractually |
| P2 | **Procurement method** | Dropdown | Design-Bid-Build, Design-Build, Alliance, Other | Ch 1-2 -- determines interactive tender process (NZTS Issue A/B/C) |
| P3 | **Project type** | Dropdown | Tunnel, Shaft/Basement, Bridge/Viaduct, Building, Road/Highway, Earthworks/Dam, Pipeline/Trenchworks, Coastal/Marine, Other | Ch 2 (Project Description), Ch 8 (Construction Considerations) |
| P4 | **Site history** | Dropdown | Greenfield, Brownfield/Urban, Former Industrial, Reclaimed Land | Ch 3 (Manmade Features) -- included only for developed sites |
| P5 | **Dominant ground conditions** | Dropdown | Soil-dominant, Rock-dominant, Mixed-face | Ch 7 (Ground Characterisation) -- completely changes the skeleton |
| P6 | **Construction methods** | Multi-select | TBM (Tunnel Boring Machine), Drill & Blast, Open Cut, Driven Piles, Bored Piles, CFA Piles, Slurry/Diaphragm Walls, Ground Freezing, Shaft Sinking, Pipe Jacking, Dredging, Other | Ch 8 (Construction Considerations) -- generates sub-sections per method |
| P7 | **Infrastructure elements** | Multi-select | Deep foundations, Shallow foundations, Retaining walls, Earthworks/embankments, Tunnels, Shafts, Dewatering systems, Ground anchors, Temporary works, Other | Ch 8 sub-sections |
| P8 | **Known hazards** | Multi-select | Contaminated land, Gas (explosive/toxic), High groundwater, Artesian pressure, Aggressive ground (sulphates/acids), Unexploded ordnance, Archaeological, None known | Ch 10 (Spoils, Groundwater, and Gas Management) |
| P9 | **Sensitive adjacent structures** | Dropdown | Yes (buildings, utilities, heritage), No | Ch 9 (Instrumentation and Monitoring) |
| P10 | **Local construction precedent** | Dropdown | Available, Not available, Unknown | Ch 6 (Previous Construction Experience) -- omitted if unavailable |
| P11 | **Seismic hazard relevance** | Dropdown | Yes, No | NZ-specific: triggers seismic baseline sub-section in Ch 7/8 |
| P12 | **Liquefaction relevance** | Dropdown | Yes (significant), Yes (minor/managed), No | NZ-specific: triggers liquefaction baseline in Ch 7 |

#### 1.2 NZ-Specific GBR Requirements (NZTS Guide Additions)

The NZTS guide adds NZ-specific requirements on top of ASCE:

- **NZS 3910 integration**: GBR must be included in "Schedule 2 -- Special Conditions of Contract -- Other Conditions of Contract"
- **RMA (Resource Management Act) compliance**: Groundwater effects must be addressed for consenting
- **Health and Safety at Work Act 2015**: PCBU (Person Conducting a Business or Undertaking) duties must be stated
- **ISO 31000 risk management**: Recommended framework for risk allocation
- **Interactive tender process**: Three-stage GBR development (Issue A/B/C)

Note: The GBR notebook sources did not contain NZ-specific soil/rock types or seismic hazard guidance. These are covered by the Engineering Standards and Report Workflows notebooks (see Section 3 below).

---

### 2. GIR Parameter Set (NZ Jurisdiction)

The GIR (Geotechnical Interpretive Report) is a technical document that applies engineering judgement to interpret subsurface data and assess ground hazards for design. Its structure is driven by NZ professional practice rather than an international standard.

#### 2.1 Parameters That Drive GIR Section Selection

| # | Parameter | Input Type | Options / Values | Sections Affected |
|---|-----------|-----------|------------------|-------------------|
| P1 | **Project type** | Dropdown | Residential subdivision, Commercial building, Industrial facility, Infrastructure (road/bridge), Critical containment (landfill), Flood protection (stopbank/dam), Coastal/marine, Transportation corridor, Civic/heritage asset, Other | All -- determines scope and conditional sections |
| P2 | **Region** | Dropdown | Auckland, Waikato, Bay of Plenty, Wellington, Canterbury, Otago/Southland, Other North Island, Other South Island | Affects geological setting, seismic parameters, and applicable council requirements |
| P3 | **Summary type** | Dropdown | Client Summary (default), Executive Summary (client-requested only) | Front matter heading and structure |
| P4 | **Deliverable splitting** | Dropdown | GIR only, GIR + separate GFR | Appendix structure (cross-reference vs include raw data) |
| P5 | **Foundation assessment required** | Dropdown | Yes -- single option, Yes -- compare options, No | Triggers Section 3 (Foundation Assessment) and sub-sections |
| P6 | **Ground improvement required** | Dropdown | Yes, No, Unknown/TBD | Triggers Section 3.X (Ground Improvement) |
| P7 | **Liquefaction path** | Dropdown | (1) Does not dictate design, (2) Limited impact, (3) Important issue for design | Section 2.3 -- determines reporting depth |
| P8 | **Slope stability relevant** | Dropdown | Yes (natural slopes), Yes (engineered slopes/earthworks), No | Triggers Section 2.4.X (Slope Stability Assessment) |
| P9 | **Fault rupture relevant** | Dropdown | Yes (site within 20 km of active fault), No | Triggers Section 2.4.X (Fault Rupture Hazard Assessment) |
| P10 | **Other geotechnical hazards** | Multi-select | Settlement (compressible soils), Lateral spread, Rockfall/cliff collapse, Coastal erosion, Flooding/scour, Expansive soils, Contamination, None identified | Triggers additional Section 2.4.X sub-sections |
| P11 | **Consent application** | Dropdown | Yes (resource consent), Yes (building consent), Both, No | Triggers Council/Regulatory Authority clause in Applicability section |
| P12 | **Canterbury-specific** | Dropdown | Yes (Canterbury residential -- MBIE Part D applies), Yes (Port Hills -- GNS hazards), No | Triggers Canterbury-specific sections (MBIE Part D, CCC requirements) |
| P13 | **Seismic site subsoil class** | Dropdown | Class A (Strong rock), Class B (Rock), Class C (Shallow soil), Class D (Deep/soft soil), Class E (Very soft soil), Not yet determined (default to E) | Section 2.2 (Seismic Hazard) pre-population |

#### 2.2 Key Differences: GIR vs GBR Parameter Set

| Aspect | GBR | GIR |
|--------|-----|-----|
| **Purpose** | Contractual risk allocation between owner and contractor | Engineering interpretation for design |
| **Structure driver** | ASCE/CIRIA/NZTS international standards | NZ professional practice (NZGS, company workflows) |
| **Contract form matters** | Critical (drives how GBR is invoked) | Not relevant (GIR is a technical document, not a contract document) |
| **Construction methods** | Critical (baseline statements per method) | Not directly relevant (GIR focuses on ground conditions, not construction) |
| **Foundation/retaining design** | Not typically included (GBR states ground conditions, not design) | Critical (Section 3 provides design parameters) |
| **Liquefaction** | May appear as baseline in Ch 7 | Always mandatory for NZ sites (Section 2.3) |
| **Legal boilerplate** | Contract-specific (DSC clauses) | Professional practice (Applicability clauses, Exclusive Use, temporal boundary) |

---

### 3. Domain-Specific Enumerated Options for NZ Practice

#### 3.1 NZ Soil and Rock Types (for dropdown/multi-select)

From Engineering Standards and Report Workflows notebooks, grouped by origin:

**Volcanic:**
- Basalt / scoria / volcanic ash (Port Hills, Auckland)
- Hamilton Ash
- Rotoehu Ash
- Younger (Post-Rotoehu) Ash
- Allophane-rich volcanic soils (Waikato, BOP)
- Pumice (BOP, Central North Island)

**Sedimentary / Alluvial:**
- Alluvial gravel (Canterbury plains, river systems)
- Alluvial sand
- Alluvial silt
- Tauranga Group sediments (BOP)
- Matua Subgroup

**Marine / Estuarine:**
- Holocene marine/estuarine deposits (clayey silts, shell fragments)
- Pleistocene alluvium
- Marine sands ("running sand" when saturated)

**Aeolian:**
- Loess (wind-deposited silt -- Port Hills, Canterbury)
- Loess colluvium (reworked loess on slopes)

**Organic:**
- Peat
- Organic silt/clay

**Bedrock:**
- Greywacke (sandstone/siltstone -- Wellington, Canterbury)
- Port Hills Gravel Formation
- Grampians Formation

**Fill:**
- Uncontrolled fill
- Reclamation fill (historic)
- Engineered fill

#### 3.2 Foundation Types

- Shallow foundations (strip/pad footings)
- Concrete raft foundations
- Timber driven piles
- Concrete driven piles
- Bored piles
- Screw piles (e.g., Stopdigging SGC 76)
- CFA (Continuous Flight Auger) ground improvement
- Stone columns

#### 3.3 Retaining Structure Types

- Timber pole retaining walls
- Concrete pile cantilever walls
- King post walls
- Gravity walls (concrete/masonry)
- MSE (Mechanically Stabilised Earth) walls
- Soil nails
- Grouted anchors
- Rock revetments / armour
- Sheet piling

#### 3.4 Earthworks Categories

- Cut to fill (balanced)
- Imported fill
- Over-excavation and replacement
- Compacted gravel raft
- Surcharging (pre-loading)
- Drainage blankets

#### 3.5 NZ Standards and Codes (for multi-select per report type)

**Always referenced (GIR):**
- NZS 1170.5:2004 -- Earthquake actions (seismic site subsoil classification)
- NZGS/MBIE Module 1 -- Overview of geotechnical earthquake engineering
- NZGS/MBIE Module 3 -- Liquefaction hazards
- NZGS Field Description of Soil and Rock (2005)

**Conditionally referenced (GIR):**
- NZS 3604 -- Timber-framed buildings (residential projects)
- NZS 4431 -- Earth fill for residential development
- AS/NZS 1170.0 -- General design actions
- AS/NZS 1170.1 -- Permanent and imposed actions
- AS/NZS 1170.2 -- Wind actions
- NZS 3101 -- Concrete structures
- NZS 3404 -- Steel structures
- NZS/AS 1720.1 -- Timber structures
- NZTA Bridge Manual (infrastructure projects)
- Austroads Guide to Road Design (transportation)
- MfE Coastal Hazards and Climate Change (coastal projects)

**GBR-specific:**
- ASCE GBR guidelines (2007)
- CIRIA C807 (2017)
- NZTS Geotechnical Baseline Reports guide
- FIDIC Emerald Book (2019) -- if FIDIC contract
- NZS 3910 -- Contract conditions (if NZS 3910 contract)
- NZGS Ground Investigation Specification (2018)
- Health and Safety at Work Act 2015
- Resource Management Act (RMA)
- ISO 31000 -- Risk management

#### 3.6 NZGS Soil Description Fields (for Geotechnical Model Table dropdowns)

Per the NZGS Field Description of Soil and Rock (2005):

| Field | Dropdown Options |
|-------|-----------------|
| **Soil type (dominant fraction)** | Boulder, Cobble, Gravel, Sand, Silt, Clay, Peat |
| **Colour** | Brown, Grey, Yellow-brown, Reddish-brown, Blue-grey, Dark grey, Black, White, Mottled |
| **Strength (cohesive)** | Very soft (<12 kPa), Soft, Firm, Stiff, Very stiff, Hard (200-500 kPa) |
| **Density (non-cohesive)** | Very loose, Loose, Medium dense, Dense, Very dense |
| **Moisture** | Dry, Moist, Wet, Saturated |
| **Grading** | Well-graded, Poorly-graded, Gap-graded |
| **Organic content** | Trace, Little, Some, And (fibrous/wood/root) |

---

### 4. NZ Jurisdiction-Specific Sections (vs International Practice)

Sections that appear ONLY or PREDOMINANTLY in NZ reports:

| Section | NZ-Specific Reason |
|---------|-------------------|
| Seismic site subsoil classification (NZS 1170.5 Classes A-E) | Mandatory for all NZ sites due to high seismicity |
| Liquefaction assessment (NZGS/MBIE Module 3) | Mandatory for most NZ sites; three reporting paths |
| Canterbury-specific requirements (MBIE Part D) | Post-earthquake regulatory framework unique to Canterbury |
| Port Hills hazards (GNS Science Stage 1) | Rockfall, cliff collapse, mass movement -- region-specific |
| Scala penetrometer acceptance criteria (NZS 3604) | NZ-specific "good ground" test for residential |
| NZS 4431 earthworks compliance | NZ-specific compaction standard |
| RMA compliance (for GBR) | NZ environmental legislation |
| Health and Safety at Work Act 2015 (for GBR) | NZ workplace safety legislation |

---

## Professional Judgement: Dropdown Sufficiency for Sprint 1

### Verdict: Dropdowns are sufficient for SECTION SELECTION. A hybrid form is needed for a USEFUL skeleton.

**What dropdowns CAN do (Sprint 1 scope):**

1. **Section inclusion/exclusion logic** -- fully achievable with dropdowns. The 12-13 parameters listed above for each report type can all be expressed as dropdown or multi-select fields. This is the primary value of Sprint 1.
2. **Standards references per section** -- fully achievable. The applicable standards can be auto-inserted based on project type, region, and scope selections.
3. **Generic domain-specific placeholder prompts** -- fully achievable. The placeholder questions documented in the existing research (20260411-gir-skeleton-section-placeholders.md) are generic to the report type and conditional section, not project-specific.
4. **Empty mandatory tables** -- fully achievable. Table headers (Geotechnical Model Table, Slope Stability Results Table, Foundation Options Table, etc.) are standard regardless of project specifics.

**What fundamentally requires free text (5 fields):**

| Field | Why Free Text Is Required |
|-------|--------------------------|
| **Project name / title** | Unique per project -- cannot be enumerated |
| **Client name (legal entity)** | Populates Exclusive Use clause -- must be exact legal name |
| **Site address** | Unique per site |
| **Job number** | Company-specific numbering scheme |
| **LOE/RFP deliverable summary** | The "touchstone" -- free-form extraction of client requirements. This is what makes the skeleton *actionable* vs generic. |

### Recommendation for Sprint 1

A **hybrid form** with:
- ~13 dropdown/multi-select fields for section selection logic
- ~5 free-text fields for project identification and the LOE touchstone
- Optional free-text field for "Additional notes / special conditions"

This is sufficient to generate a skeleton that:
1. Has the correct sections included/excluded
2. Has the right standards referenced per section
3. Has domain-specific placeholder prompts (not generic TODOs)
4. Has populated front-matter metadata
5. Has the correct mandatory tables with headers

What it will NOT do (deferred to later sprints):
- Extract deliverables automatically from an uploaded LOE/RFP document
- Map LOE deliverables to specific report sections (traceability matrix)
- Generate project-specific placeholder questions (requires LOE parsing)

### Risk Flag

The LOE deliverable summary (P5 free-text field) is the highest-value input. Without it, the skeleton is structurally correct but lacks the "touchstone" that makes it genuinely useful to the author. If Sprint 1 omits this field, the skeleton degrades to a "smart template" rather than an "actionable starting point." I recommend including it as an optional free-text field with guidance text.

---

## Open Questions

| # | Question | Impact | Who Resolves |
|---|----------|--------|-------------|
| OQ1 | Should the form capture NZ region at a finer granularity than the 8 options listed? E.g., specific district/council (CCC, WCC, Auckland Council) since council requirements differ. | Affects conditional sections (Canterbury-specific) and applicable local guidance. | Product decision (Mark) + Graeme |
| OQ2 | For GBR: should seismic and liquefaction baselines be explicitly enumerated in the NZTS framework, or are these treated as sub-topics within Ch 7/8? The GBR notebook sources did not contain NZ seismic/liquefaction guidance. | Affects GBR skeleton completeness for NZ seismic projects. | Graeme -- requires NZTS guide direct review. |
| OQ3 | The soil/rock type list covers Canterbury and BOP well but gaps remain for Auckland (Waitemata Group, East Coast Bays Formation) and Otago (schist). Should the initial dropdown be kept generic (NZGS classification) with a regional overlay? | Affects form complexity vs accuracy. | Graeme -- needs broader NZ geological reference. |
| OQ4 | For Sprint 1, should the form support BOTH GBR and GIR, or focus on GIR only (higher volume, more established workflow in existing research)? | Affects Sprint 1 scope and delivery risk. | Ron + Mark |

---

## Sources Consulted

| Notebook | Session ID | Queries | Key Citations |
|----------|-----------|---------|---------------|
| Geotechnical Baseline Reports (GBR) | ea361db5 | 2 | ASCE guidelines, CIRIA C807, NZTS guide, FIDIC Emerald Book, NZS 3910 |
| Geotechnical Report Workflows | 007e335f | 1 | NZ professional practice, project types, soil types, foundation types, standards |
| Engineering Standards | 6a5f29bd | 1 | NZGS Field Description, NZS 1170.5, NZS 4431, NZS 3604, Scala penetrometer |
| Existing research: 20260411-gir-skeleton-section-placeholders.md | N/A | N/A | Section-by-section placeholder prompts, mandatory tables, conditional triggers |
| Existing research: 20260411-gir-skeleton-acceptance-criteria.md | N/A | N/A | Acceptance criteria, quality gates, formatting rules |
| Existing research: 20260412-report-drafting-initiation-workflow.md | N/A | N/A | Early skeletonization workflow, "touchstone" concept |

---

## Glossary

| Term | Definition |
|------|-----------|
| GBR (Geotechnical Baseline Report) | A contract document providing measurable interpretations of subsurface conditions to allocate financial risk between owner and contractor. |
| GIR (Geotechnical Interpretive Report) | A technical document applying engineering judgement to interpret subsurface data and assess ground hazards for design. |
| GFR (Geotechnical Factual Report) | A separate document containing purely factual, uninterpreted site investigation data. |
| GDR (Geotechnical Data Report) | International equivalent of GFR -- factual data only. |
| DSC (Differing Site Conditions) | A contractual clause allowing a contractor to claim additional time/money if actual ground differs materially from the GBR. |
| LOE (Letter of Engagement) | The contract document defining project scope, deliverables, and conditions. |
| RFP (Request for Proposal) | The client's document requesting services and defining requirements. |
| NZTS | New Zealand Tunnelling Society. |
| NZGS | New Zealand Geotechnical Society. |
| MBIE | Ministry of Business, Innovation and Employment (NZ). |
| ASCE | American Society of Civil Engineers. |
| CIRIA | Construction Industry Research and Information Association (UK). |
| FIDIC | International Federation of Consulting Engineers. |
| SPT (Standard Penetration Test) | An in-situ test measuring soil resistance by counting hammer blows to drive a sampler 300 mm. |
| CPT (Cone Penetration Test) | An in-situ test measuring continuous soil resistance by pushing an instrumented cone into the ground. |
| UCS (Unconfined Compressive Strength) | A laboratory test measuring the compressive strength of rock or stiff soil. |
| RQD (Rock Quality Designation) | A measure of rock mass quality based on the percentage of intact core pieces longer than 100 mm. |
| TBM (Tunnel Boring Machine) | A machine used to excavate tunnels with a circular cross-section. |
| CFA (Continuous Flight Auger) | A piling/ground improvement technique using a hollow-stemmed continuous auger. |
| MSE (Mechanically Stabilised Earth) | A retaining wall system using layers of soil reinforcement (geogrid or steel strips). |
| FoS (Factor of Safety) | The ratio of available strength to required strength -- a margin against failure. |
| PCBU | Person Conducting a Business or Undertaking (NZ health and safety legislation). |
| RMA | Resource Management Act (NZ environmental legislation). |
| Scala Penetrometer | A NZ-standard dynamic cone penetrometer used to test soil bearing capacity for residential foundations. |
| MDD (Maximum Dry Density) | The maximum achievable dry density of a soil at optimum moisture content. |
