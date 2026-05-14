# Problem Statement: The Quality-Committed Firm Segment

**Status**: Draft v1. **Owner**: Mark. **Date**: 2026-05-14.
**Strategic bet**: [Bet 1 — The Free Skeleton Wedge Beats Paid Acquisition](../strategy/strategic-bets.md)
**Resolution source**: Advisory board session 2026-05-14 — Ron identified quality-committed firms as Redline's real ICP (Ideal Customer Profile).

---

## Segment Definition

The quality-committed firm is identifiable by at least one of the following signals:

- **PI (Professional Indemnity) claim or near-miss history** — the firm has changed its QA process in response to a project experience: a near-miss, an unexpected client escalation, or an incident that prompted a review. *Do not ask about claims directly — engineers are trained to be cautious about what they disclose to vendors. Ask instead: "Has your firm changed its QA process in response to a project experience?" This surfaces the same underlying experience without triggering a defensive response.*
- **Named QA Principal or formal review-stage policy** — the firm has assigned a named individual responsibility for QA, or has a written policy that mandates a review stage before report submission.
- **QA is funded from firm overhead, not the project budget** — the practical test for whether review time is genuinely protected. When QA comes out of the project budget, project managers compress it under deadline pressure regardless of policy. The behavioural test: *when a senior engineer pushes back a delivery date because review is incomplete, does the project manager accept that?* A principal who answers yes without hesitation is in the target segment.
- **Fixed-fee or write-off-reduction billing model** *(hypothesis — validate in co-development conversations)*: firms that bill by the hour have a structural disincentive to reinvest freed review time into deeper review — efficiency means fewer billable hours. The genuine use condition (freed time reinvested in engineering judgment) is commercially sustainable primarily for fixed-fee firms or firms motivated by reducing write-offs and rework cost. Test for billing model alongside the other signals.

These are observable, pre-sale qualification signals. They can be surfaced through outbound conversations with firm Principals and through PI renewal discussions.

---

## The Segmentation Rationale

Graeme established the following benchmark (2026-05-14): approximately 55% of senior engineer review time is currently consumed by compliance mechanics — citation accuracy, wording, clause presence, standard applicability. The remaining 45% is genuine engineering judgment: calculation review, parameter plausibility, methodology assessment.

Redline frees the 55%.

What the firm does with that freed time determines whether Redline creates or destroys value:

- The **quality-committed firm** reinvests the freed time into the 45% — deeper technical review, more senior attention on engineering substance. Redline makes this firm more rigorous, and the firm's PI position improves.
- The **throughput firm** pockets the freed time as volume — more reports shipped per week, same review depth. Redline accelerates output without improving quality.

These two outcomes are not equally good for Redline.

---

## The Throughput Firm Risk

If a throughput firm uses Redline to accelerate report production without reinvesting review time, and a calculation error or engineering judgment failure slips through, Redline may have contributed to that outcome: the compliance layer appeared clean, which generated false confidence in the report as a whole.

This is a brand risk, not a theoretical one. Redline's positioning is "we check the document, not the design." That boundary holds only if the buyer understands it and chooses to maintain engineering review independently. Throughput firms are structurally unlikely to maintain that discipline.

**Selling to throughput firms first is a brand risk.** The segment to acquire in Phase 1 is quality-committed firms, even if throughput firms are easier to close on a time-saved value proposition.

---

## Commercial Implication

| Buyer type | Buys on | Price ceiling | Redline outcome |
|---|---|---|---|
| Quality-committed firm | Value — risk reduction, PI defensibility | Higher (value-based) — *hypothesis, to be tested in co-development conversations; do not use as a basis for pricing decisions before validation* | Positive — Redline improves firm's risk position |
| Throughput firm | Price — time saved per report | Lower (cost-based) | Risky — Redline may enable volume without quality |

These are different sales conversations, different economic buyers, and different price ceilings. Conflating them in the early sales motion will produce a mixed customer base and a diluted brand.

---

## Phase 2 Enterprise Buyer

Firm principals who are about to lose a senior engineer to retirement face an acute knowledge loss problem. The institutional knowledge of which standards apply, which clauses are mandatory, and which jurisdiction-specific requirements have been learned through years of practice walks out the door.

The skeleton as a knowledge externalisation tool directly addresses this. For this buyer, the value proposition is not "save 2 hours per report" — it is "preserve what your senior engineer knows before they leave."

This buyer segment becomes reachable in Phase 2, once the skeleton has demonstrated value with quality-committed firms and the knowledge externalisation framing is validated.

---

## Next Hypothesis to Test

**Ron's hypothesis (2026-05-14)**: Does PI claim history or formal QA policy correlate with willingness to pay a value-based price (vs. a cost-based price)?

Proposed test: in the next 10 outbound conversations with firm Principals, ask directly about PI claim history and QA policy before presenting pricing. Record whether firms with PI history or formal QA policy respond differently to the value-based price anchor than firms without.

Kill criterion: if firms with PI/QA signals show no higher price acceptance than the general population after 10 conversations, the segmentation hypothesis is not supported and the ICP framing requires revision.
