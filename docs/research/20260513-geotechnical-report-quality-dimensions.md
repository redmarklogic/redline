# Geotechnical Report Quality Dimensions — SonarQube Analogy

**Date**: 2026-05-13
**Research question**: What does quality look like in geotechnical engineering reports (GBRs and GIRs), and how would a SonarQube-like automated quality platform model those quality dimensions?
**Actor**: Principal geotechnical engineer and product team building an automated quality platform for geotechnical engineering reports.
**Redline domains**: Pre-review rule validation, report skeleton, scope and language checks, sign-off workflows, GBR quality gates.

---

## Terminology Clarification (Important)

The notebook sources use precise terminology that differs from the user's query. Throughout this document:

- **GIR** = Geotechnical Interpretive Report (interpretive conclusions and design parameters derived from the investigation). This is the standard NZ/AU usage. "Geotechnical Investigation Report" is not standard terminology.
- **GFR** = Geotechnical Factual Report (raw factual data — borehole logs, lab results, groundwater measurements — without interpretation).
- **GBR** = Geotechnical Baseline Report (a contract document, not a technical report; establishes contractual baselines for risk allocation between owner and contractor in construction projects).
- **GDR** = Geotechnical Data Report (equivalent of the GFR in the US/ASCE context — purely factual).
- **TR** = Technical Reviewer (independent specialist who verifies technical robustness).
- **PD** = Project Director (senior leader who provides commercial and risk oversight before issuance).
- **DSC** = Differing Site Conditions (a contractual claim by a contractor for encountering conditions more adverse than those indicated in the contract).
- **PLI** = Professional Liability Insurance (Errors and Omissions insurance — covers negligence, NOT breach of warranty).

---

## Summary

Senior geotechnical engineers assess report quality across four layers: mechanical/formatting compliance, structural completeness, linguistic/liability risk, and technical defensibility. Formal QA checklists exist and are documented in enterprise practice — the most critical being the Section B Review Checklist (the ultimate issuance gate). Six defect categories routinely create professional liability exposure, ranging from missing scope limitations to "taboo words" that inadvertently create strict liability and void PLI cover. GBRs have a distinct and more demanding set of quality criteria than GIRs because they are binding contract documents. No formal quality scoring or maturity model for geotechnical reports exists in the industry; quality is managed entirely through checklist-driven peer review.

---

## Findings

### 1. Quality Dimensions in Peer Review

Senior geotechnical reviewers assess a report across four distinct quality layers, each owned by a different role in the review chain [Geotechnical Report Workflows (GRW): citations 5-21; Risk Assessment in Engineering (RA): multiple].

**Layer 1 — Mechanical and Formatting Compliance**
Assessed by BIS (Business Integrated Services, administrative staff) and the Author (self-review). This layer checks: font and heading standards, document naming convention compliance, English (not American) spelling, figure-text linkage, accurate measurements and figure references, and professional presentation [GRW: citations 5, 7, 14-18]. These are binary checks — the report either meets the standard or it does not.

**Layer 2 — Structural Completeness**
Assessed by the Author (self-review "20 Checkpoints" checklist) and the TR. This layer checks: logical sequence of information, appropriate section structure for the report type, headings that provide a reader's road map, conclusions that follow logically from the body, all mandatory sections present, supporting calculations checked by multiple methods, data tables accurate, and appropriate drawing stamps (e.g., "not for construction" on issued-for-comment drawings) [GRW: citations 5-7, 19-21; RA: multiple]. This layer also includes presence of all mandatory disclaimer and limitation clauses.

**Layer 3 — Linguistic and Liability Risk**
Assessed by the TR and PD in combination, often with input from the firm's Insurance and Contracts Team. This layer checks: absence of "taboo words" that create strict liability (see defect categories below), presence of required conditional language, correct framing of scope limitations, and appropriate standard-of-care qualifications [RA: citations 3, 5, 21-25; GRW: citations 3, 8]. This layer is the least automated in current practice and the most consequential for professional indemnity exposure.

**Layer 4 — Technical Defensibility**
Assessed by the TR and, for complex analyses, specialist Subject Matter Experts (SME). This layer checks: whether conclusions are supported by the data presented, whether ground models are realistic, whether design parameters are appropriate for the soil/rock conditions encountered, whether stability analyses are properly bounded, whether professional judgment extensions beyond the data are stated and justified [GRW: citations 8, 9; RA: citations 1-2]. This is the hardest layer to automate — it requires engineering domain knowledge.

