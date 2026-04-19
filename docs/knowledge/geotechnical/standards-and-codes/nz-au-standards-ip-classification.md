# NZ/AU Standards — IP Classification and Licensing for Software Use

**Sub-domain**: standards-and-codes
**Last verified**: 2026-04-19
**Confidence**: single-source (professional practice knowledge; no notebook citation possible — NotebookLM unavailable at time of authorship)
**Sources**: Graeme's professional experience (25+ years, large NZ geotechnical consultancy); existing Redline research documents `20260412-standards-management-and-mapping.md`, `20260413-standards-clause-extraction.md`

**⚠ External verification required before acting on Q1 and Q3 findings — see Open Questions.**

---

## Summary

NZS and AS standards are proprietary publications with clear copyright held by Standards New Zealand and Standards Australia respectively. NZGS and ACENZ guidance documents are likely in a softer category (freely distributed by professional societies) but their terms for derivative software use have not been verified. Citation-only architecture (referencing clause numbers without reproducing text) is fully defensible in professional engineering practice. Licensing pathways for software vendor use of standards content are not well-known from practice and require direct enquiry with the standards bodies.

---

## Key Facts

### IP Classification

1. **NZS 3910:2013 (Conditions of Contract for Building and Civil Engineering Construction)** is a Standards New Zealand publication. Standards New Zealand is a business unit of MBIE. All NZS publications are protected by Crown copyright. NZS 3910 must be purchased; verbatim reproduction is not permitted. Clause references (e.g., "NZS 3910:2013 Clause 14.4") are standard practice in engineering reports and contracts. Whether a software tool that generates derived output triggering applicability mappings based on NZS 3910 content requires a separate licence from Standards NZ has **not been verified** — this is a legal/commercial question, not a professional practice question.
   - **Classification: (b) Proprietary but citation-safe** — clause references and applicability mappings are professionally standard. Whether (c) applies for derived output depends on Standards NZ's specific licensing terms. **Must verify directly with Standards NZ.**

2. **AS 4000 (General Conditions of Contract)** is a Standards Australia publication. Standards Australia holds copyright. Same structure as NZS: proprietary, purchased, not reproducible verbatim. Clause references are standard professional practice. Software tooling use requires direct verification with Standards Australia.
   - **Classification: (b) citation-safe; (c) uncertain for software-derived output. Must verify directly with Standards Australia.**

3. **AS/NZS 4122 (General Conditions of Contract for Consultants)** is a joint publication of Standards Australia and Standards New Zealand. Both bodies hold joint copyright. Same classification reasoning as AS 4000 and NZS 3910.
   - **Classification: (b) citation-safe; (c) uncertain for software-derived output. Must verify with both Standards Australia and Standards NZ.**

4. **NZGS guidance documents** (e.g., Module 1 — Site Characterisation, CPT Guideline, Liquefaction Assessment Guideline) are published by the New Zealand Geotechnical Society, a not-for-profit professional membership organization. Many NZGS guidance documents are freely downloadable from the NZGS website and carry no purchase requirement. However, "freely downloadable" does not automatically mean "freely reproducible in derivative works." NZGS documents carry copyright notices. The specific terms for use in a software product that generates derived output have **not been verified**.
   - **Classification: Likely closer to (a) or (b) — but this cannot be stated with confidence. Must verify with NZGS directly.** Given NZGS's mission to share geotechnical knowledge, a permissive arrangement may be achievable at low cost or for free, but this is speculation.

5. **ACENZ guidance documents** (e.g., fee guidance, procurement guidance) are published by the Association of Consulting Engineers New Zealand, a membership and advocacy organization. Similar to NZGS: some documents are publicly available, but reproduction terms for software use are not known from practice.
   - **Classification: Uncertain. Must verify with ACENZ directly.**

### Citation-Only Architecture — Professional Defensibility

6. **Citing clause references without reproducing text is standard engineering practice.** In 25+ years of professional practice, I have never seen an engineering report, GBR, GIR, or contract that reproduced full clause text from NZS or AS standards. Standard practice is: "The contract conditions shall comply with NZS 3910:2013, Clause 14.4 — Latent Conditions." The engineer is expected to hold (or have employer-library access to) the relevant standards.

