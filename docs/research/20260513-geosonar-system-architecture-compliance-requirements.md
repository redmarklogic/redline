# System Architecture and Compliance Requirements for Automated Geotechnical Investigation Report Quality Assurance

**Date**: 2026-05-13
**Type**: Deep research synthesis
**Purpose**: Domain grounding for GeoSonar quality platform mockups

---

## Executive Summary of Terms

| Acronym | Definition |
|---------|-----------|
| AGS | Association of Geotechnical and Geoenvironmental Specialists. Standard-setting body for electronic exchange formats (AGS 3.1, AGS 4.0.4) |
| BIM | Building Information Modeling. Digital representation and lifecycle management framework |
| CDEM | Civil Defence Emergency Management |
| CityGML | Standardized multi-dimensional level of development (LOD) standard |
| CPEng | Chartered Professional Engineer. Accreditation required for authorizing geotechnical practice documents |
| CPT | Cone Penetration Test. In-situ subsurface testing for continuous geotechnical data profiles |
| DAR | Durability Assessment Report |
| DMT | Dilatometer Test. In-situ testing mechanism correlated with index properties |
| DOT | Department of Transportation |
| DPGR | Draft Preliminary Geotechnical Report |
| EIR / EIS | Environmental Impact Report / Environmental Impact Statement |
| ERI | Electrical Resistivity Imaging |
| GBR | Geotechnical Baseline Report. Establishes anticipated ground conditions and contractual baselines |
| GDR | Geotechnical Design Report |
| GFR | Geotechnical Feedback Report. Post-construction analysis and observational records |
| GIR | Geotechnical Investigation Report. Primary deliverable presenting subsurface exploration data |
| GIS | Geographic Information Systems |
| GSI | Geological Strength Index |
| GRD | Geotechnical Reporting Document. Overarching term for any geotechnical deliverable |
| IoT | Internet of Things |
| LOD | Level of Development. Metric framework for progressive completeness |
| MBIE | Ministry of Business, Innovation & Employment (NZ) |
| MMI | Model Maturity Index. Discrete numerical metric system (100-600) for model completeness |
| Model MRI | Model Maturity Risk Index. Toolkit tracking maturity and reporting risk probabilities |
| ModelXP | Modeling Execution Plan |
| NZGS | New Zealand Geotechnical Society |
| P.E. | Professional Engineer |
| PEngGeol | Professional Engineering Geologist |
| PGDR | Preliminary Geotechnical Design Report |
| PI | Plasticity Index |
| PMT | Pressuremeter Test |
| QA | Quality Assurance |
| QC | Quality Control |
| RHRS | Rockfall Hazard Rating Score |
| RQD | Rock Quality Designation |
| SAST | Static Application Security Testing |
| SDIM-Geo-TR | Sustainable Digital Transformation in Geotechnical-Related Engineering Disciplines |
| SPT | Standard Penetration Test |
| TIDP | Task Information Delivery Plan |
| TRL | Technology Readiness Level |
| UAV | Unmanned Aerial Vehicles |
| USACE | United States Army Corps of Engineers |
| USCS | Unified Soil Classification System |
| WBS | Work Breakdown Structure |

---

## Part 1: Formal QA Checklists & Peer Review

### CERT 10a Guide for Geotechnical Report Checklist

- **Structure**: Boolean tabular structure. Yes / No / N/A checkbox methodology.
- **Sections Covered**: Introduction, Topography, Geology, Field and Laboratory Investigation Scope, Subsurface Conditions, Discussion of Subsurface Features, Groundwater and Surface Water Considerations, Settlement Considerations, Allowable Foundation Bearing Pressures, Slope Stability, Effluent Disposal, Stormwater Disposal, Earthworks Considerations, Existing Fills, Conclusions and Recommendations, Data Tables.
- **Specific Items Checked**: Site history, aerial photography analysis, documentation of past/present filling, borehole locations mapped on drawings, documented topsoil and soil strengths, organic soils and groundwater mapping, sub-surface drainage, seasonal groundwater fluctuation, post-construction overland flow paths, undrained soil strengths, bulk filling settlement versus time, slope stability conditions (cut slopes, fill slopes, run-out zones, strength parameters), suitability of existing fills (engineered vs non-engineered), soakage characteristics, formal statement of professional opinion.
- **Review Stage**: Development Code review and Construction certification stages.
- **Responsible Role(s)**: Not covered in sources.

### Mason County Geologically Hazardous Areas Checklist