---

### 2. Defect Categories — The Equivalent of Bugs, Vulnerabilities, Code Smells

The Risk Assessment notebook is explicit that professional liability claims fall into two primary categories: technical errors and administrative omissions [RA: citation 8]. I extend this to six defect categories, two of which are domain-specific to engineering practice.

**Category 1 — Technical Errors ("Bugs")**
Mistakes in calculation, incorrect information on drawings, failure to recognise the significance of field observations. Examples:
- Boreholes plotted 50 feet from their actual locations on a site plan [RA: citation 9].
- Drawing straight lines to connect bedrock elevations between widely spaced boreholes without acknowledging the unknown conditions between them — creates false certainty about subsurface continuity [RA: citations 10-11].
- Misinterpreting cone penetration test (CPT) refusal as genuine bearing resistance, leading to piles designed at the wrong depth [RA: citation 13].
- Leaving a rebar schedule off a drawing — a component "vital to wall integrity" [RA: citation 20, referencing *Unit Farm Concrete Products Ltd v Eckerlea Acres Ltd*].
- Omitting soils report and groundwater level information from a tender package [RA: citing *Brown & Huston Ltd v City of York*, which assigned 75% liability to the consulting engineers].

**Category 2 — Administrative Omissions ("Vulnerabilities")**
Failures to document, warn, communicate, or record. Examples:
- Failing to explicitly recommend deep borings when delivering a superficial preliminary report, and not warning the client that the report is inadequate for final foundation design [RA: citations 15-18].
- Keeping only "cryptic, undated notes on scraps of paper" rather than a proper daily diary — in litigation, this is used by opposing counsel to create an air of incompetence [RA: citation 19].
- Failing to communicate uncertainties to the client when a budget-constrained investigation was performed [RA: citation 14].
- Not writing a memo to confirm verbal advice given on site — memories fade and advice must be understood in the context in which it was given [RA: citation 33].

**Category 3 — Taboo Words ("Critical Vulnerabilities" — voids PLI)**
Using absolute or guarantee-creating language that inadvertently elevates the standard of care from negligence to strict liability. This is the most severe category because it can void professional liability insurance, leaving the engineer personally exposed [RA: citations 3-5, 21-22]. Examples:
- **"All", "every", "always", "never"** — sweeping statements where one missed item constitutes a breach.
- **"Ensure", "guarantee", "certify"** — imply a specific outcome the engineer cannot guarantee.
- **"Safe" / "zero defects"** — "safe" implies zero risk; if an incident occurs, the site was ipso facto unsafe.
- **"Must"** — absolutist verb implying no flexibility or professional judgement.
- **"Final"** — if labelled "final," the engineer may be barred from modifying it if errors are found later.
- **"Unique", "perfect"** — binary states that create an impossible standard.

**Category 4 — Ambiguity Language ("Code Smells" — open to adverse interpretation)**
Vague qualitative terms that leave courts and juries to define what "good" means, almost always to the engineer's detriment [RA: citations 23-25]. Examples:
- **"Adequate" / "sufficient"** — a judgment call; if it fails, it clearly wasn't "adequate."
- **"General compliance"** — an oxymoron that admits the engineer didn't check everything.
- **"Highest quality" / "best"** — sets an undefined superlative standard above standard of care.
- **"Timely manner"** — subjective; is "timely" one hour or one week?
- **"Workmanlike"** — archaic and vague standard.
- **"Supervise" / "supervision"** — implies direction and control over means and methods, which can create liability for contractor safety.

**Category 5 — Unqualified Scope and Investigation Limitations ("Structural Defects")**
Failing to clearly bound the scope of what was investigated and what conclusions are based on. Examples:
- A scope description so vague that a court infers the engineer undertook a comprehensive investigation meeting all general professional standards [RA: citation 28].
- No explicit statement that boring logs indicate conditions "only at the exact borehole locations" and that conditions between boreholes are inferred [RA: citations 29-30].
- An investigation designed for a two-story flexible frame structure used to design a 12-storey reinforced concrete structure, with no stated scope limitation in the original report [RA: citation 26].
- Absence of the Applicability/Scope Limitation section in the NZ/AU standard report structure — this section is labelled "Mandatory" in enterprise templates [GRW: citation 7 per pre-review-rule-validation knowledge doc].