7. **Clause references are legally binding in contracts.** Courts, engineers, and expert witnesses routinely work from clause references as primary citations. This is well-established in NZ and AU construction law practice. A reference is considered unambiguous: "NZS 3910 Clause 14.4" points to exactly one piece of text.

8. **Engineers do not routinely need text reproduced for them.** At any consultancy where engineers work with NZS 3910 or AS 4000, those standards are purchased and available in the office (hard copy or digital subscription). Providing a clause reference is an instruction to look up the clause, not a request for the text to be supplied.

9. **The citation-only architecture is professionally sound.** It is consistent with how all engineering references work: Producer Statements cite specific standards without reproducing them [see `20260412-standards-management-and-mapping.md`, Source 7–10]. Contract Quality Plans and Audit & Test Schedules cite clause numbers and acceptance criteria without reproducing the full standard [ibid, Source 20–22].

10. **One professional nuance:** For junior engineers using a tool like Redline, pointing to a clause they don't have ready access to creates a friction point. This is a **product design concern** (UX), not a legal or professional practice concern. The architect should be aware that removing full-text reproduction in the output may require a "where to find this standard" link or employer-library integration to avoid frustrating users.

### Licensing Pathways

11. **Standards NZ corporate subscription model.** In my consultancy, we purchased a Standards NZ Online Standards Library corporate licence covering all NZS and joint AS/NZS publications for staff. This is the standard large-consultancy arrangement. Whether this licence extends to building a software product that triggers applicability mappings from standards content is **not known from practice** — it was never a question we encountered because we were not building software products.

12. **No known precedent for formal "software vendor licence" from Standards NZ.** In 25 years of large consultancy practice, I have not personally encountered a consultancy obtaining a specific software-tooling licence from Standards NZ or Standards Australia. This does not mean such a pathway does not exist — only that it is not visible from my experience.

13. **No known NZ/AU precedent for citation-only tools being formally challenged.** I am not aware of any case where a professional software tool operating on a citation-only basis (referencing clause numbers without reproducing text) was challenged by Standards NZ or Standards Australia. This is not a legal opinion — it is an absence of known precedent, which is not the same as a safe harbour.

---

## Standards Referenced

- NZS 3910:2013 — Conditions of Contract for Building and Civil Engineering Construction (Standards New Zealand)
- AS 4000:1997 — General Conditions of Contract (Standards Australia)
- AS/NZS 4122:2000 — General Conditions of Contract for Consultants (Standards Australia / Standards New Zealand)
- NZGS publications — New Zealand Geotechnical Society
- ACENZ publications — Association of Consulting Engineers New Zealand

---

## Open Questions

1. **Standards NZ licensing for software use.** Does Standards NZ offer a specific licence (or extend its corporate subscription) to software products that generate outputs triggered by applicability mappings of standards content? **Action: Direct enquiry to Standards NZ licensing team required before any content ingestion.**

2. **Standards Australia equivalent.** Same question for AS 4000 and the AS/NZS joint publications. **Action: Direct enquiry to Standards Australia required.**

3. **NZGS copyright terms for derivative works.** Does NZGS permit a software product to store clause references and applicability mappings derived from their guidance documents? Given their open-distribution intent, a positive response may be achievable. **Action: Enquiry to NZGS Executive Officer required.**

4. **ACENZ copyright terms.** Same question for ACENZ guidance documents. **Action: Enquiry to ACENZ required.**

5. **Whether "applicability mapping" constitutes a derivative work.** This is a legal question. A copyright lawyer with IP experience in standards and technical publications should provide a written opinion before the system goes to production. The citation-only principle is professionally sound but its legal status under NZ copyright law (Copyright Act 1994) has not been assessed.

---

## Further Reading

These are unverified pointers. I have not read these sources, but they may contain the answer:

- **Standards New Zealand licensing page** — `standards.govt.nz/support/licensing/` — should document available licence types for corporate and software use.
- **Standards Australia IP and licensing** — `standards.org.au` — equivalent for AS publications.
- **NZ Copyright Act 1994, Section 43** — fair dealing for research and private study; may or may not apply in a commercial software context.
- **ISO POCOSA (Procedures for the Consumption of Standards in Automation)** — ISO has published guidance on machine-readable standards; may contain precedents for the standards-in-software licensing problem. (I have not verified whether NZS or SA have adopted this.)
