# Pre-Review Rule Validation — Scope, Clause, Citation, and Language Checks

**Sub-domain**: report-writing
**Last verified**: 2026-05-10
**Confidence**: cross-referenced
**Sources**: Geotechnical Report Workflows and Standard Procedures (GRW), Risk Assessment in
Engineering (RA), Geotechnical Baseline Reports (GBR), Engineering Standards (ES),
CEAS Indemnity Matters Issue 88 — April 2026 (CEAS-88)

---

## Summary

This document records Graeme's domain validation of six proposed Pre-Review quality-check rule
families for the Redline product. The rules were derived from signals in CEAS Indemnity Matters
Issue 88 (April 2026) and a 1979 CEAS historical case study. Each rule verdict addresses
soundness, false-positive risk, severity calibration, and domain nuances affecting implementation.

---

## Rule Verdicts

### SCOPE-LIM-01 — Scope-Limitation Presence Check

**Domain verdict**: VALID. HIGH severity is appropriate.

**Notebook grounding**:
- The GRW notebook template labels the Applicability section as **Mandatory** and requires two
  sub-clauses: (a) third-party reliance restriction, and (b) inferred conditions caveat [GRW:
  citations 4-9]. The template wording reads: *"Mandatory: Recommendations and opinions in this
  report are based on data from discrete investigation locations. The nature and continuity of
  subsoil away from these locations are inferred but it must be appreciated that actual conditions
  could vary from the assumed model."* [GRW: citation 7].
- The RA notebook confirms: courts will infer a comprehensive investigation if scope is described
  in vague terms; explicit scope qualification is the only protection [RA: citation 18].

**Implementation nuance — location of the clause**:
The Applicability section in NZ/AU reports is typically located **at the end of the report body**
(before signatures), not inside the Conclusions section. Checking only the Conclusions section
will produce false negatives for every correctly structured NZ report. The rule should search
the full document for an Applicability/Scope Limitation section, or at minimum should check a
50-word window before the signature block as well as the Conclusions section.

**Desk-study exception**: There is no legitimate case for omitting a scope limitation from any
conclusions section, including a narrow desk study. If anything, desk studies require MORE
explicit qualification because they rely entirely on secondary data.

**Failure mode in practice**: Engineers typically fail through omission of the Applicability
section entirely (rushed reports), not through wording that fails to cover the right risks.
The CEAS 1979 case study is a direct example of omission.

**Recommended wording patterns** (notebook-grounded):
1. *"Recommendations and opinions in this report are based on data from discrete investigation
   locations. The nature and continuity of subsoil away from these locations are inferred but it
   must be appreciated that actual conditions could vary from the assumed model."* [GRW: T+T
   template, mandatory]
2. *"The nature and continuity of geotechnical data away from test locations is inferred and
   therefore there is always a residual risk that actual conditions could vary from the assumed
   model."* [GRW: citation 9]
3. *"Recommendations and opinions in the report are based on data from limited investigations."*
   [GRW: citation 8]
4. *"The interpretations and recommendations contained in this report pertain to a specific
   project as described in the report and are not applicable to any other project or site."* [RA:
   citation 11]

---

### SCOPE-CON-01 — Scope-Conclusion Consistency Check (LLM-assisted)

**Domain verdict**: VALID as a check, but HIGH severity is **wrong**. Downgrade to MEDIUM.
Frame as "flag for human review" only.

**Notebook grounding**:
- The GBR notebook explicitly states that conclusions legitimately extend beyond the investigation
  data using professional judgment, and this is an **expected and necessary practice**: *"In most
  instances the available exploration database is not sufficiently complete to fully characterize
  the anticipated subsurface conditions. In this instance, the GBR must go beyond the available
  data to provide a reasonable baseline of anticipated conditions."* [GBR: citation 1]
- The GBR notebook further states: *"if factual data is not available, or is considered to be
  misleading and not representative of field conditions, baselines may be based on other
  information (e.g., previous tunneling experience in similar geology) and engineering judgment,
  provided the reasoning is clearly explained."* [GBR: citation 5]
