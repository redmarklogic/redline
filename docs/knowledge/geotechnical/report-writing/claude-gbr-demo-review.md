# Claude-Generated GBR Review — Standards Errors, Structural Gaps, Domain Accuracy

**Sub-domain**: report-writing
**Last verified**: 2026-05-14
**Confidence**: cross-referenced (notebook-grounded findings combined with practitioner judgment)
**Sources**: Engineering Standards notebook, Geotechnical Report Workflows notebook, GBR notebook, Risk Assessment in Engineering notebook, knowledge store documents (NZS 4431 supersession, AI-GBR liability assessment, pre-review rule validation)

## Summary

A Claude-generated geotechnical report for a NZ residential development was reviewed for
standards citation errors, structural gaps, and domain accuracy issues. The report
demonstrates competent assembly of plausible-sounding geotechnical language but contains
multiple errors that would not survive senior review at any major NZ consultancy.

---

## Part 1 — Standards Citation Errors

### Error 1: NZS 4431 completely absent

- **The error**: The report specifies earthworks and compaction for a residential development
  but does not cite NZS 4431:2022 (Code of Practice for Earth Fill for Residential Development)
  at all — not the current edition, not the 1989 edition, nothing. This is the governing
  compliance framework for residential earthworks in New Zealand.
- **Redline rule**: CITE-EXIST-01 (Citation existence check) — missing mandatory standard
- **Severity**: HIGH
- **Flag text**: "NZS 4431 is not cited. This standard governs earthworks compliance for
  residential development in NZ, including fill quality control, construction procedures,
  inspection, and the Statement of Suitability. Its omission means the report's compaction
  recommendations have no compliance framework."
- **Grounding**: Notebook-grounded. The Engineering Standards notebook confirms NZS 4431:2022
  is the current edition and that CCC CSS updated to reference it in October 2025. The
  knowledge store document `nzs-4431-supersession.md` records the supersession history.

### Error 2: NZS 4402:1986 test numbering convention incorrect

- **The error**: Claude cites "NZS 4402:1986 Test 4.1.3" for Modified Proctor compaction.
  The NZS 4402 numbering convention uses a decimal-dot format (e.g., NZS 4402.4.1.1 for
  standard compaction, NZS 4402.4.1.3 for vibrating hammer). "Test 4.1.3" is not a valid
  reference — it conflates the clause numbering with a test numbering convention that does
  not exist in the standard.
- **Redline rule**: CITE-EXIST-01 (Citation existence check — clause-level citation pattern)
- **Severity**: MEDIUM
- **Flag text**: "NZS 4402 clause reference 'Test 4.1.3' does not match the standard's
  numbering convention. Verify the correct clause reference for the intended compaction test
  method (NZS 4402.4.1.1 for standard compaction, NZS 4402.4.1.3 for vibrating hammer)."
- **Grounding**: Notebook-grounded. The Engineering Standards notebook confirms the clause
  numbering differs from what Claude cited.

### Error 3: ASTM D1586 cited for SPT instead of a NZ/AU standard

- **The error**: Claude cites ASTM D1586 for Standard Penetration Test (SPT) procedures. While
  ASTM D1586 is technically accurate as a method description, NZ practice references SPT
  through NZS 4402 (which contains the NZ test method) or NZGS Field Description of Soil and
  Rock guidelines. Citing only an American standard for a NZ residential project is unusual
  and would draw comment from a reviewer.
- **Redline rule**: CITE-EXIST-01 (Citation existence check — jurisdiction mismatch)
- **Severity**: LOW-MEDIUM
- **Flag text**: "ASTM D1586 is an American standard. NZ practice typically references SPT
  through NZS 4402 or NZGS guidelines. Verify whether the ASTM reference is intentional or
  whether the NZ equivalent should be cited."
- **Grounding**: Practitioner judgment. The notebooks do not explicitly address which standard
  NZ engineers cite for SPT. However, in 25 years of NZ practice, I have rarely seen a
  residential geotechnical report cite only an ASTM standard for SPT without also referencing
  the NZ equivalent. It is not wrong, but it is unusual and signals that the author may not
  be familiar with NZ practice conventions.

### Error 4: NZS 4407:2015 cited for SPT

- **The error**: Claude references NZS 4407:2015 (Methods of sampling and testing road
  aggregates) in the context of SPT testing. NZS 4407 is a roading materials standard —
  it covers aggregate sampling and testing for pavement construction. It has nothing to do
  with SPT or geotechnical soil testing. This is a hallucination.