- **Structure**: Formal certification statement paired with signature block. Absolute validation checklist for ordinance compliance.
- **Sections Covered**: Final geotechnical report alignment with Mason County Resource Ordinance (Geologically Hazardous Areas).
- **Specific Items Checked**: Certifies that assessment demonstrates risks posed by landslide hazards can be effectively mitigated through geotechnical design recommendations. Validates hazards are mitigated to prevent harm to property, public health, and general safety.
- **Review Stage**: Final report submission and legal certification phase.
- **Responsible Role(s)**: Geotechnical Design Professional (requires signature and professional stamp).

### Oregon City Geotechnical Engineering Review Checklist

- **Structure**: Field-based verification with blank linear checkbox arrays for spatial thresholds, volumetric exemptions, and development conditions.
- **Sections Covered**: Project permit exemptions, report dating, density controls, slope disturbance parameters, zoning code alignment.
- **Specific Items Checked**: Excavation depth/volume thresholds (cut/fill <2 feet or <25 cubic yards), density limits linked to topography (slopes 25%-35% restricted to 2 dwelling units/acre), parcel size constraints (<0.5 acre = single dwelling only).
- **Review Stage**: Not covered in sources.
- **Responsible Role(s)**: Not covered in sources.

### USACE Geotechnical Design Checklist

- **Structure**: Comprehensive tabular accountability format with mandatory three-tier rating: Compliance (C), Noncompliance (NC), Nonapplicability (NA).
- **Sections Covered**: Technical drawings, project specifications, field/laboratory exploration deliverables for structural design.
- **Specific Items Checked**: All exploration logs and laboratory data physically included. Raw design parameters correctly excluded from specifications. Drawings/specs omit unapproved proprietary/sole-source materials. Testing protocols edited to match project-specific geotechnical requirements.
- **Review Stage**: Engineering design review phase.
- **Responsible Role(s)**: Formally designated Reviewer.

### MBIE/NZGS CPT Fieldwork Checklists

- **Structure**: Detailed procedural checklists (Appendix C) within MBIE/NZGS Module 2.
- **Sections Covered**: Field execution methodologies and data acquisition parameters for CPT operations.
- **Specific Items Checked**: Not covered in sources (granular items unavailable).
- **Review Stage**: Preliminary site investigation and field data acquisition.
- **Responsible Role(s)**: Ground Investigation Contractors (safe execution, data quality) under Geotechnical Professionals (CPEng or PEngGeol, minimum 10 years experience in earthquake geotechnical hazards).

### MBIE/NZGS SPT Procedures Checklist

- **Structure**: Procedural guidelines (Appendix D) in MBIE/NZGS Module 2.
- **Sections Covered**: SPT execution standards for liquefaction hazard assessments.
- **Specific Items Checked**: Strict methodological compliance for drilling and sampling. Ensures data accurately represents subsurface matrix for calculating liquefaction triggering parameters.
- **Review Stage**: Field operations and active site investigation.
- **Responsible Role(s)**: Ground Investigation Contractors and authorizing Geotechnical Professionals.

### FHWA GEC 14 GRD Quality Assurance Checklist

- **Structure**: Categorical framework with qualitative "comment forms" (no numerical scores or letter grades). Forms forwarded to authors to track error resolution.
- **Sections Covered**: General Information Form (Project Name, Section, Contracting Method), major geohazards, massive earthworks, structural foundation elements, ground improvement technologies.
- **Specific Items Checked**: Project Contracting Method, GRD Title, GRD Type (GIR, GBR, GDR, Memo), Reviewer affiliation/licensure, structural loads and load combinations (strength/service/extreme limit states), structural performance requirements, engineering calculations for embankments/cuts/landslides/retaining structures.
- **Review Stage**: Document preparation and peer review prior to finalization.
- **Responsible Role(s)**: QA Reviewer (must identify P.E. status and DOT/Firm affiliation) + GRD Author.

### TDOT Quality Assurance Milestone Checklists

- **Structure**: Standardized checklists integrated within ProjectWise digital architecture.
- **Sections Covered**: Overarching QC workflow for engineering design and deliverable documents.
- **Specific Items Checked**: Confirms each discipline has completed mandatory internal QC. Validates procedural compliance (QC documentation complete, procedures followed) rather than granular technical review.
- **Review Stage**: Milestone stage reviews during project production.
- **Responsible Role(s)**: Regional Quality Team and Project Manager.

### Auckland Council AC1009 Lodgement Checklist Commercial

- **Structure**: Hybrid regulatory structure with Yes/No/N/A tabular checklists interfacing with Practice Notes AC2229 and AC2253.
- **Sections Covered**: Resource consent integration, vehicle maneuvering, site topography, earthworks volumetrics, structural engineering producer statements, natural hazard identification.
- **Specific Items Checked**: Approved resource consent copies and stamped plans, parking gradients and vehicle crossings, impermeable coverage calculations, earthworks area and volume, structural engineering producer statements completed in full, construction monitoring levels identified, author on Council's registered Producer Statement Author list.
- **Review Stage**: Building consent and resource consent application lodgement.
- **Responsible Role(s)**: Council Officers (reviewers) and Producer Statement Authors (Registered Engineers).