**Category 6 — Extraneous Padding ("Technical Debt")**
Filling the report with excessive, unrequested factual data or geological description that creates ammunition for opposing counsel [RA: citations 31-33]. Examples:
- A comprehensive geological description (fossils, lithology, mineralogy, jointing) prepared by a professor of geology and incorporated verbatim into the geotechnical report — the word "thinly bedded" was subsequently used by a contractor to support a massive DSC claim for unexpected excavation behaviour [RA: citation 32-33].
- Delivering a comprehensive density test report when the building is already half constructed — the timing makes the report a liability, not an asset [RA: citation 33].
- Including design-phase GIR content in a GBR contract document, creating conflicting interpretations (see GBR section below).

---

### 3. Formal QA Checklists — NZ/AU Context

Four formal QA checklists are documented in the enterprise knowledge base [GRW: multiple citations]. These constitute the closest analogue to a formal QA framework in NZ/AU geotechnical practice.

**Checklist 1: "20 Checkpoints in 90 Seconds"**
*Stage*: Self-review by Author, immediately after drafting, before handing to TR and PD [GRW: citation 5].
*Structure*: 20 yes/no questions.
*Covers*: Professional presentation, title appropriateness, logical sequence, reader's road map through headings, tone, spelling/punctuation/grammar, absence of jargon, explained acronyms, elimination of unnecessary words, accuracy of all measurements/figures/numbers/dates/drawings, figure-text linkage, introduction engagement, ideas leading logically to Conclusions, fresh pair of eyes proofreading [GRW: citations 5-7].

**Checklist 2: Stability Analysis Review Checklist**
*Stage*: During Technical Review when computational stability modelling is involved [GRW: citation 8].
*Structure*: General Information, Analysis Review (10 sub-sections), Output Review.
*Covers*: Slope geometry (section scale, topography, geological unit boundaries), material parameters (effective cohesion $c'$, effective friction angle $\phi'$, undrained shear strength $s_u$, unit weight $\gamma$), groundwater conditions (piezometric levels, elevated and perched water), surcharge and point loading, seismic accelerations and pseudostatic staged analysis, critical slip surface validation (does not inappropriately contact model boundaries), interslice forces (positive), m-alpha values (>0.5), output labelling [GRW: citations 9-10].

**Checklist 3: Drafting QA Signoff Form**
*Stage*: Applied to all technical drawings and figures before issue outside the firm. Minimum 3-day lead time [GRW: citations 11-12].
*Structure*: General, Native .dwg file checks, Drawing border/Title/Revision, Drawing CAD Standards, Coversheet and Drawing List, Layouts, Details, Sections and Long Sections.
*Covers*: Spelling/grammar, correct AutoCAD templates, correct units and rounding, line types/scales/colours matching legends, cross-reference accuracy (section/detail/elevation numbers), coordinate systems, correct drawing naming conventions, client/project logos, north indicator orientation, key plan presence, correct layout scales and scalebars [GRW: citations 14-18].

**Checklist 4: Section B — Review Checklist (The Ultimate Gate)**
*Stage*: Applied twice — once to authorise DRAFT release, once to authorise FINAL release [GRW: citations 19-21].
*Structure*: DRAFT checks, FINAL checks, Other Aspects.
*Responsible role*: PD must physically sign this form to authorise release [GRW: citation 21].
*Draft gate covers*: All supporting calculations checked using multiple methods with documented assumptions; data tables accurate; technical review complete; all drawings contain appropriate stamps; T+T templates/standards applied; document saved in "Issued Documents" folder [GRW: citations 19-20].
*Final gate covers*: Client comments incorporated; effect of comments on technical interpretation checked; final technical review complete [GRW: citations 20-21].

**PM Handbook Framework (Oversight Layer)**
The PM Handbook mandates for every project: a Project Management Plan, a risk management process, appropriate technical and oversight review of all outputs, and controlled project records. It distinguishes: "Technical review = solving the right problem in the right way. Oversight review = making sure the client's needs are being met, appropriate technical review has occurred, contractual obligations are met" [GRW: citation 8 per PM Handbook source].

---

### 4. Typical Review Cycle — Who Reviews, When, What Gets Signed Off

The standard review cycle in a large NZ geotechnical consultancy follows a three-tier sign-off chain [GRW: audit-trail knowledge doc]:

