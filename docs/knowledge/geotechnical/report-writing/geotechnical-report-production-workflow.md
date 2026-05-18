# Geotechnical Report Production Workflow — EventStorming Domain Map

**Sub-domain**: report-writing
**Last verified**: 2026-05-17
**Confidence**: cross-referenced
**Sources**: Geotechnical Report Workflows (GRW), Risk Assessment in Engineering (RA),
Geotechnical Baseline Reports (GBR notebook), Ground Engineering Magazine (GEM),
Engineering Standards (ES), existing knowledge store documents (audit-trail-sign-off-workflows,
geotechnical-report-quality-dimensions, report-types-and-common-mistakes,
template-management-domain-perspective, practice-vs-business-of-engineering,
before-vs-after-the-fact-standards-checking, ui-terminology-glossary)

## Summary

This document maps the end-to-end geotechnical report production process for EventStorming,
covering workflow phases, data flows, report structure, standards compliance, review cycles,
pain points, quality gates, and domain terminology. It synthesises notebook-grounded
knowledge with practitioner experience. All practitioner-only observations are explicitly
labelled as such.

---

## 1. End-to-End Workflow

### Phase 1 — Project Initiation and Winning Work

**Roles**: Client, PM (Project Manager), PD (Project Director), Legal Team, RAT (Risk
Assessment Task Group, for complex projects).

**Activities**:
- Client engagement and scoping: PM and PD engage with client to understand drivers, "hot
  buttons" (pain points), and scope [GRW].
- **Go/No-Go decision gate**: PM and PD evaluate opportunity risk and profitability. High-risk
  projects require internal review by the RAT group [GRW].
- Proposal/LOE (Letter of Engagement) drafting: defines scope, tasks, budget.
- **Internal approval gate**: PD approves proposal. Non-standard contract terms require Legal
  Team review [GRW].
- **Instruction to proceed gate**: work cannot begin until client provides written acceptance
  or signs the LOE [GRW].
- Six Key Business Rules require a commercially acceptable documented contract with a
  liability cap before any work proceeds [GRW].

### Phase 2 — Desktop Study and Investigation Planning

**Roles**: PM, Geotechnical Engineers, SMEs (Subject Matter Experts).

**Activities**:
- PM creates the PMP (Project Management Plan), sets up collaboration folders, runs kick-off
  meeting [GRW].
- Engineers review archival information, historical aerial imagery, published geology to
  establish a preliminary ground model and identify geotechnical hazards [GRW].
- Preliminary geotechnical parameters developed and shared early with other design disciplines
  (civil, structural) to guide their work before the GIR is available [GRW].
- **Interdisciplinary checkpoint gate**: formal hold point after desktop review to confirm
  alignment across all technical teams before fieldwork begins [GRW].

### Phase 3 — Field Investigation and Factual Reporting

**Roles**: Field engineers, drilling technicians, Engineering Geologist, Laboratory
technicians (external or internal).

**Activities**:
- Intrusive investigations: machine boreholes, test pits, CPT (Cone Penetration Tests),
  soil/rock sampling [GRW].
- Samples dispatched to laboratory for testing (strength, permeability, classification,
  chemical analysis).
- Factual data compiled into GFR (Geotechnical Factual Report): borehole logs, test pit logs,
  lab results, groundwater monitoring, geomorphological mapping [GRW].
- **Hold point gate**: formal checkpoint after GFR submission — team meets with other
  specialists to verify adequate investigations completed before proceeding to interpretive
  phase [GRW].

### Phase 4 — Data Interpretation and Report Drafting

**Roles**: Geotechnical Engineer (Author), PM, PD.

**Activities**:
- Slope stability analysis, settlement analysis, design parameter derivation using GFR
  data [GRW].
- Author opens enterprise template, completes "What is the client seeking?" section as a
  touchstone [GRW].
- Drafts GIR following structural flow: Introduction, Data Review, Methodology,
  Interpretation, Conclusion and Recommendations [GRW].
- **Author self-review gate**: mandatory "20 Checkpoints in 90 Seconds" checklist before
  handing to reviewers [GRW].

### Phase 5 — Quality Assurance and Review

**Roles**: Component Reviewer (peer engineer), TR (Technical Reviewer), PD, BIS/PC
(administrative staff).

**Activities**:
- Component review: peer engineer checks calculation inputs, arithmetic, runs parallel
  simplified calculation [GRW].
- Technical review: TR reads full document — "the right answer has been given to the right
  question" [GRW].
- Oversight review: PD checks client needs met, legislative requirements, risk, reputation,
  mandatory caveats (Applicability) [GRW].