- **Redline rule**: CITE-EXIST-01 (Citation existence check — standard exists but is
  irrelevant to the stated purpose)
- **Severity**: HIGH
- **Flag text**: "NZS 4407:2015 is cited for SPT testing but this standard covers road
  aggregate sampling and testing, not geotechnical soil investigation. This appears to be
  an incorrect standard reference."
- **Grounding**: Practitioner judgment. I know NZS 4407 well — it is a roading standard.
  It does not contain SPT procedures. I cannot verify whether the notebooks explicitly
  address NZS 4407, but the error is clear from domain knowledge.

### Error 5: NZS 4402:1986 used as compliance framework rather than test methodology

- **The error**: Claude treats NZS 4402:1986 as the governing framework for compaction
  compliance. NZS 4402 is a test methodology standard — it describes HOW to perform tests
  (Atterberg limits, compaction, CBR, etc.). The compliance framework — the standard that
  tells you WHAT compaction level is required and how to certify it — is NZS 4431. This is
  a fundamental conceptual error that conflates "how to measure" with "what to achieve."
- **Redline rule**: CITE-EXIST-01 / SCOPE-CON-01 (scope-conclusion consistency — compliance
  framework mismatch)
- **Severity**: HIGH
- **Flag text**: "NZS 4402 is a test methodology standard. The compliance framework for
  residential earthworks is NZS 4431:2022, which governs fill quality, compaction
  requirements, and certification (Statement of Suitability). Verify that the correct
  compliance standard is referenced."
- **Grounding**: Notebook-grounded. The Engineering Standards notebook explicitly states
  that NZS 4402 is the testing methodology and NZS 4431 is the compliance framework.

### Error 6: Transit NZ TNZ B/02:2003 cited for DCP soundings

- **The error**: Claude cites Transit NZ TNZ B/02:2003 for Dynamic Cone Penetrometer (DCP)
  soundings. Transit NZ was reorganised into NZ Transport Agency (NZTA) in 2008. While the
  technical content may still be applicable, citing a Transit NZ specification for a residential
  development report is unusual — DCP in residential geotechnical practice is typically
  referenced through NZGS or industry guidance, not roading specifications. Additionally, the
  currency of a 2003 Transit NZ specification should be verified.
- **Redline rule**: CITE-EXIST-01 (Citation existence check — potentially superseded
  organisational reference)
- **Severity**: LOW
- **Flag text**: "Transit NZ was reorganised into NZTA in 2008. Verify whether TNZ B/02:2003
  has been superseded by an NZTA specification or whether an alternative NZ reference for DCP
  testing is more appropriate."
- **Grounding**: Practitioner judgment. I know Transit NZ became NZTA. I cannot verify from
  the notebooks whether TNZ B/02:2003 has been formally superseded, but citing a Transit NZ
  document in 2026 will draw reviewer comment.

---

## Part 2 — Structural and Domain Accuracy Issues

### Issue 1: No GDR separation — factual and interpretive data mixed

- **The issue**: A proper GBR requires a separate factual Geotechnical Data Report (GDR) to
  be referenced. The GBR establishes baselines and interpretations; the GDR contains the raw
  factual data (borehole logs, test results, field observations). Claude's report mixes
  factual data and interpretation in a single document with no reference to a GDR.
- **Why it matters**: In a Differing Site Conditions (DSC) dispute, the contractual hierarchy
  requires the GBR to take precedence over the GDR. If there is no GDR separation, the
  contractor's lawyer will argue that factual data and interpretation are inseparable, making
  it impossible to establish which "baseline" applies. This is the foundational structural
  requirement of a GBR.
- **Would this survive senior review?**: No. Any senior engineer who has worked on a
  contested project would immediately flag the absence of GDR separation. This is a
  structural deficiency, not a drafting error.
- **Confidence**: HIGH. Notebook-grounded — the GBR notebook explicitly states that a GBR
  must reference a GDR and establish contractual hierarchy.

### Issue 2: Missing mandatory third-party reliance clause — or generic wording

- **The issue**: The report contains a third-party reliance clause but it is described as
  "generic." The Geotechnical Report Workflows notebook specifies exact mandatory wording:
  "This report has been prepared for the exclusive use of our client [Name]... it may not
  be relied upon in other contexts or for any other purpose, or by any person other than
  our client, without our prior written agreement."
- **Why it matters**: A generic reliance clause may not provide adequate legal protection.
  The CEAS 1979 case study and Indemnity Matters Issue 88 (April 2026) both demonstrate
  that inadequate scope limitation clauses expose the signing engineer and the firm to
  third-party claims. NZ PI (Professional Indemnity) policies require that reasonable steps
  were taken to limit reliance — generic wording may not satisfy this requirement.