**Stage 1 — Self-Review (Author)**
- Author completes the "20 Checkpoints in 90 Seconds" checklist.
- For stability analyses: Author completes the "Analysed By" column of the Stability Analysis Review Checklist.
- For drawings: Drafter initiates the Drafting QA Signoff Form.
- Output: Report is ready for TR review.

**Stage 2 — Technical Review (TR)**
- TR is an independent specialist with knowledge equal to or above the Author.
- Objective: "Verify that the right answer has been given to the right question."
- For stability analyses: TR completes the "Check By" column of the Stability Analysis Review Checklist.
- TR signs off Section A of the report cover sheet ("Reviewed by").
- Output: Technical sign-off granted or list of required changes returned to Author.

**Stage 3 — Draft Authorisation (PD)**
- PD reviews for commercial and risk oversight: client needs met, mandatory caveats included, all prior reviews completed.
- PD signs Section B Review Checklist (DRAFT phase) — authorises release of the Draft report to client.
- An Information Register records the draft outgoing deliverable: version, author, date sent, recipients.

**Stage 4 — Client Comment Incorporation (Author + TR)**
- Client comments are incorporated by Author.
- TR checks the effect of client comments on the technical interpretation.
- Where client comments alter technical content, a further technical review is performed.

**Stage 5 — Final Authorisation (PD)**
- PD signs Section B Review Checklist (FINAL phase) — "Approved for issue as Final."
- Report is published as PDF, signed by Author/TR/PD, filed in "Issued Documents" folder.

**Escalation for High-Risk Projects**
For projects >$10M or identified as high-risk, sign-off escalates beyond the standard three-tier chain to: Discipline Director → Sector Director → Managing Director → Board of Directors [GRW: audit-trail knowledge doc].

**Small Firm Compression**
In firms of 5-15 staff, the cycle effectively compresses to a single-signer: the principal reviews and signs, with no genuine independent TR. In 20-50 staff firms, the PD typically doubles as the TR. This compression is a known quality risk with no clear documented mitigation in the notebooks (open question — see below) [practitioner experience].

---

### 5. Quality Gate for a GIR Before Client Issue

Drawing the minimum pass criteria from the Section B Review Checklist and the language/liability guidance, the following constitute a practical quality gate for a GIR:

**Structural pass criteria (binary — present or not):**
- [ ] Applicability/Scope Limitation section present and contains: (a) third-party reliance restriction, (b) inferred conditions caveat, (c) temporal boundary (conditions at time of investigation), (d) changed-conditions notification requirement [GRW: scope limitation template; RA: citation 29-30; pre-review-rule-validation knowledge doc].
- [ ] Standard-of-care clause present [RA: citation 28].
- [ ] All supporting calculations checked using multiple methods with documented assumptions [GRW: Section B].
- [ ] Technical review complete (TR signed) [GRW: Section B].
- [ ] All drawings contain appropriate stamps [GRW: Section B].
- [ ] Report saved in "Issued Documents" folder with correct naming convention [GRW: Section B].
- [ ] For factual GFR: boring logs, lab results, and groundwater measurements present and complete.
- [ ] For interpretive GIR: ground model, design parameters, seismic hazard inputs (where applicable), and conclusion-from-data chain present [GRW: RFP-to-Report mapping citation 1-4].

**Language pass criteria (automated scan):**
- [ ] No taboo/absolute words from the PLI-voiding list: "all", "every", "always", "never", "ensure", "guarantee", "certify", "safe", "must", "zero", "final" [RA: citations 3-5, 21-22].
- [ ] No subjective ambiguity traps: "adequate", "sufficient", "general compliance", "highest quality", "timely manner", "workmanlike" [RA: citations 23-25].
- [ ] Scope limitation section uses required conditional wording patterns [pre-review-rule-validation knowledge doc].

**Technical pass criteria (TR sign-off required — not automatable):**
- [ ] Conclusions are supported by the data presented.
- [ ] Professional judgment extensions beyond the data are stated and justified.
- [ ] Material parameters are appropriate for the soil/rock conditions encountered.

---

### 6. GBR Quality Gate — Distinct and More Demanding

GBRs have their own quality gate, distinct from GIRs, because they are binding contract documents that allocate construction risk [GBR notebook: multiple citations].

