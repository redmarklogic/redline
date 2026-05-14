# Launch Planning Session — Advisory Board Agenda

**Date**: 2026-05-14
**Participants**: Ron (strategy), Mark (product), John (marketing), Graeme (domain), Harriet (people & agent development)
**Purpose**: Define what Redline needs to achieve quickly at launch — media wing, website, demo use cases, and activation sequence.

---

## Item 1 — Launch Perimeter

**What will be decided:** The minimal website scope and feature state that unblocks beta launch — specifically which of the following must be true before anything else starts: company LinkedIn profile, website live, skeleton generator demo-able, demo video exists.

**Agents:** Ron, Mark

---

## Item 2 — Use Case Portfolio

**What will be decided:** A complete enumerated list of use cases Redline can demonstrate or check — sourced from the PI webinar, Indemnity Matters, prior research, and Graeme's domain expertise — ready for joint prioritisation.

**Agents:** Graeme (domain validity), Mark (product feasibility), Ron (strategic framing), John (marketing power)

---

## Item 3 — Demo Asset and Test Coverage

**What will be decided:** Which use case(s) become the public demo — including whether the proposed council-report-with-altered-citation approach is viable (copyright, domain accuracy, reproducibility) — and how the chosen demo is mirrored in the test suite.

**Agents:** Graeme (copyright and domain accuracy), Mark (test suite coverage), John (marketing impact)

---

## Item 4 — Market Activation Sequencing

**What will be decided:** The order in which the LinkedIn media wing, website launch, and co-development partner outreach activate — and how the June 2027 renewal window shapes the timing of first co-development conversations relative to the website being live.

**Agents:** Ron, John

---

## Item 5 — Acceptance Test Ownership

**What will be decided:** Who is responsible for defining, reviewing, and signing off acceptance tests for domain-specific use cases — for example, when a vetted geotechnical report has its cited standard altered to (a) an older version, (b) a non-existent standard, or (c) an irrelevant standard (e.g. an Australian standard substituted for a NZ one), the system must capture all three cases. Specifically: does Graeme define the acceptance criteria alongside Mark? Does Mark own test specification and engineering implementation? And is Mark the one who confirms a test passes — or does Graeme hold the domain sign-off gate?

**Agents:** Harriet (clarify role boundaries and ownership model between domain expert and product owner), Mark (product owner responsibilities: spec, implementation oversight, pass/fail confirmation)

---

## Most Time-Critical

Item 4 — but on the June **2027** renewal cycle, not 2026. By June 2027, AI usage in NZ engineering firms will be heavier, the probability of AI-related mistakes higher, and the renewal conversation more charged. Redline should be positioned with a mature product and demonstrated use cases before that window opens.

---

## Status

| Item | Status |
|---|---|
| Item 1 — Launch Perimeter | Complete — see `launch-perimeter-constraints.md` |
| Item 2 — Use Case Portfolio | Complete — D/E/V table in session transcript (not yet committed to a file; Mark to formalise before Sprint planning) |
| Item 3 — Demo Asset and Test Coverage | Complete — synthetic report decision; UC-01/UC-02 anchors; NZS 4431:1989 fixture; Sprint 1 test coverage; video deferred Sprint 2-3. Claude GBR experiment validated as Sprint 2-3 demo fixture — see `docs/knowledge/geotechnical/report-writing/claude-gbr-demo-review.md` |
| Item 4 — Market Activation Sequencing | Not started |
| Item 5 — Acceptance Test Ownership | Not started |

## Claude GBR Experiment — Conclusion (2026-05-14)

Claude was prompted to generate a GBR for a NZ residential development. Graeme reviewed it
against NZ standards from the NotebookLM notebooks.

**Result**: 6 citation errors (3 HIGH), 10 structural/domain issues. Every error maps to a
Redline rule. No errors were planted — all are organic AI failure modes.

**Key findings**:
- NZS 4431 (governing residential earthworks standard) completely absent
- NZS 4407:2015 hallucinated for SPT (it is a road aggregate standard)
- NZS 4402 conflated as compliance framework (it is test methodology)
- Third-party reliance clause generic (not mandatory exact wording)
- "Suitable for" warranty language present
- Liquefaction conclusion unsupported

**Decision**: This Claude-generated GBR becomes the demo fixture for Sprint 2-3 video.
The hand-crafted NZS 4431:1989 fixture remains the Sprint 1 test coverage anchor.

**Demo video script** (Sprint 2-3): Lead with NZS 4431 absence, follow with NZS 4407
hallucination, close with warranty language flag. Three flags, ninety seconds, all organic.

**Next step**: Create an HTML mockup emulating a Word document with Redline review comments
overlaid on the Claude-generated GBR text (see `output/mockups/`).
