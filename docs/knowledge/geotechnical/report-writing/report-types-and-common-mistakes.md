# Geotechnical Report Types and Common Mistakes

**Sub-domain**: report-writing
**Last verified**: 2026-05-17
**Confidence**: cross-referenced
**Sources**: Geotechnical Report Workflows (GRW), Risk Assessment in Engineering (RA),
Geotechnical Baseline Reports (GBR notebook), Ground Engineering Magazine (GEM),
Engineering Standards (ES), knowledge store documents (geotechnical-report-quality-dimensions,
claude-gbr-demo-review, parameter-completeness-checking-standard-of-care,
design-type-taxonomy-and-parameter-completeness)

## Summary

Geotechnical engineers in NZ/AU practice produce seven distinct report types, each serving
a different purpose in the project lifecycle. The five most common mistakes — all of which
have produced professional liability claims — are: (1) taboo/absolute language that voids
PLI cover, (2) missing or vague scope limitations, (3) omitted parameters and information,
(4) extraneous padding that provides ammunition for claims, and (5) outdated or incorrect
standards citations. These defects span four quality layers: mechanical/formatting,
structural completeness, linguistic/liability risk, and technical defensibility.

## Part 1 — Report Types

### 1. Geotechnical Desktop Study Report

A preliminary assessment prepared at the concept stage of a project, before any physical
site investigation. Reviews existing archival information, historical aerial imagery,
published geology, and previous ground investigations to establish a preliminary ground
model, identify potential geotechnical hazards, and recommend the scope for future physical
investigations [GRW: citations 1-4].

**When used**: Very beginning of a project. Sets the scene for all subsequent work.

### 2. Geotechnical Factual Report (GFR)

The definitive record of factual surface and subsurface geotechnical data. Strictly
separates observable facts from subjective conclusions. Contains borehole and test pit
logs, laboratory testing results, geomorphological mapping, and groundwater monitoring
data. Presented in accordance with NZGS 0200 standards [GRW: citations 5-12].

**When used**: Immediately after site investigations are completed, before any
interpretive analysis begins.

### 3. Geotechnical Interpretive Report (GIR)

Uses the factual data from the GFR to derive a geological ground model, establish
engineering design parameters (soil shear strength, permeability, etc.), determine seismic
hazards, and provide mitigation recommendations. Often formatted for direct inclusion in
regulatory submissions such as an Assessment of Environmental Effects (AEE) [GRW:
citations 13-17].

**When used**: Follows the GFR. Informs detailed design phases.

### 4. Slope Stability and Settlement Report (SSSR)

An analytical report evaluating the static and seismic stability of natural and engineered
slopes, and estimating long-term ground settlement. Uses finite element modelling software
(GeoStudio Slope/W, PLAXIS). Can be a standalone report or form part of a GIR [GRW:
citations 17-20].

**When used**: When slope performance or settlement is a design-critical issue.

### 5. Geotechnical Baseline Report (GBR)

A binding contract document containing measurable descriptions of anticipated subsurface
conditions. Used to allocate ground-related financial risk between the employer and
contractor. Distinct from other report types because it creates contractual obligations —
every word carries legal weight [GBR notebook: citations 1-2; RA: DSC clause context].

**When used**: Major infrastructure and tunnelling projects where subsurface risk
allocation is contractually significant.

### 6. Letter Report

A condensed report format for smaller scopes of work, short assessments, or reporting on
specific trials when a full report is unnecessary [GRW: citations 25, 27].

**When used**: Small projects, trial results, preliminary advice.

### 7. Multi-Disciplinary Design Reports (Preliminary / Detailed)

Reports that include dedicated geotechnical design statements alongside civil, structural,
coastal, and other engineering inputs. Contains design philosophy, methodology, design
standards, constructability, and safety-in-design sections [GRW: citations 28-33].

**When used**: Resource consent applications, detailed design packages, construction
issue documentation.

### Also: NHI Act Assessment Reports

A specialised assessment report format used for Natural Hazards Cover (NHCover) land claims
under the NHI Act. Documents property damage, unrepairable land, and conceptual
remediation strategies following a natural hazard event [GRW: citations 21-23].

## Part 2 — Most Common Mistakes

### Mistake 1 — Taboo and Absolute Language (Voids PLI Cover)

Using words like "all", "every", "always", "never", "ensure", "guarantee", "certify",
"safe", "must", "zero", or "final" in a report. These words elevate the standard of care
from negligence (doing what a reasonable professional would do) to strict liability
(guaranteeing a specific result), which is excluded from professional indemnity insurance
(PLI) policies. A single instance of "we guarantee the foundation will be safe" can void
coverage for the entire claim [RA: citations 29-32; quality-dimensions doc: Key Fact 7].

