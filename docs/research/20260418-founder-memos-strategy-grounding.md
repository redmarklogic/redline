# Founder Memos — Strategy Grounding (April 2026 Pass)

**Date**: 2026-04-18
**Author**: Ron (Strategy & GTM Advisor)
**Purpose**: Consolidate the grounded inputs used to write the strategy artifact set
under `docs/product/strategy/` in the April 2026 pass.

---

## Source Provenance

This grounding pass deliberately did **not** issue fresh NotebookLM queries against the
Founder Memos. The founder's brief in this conversation was unusually explicit (decisions
table, verbatim prioritisation rubric, candidate feature list, wedge hypothesis), and the
following prior research files already capture the relevant memo-derived findings I needed
to ground the artifacts:

| Prior research file | What it grounds |
|---|---|
| `docs/research/20260411-gir-skeleton-acceptance-criteria.md` | Skeleton-generator acceptance criteria; what "good" looks like |
| `docs/research/20260411-gir-skeleton-section-placeholders.md` | Placeholder/prompt pattern inside the skeleton |
| `docs/research/20260412-report-drafting-initiation-workflow.md` | Skeleton-before-fieldwork workflow; "touchstone" + Sense Check gate |
| `docs/research/20260412-modularity-vs-layering.md` | Architecture posture (one product / two modes feasibility) |
| `docs/research/20260412-standards-management-and-mapping.md` | Standards registry foundation for localisation penalty scoring |
| `docs/research/20260413-standards-clause-extraction.md` | Confidence input for Citation/Reference Validator scoring |
| `docs/research/20260413-standards-registry-knowledge-architecture-gaps.md` | Risk inputs for Standards Lookup Bot scoring |

All claims in the strategy artifacts that require domain grounding either cite one of the
files above or are explicitly flagged as **strategy synthesis** (Ron's view), not memo
fact. Where a memo claim is invoked without a citation, that is a defect — flag it back to
me and I will retro-cite or downgrade the claim.

## What Was Grounded vs. What Is Strategy Synthesis

| Claim in artifacts | Grounded by | Type |
|---|---|---|
| Skeleton is the *natural* first artifact in the GBR workflow | `20260412-report-drafting-initiation-workflow.md` | Memo fact |
| Skeleton must inject standards-derived placeholders, not just structure | `20260411-gir-skeleton-section-placeholders.md` | Memo fact |
| Standards corpus is the long-pole on localisation | `20260412-standards-management-and-mapping.md`, `20260413-standards-registry-knowledge-architecture-gaps.md` | Memo fact |
| Intermediate engineer is Day-1 ICP | Founder verbal (this pass) + memo workflow context | Mixed |
| Principal/Partner is Phase-2 ICP | Founder verbal (this pass) | Strategy synthesis |
| ONE product / TWO modes / THREE tiers architecture | Founder decision (this pass) | Founder decision |
| 5 paying customers in 90 days | Founder ask; Ron's counter is strategy synthesis | Founder ask + Ron rebut |
| Free skeleton wedge beats Google Ads on CAC | Founder hypothesis; not yet evidenced | Hypothesis |
| Adversarial Scan engine is Phase-2 (Confidence too low for Sprint 1) | Strategy synthesis based on absence of labelled adversarial corpus | Strategy synthesis |
| Standards corpus localisation penalty | `20260412-standards-management-and-mapping.md` | Memo fact |

## Open Grounding Gaps (Worth a NotebookLM Pass Later)

These were not re-queried this pass. Schedule before the next strategy refresh:

1. **Procurement cycle length for SME geotechnical firms in NZ/AU.** Used to challenge
   "5 paying in 90 days." Currently relying on common SaaS-into-AEC sector benchmarks
   (6–8 weeks bottom-up). Worth confirming against any procurement memos.
2. **Intermediate engineer's stated pain ranking** — judgement vs. structure vs. lookup.
   Affects Sprint 1 wedge choice (Skeleton vs. Pre-Review Lite). Currently decided on
   funnel mechanics, not ranked customer-stated pain.
3. **Indemnification clause as standalone free tool** — viability and viral mechanics.
   Currently scored on first-principles, not memo-grounded.
4. **House Rules authoring complexity at Partner level.** Affects Phase-2 sequencing.

## Sources Consulted (This Pass)

| Source | Type | Notes |
|---|---|---|
| Founder brief (this conversation) | Direct founder input | Decisions table, verbatim rubric, candidate list, wedge hypothesis |
| `docs/research/20260411-*` and `20260412-*` and `20260413-*` | Prior memo-grounded research | Listed above |
| `docs/architecture/domain-model.md` | Vocabulary alignment | Confirmed "GBR" / "GIR" / "skeleton" terminology consistent |
| NotebookLM (Founder Memos, Monetizing & Scaling Innovation) | **Not queried this pass** | Logged here for transparency |

## Glossary

| Term | Definition |
|---|---|
| GBR | Geotechnical Baseline Report — contractually relied-upon characterisation of subsurface conditions used in tendering and risk allocation. |
| GIR | Geotechnical Interpretive Report — engineer's interpretation of site investigation data. |
| Skeleton | A structured, placeholder-populated report shell that guides the human engineer through the required content sections before any factual data is gathered. |
| Wedge | A free, narrowly-scoped product surface used to acquire users at low CAC and convert them to paid tiers. |
| WTP | Willingness To Pay — pricing research methodology (per Ramanujam, *Monetizing Innovation*). |
| ICP | Ideal Customer Profile. |