- Formatting check: BIS/PC checks Style Reference Guide compliance [GRW].
- **Section B Review Checklist gate (DRAFT)**: PD must physically sign to authorise release
  of DRAFT report [GRW].
- Client receives draft, provides comments.

### Phase 6 — Client Feedback and Final Issue

**Roles**: Author, TR, PD, PM, Client.

**Activities**:
- Author and TR incorporate client comments.
- TR and PD assess whether client comments affect technical interpretation [GRW].
- **Section B Review Checklist gate (FINAL)**: PD signs final authorisation [GRW].
- PDF publication and filing in "Issued Documents" folder.
- Information Register updated: version, author, date sent, recipients [GRW].

### Phase 7 — Project Close

**Roles**: PM, PD, PC (Project Controller).

**Activities**:
- PM seeks client feedback.
- PM and PD complete "PM Closure Checklist": deliverables accepted, Deltek records updated,
  project files archived [GRW].
- Post-report actions — "possibly the most overlooked part of the report writing process"
  [GRW].

---

## 2. Data Flows

### Formal Workflow (Notebook-Grounded)

The formal workflow mandates a strict sequential dependency:
1. Desktop study produces preliminary parameters [GRW].
2. Field investigation produces physical data.
3. Laboratory testing processes samples.
4. GFR compiles all factual data.
5. Formal hold point verifies investigative adequacy.
6. GIR interprets the factual data.

Preliminary geotechnical parameters are "provided early in the project to guide other work
packages in lieu of the Geotechnical Interpretive Report and will be reviewed and updated
as appropriate based on new information" [GRW].

### Practitioner Reality (Not Covered in Sources)

The formal hold point between GFR and GIR rarely works as cleanly as the documentation
describes. In practice:

- **Lab data trickles in over weeks.** Different tests take different times: moisture content
  and Atterberg limits (plasticity tests) may take 1-2 weeks; consolidation tests take 4-6
  weeks; triaxial strength tests take 3-8 weeks; chemical analysis for contamination can
  take 4-12 weeks. The engineer does not sit idle waiting.
- **Engineers begin drafting the GIR while lab results are still pending.** They populate the
  template, write the site description, the desktop study summary, the methodology, and
  begin preliminary interpretation using field observations and any early lab results. The
  sections that depend on complete lab data (engineering design parameters, settlement
  calculations, foundation recommendations) are left as placeholders or marked "preliminary
  — subject to final lab results."
- **Parallel streams are the norm**, not the exception: while lab results trickle in, the
  engineer is simultaneously drafting report text, updating the ground model with each batch
  of results, and communicating preliminary findings to the structural engineer or architect
  who needs foundation guidance to proceed with their own design.
- **Late-arriving data contradicting early assumptions** is a known risk. If consolidation
  test results show unexpectedly soft clay, the entire foundation design may need to change.
  The engineer must update the ground model, re-run analyses, and potentially revise sections
  already drafted. This is a major source of rework.
- **The GFR and GIR are sometimes combined** into a single Geotechnical Investigation Report
  (GIntR) on smaller projects, bypassing the formal hold point entirely.

---

## 3. Report Structure

### GIR (Geotechnical Interpretive Report) — Typical Sections

| Section | Content type | Depends on lab data? |
| --- | --- | --- |
| Introduction / Scope of work | **Bespoke** — must reflect actual work done, not copied from LOE [GRW] | No |
| Site description | **Formulaic** — location, topography, existing features [GRW] | No |
| Proposed development | **Formulaic** — what is being built (from client brief) | No |
| Desktop study / existing information | **Formulaic** — archival review, published geology | No |
| Ground investigation methodology | **Formulaic** — what was drilled, where, how deep | No |
| Ground and groundwater conditions | **Bespoke** — interpreted ground model, stratigraphy table [GRW] | Yes |
| Seismic shaking hazard | **Boilerplate** — "Standard T+T text that has been PD and TD reviewed" [GRW] | No |
| Liquefaction assessment | **Hybrid** — templated starting text selected by engineer based on judgment [GRW] | Yes |
| Other geotechnical hazards | **Bespoke** — slope stability, lateral spread, settlement [GRW] | Yes |
| Foundation assessment / options | **Bespoke** — engineering judgment, design parameters [GRW] | Yes |
| Foundation pile design parameters | **Bespoke** — derived from lab data and analysis | Yes |
| Residual geotechnical risk | **Bespoke** — "If we don't report the risks, when it goes wrong T+T becomes responsible" [GRW] | Yes |
| Further work | **Bespoke** — engineer judgment on what remains | Partially |
| Applicability | **Boilerplate** — mandatory legal clauses, unalterable [GRW] | No |
| Appendices (figures, logs, lab certs) | **Formulaic** — compiled factual data | Yes |