### FHWA-ED-88-053 Review Checklists

- **Structure**: Formalized review checklists with associated technical guidelines for major infrastructure.
- **Sections Covered**: Major and unusual geotechnical design features, extensive earthworks, complex structural foundations.
- **Specific Items Checked**: Design parameters for deep cuts, massive fills, retaining structures requiring special attention due to size, scope, geological complexity, or cost.
- **Review Stage**: Preliminary plan phase through technical design phase (before Project Approval and Environmental Document phases conclude).
- **Responsible Role(s)**: Review Engineers and District Project Engineers.

---

## Part 2: Quality Scoring & Maturity Models

### Overview

The sector employs frameworks ranging from categorical rating systems for discrete geological samples to sophisticated digital maturity scales measuring holistic integration of geotechnical parameters into enterprise-wide modeling systems.

### SDIM-Geo-TR (Sustainable Digital Transformation in Geotechnical-Related Engineering Disciplines)

A four-stage digital maturity model specifically for transitioning fragmented, project-bound geotechnical data into unified lifecycle-integrated architectures. Developed in response to challenges in Turkiye (extreme seismicity, rapid urbanization, mega-projects).

**Four progressive levels:**

1. **Foundational Platforms**: Standardizing spatial data through GIS and BIM adoption. Addressing fragmented borehole archives.
2. **Advanced Technology Integration**: Merging foundational data with UAVs and IoT for automated field monitoring.
3. **Advanced Analytics**: Implementing predictive analytics and high-fidelity monitoring on continuous data streams.
4. **Comprehensive Digital Twin Systems**: Real-time monitoring and holistic lifecycle integration. Proactive seismic risk management and system-level coordination.

**Five assessment dimensions:**

| Dimension | Focus | Lifecycle Evolution |
|-----------|-------|-------------------|
| Sustainability Impact | Resource optimization, circular economy, environmental risk reduction | Evolves from constraint to strategic benefit |
| Technical Feasibility | Integration potential against current practices and legacy systems | Transitions from barrier to enabler |
| Data Compatibility | Interoperability and spatial standardization (GIS/BIM gaps) | Requires continuous structural development |
| Cost-Effectiveness | Financial viability of comprehensive systems vs lifecycle benefits | From investment constraint to operational benefit |
| Adoption Level | Institutional literacy, digital competency, stakeholder readiness | From fragmented expertise to mature scaling |

### Model Maturity Index (MMI)

Designed to counteract ambiguity of traditional design progress reporting. Discrete numerical definitions scaling from **100 to 600** measuring exact progression, completeness, and productivity of specific modeling disciplines.

- **MMI 100**: Existing conditions graphically represented
- **MMI 200**: Preliminary geotechnical investigation report formally received and integrated
- **MMI 300-600**: Progressive engineering verification stages

**Model MRI (Model Maturity Risk Index)**: Derivative toolkit tracking maturity of specific WBS locations while calculating risk probabilities for achieving target MMI thresholds.

### Level of Development (LOD)

Tracks progressive resolution of geometric and non-geometric BIM components. Incorporates "Schedule LODs" mapped on separate analysis scale. Evaluated dimensions:
- Geometric complexity
- Physical dimensionality
- Appearance
- Semantic presence
- Alphanumerical attributes
- Data fuzziness/uncertainty
- Quantitative properties (CityGML): triangle count, surface area, volume, memory size

### FHWA BIM for Infrastructure Maturity Model

Four levels of BIM integration (Level 0-3). Emphasizes digital information exchange depth and interdisciplinary coordination. Measures:
- Ability to extract unstructured data from GIR into structured tables for other disciplines
- Construction planning using geotechnical data
- Asset inspection forecasting integration
- Design data transfer to GIS environments

### Technology Readiness Levels (TRL)

Formal assessment metrics scaled to Level 9. Used to consistently compare operational maturity and field-proven reliability of advanced geotechnical testing methods (e.g., ERI) before project integration.

### Rock Quality Designation (RQD)

Categorical rating system based on continuous core data:
- Rating "3" for RQD 0-20%
- Rating "5" for discontinuity spacings <0.06m

### Rockfall Hazard Rating Score (RHRS)

Quantitative system for evaluating, scoring, and prioritizing unstable slope management risks.

### AGS Geotechnical Data Reliability Framework

**The closest existing analogue to SonarQube for geotechnical data.**