- **Would this survive senior review?**: Depends on the firm. At a Tier 1 NZ firm (T+T,
  Beca, WSP, Aurecon), the reviewer would replace the generic clause with the firm's
  standard wording. At a smaller firm without a standard template, it might slip through —
  and that is exactly the risk Redline is designed to catch.
- **Confidence**: HIGH. Notebook-grounded — the GRW notebook labels this as mandatory and
  provides exact wording. The knowledge store document `pre-review-rule-validation-scope-and-language-checks.md`
  validates SCOPE-CLAUSE-05 as HIGH severity.

### Issue 3: No temporal validity caveat

- **The issue**: The report contains no statement limiting the temporal validity of its
  recommendations. NZ practice typically includes a caveat that recommendations are valid
  for a defined period (commonly 12-18 months) and should be reviewed if construction has
  not commenced within that period.
- **Why it matters**: Ground conditions can change — particularly in seismically active
  regions. A report without a temporal caveat could be relied upon years after the
  investigation, by which time the ground conditions (water table, fill placement,
  adjacent construction, seismic events) may have materially changed. If the report is
  used to support a building consent application three years after the investigation and
  the ground conditions have changed, the engineer has no contractual protection.
- **Would this survive senior review?**: At a well-run firm, no — the reviewer would add
  the temporal caveat. But the notebook sources note this is "not explicitly covered" in
  the training materials, which suggests it is a practice convention rather than a
  standards-mandated requirement. This makes it exactly the kind of gap that junior
  engineers and AI miss.
- **Confidence**: MEDIUM. The feature backlog includes SCOPE-CLAUSE-NEW (temporal validity
  of recommendations, MEDIUM severity) as a validated rule, but the notebook sources do not
  explicitly mandate it. This is practitioner judgment based on NZ industry convention.

### Issue 4: Potential warranty language — "suitable for conventional shallow foundations"