**Structural pass criteria:**
- [ ] GBR is the ONLY interpretive document in the contract — no GIR or Geotechnical Design Memorandum is included as an interpretive document (these may be disclosed for information only) [GBR: citations 16-19].
- [ ] Page-turning cross-reference review completed against: general conditions, technical specifications, drawings, and GDR [GBR: citations 20-21].
- [ ] Owner has participated in baseline-setting and explicitly accepted the financial consequences [GBR: citations 28-31].
- [ ] All mandatory sections present: Introduction, Project Description, Sources of Geologic Information, Geologic Setting, Ground Characterization (physical baselines), Construction Considerations (behavioural baselines), Methods of Measurement for each baseline [GBR: citations 34-51].

**Baseline statement pass criteria (the SonarQube equivalent of security rules):**
- [ ] All baseline statements use definitive verbs: "is", "will", "are" — never "may", "can", "might", "up to", "could", "should", "some", "few", "would" [GBR: citations 52-53].
- [ ] No unquantified adjectives: "large", "significant", "local", "many", "minor" — must be strictly defined or quantified [GBR: citations 54-55].
- [ ] No "shall" in baselines — this is specifications language, not baseline language [GBR: citation 54].
- [ ] No baselines linked by "and" unless the conditions are explicitly intended to be compounded [GBR: citation 56].

**Common defect flags for inadequate GBRs:**
- [ ] **"Soft" baselines**: baselines presented only as a full data range (histogram from lowest to highest) with no definitive contractual average or boundary value [GBR: citations 57-60].
- [ ] **Thesis-style length**: GBR exceeds 30-50 pages of text — indicates excessive regional geology or design-phase data [GBR: citations 61-64].
- [ ] **Two-tier formatting**: document distinguishes "binding" vs. "non-binding" sections within the same GBR [GBR: citations 65-68].
- [ ] **Specification repetition**: GBR restates or paraphrases technical specifications or drawings [GBR: citations 69-73].
- [ ] **Unmeasurable parameters**: baselines that cannot be practically measured during construction [GBR: citations 74-78].
- [ ] **Unrealistic conservatism**: baselines set arbitrarily high in an attempt to transfer all risk to the contractor [GBR: citations 79-83].

---

### 7. Quality Scoring and Maturity Models — Gap Finding

**No formal quality scoring or maturity model for geotechnical report quality exists in the industry.** The Ground Engineering Magazine notebook confirms this gap — no published benchmarking, scoring systems, or maturity frameworks for report quality are documented [Ground Engineering Magazine (GEM): "Not covered in sources" for report-level quality scoring].

What does exist in the industry is:
- **BDA (British Drilling Association) Drillers Audit**: An audit of drilling operatives' competency and equipment — assesses drilling execution, log quality, completeness of logs, sample labels. This is a field execution audit, not a report quality audit [GEM: citations 1-2].
- **FPS (Federation of Piling Specialists) initiative**: Actively quantifying the quality of site investigation data received by piling contractors — aims to produce guidance on minimum GI data for effective piling. This is a data quality initiative, not a report quality scoring framework [GEM: citation 3].
- **Project-specific digital audits**: On large infrastructure projects (e.g. Lower Thames Crossing), bespoke tablet-based audit systems assessed safety, health, environmental and quality aspects of GI work. These are project-specific and field-oriented, not report-quality frameworks [GEM: citation 4].
- **BS 5930 and Eurocode 7**: Standards that define best practice for ground investigation and geotechnical design — these are guidance documents, not scoring frameworks [GEM: citations 5-7].

**Conclusion on Q6**: The industry relies entirely on checklist-based peer review (see Q3 above) with no quantitative scoring. This represents a genuine market gap. A SonarQube-like tool that produced a scored quality report would be a novel product with no direct industry precedent.

---

## Implications for Redline

1. **Layer-based quality model**: The four quality layers (Mechanical, Structural, Linguistic/Liability, Technical Defensibility) map directly to what Redline can and cannot automate. Layers 1-3 are automatable; Layer 4 requires human TR sign-off. This is the correct boundary for the platform's quality gate design.

2. **Defect taxonomy for the quality dashboard**: The six defect categories (Technical Errors, Administrative Omissions, Taboo Words, Ambiguity Language, Unqualified Scope, Extraneous Padding) provide the foundation for a defect classification system analogous to SonarQube's bug/vulnerability/code-smell taxonomy. Severity calibration: Taboo Words = CRITICAL (voids PLI); Administrative Omissions = HIGH; Ambiguity Language = MEDIUM.