**Also dangerous**: Ambiguity traps like "adequate", "sufficient", "general compliance",
"highest quality", "timely manner", "workmanlike", "supervise" — courts interpret these
terms to the engineer's detriment [RA: citations 23-25; quality-dimensions doc: Key Fact 8].

### Mistake 2 — Missing or Vague Scope Limitations

Failing to include an Applicability section (scope limitation) that restricts third-party
reliance, states that conditions are inferred between investigation locations, sets a
temporal boundary, and requires notification if conditions change. Without this, courts
will infer that the engineer undertook a comprehensive investigation meeting the full
standard of the profession. This is the single most consequential omission in a report
[RA: citations 18, 26-30; pre-review doc: SCOPE-LIM-01].

**How it happens**: Engineers omit the Applicability section entirely in rushed reports —
not through poor wording, but through complete omission.

### Mistake 3 — Omitted Parameters and Information

Failing to document key assumptions, design parameters, or investigation limitations.
Case law demonstrates clear liability:

- *Unit Farm Concrete Products Ltd v Eckerlea Acres Ltd*: Engineer failed to note a
  missing rebar schedule — found negligent [RA: Source 11].
- *Brown & Huston Ltd v City of York*: Engineers omitted a soils report and groundwater
  data from a tender package — held 75% liable [RA: Sources 12, 17, 23-24].
- *Mawson Gage Associates Ltd v R*: Missing pages of specifications from tender details
  led to a successful tort claim [RA: Source 18].

The IDS requires that design reports include "the constraints, parameters, assumptions and
raw data on which the design is based" [ES: Source 10]. Omission of "vital" information
constitutes a breach of the standard of care [RA: Source 11].

### Mistake 4 — Extraneous Padding

Padding a report with excessive factual data or geological descriptions that provide
ammunition for contractor claims. In Case History V, a report included an overly
comprehensive geological description — including "thinly bedded" — which the contractor
scrutinised after encountering excavation difficulties and successfully claimed extra
payment for overbreak [RA: citations 25-27].

The opposite of Mistake 3, but equally dangerous. Corporate guidance actively warns:
"many of our reports are too wordy and complex" and include "information which is not
relevant to the reader" [GRW: Source 4].

### Mistake 5 — Outdated or Incorrect Standards Citations

Citing superseded standards, wrong clause numbers, or standards from the wrong
jurisdiction. The Claude-generated GBR review documented six specific citation errors
including: NZS 4431 completely absent (the governing compliance framework), incorrect
NZS 4402 clause numbering, citing ASTM standards instead of NZ equivalents, citing a
roading standard (NZS 4407) for SPT testing (a hallucination), and citing a superseded
Transit NZ specification [claude-gbr-demo-review].

**How it happens**: Engineers recycle sections from old reports (warned against by
corporate guidance [GRW: citations 19-21]), or AI-generated content hallucinates plausible
but incorrect standard references.

### Mistake 6 — Misrepresentation by Silence

Observing a problem during site work but remaining silent because the engineer believes
their limited contract does not require intervention. In Case History IX, a geotechnical
engineer observed a poorly shaped sand preload but stayed silent — the court ruled this
fell short of the standard of care and held the engineer 50% liable [RA: citations 21-22].

### Mistake 7 — Simplistic Interpolation Between Boreholes

Connecting subsurface data points with straight lines without qualification, especially
when the investigation spacing does not support such interpolation. In Case History VI,
an engineer connected rock elevations between boreholes 150 metres apart with straight
lines. A hidden knob of bedrock was encountered during construction, causing massive cost
overruns. Both the prime consultant and the geotechnical consultant lost credibility
[RA: citations 11-13].

## Open Questions

1. What proportion of NZ/AU liability claims fall into each of these seven mistake
   categories? No breakdown by category exists in the sources.
2. Are there additional report types used in NZ/AU practice that are not represented
   in the notebook sources (e.g., contamination assessment reports, pavement subgrade
   reports)?

## Further Reading

- I have not verified these sources, but they may contain relevant data:
  - ACENZ Practice Note on Professional Indemnity Insurance claims analysis
  - Engineering NZ guidance on report writing standards
  - CEAS (Consulting Engineers Advancement Society) Indemnity Matters newsletter archive
  - NZGS Module 2 — Guidelines for Geotechnical Reporting