### GFR (Geotechnical Factual Report) — Typical Sections

All sections are **formulaic** data presentation [GRW]:
- Borehole and test pit logs, field observations
- Laboratory testing results (permeability, dry density, moisture content, etc.)
- Geomorphological mapping
- Groundwater and leachate monitoring data
- Fault mapping (if applicable)

---

## 4. Standards and Compliance

### How Standards Are Selected (Practitioner Knowledge)

Standards selection is not a simple lookup. The engineer considers:

1. **Jurisdiction**: NZ projects use NZ standards (NZS series) and joint AU/NZ standards
   (AS/NZS series). The Building Code (via MBIE Acceptable Solutions) mandates specific
   standards for specific work types.
2. **Client specification**: some clients (e.g., NZTA for roading, Waka Kotahi) mandate
   specific standards in their procurement documents.
3. **Project type**: new design uses current codes; assessment of existing assets may use
   the codes that were current when the structure was built [knowledge store:
   before-vs-after-the-fact-standards-checking].
4. **Local authority requirements**: Canterbury has MBIE earthquake rebuild guidelines and
   liquefaction zoning (LR 0-4) that are regulatory requirements, not optional [knowledge
   store: ui-terminology-glossary].

### Standards That Govern Geotechnical Reports (Notebook-Grounded)

- **NZS 1170.5** — Earthquake actions (seismic design parameters) [GRW, ES]
- **AS/NZS 1170.0** — Structural design actions, general principles [ES]
- **NZS 3101** — Concrete structures [ES]
- **NZS 4431** — Code of practice for earth fill for residential development [ES]
- **NZGS 0200** — Guidelines for geotechnical reporting (factual report standards) [GRW]
- **Eurocode 7 (EC7)** — Geotechnical design (European, sometimes referenced for methods) [GEM]
- **BS 5930** — Code of practice for ground investigations [GEM]
- **CIRIA C807** — Geotechnical Baseline Reports guidance [GBR notebook]
- **NZGS Module Series** — Geotechnical Earthquake Engineering Practice [ES]

### Standards Conflicts (Practitioner Knowledge)

Standards conflicts occur and must be resolved by professional judgment:

- **NZ vs Eurocode**: NZ does not have a comprehensive national geotechnical design code
  equivalent to Eurocode 7. Engineers often reference EC7 methods (e.g., for bearing capacity
  calculations) while applying NZ seismic parameters from NZS 1170.5. The engineer must
  document which standard is used for which purpose.
- **NZ vs ASTM/ASCE**: Lab testing in NZ uses NZ/AU standard test methods (NZS 4402 series),
  not ASTM. Citing ASTM when NZ equivalents exist is an error [knowledge store:
  report-types-and-common-mistakes].
- **Superseded standards**: NZS 4431 has been superseded but is still referenced in some
  council consent conditions. The engineer must decide whether to cite the superseded version
  (because it is contractually required) or the current version [knowledge store:
  nzs-4431-supersession].

### Consequences of Wrong Standards

"Failure to conform to standards generally accepted in the profession is strong evidence of
negligence" [RA]. Using out-of-date design tables has led to tort liability in documented
case law [RA].

---

## 5. Review and Revision Cycles

### Typical Review Cycle (Notebook-Grounded)

Five-stage cycle [GRW, knowledge store: audit-trail-sign-off-workflows]:
1. Author self-review (20 Checkpoints in 90 Seconds)
2. TR technical review
3. PD DRAFT authorisation (Section B Review Checklist)
4. Author + TR incorporate client comments
5. PD FINAL authorisation (Section B Review Checklist)

For high-risk/high-value projects (>$10M): escalates through Discipline Director, Sector
Director, Managing Director, Board [GRW].

### What Triggers Revision (Practitioner Knowledge)

| Trigger | Who decides? | Scope boundary |
| --- | --- | --- |
| Internal TR feedback | TR | Always in scope — that is the TR's job |
| PD oversight comments | PD | Always in scope — PD has final authority |
| Client editorial feedback (typos, clarity) | Author | Editorial fix — no scope question |
| Client requests additional analysis or sections | PM + PD | Scope creep — PM assesses against LOE, PD decides whether to absorb or request variation |
| Lab anomalies (unexpected results) | Author + TR | In scope if within original investigation; variation if re-testing required |
| Regulatory change mid-project | PD + Legal | Variation — new standard may invalidate completed work |
| Peer reviewer / consent authority comments | PM + PD | In scope if within LOE; variation if scope expands |
| Third-party reviewer (council reviewer, BCA) | PM + PD | Often triggers additional work — PM must assess |