- Engineers assess parameters from disparate reports and input scores into a structured framework
- All scores algorithmically combined into a single reliability rating per field log
- Points color-coded within a centralized WebApp
- Provides immediate visual scoring of ground information reliability across an entire site
- Mimics dashboard functionality of a code-quality scanner

> Note: Applying SonarQube directly to evaluate geotechnical engineering reports is "Not covered in sources" -- the AGS framework operates on field data, not report documents.

---

## Part 3: Published Benchmarks & Standards

### Federal and National Highway Benchmarks

| Standard | Focus |
|----------|-------|
| FHWA GEC 14 (FHWA-HIF-17-016) | Assuring Quality in GRDs. Organizational content, roles, QA frameworks. Limits claims, change orders, bid discrepancies |
| FHWA GEC 10 (FHWA-NHI-18-024) | Construction procedures and LRFD design for drilled shafts |
| FHWA-ED-88-053 | Review checklists for major earthworks, deep foundations, retaining structures |

### Digital Data Exchange Standards

| Standard | Focus |
|----------|-------|
| AGS Data Format (3.1, 4.0.4) | Strict data dictionary rules mandating relational formatting of electronic geotechnical data. Rigid structures for pick lists and data groups (ABBR, CODE, UNIT). Eliminates manual transcription errors, ensures software backward compatibility |

### International and Regional Geotechnical Codes

| Standard | Focus |
|----------|-------|
| MBIE/NZGS Module 2 | Geotechnical Investigations for Earthquake Engineering (NZ). Minimum required technical content, conceptual model refinement, limitations statements, CPT/SPT methodology |
| MBIE/NZGS Module 3 | Liquefaction hazard identification/assessment/mitigation. Boulanger & Idriss (2014) methodology |
| BS EN 1997-1:2004 (Eurocode 7) | Geotechnical Categories (1-3) scaled by ground complexity and risk. Determines mandatory investigation scope |
| BS6031 | British Code of Practice for Earthworks |
| CD 622 (Rev 2.0.0) | Managing Geotechnical Risk. Requires GDR and GFR. GFR forces alignment of predicted vs observed conditions |

### Municipal Regulatory Standards

| Standard | Focus |
|----------|-------|
| Auckland Council AC2229 | Legislative compliance for land subject to extreme natural hazards (coastal instability, severe landslides). Macro-to-local assessment hierarchy |
| Auckland Council AC2253 | Formatting standard for consistent interpretation across meta-analysis studies and regional geotechnical maps |
| Auckland Transport ATCOP | Unified code consolidating seven former legacy councils' standards. Minimum standards of work, prevents asset degradation |

---

## Key Implications for GeoSonar Platform Design

### 1. Rule Engine Architecture

The checklists reveal a consistent pattern: **Boolean pass/fail items** that can be encoded as deterministic rules. The platform needs:
- A configurable rule registry (analogous to SonarQube's Quality Profiles)
- Rules categorized by: jurisdiction (NZ/AU/international), report type (GIR/GBR/GDR/GFR), and review stage (draft/final/lodgement)
- Three-tier rating output: Compliant / Non-Compliant / Not Applicable

### 2. No Existing Numerical Scoring for Report Quality

The AGS Data Reliability Framework is the closest analogue but operates on **field data**, not **report documents**. GeoSonar would be genuinely novel as an automated report-quality scorer.

### 3. Maturity Model as Portfolio Metric

The MMI (100-600) scale provides a tested mental model for "how complete/mature is this deliverable." A firm-level dashboard could adopt a similar categorical scale for report quality maturity, giving TR/PD an at-a-glance portfolio health view.

### 4. Standards Compliance is Jurisdictionally Specific

The platform must support jurisdiction-specific rule profiles (MBIE/NZGS for NZ, Eurocode 7 for UK/EU, FHWA for US). This aligns with Redline's existing per-jurisdiction approach.

### 5. The Quality Gate Pattern is Universal

Every reviewed checklist implements a gate: the report cannot progress to the next stage until the checklist passes. This validates the "author must pass gate OR document exception" workflow design.

### 6. Word Task Pane as CI/CD Analogue

In software, SonarQube triggers in the CI/CD pipeline. In geotechnical reporting, the equivalent trigger points are:
- **Draft stage** (before TR review) -- triggered from Word task pane
- **Final stage** (before PD sign-off) -- triggered from Word task pane or dashboard
- **Lodgement stage** (before submission to council) -- triggered from portfolio dashboard

### 7. Producer Statement Author Registry

Auckland Council requires authors to be on a registered list. The platform could integrate CPEng/PEngGeol verification as a gate -- confirming the signing engineer has appropriate credentials for the report type.