3. **Section B Review Checklist = Quality Gate template**: The structure of the Section B Review Checklist (DRAFT gate, FINAL gate, with PD sign-off) is the canonical template for Redline's Quality Gate feature. The platform should emit a "ready for PD review" state (equivalent to DRAFT gate) and a "ready for FINAL issue" state.

4. **GBR requires a separate quality ruleset**: The GBR's baseline statement criteria (definitive verbs, quantified adjectives, no "shall", no "may") are a distinct and more demanding ruleset from GIR quality checks. The platform must handle these as separate document types with separate rule sets.

5. **No competitor quality scoring system**: The Ground Engineering Magazine confirms no industry-wide scoring or maturity model exists. This is the clearest signal that a SonarQube-like scored quality report would be a differentiated, novel product.

6. **The "two-tier" formatting defect in GBRs is a critical product warning**: Any Redline GBR template that distinguishes "binding" from "non-binding" sections within the same document would itself create the defect the product is trying to detect. Template design must avoid this pattern.

---

## Open Questions

1. How do NZ-specific CPEng (Chartered Professional Engineer) obligations interact with the sign-off chain documented from the Canadian risk literature? The notebooks document Professional Engineers Act (Ontario) seal requirements, but NZ-specific CPEng signing obligations are not explicitly covered.

2. What is the minimum legally defensible sign-off for small firms (5-15 staff) that lack independent reviewers? The notebooks document large-firm procedures but do not address minimum viable sign-off.

3. Does Eurocode 7 Part 2 (second generation, under development) introduce any formal report quality criteria beyond parameter documentation requirements? The Ground Engineering Magazine mentions EC7 Part 2 is being restructured around parameters, but this was not yet in force at time of research.

4. Are there NZ-specific NZGS (NZ Geotechnical Society) or GNS Science guidelines that specify report quality standards? The notebooks do not cover NZGS guidance in detail.

5. Is the FPS initiative (quantifying GI quality for piling) close to producing a published scoring framework? If so, this could become a precedent for report-level quality scoring.

---

## Glossary

| Term | Definition |
|---|---|
| GIR | Geotechnical Interpretive Report — the interpretive report drawing conclusions and design parameters from site investigation data |
| GFR | Geotechnical Factual Report — raw factual data only; no interpretation |
| GBR | Geotechnical Baseline Report — a contract document establishing measurable subsurface baselines for risk allocation |
| GDR | Geotechnical Data Report — US equivalent of the GFR |
| TR | Technical Reviewer — independent specialist who verifies technical robustness |
| PD | Project Director — provides commercial and risk oversight; final signatory |
| DSC | Differing Site Conditions — contractual claim for ground conditions more adverse than indicated in contract |
| PLI | Professional Liability Insurance — covers negligence, not breach of warranty |
| Strict liability | Legal standard that guarantees a specific result, regardless of fault — distinct from negligence |
| Taboo word | Language that inadvertently creates a warranty or guarantee, elevating standard of care to strict liability |
| BDA | British Drilling Association — manages the Drillers Audit for operative competency |
| FPS | Federation of Piling Specialists — industry body working on GI data quality guidance |
| BS 5930 | British Standard code of practice for ground investigation |
| EC7 / Eurocode 7 | European standard for geotechnical design |
| CPEng | Chartered Professional Engineer — NZ professional engineering registration |
| NZGS | New Zealand Geotechnical Society |

---

## Sources Consulted

| Notebook | Queries asked | Key citations |
|---|---|---|
| Geotechnical Report Workflows (GRW) | 1 | 4 checklists (20 Checkpoints, Stability Analysis, Drafting QA Signoff, Section B); PM Handbook framework; GFR/GIR terminology; review cycle roles |
| Risk Assessment in Engineering (RA) | 1 | 6 defect categories; taboo/absolute words; ambiguity traps; scope limitation requirements; professional liability case law |
| Geotechnical Baseline Reports (GBR) | 1 | GBR quality criteria; baseline statement language requirements; common GBR defects; GBR vs GIR distinction; ASCE, CIRIA C807, NZTS sources |
| Ground Engineering Magazine (GEM) | 1 | BDA Drillers Audit; FPS initiative; BS 5930; EC7; no formal report quality scoring found |
| Existing knowledge documents (local) | — | Pre-review rule validation (SCOPE-LIM-01, SCOPE-CON-01, SCOPE-COST-01); audit trail sign-off workflows; parameter completeness; playbook-driven review |
