# UI Terminology Glossary for Geotechnical Products

**Sub-domain**: report-writing
**Last verified**: 2026-05-09
**Confidence**: practitioner-grounded
**Sources**: Geotechnical Report Workflows, Engineering Standards, GBR notebook,
dropdown parameter sufficiency research (2026-04-21), GIR skeleton research (2026-04-11)

**Purpose**: Reference document for Matt (UI/UX Designer) and any contributor who writes
UI labels, dropdown options, placeholder text, tooltips, error messages, or section
headings that contain geotechnical terminology. All terms must be used exactly as defined
here. Do not abbreviate, simplify, or rename without Graeme's approval.

## Summary

This glossary defines every geotechnical term likely to appear in Redline product
surfaces. It is organised by UI context (where the term appears) rather than by
engineering sub-discipline. Each entry includes the correct term, acceptable abbreviation
(if any), a plain-English definition, and common mistakes to avoid.

## Report Type Terms

| Correct term | Abbreviation | Definition | Do NOT use |
| --- | --- | --- | --- |
| Geotechnical Interpretive Report | GIR | Engineering interpretation of ground conditions for design. Contains professional judgment. | "Interpretive report" alone (ambiguous), "Ground report", "Geotech report" |
| Geotechnical Baseline Report | GBR | Contractual document defining anticipated subsurface conditions for financial risk allocation between owner and contractor. | "Baseline report" alone (ambiguous), interchangeable with GIR |
| Geotechnical Factual Report | GFR | Raw data from ground investigation — bore logs, test results, lab certificates. No engineering interpretation. | "Data report", "Investigation report" |
| Letter of Engagement | LOE | Contractual scope document between consultancy and client. Defines inclusions and exclusions. | "Contract", "Proposal", "Brief" |

## Investigation and Testing Terms

| Correct term | Abbreviation | Definition | Do NOT use |
| --- | --- | --- | --- |
| Borehole | — | A drilled hole in the ground for sampling and testing. | "Bore hole" (two words) |
| Bore log / borehole log | — | Written record of subsurface conditions from a single borehole. | "Drill log", "soil log" |
| Test pit | — | Shallow excavation (typically <4.5 m) to expose near-surface soils. | "Trial pit" (UK term) |
| Cone Penetration Test | CPT | In-situ test pushing an instrumented cone into the ground. | "Cone Penetrometer Test" |
| Standard Penetration Test | SPT | In-situ test measuring resistance to driving a sampler. Result is the N-value. | "SPT value" without specifying raw N or corrected N₆₀ |
| In-situ testing | — | Testing performed in the ground at the test location. | "On-site testing" (ambiguous) |
| Laboratory testing | — | Testing performed on samples in a laboratory. | "Lab testing" in formal UI (acceptable in tooltips) |

## Geotechnical Hazard Terms

| Correct term | Definition | UI presentation notes |
| --- | --- | --- |
| Liquefaction | Loss of soil strength during earthquake shaking, causing ground to behave like a liquid. | Three-tier dropdown: (1) Does not dictate design, (2) Limited impact, (3) Important issue for design. Never a simple yes/no. |
| Lateral spread | Horizontal ground displacement during liquefaction, typically towards a free face. | Specific liquefaction consequence — not generic "ground movement". |
| Fault rupture | Ground displacement along a geological fault during an earthquake. | One specific seismic hazard type — not synonymous with "seismic hazard". |
| Slope stability | Engineering assessment of whether a slope will remain stable under loading. | Not "landslide risk" (that is the failure event, not the assessment). |
| Artesian pressure | Groundwater pressure that exceeds hydrostatic — water rises above the ground surface if penetrated. | Not "high groundwater" (related but distinct). |

## Section Structure Terms

| Correct term | Definition | Do NOT use |
| --- | --- | --- |
| Client Summary | Default front-matter summary (max 1 page, plain language). | "Executive Summary" — only if client explicitly requests in LOE. |
| Applicability | Section stating what the report covers, what it does not, and conditions of validity. Includes limitations and disclaimers. | "Scope" (different meaning), "Disclaimer" (subset of Applicability) |
| Site Description | Description of the physical site as it currently exists. | Not "Project Description" (what is being built). |
| Seismic site subsoil class | NZS 1170.5 classification (Class A through E) for design earthquake loads. | "Soil class", "site class" (incomplete terms). |

## Metadata and Document Control Terms

| Correct term | Definition | Do NOT use |
| --- | --- | --- |
| Job number | Internal reference number for the project within the consultancy. | "Project number", "Reference number" |
| Prepared by | The originating engineer who wrote the report. | "Author" (acceptable in tooltips, not in formal document control) |
| Reviewed by | Independent technical reviewer (same discipline, different person). | "Checked by" (implies less rigour than review) |
| Authorised by | Project Director who takes responsibility for the final document. | "Approved by" (implies client approval, not internal authorisation) |
| Producer Statement — Design | PS1 | Formal certification by a named CPEng that the design complies with the Building Code. | Never imply Redline issues or co-signs a PS. |
| Producer Statement — Design Review | PS2 | Formal certification that an independent review of the design has been completed. | As above. |
| Producer Statement — Construction Review | PS4 | Formal certification that construction was reviewed for compliance with the design. | As above. |

## Professional Terms

| Correct term | Abbreviation | Definition |
| --- | --- | --- |
| Chartered Professional Engineer | CPEng | NZ registration for engineers authorised to practise independently. |
| Person Conducting a Business or Undertaking | PCBU | Health and Safety at Work Act 2015 duty holder. |
| Standard of care | — | Legal benchmark: the skill, care, and diligence ordinarily exercised by practitioners under similar conditions. |

## Canterbury-Specific Terms

| Correct term | Definition | UI notes |
| --- | --- | --- |
| MBIE earthquake rebuild guidelines | Ministry of Business, Innovation and Employment guidance for Canterbury rebuild. | Not optional — regulatory requirement for Canterbury projects. |
| Liquefaction Resistance Index (LR 0-4) | Canterbury-specific zoning for liquefaction susceptibility. | Specific to Canterbury, not applicable elsewhere in NZ. |
| Christchurch Drainage Datum | Local datum for drainage design in Christchurch. | Canterbury-specific metadata field. |
| Port Hills rockfall hazard zones | GNS-defined hazard zones for rockfall in the Port Hills area. | Triggers additional section requirements. |

## Rules for Matt

1. **Never rename a term for UI aesthetics without Graeme's approval.** "GIR" is
   acceptable as a short label; "Ground Report" is not.
2. **Always expand abbreviations on first use.** Dropdown labels can use abbreviations
   (GIR, GBR, CPT) but tooltips must show the full term and a one-sentence definition.
3. **Canterbury is not optional.** Canterbury-specific parameters are regulatory
   requirements triggered by project location, not preferences.
4. **Liquefaction is three-tier, not binary.** The dropdown must offer three options, not
   yes/no.
5. **"Client Summary" is the default heading.** Never default to "Executive Summary".
6. **The Applicability section cannot be removed.** Any "customise your skeleton" UI must
   lock this section as mandatory.
7. **Redline does not practise engineering.** Every label, heading, and micro-copy must
   reinforce that Redline provides structure and completeness checking, not engineering
   judgment.