- The risk is NOT extension beyond the data — the risk is extension without explanation.

**Signal distinguishing legitimate inference from scope overreach**:
- Legitimate: The conclusion states conditions for an area beyond the investigation, and includes
  a reason grounded in regional geology, comparable nearby data, or professional experience.
- Scope overreach: The conclusion makes specific quantitative claims about uninvestigated areas
  with no stated basis.
- An LLM cannot reliably distinguish these two patterns without engineering domain knowledge. This
  is not a rule the product can flag definitively.

**Recommended severity**: MEDIUM, with mandatory human-review framing. The flag should read:
"Conclusion may extend beyond stated investigation scope — confirm professional judgment basis is
stated."

**False-positive risk management**: The LLM should be instructed NOT to flag as scope overreach
when the conclusion includes hedging language (e.g., "is unlikely to be", "is expected to",
"based on regional geology", "consistent with nearby sites").

---

### SCOPE-COST-01 — Cost-Constrained Investigation Warning

**Domain verdict**: VALID. MEDIUM severity is appropriate.

**Notebook grounding**:
- The RA notebook directly confirms the failure pattern: *"The developer naturally pressured the
  geotechnical engineer to adopt an optimistic view in order to keep the project alive. When time
  failed to bear out the optimism, the developer was obliged by the economics of the situation to
  try to recoup his losses."* [RA: citation 23]
- The RA notebook confirms the legal mechanism: *"The courts will infer that the geotechnical
  engineer undertook to do an investigation meeting the current standards of the profession. If on
  the other hand your proposal says 'we will drill three holes which we believe will give an
  adequate picture... This information will be suitable for... Further drilling may be required for
  design purposes', the court will be more inclined to recognize that your drilling program was
  based on an engineering assessment."* [RA: citation 18]