### "Scope Creep" vs "Editorial Fix" (Practitioner Knowledge)

The PM is the gatekeeper. The test is: "Does this request require engineering analysis that
was not included in the original LOE?" If yes, it is a variation. If it is wording, layout,
or clarification of existing content, it is an editorial fix. In practice, the boundary is
fuzzy — a client asking "can you add a section on liquefaction" when liquefaction was not in
scope is scope creep. A client asking "can you explain this section more clearly" is
editorial. The PM should never absorb scope creep silently — it must be documented as a
variation even if the firm chooses not to charge for it.

### Number of Review Cycles (Practitioner Knowledge)

Typical: 2-3 internal review cycles before DRAFT issue to client. 1-2 cycles of client
comments before FINAL issue. Complex or contentious projects can go through 5+ cycles.

---

## 6. Pain Points and Bottlenecks

### Writing Pain Points (Notebook-Grounded)

- Engineers describe report writing as "Tedious", "Terrified", "Exhausting", "Formatting
  nightmares" [GRW].
- **Unclear client briefs**: biggest source of rework — engineers write without understanding
  client needs. One 30-page report was rejected entirely because layout did not support a
  consent application [GRW].
- **"Going in circles"**: engineers get stuck on a section instead of leaving a note for
  their reviewer [GRW].
- **Scope copying**: engineers copy/paste scope from LOE instead of writing what was actually
  done [GRW].
- **Time underestimation**: engineers consistently underestimate writing and formatting
  time [GRW].

### Reviewer Pain Points (Notebook-Grounded)

- **Reviewers used as "cleanup crews"**: junior authors abdicate quality responsibility,
  expecting reviewers to fix basic errors. "Reviewers are safety nets, not cleanup crews"
  [GRW].
- **Recurring mechanical defects**: inconsistent tenses, paragraph-length sentences, reports
  returned with "commas everywhere" in red pen [GRW].
- **Wordiness**: "many of our reports are too wordy and complex" and "include information
  which is not relevant to the reader" [GRW].

### Knowledge Transfer Pain Points (Notebook-Grounded)

- **"Frankenstein" reports**: inappropriate reuse of old reports — engineers assume similar
  circumstances mean similar outcomes [GRW].
- **Template recycling risk**: using outdated templates exposes the firm to legal risk because
  templates are regularly updated for emerging risks [GRW].
- **Lost lessons**: post-report actions (feedback, lessons captured) are "possibly the most
  overlooked part of the report writing process" [GRW].

### Bottlenecks (Practitioner Knowledge)

- **Lab turnaround**: engineers waiting for lab results while project deadlines do not move.
  The lab is often the critical path.
- **Reviewer availability**: TRs and PDs are senior people with many projects — getting their
  time for a thorough review is a constant bottleneck.
- **CAD/drafting queue**: technical drawings go through a separate drafting team with a
  minimum 3-day lead time [GRW]. Drawings are often the last item completed and delay
  report issue.
- **Client-side delays**: clients slow to provide site access, brief clarification, or
  consent documentation. The project clock keeps running.
- **Inter-discipline coordination**: on multi-disciplinary projects, the geotechnical
  engineer cannot finalise foundation recommendations until the structural engineer confirms
  loads, and the structural engineer cannot confirm loads until the architect finalises the
  building layout. Circular dependency.
- **Version control**: engineers working on the same Word document on a shared drive —
  "who has the latest version?" is a perennial problem.

---

## 7. Quality Gates

### Formal Checklists (Notebook-Grounded)

Four named checklists in enterprise practice [knowledge store:
geotechnical-report-quality-dimensions]:

1. **"20 Checkpoints in 90 Seconds"**: 20 yes/no questions for Author self-review. Covers
   presentation, logical flow, tone, spelling/grammar, fresh-eyes proofreading [GRW].
2. **Stability Analysis Review Checklist**: 10 sub-sections covering slope geometry, material
   parameters, groundwater, seismic loading, critical slip surface validation [GRW].
3. **Drafting QA Signoff Form**: for all technical drawings. Minimum 3-day lead time. Covers
   CAD standards, coordinate systems, naming conventions [GRW].
4. **Section B Review Checklist** (ultimate gate): PD must physically sign. Applied twice —
   DRAFT gate and FINAL gate [GRW].