- **The issue**: The phrase "The site is considered suitable for conventional shallow
  foundations" may function as a warranty rather than a qualified professional opinion. The
  word "suitable" without conditioning language ("subject to", "provided that", "based on
  the investigation data") can be interpreted as an express warranty of fitness.
- **Why it matters**: NZ PI policies typically contain warranty exclusions — they do not
  cover liability arising from contractual guarantees of outcome. If a court interprets
  "suitable for" as a warranty, the PI insurer may decline the claim. The CEAS Indemnity
  Matters publications have repeatedly warned about this distinction. The knowledge store
  document on AI-GBR liability explicitly identifies AI-generated confident language as the
  highest-risk failure mode.
- **Would this survive senior review?**: Maybe — and that is the problem. "Suitable for"
  is extremely common in NZ geotechnical reports. Many senior engineers use it habitually.
  But it is exactly the kind of language that a plaintiff's lawyer will seize on, and
  exactly the kind of language that CEAS has been warning engineers about. A cautious
  reviewer would change it to "the investigation data indicates that conventional shallow
  foundations are likely to be feasible, subject to the recommendations in this report."
- **Confidence**: MEDIUM-HIGH. Notebook-grounded via AI-GBR liability assessment and
  RISK-LANG-01 rule validation. The specific phrase "suitable for" is not listed as a
  HIGH-tier guarantee word but falls in the CONTEXT-CHECK tier — it requires a conditioning
  clause within approximately 30 words.

### Issue 5: Missing inferred conditions caveat

- **The issue**: No explicit statement that "recommendations and opinions in this report
  are based on data from discrete investigation locations. The nature and continuity of
  subsoil away from these locations are inferred but it must be appreciated that actual
  conditions could vary from the assumed model."
- **Why it matters**: This is the single most important protective clause in a NZ
  geotechnical report. It establishes that the engineer has not investigated every square
  metre of the site and that actual conditions may differ from what the report describes.
  Without it, a court may infer that the engineer intended the report to be comprehensive.
  The RA notebook confirms: courts will infer a comprehensive investigation if scope is
  described in vague terms.
- **Would this survive senior review?**: No. This is mandatory at every major NZ firm.
  SCOPE-CLAUSE-01 is rated HIGH severity.
- **Confidence**: HIGH. Notebook-grounded — the GRW notebook template labels this as
  mandatory. The knowledge store document on pre-review rule validation confirms
  SCOPE-LIM-01 and SCOPE-CLAUSE-01 as HIGH severity.

### Issue 6: Bearing capacity values stated without method or safety factor basis

- **The issue**: The report states bearing capacity as "SLS 100-150 kPa, ULS 300-450 kPa"
  with a "Factor of Safety 3.0 against general shear failure." However, it does not state
  which bearing capacity method was used (Terzaghi, Meyerhof, Hansen, Vesic), what soil
  parameters were adopted, or how the SLS and ULS values were derived from the factored
  soil parameters.
- **Why it matters**: A reviewer needs to verify the calculation, not just accept the
  answer. Stating a bearing capacity without showing the method, input parameters, and
  calculation basis is not a GBR baseline — it is an unsupported assertion. Additionally,
  the relationship between SLS (100-150 kPa) and ULS (300-450 kPa) implies a factor of
  approximately 3.0, which is consistent with the stated FoS — but the derivation should
  be traceable.
- **Would this survive senior review?**: The values themselves are plausible for a stiff
  clay or medium-dense gravel in NZ — they are not obviously wrong. But a senior reviewer
  would ask for the calculation basis and would not sign off without seeing the derivation.
  In a consultancy report (as opposed to a GBR), the derivation would typically be in an
  appendix.
- **Confidence**: HIGH. This is standard practice — no notebook needed. You do not state
  bearing capacity values without showing your working.

### Issue 7: Seismic parameters — Z = 0.13 and Site Class C stated without location

- **The issue**: The report states Z = 0.13 and Seismic Site Class C but the user's prompt
  was generic ("a site in New Zealand"). Z = 0.13 corresponds to a specific location
  (approximately Christchurch under the pre-2022 NSHM hazard model). Without stating
  the specific site location, these parameters cannot be verified.
- **Why it matters**: The 2022 National Seismic Hazard Model (NSHM) update significantly
  revised Z values for many NZ locations. The GRW notebook warns engineers to "be aware
  of any possible modifications to the NZ code (especially with reference to the 2022
  NSHM update)" when assessing seismic parameters. An AI generating a Z value without a
  stated location is producing an unverifiable parameter.
- **Would this survive senior review?**: No. A reviewer would immediately ask "what site
  is this for?" and check the Z value against NZS 1170.5 Table 3.3 (or the updated NSHM).
- **Confidence**: HIGH. Notebook-grounded (NSHM warning from GRW notebook) combined with
  practitioner judgment.

### Issue 8: Liquefaction assessment — "Low risk" without methodology

- **The issue**: The report states "Liquefaction risk: Low" without describing the
  assessment methodology (e.g., Boulanger & Idriss 2014, Robertson 2009, NZGS/MBIE
  Module 3), the triggering earthquake scenario (return period, PGA), or the specific
  soil layers assessed. "Low risk" is a conclusion without a traceable basis.
- **Why it matters**: Post-Canterbury, liquefaction assessment in NZ is heavily regulated.
  MBIE guidance documents (particularly for TC2/TC3 land categories in Canterbury) specify
  detailed assessment procedures. Even for residential sites outside Canterbury, a credible
  liquefaction assessment must state the method, the design earthquake, the soil profile
  assessed, and the factor of safety against liquefaction for each susceptible layer. "Low
  risk" without this basis is not a professional opinion — it is a guess.
- **Would this survive senior review?**: No. Post-Canterbury, no NZ reviewer would accept
  an unsupported liquefaction conclusion. This is a domain-critical error.
- **Confidence**: HIGH. Practitioner judgment — this is fundamental post-Canterbury NZ
  practice. I cannot verify the specific MBIE module references from the notebooks, but
  the requirement for a traceable liquefaction assessment methodology is beyond question.

### Issue 9: Settlement criteria stated without context

- **The issue**: The report states "Settlement < 25 mm total, < 15 mm differential" but
  does not state what these limits are based on (e.g., NZS 3604 for timber-framed
  buildings, AS/NZS 1170.0 serviceability requirements, or project-specific criteria),
  nor does it describe the settlement calculation method (e.g., Schmertmann, elastic
  theory, consolidation analysis).
- **Why it matters**: Settlement limits depend on the structure type, the foundation
  system, and the performance criteria. 25 mm total / 15 mm differential are reasonable
  for a standard NZ residential building, but they need to be tied to a standard or
  project requirement, not stated as free-floating numbers.
- **Would this survive senior review?**: The numbers are plausible and would not be
  challenged on magnitude — but the missing basis would be flagged. A senior reviewer
  would ask "where do these limits come from?"
- **Confidence**: MEDIUM-HIGH. Practitioner judgment.

### Issue 10: GBR structure does not follow ASCE/CIRIA conventions

- **The issue**: The GBR notebook specifies required sections per ASCE/CIRIA: Introduction,
  Project Description, Man-Made Features, Sources of Information, Geologic Setting,
  Previous Construction Experience, Ground Characterization, Construction Considerations,
  Methods of Measurement. I cannot confirm from the information provided whether Claude's
  report follows this structure, but the absence of a GDR reference (Issue 1) and the
  mixing of factual and interpretive content suggest it does not.
- **Why it matters**: A GBR is a contractual document with a specific structural convention.
  Deviating from the ASCE/CIRIA structure does not invalidate the report, but it makes it
  harder for a reviewer to confirm completeness and harder for a contractor to navigate
  during a DSC dispute.
- **Would this survive senior review?**: Depends on the firm's GBR template. Most NZ firms
  have not adopted the full ASCE/CIRIA GBR structure for residential work — GBRs are more
  common on infrastructure and tunnelling projects. For a residential development, the
  document is more likely structured as a Geotechnical Investigation Report (GIR) than a
  true GBR.
- **Confidence**: MEDIUM. Notebook-grounded for the structural requirements; practitioner
  judgment for the observation that GBRs are unusual for NZ residential projects.

---

## What Claude Gets Right

In the interest of a fair assessment:

1. **Plausible parameter values**: The bearing capacity range (SLS 100-150 kPa, ULS 300-450
   kPa), settlement limits (25 mm / 15 mm), and FoS of 3.0 are all within the range a
   competent engineer might specify for a stiff clay or medium-dense gravel site. The
   numbers are not obviously wrong.

2. **Correct identification of relevant NZ standards**: NZS 3604, NZS 1170.5, NZS 4402,
   and MBIE 2017 guidance are all genuinely relevant to a NZ residential geotechnical
   report. Claude identified the right standards universe — it just missed the most important
   one (NZS 4431) and got the citation details wrong on others.

3. **NZGS Field Description reference**: Citing NZGS Field Description of Soil and Rock
   (2005, 2nd Edition) is correct and demonstrates awareness of NZ-specific guidance
   documents rather than relying solely on international standards.

4. **Site Class and Z value are internally consistent**: Z = 0.13 and Site Class C are a
   plausible combination for a NZ location, even though the location is not stated. The
   AI has not generated an internally contradictory seismic parameter set.

5. **Report structure includes key sections**: The report apparently includes investigation
   results, foundation recommendations, seismic assessment, and a reliance clause — the
   broad structure of a NZ geotechnical report is present even if the details are flawed.

6. **Third-party reliance clause is present**: While generic, the fact that Claude included
   one at all shows awareness that it is expected. Many AI outputs would omit it entirely.

---

## Summary Assessment

**Overall verdict**: This report would not pass senior review at any major NZ consultancy.
It demonstrates Claude's ability to assemble plausible geotechnical language and
approximately correct parameter values, but it contains fundamental errors in standards
citation (NZS 4431 omission, NZS 4407 hallucination), structural convention (no GDR
separation), and professional practice (unsupported conclusions, missing mandatory clauses,
potential warranty language).

**Demo asset value**: HIGH. This is exactly the kind of output that demonstrates Redline's
value proposition. Every error I have identified above maps directly to an existing or
planned Redline Pre-Review rule. The NZS 4431 omission alone is a compelling demonstration
— it is the single most frequently cited NZ standard in residential earthworks and Claude
omitted it entirely while citing the test methodology standard (NZS 4402) as if it were the
compliance framework.

**Key message for the demo**: An AI can produce a report that LOOKS competent to a non-expert
but contains errors that a senior reviewer would catch in minutes. The question is not whether
senior reviewers exist — it is whether they are available, consistent, and scalable. Redline
automates the checks that senior reviewers perform, ensuring every report gets the same
level of scrutiny regardless of workload pressure.

---

## Open Questions

1. The NZS 4407:2015 citation for SPT needs verification — is this a pure hallucination
   (the standard exists but covers road aggregates) or has Claude confused it with another
   standard? I am confident it is a hallucination based on my knowledge of NZS 4407, but
   the notebooks do not explicitly address this.

2. The Transit NZ TNZ B/02:2003 reference for DCP needs verification against the NZTA
   specifications register to confirm whether it has been formally superseded.

3. The 2022 NSHM update's impact on Z values for specific NZ locations should be researched
   and documented — this is a gap in the current knowledge store.

4. The specific MBIE guidance documents for liquefaction assessment (Module 3, TC category
   requirements) should be ingested into the Engineering Standards notebook to enable
   notebook-grounded verification of liquefaction assessment methodology claims.