- The CEAS 1979 case study (engineer reported favourably on 3 hand-auger holes, architect imposed
  cost constraint, engineer didn't qualify, sued when unexpected fill was found) is a direct
  precedent. The lesson stated: *"It is very important that where any restriction on costs is
  imposed by the client that the Engineer should draw attention to this in their report and qualify
  it accordingly."* [CEAS-88: page 5]

**How often do reports mention cost constraints explicitly?**
Rarely. In my experience, cost constraints appear in the engagement letter or scope of work
document, not in the main report body. When they appear in the report, it is usually in the
Methodology section as "the investigation scope was limited to..." without the word "cost".
The rule's current trigger is too narrow.

**Recommended trigger expansion**:
The rule should fire on ANY of the following in the Scope or Methodology section:
- "limited to" / "limited investigation" / "limited scope"
- "preliminary investigation" / "preliminary assessment" / "preliminary only"
- "indicative only" / "indicative assessment"
- "budget" / "cost" / "financial constraint"
- "reconnaissance" (when used to describe the investigation itself, not a specific technique)
- "not included in this scope" / "outside the scope of this investigation"

The detection of ANY of these should trigger a check for corresponding qualification language in
the Conclusions section.

---

### SCOPE-CLAUSE-01 through -06 — Mandatory Clause Presence Checks

**Verdicts by clause**:

| Clause | Verdict | Confidence | Severity |
|---|---|---|---|
| 01: Inferred conditions caveat | MANDATORY in NZ/AU practice | notebook-grounded | High |
| 02: Temporal boundaries | NOT standard NZ boilerplate; present in US guidance | single-source | Low |
| 03: Groundwater fluctuation | Context-dependent — required only when groundwater is relevant | cross-referenced | Medium |
| 04: Changed conditions | Context-dependent — often replaced by "Further Work" section in NZ practice | notebook-grounded | Low |
| 05: Third-party reliance | MANDATORY in NZ/AU practice | notebook-grounded | High |
| 06: Standard-of-care | NOT standard NZ boilerplate; present in US guidance | single-source | Low |

**Detail on each clause**:

**Clause 01 — Inferred conditions caveat**: Definitively mandatory per the GRW template
[citation 7]. The template marks it "Mandatory" and provides the exact wording. This clause is
present in every correctly formatted report from a NZ firm. Absence is a genuine quality failure.
HIGH severity is warranted.

**Clause 02 — Temporal boundaries**: The RA notebook includes the clause ("Groundwater conditions
described in this report refer only to those observed at the place and time of observation")
[RA: citation 13], but the GRW notebook template does NOT include it as a standard boilerplate
requirement. This is a US ASCE-derived practice. NZ reports typically handle temporal scope
through the Applicability section's inferred conditions caveat rather than a separate temporal
clause. Implementing SCOPE-CLAUSE-02 as HIGH severity in NZ context will produce false positives
on correctly-formed NZ reports.

**Clause 03 — Groundwater fluctuation**: The GRW template requires engineers to *"consider
effects of seasonal and tidal groundwater level (gwl) changes, and of climate change sea level
rise over the design life of the structure"* [GRW: citation 16], but this is a methodology
requirement, not a disclaimer. The RA notebook includes a groundwater disclaimer clause [RA:
citation 13]. In NZ practice, groundwater fluctuation is addressed in the body of the report
where groundwater is discussed, not as a separate disclaimer clause. Check the Groundwater
section of the report for fluctuation discussion before flagging absence.

**Clause 04 — Changed conditions**: The RA notebook includes this clause [RA: citation 14].
However, the GRW template notes it is *"often (normally) not relevant and is better replaced by
previous section 'Further Work'"* [GRW: citation 7 guidance note]. In NZ practice, this clause
has been largely superseded by explicit construction monitoring requirements under the Building
Act. Checking for its absence will produce false positives. This clause should not be a presence
check rule; it should be a "Further Work section present?" check instead.

**Clause 05 — Third-party reliance**: Definitively mandatory. The GRW template marks it
"Mandatory" and provides exact wording [GRW: citations 4-6]. This clause is present in every
correctly formatted NZ report. Absence is a genuine quality failure. HIGH severity is warranted.

**Clause 06 — Standard-of-care**: The RA notebook includes this clause [RA: citation 10].
The GRW template does NOT include a standard-of-care boilerplate clause; it is not part of the
NZ/AU template tradition. This clause is a US ASCE practice. In NZ/AU, standard-of-care
protection comes through the Engineering NZ Code of Ethics, the IPENZ rules, and professional
registration — not through explicit boilerplate in reports. Implementing this as a presence check
in the NZ context will flag virtually every correctly-formed NZ report as deficient.

**Missing clauses for the list**:
The six-clause list is missing one important NZ/AU clause:
- **Temporal validity of recommendations**: *"If the project is modified in any significant way,
  or if the project is not initiated within eighteen months of the date of the report, [firm]
  should be given an opportunity to confirm that the recommendations are still valid."* [RA:
  citation 11]. This clause protects against stale reports being used without re-engagement. It
  is present in the RA notebook template and is important in NZ practice where development
  timelines often slip.

---

### CITE-EXIST-01 — Citation Existence Check

**Domain verdict**: VALID. MEDIUM-HIGH severity is appropriate.

**Notebook grounding**: Both clause-level and whole-standard citations are common in NZ
geotechnical reports; the rule must handle both patterns [ES: citations 11-19].

**Top 8 NZ/AU standards to prioritise in the Standards Knowledge Store build**:

| Standard | Citation pattern | Notes |
|---|---|---|
| NZS 4431 | Whole-standard; sometimes year-specific | HIGH priority — 1989 version widely cited; 2022 version is current |
| NZS 3604 | Clause-level (e.g., Clause 3.3.4, 3.1.3) | 1999 version superseded by 2011 |
| NZS 4402 | Test-level (e.g., Test 2.2, 2.6) | Soil testing; cited at sub-test level |
| NZS 1170.5 | Clause-level (e.g., Clause 3.1.3) | Earthquake actions |
| NZS 4404 | Whole-standard | Land development/subdivision |
| AS 2870 | Section-level (Sections 3, 5, 6) | Residential slabs; used for expansive soils |
| NZGS Field Description Guidelines | Whole-document; no clause | 2005 version in circulation |
| MBIE Canterbury Guidelines (Part D) | Whole-document | Geotechnical assessment; 2012 version |

**Standards with known version risk (engineers citing superseded versions)**:
1. **NZS 4431**: The 1989 version is still widely cited. The current version is 2022. Canterbury
   IDS was explicitly updated to mandate the 2022 version in October 2025 [ES: citation 22].
   This is a real and active problem.
2. **NZS 3604**: The 1999 version was superseded by the 2011 version. Some engineers in the field
   still reference NZS 3604:1999 [ES: citation 3].
3. **MBIE Canterbury Technical Categories (TC1/TC2/TC3)**: These were superseded by
   "Vulnerability to Liquefaction" mapping based on 2017 national guidance [ES: citations 29-30].
   Engineers may still reference the TC classification.

**Both citation patterns are real and the rule must handle both**:
- Whole-standard: "in accordance with NZS 3604" — check if standard exists and is not withdrawn
- Clause-level: "NZS 3604 Clause 3.3.4" — check if standard AND clause exist and are current

---

### RISK-LANG-01 — Absolute Word Detection in Conclusions

**Domain verdict**: VALID but HIGH false-positive risk as currently specified. The word list needs
tiering.

**Notebook grounding**: The RA notebook contains an explicit taboo-word list with risk categories
[RA: citations 1-9]. The sources identify three categories:
1. **100% success / zero-defect words**: "all", "every", "always", "never", "complete", "entire",
   "100%", "none", "zero", "perfect"
2. **Warranty/guarantee words** (create insurance gap): "assure", "ensure", "certify", "confirm",
   "guarantee", "warrant", "insure"
3. **Vague elevated-standard words**: "adequate", "sufficient", "highest quality", "best", "safe",
   "workmanlike"

**The word "suitable" is a special case**:
"Suitable" is one of the most common words in professional geotechnical conclusions. "The site is
suitable for the proposed residential development subject to the following conditions..." is the
standard conclusion form taught in every geotechnical training programme. Flagging every instance
of "suitable" would flag nearly every correctly-written geotechnical report conclusion. The risk
arises ONLY when "suitable" appears WITHOUT a qualifying condition following it (e.g., "The site
is suitable" as a terminal statement with no conditions). The rule must look for "suitable" +
absence of a following conditions clause, not "suitable" alone.

Similarly, "all" is routinely used in procedures ("all samples were tested") and in conditional
qualifications ("all recommendations are subject to"). These are not liability phrases.

**Recommended tiering**:

| Tier | Words | Flag action |
|---|---|---|
| HIGH (always flag) | guarantee, warrant, certify, insure, ensure [followed by physical outcome], safe [without qualification], "no risk", "zero risk" | Flag as definitive quality issue |
| MEDIUM (flag with context) | "all" + [site conditions / design claims], "every", "complete" [in conclusions context], "none" [in conditions context] | Flag for human review |
| CONTEXT-DEPENDENT (inform only) | suitable [without following conditions], adequate, sufficient | Flag only if no conditioning clause follows |

**Five specific phrases that should ALWAYS trigger a review** (notebook-grounded + practitioner):
1. "the site is safe for..." — implies zero risk; ipso facto unsafe if any incident occurs [RA:
   citation 7]
2. "all geotechnical risks have been [addressed/mitigated/eliminated]" — impossible to achieve
   [RA: citation 1]
3. "we guarantee / the engineer guarantees..." — creates strict liability regardless of negligence
   [RA: citation 4]
4. "there will be no [settlement/movement/failure]" — absolute negative, unprovable [RA: citation 2]
5. "the site is suitable for [purpose]" [with NO following conditions] — removes the qualification
   that makes the statement defensible [practitioner-grounded]

**Additional high-risk phrases not in the proposed list**:
- "...in accordance with the highest quality standards" — undefined elevated standard [RA:
  citation 6]
- "...we certify that..." — transforms report into legal certification [RA: citation 4]
- "...this report is final..." — bars correction of errors found post-issue [RA: citation 9]
- "the engineer confirms that..." — implies personal verified knowledge [RA: citation 4]
- "the design will perform as intended" — outcome guarantee [RA: citation 2]

---

## Checklist-Derived Rule Expansions (2026-05-13)

Analysis of 10 geotechnical report checklists across 5 jurisdictions (NZ, US FHWA, US TDOT,
US Mason County, US USACE) identified the following rule gaps not covered by the six families
above. See `checklist-taxonomy-cross-jurisdiction.md` for the full taxonomy and
`fhwa-reviewer-checklist-rule-vocabulary.md` for the FHWA candidate seed set.

### Cross-Section Limitations Statement (Drawings)

CERT 10a (Western Bay of Plenty 2009) explicitly requires a "Cross sections (limitations
statement)" item under the Drawings deliverable section. This embeds scope limitation logic in
a drawing deliverable, not in the report text. Engineers produce cross-sections with interpolated
subsurface profiles between boreholes without stating that the interpolation is inferred. The
SCOPE-LIM-01 check must be extended to run against figures and drawings, not just the report
body text.

### FHWA "Subjective Terminology" Additions

The FHWA reviewer checklist asks: "Has the use of subjective subsurface terminology been
avoided?" with examples: "relatively soft rock" and "gravel with occasional boulders." These
should be added to the TABOO-01 vague/subjective word detection list alongside the existing
taboo word families.

### Four Checklist Categories as Workflow Moments

The universal taxonomy carries a `workflow_moment` dimension: Pre-Investigation, During Drafting,
Pre-Review, Pre-Submission. Each rule should declare which workflow moment it belongs to. All
current SCOPE- and TABOO- rules belong to the Pre-Review moment. See
`checklist-taxonomy-cross-jurisdiction.md` for the full four-moment model.

### Seismic/Liquefaction Method Rules (NZ Configuration)

The NZGS 2016 Module 2 provides quantitative investigation method rules for liquefaction
assessment. These are NZ-specific and sit at the boundary of Layers 3 and 4. See
`nzgs-seismic-liquefaction-checklist-rules.md` for the full rule catalogue.

---

## Open Questions

1. Do NZ/AU professional indemnity insurers (CEAS/Aon) have specific standard-of-care boilerplate
   language requirements? I have no notebook-grounded answer to this. The CEAS documentation
   (Issue 88) discusses insurance coverage but does not specify required disclaimer wording.
2. Does Engineering NZ or ACE NZ publish a recommended Applicability clause that differs from the
   Tonkin & Taylor template? I have not seen such a document in the notebooks.
3. The Risk Assessment notebook's risky-word list appears to be a US-sourced document (ASCE
   practice). I cannot confirm that NZ/AU courts apply the same strict-liability interpretation
   for all listed words. Legal advice would be needed for full certainty on NZ/AU liability
   exposure from each word category.

## Further Reading

- CEAS Indemnity Matters Issue 88 (April 2026): [docs/references/Indemnity-Matters-Issue-88-April-2026.md](../../../references/Indemnity-Matters-Issue-88-April-2026.md)
- AI Workflow Expansion Boundaries: [contracts-and-risk/ai-workflow-expansion-boundaries.md](../contracts-and-risk/ai-workflow-expansion-boundaries.md)
- Parameter Completeness and Standard of Care: [parameter-completeness-checking-standard-of-care.md](parameter-completeness-checking-standard-of-care.md)
- Risk Assessment notebook: notebook ID 0b726429-82bc-43f7-9225-ba06f71046c3