### Sign-Off Authority (Notebook-Grounded)

- **Author (Prepared by)**: owns initial quality.
- **TR (Reviewed by)**: verifies technical robustness. Must be independent of the author.
- **PD (Authorised by)**: final authority. Must be a different person from the PM [GRW].
- For high-risk projects: escalation through Discipline Director, Sector Director, MD,
  Board [GRW].

### What Happens When Reviewer Disagrees (Practitioner Knowledge)

If the TR disagrees with the Author's analysis:
1. TR raises the issue with the Author directly — most disagreements are resolved through
   technical discussion.
2. If unresolved, PD arbitrates. The PD may commission an independent third-party peer review.
3. The PD has ultimate authority — if the PD is uncomfortable signing, the report does not
   issue.
4. In rare cases, the disagreement is escalated to the Discipline Director or an external
   peer reviewer.

The key principle: the person who signs bears the liability. No one should be pressured to
sign a report they are not comfortable with.

---

## 8. Terminology — Common Misunderstandings

### Terms That Mean Different Things in Different Contexts

| Term | Field context | Lab context | Report context |
| --- | --- | --- | --- |
| Sample | A physical specimen retrieved from the ground (disturbed or undisturbed) | The specimen received for testing (may be a sub-sample of the field sample) | A data point — "the sample shows..." means the test result |
| Anomaly | An unexpected observation during fieldwork (e.g., unexpected fill, artesian water) | An unexpected test result (e.g., strength much lower/higher than expected) | A data point requiring engineering judgment — may indicate a real ground condition or a testing error |
| Log | A borehole log — the written record of what was encountered during drilling | A laboratory log — record of tests performed | A document — the bore log as a report appendix |
| Ground model | A conceptual understanding of what is in the ground (developed progressively) | Not used in lab context | The definitive interpreted subsurface profile presented in the report |
| Parameter | An assumed value used for preliminary design (during field phase) | A measured value from a specific test (e.g., shear strength = 25 kPa) | A design value — the engineer's selected value after considering all data, which may differ from any single test result |

### Terms Commonly Misunderstood by Non-Geotechnical People

| Term | What people think it means | What it actually means |
| --- | --- | --- |
| Factual Report (GFR) | A report containing facts and conclusions | A report containing ONLY measured data — NO engineering interpretation |
| Interpretive Report (GIR) | An opinion piece | A report where an engineer applies professional judgment to measured data to derive design parameters — not opinion, but engineering analysis |
| Standard of care | A quality standard to aim for | A LEGAL benchmark — the minimum level of skill and diligence expected of a competent practitioner. Falling below it = negligence |
| Applicability (section) | A disclaimer the lawyer made them add | A legally critical section that defines the boundaries of the report's validity — what it covers, what it does not, and who may rely on it |
| Residual risk | Remaining risk after mitigation | Risks that the engineer has CHOSEN not to mitigate (or cannot mitigate) and is explicitly disclosing to the client so the client bears the risk |
| Producer Statement (PS1/PS2) | A certificate that the design is correct | A statement that a named CPEng has reviewed the design and believes it complies with the Building Code. It is NOT a guarantee |
| Scope creep | Extra work | Work outside the original LOE that was not priced. The firm must choose to absorb the cost, request a variation, or decline |
| Technical Reviewer (TR) | Someone who checks spelling and formatting | An independent engineer who checks whether "the right answer has been given to the right question" — a substantive technical check |
| "Adequate" | Good enough | A DANGEROUS word in reports — courts interpret it to the engineer's detriment. What is "adequate" by whose measure? |

---

## Open Questions

1. How do NZ-specific CPEng signing obligations interact with the sign-off chain? The
   notebooks document Canadian seal requirements but NZ CPEng-specific signing obligations
   are not explicitly covered.
2. What is the minimum legally defensible sign-off process for small firms (5-15 staff) that
   lack independent reviewers?
3. How do PI insurers view compressed review processes in small firms?
4. What proportion of NZ/AU geotechnical report rework is caused by lab data arriving late
   vs other causes?
5. How do different NZ territorial authorities vary in their standards requirements for
   geotechnical reports?

## Further Reading

- I have not verified these sources, but they may contain relevant answers:
  - NZGS Module 2 — Guidelines for Geotechnical Reporting
  - Engineering NZ Practice Note 19 (Engineers and the Law)
  - ACENZ Conditions of Engagement
  - IPENZ guidance on Forensic Engineering
  - NZSEE/MBIE "The Seismic Assessment of Existing Buildings" (the "Red Book")
