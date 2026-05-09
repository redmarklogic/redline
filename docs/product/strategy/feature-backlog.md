# Feature Backlog — Scored (April 2026)

**Status**: Draft v1. **Owner**: Mark (per-feature ranking from this point forward).
**Methodology**: Founder's 5-vector rubric — see `prioritisation-framework.md`.
**Last scored**: 2026-04-18 by Ron.

> Mark: this is your inheritance. Re-score before Sprint 1 planning closes. Disagreements
> with Ron's scores are welcome; log them in `docs/product/decisions/` per the framework
> handoff rules.

## Scoring Conventions

- Each feature scored 1–5 on Client Impact, Ease of Building, Localisation Penalty,
  Confidence, GTM Alignment. Total /25.
- Infrastructure features (M, N) are scored on enabling impact, not direct customer
  impact. Their position in the table reflects that they are *required dependencies*,
  not customer-visible bets.
- Adversarial-mode features (H, I) are scored as if built today — Confidence is low
  because the engine prerequisites are absent. They will rescore higher in Phase-2.

## Scored Backlog

| # | Feature | Mode / Tier | Client Impact | Ease | Localisation | Confidence | GTM | **Total** | Sprint band |
|---|---|---|---|---|---|---|---|---|---|
| G | Justification Email Generator (bottoms-up viral, asks Partner to fund team licence) | Pre-Review / Pro | 3 | 5 | 5 | 4 | 5 | **22** | Sprint 2 |
| A | GBR / GIR Skeleton Generator (free, SSO-gated download, capped 3–5 docs × 100 pages) | Free wedge | 3 | 5 | 3 | 5 | 5 | **21** | **Sprint 1** |
| D | Inline Annotation Engine (browser upload only; flags ambiguity, missing definitions, undefined acronyms, unit inconsistencies). Word task pane parked — see P-024. | Pre-Review / Pro | 5 | 3 | 3 | 4 | 5 | **20** | Sprint 2-3 |
| M | Document Parser / Chunking Pipeline | Infra (cross-cutting) | 3 | 3 | 5 | 4 | 5 | **20** | **Sprint 1** (infra dep of A) |
| L | Audit Log + Reviewer Sign-off | Business | 3 | 4 | 5 | 5 | 2 | **19** | **Sprint 1** (core subset); full scope Sprint 5+ *(elevated 2026-04-20, Archie CI session --- insurance bifurcation; sign-off via OOXML metadata confirmed 2026-05-06, conditional on P-024)* |
| F | Citation / Reference Validator (verifies cited standards exist + are current) | Pre-Review / Pro | 3 | 4 | 2 | 4 | 3 | **16** | Sprint 3 |
| D.pc | Parameter Completeness Checking (rule type within D — presence check for design-type-specific parameters; requires design-type taxonomy. Pareto 5: shallow foundations, timber pole retaining walls, slope stability, liquefaction assessment, piled foundations. Both under-inclusion and over-inclusion are failure modes.) | Pre-Review / Pro | 4 | 2 | 3 | 3 | 4 | **16** | Sprint 3-4 |
| E | Senior Reviewer Anticipator (predicts senior markups, ranks by severity) | Pre-Review / Pro | 5 | 2 | 3 | 2 | 4 | **16** | Sprint 4+ (needs labelled corpus) |
| J | Multi-Document Cross-Check (GBR vs. RFP vs. proposal) | Adversarial / Business | 4 | 2 | 4 | 3 | 3 | **16** | Sprint 5+ |
| B | Indemnification Clause Flagger (free single-doc scan, no sign-in) | Free | 4 | 3 | 2 | 3 | 4 | **16** | **Defer** (alternative wedge — see Sprint 1 reasoning below) |
| K | House Rules Authoring Console (Principal-configured firm QA standards) | Business | 4 | 2 | 4 | 3 | 2 | **15** | Sprint 5+ |
| N | Standards Knowledge Store (NZS 3910, AS 4000, AS/NZS 4122, NZGS, ACENZ) | Infra | 2 | 3 | 1 | 4 | 4 | **14** | **Sprint 1** (infra dep of A and D) |
| C | Standards Lookup Bot (NZ/AU geotech standards Q&A, free, email-gated) | Free | 2 | 4 | 1 | 4 | 2 | **13** | Reject (utility, not differentiation) |
| I | Indemnification + Limitation-of-Liability Auditor (for RFP responses) | Adversarial / Business | 5 | 2 | 2 | 2 | 2 | **13** | Phase-2 (P-008) |
| H | Differing-Site-Conditions Probe (simulates contractor lawyer attacks on baseline language) | Adversarial / Business | 5 | 1 | 2 | 2 | 2 | **12** | Phase-2 (P-008) |

## Sprint Bands

### Sprint 1 — Vertical slice (must ship end-to-end)

- **A. GBR Skeleton Generator** (the wedge)
- **M. Document Parser / Chunking Pipeline** (required infra)
- **N. Standards Knowledge Store — minimum viable subset** (3–5 NZ documents only;
  enough to populate skeleton placeholders for residential GBR scope)
- **L. Audit Log — core subset only** *(added 2026-04-20, Archie CI session)*.
  NZ insurance market is bifurcating on AI coverage (affirmative vs. absolute exclusion).
  Audit trail is now a Day-1 requirement, not a Phase-2 feature. Core subset: log every
  AI action with timestamp, input hash, and model version. Full scope (reviewer sign-off,
  export, retention policies) remains Sprint 5+. Provenance:
  `docs/research/20260420-archie-competitive-intelligence-prompt.md`.

### Sprint 2–3 — Convert wedge to paid

- **G. Justification Email Generator** (bottoms-up conversion mechanic for Pro → Business)
- **D. Inline Annotation Engine** (the paid product surface — Pre-Review). Decomposes into
  taxonomy-free rules first (15–20 rules: taboo words, undefined acronyms, ambiguity flags,
  unit inconsistencies, citation validator, section/structural completeness, passive voice /
  readability). Parameter completeness rules follow in Sprint 3–4 (see D.pc below).
- **F. Citation / Reference Validator** (sub-feature of D; ships inside D's first release)

### Sprint 3–4 — Parameter Completeness Rules (D.pc)

- **D.pc. Parameter Completeness Checking** — pluggable rules that check presence of
  design-type-specific parameters (e.g., bearing capacity for shallow foundations,
  FoS against sliding for timber pole retaining walls). Presence check only — no
  numeric validation. Blocked by two dependencies:
  1. **Stream 2**: Feature D rule engine scaffold must be built (Sprint 2-3, after P-030 unfreezes).
  2. **Stream 3**: Graeme's taxonomy discovery must validate parameter checklists for
     Pareto 5 design types (`docs/knowledge/geotechnical/report-writing/design-type-taxonomy-and-parameter-completeness.md`).
- Taxonomy discovery (Stream 3) proceeds in parallel with all other streams — no code dependency.
- Integration point: same rule interface as taxonomy-free rules (takes parsed document,
  returns annotations).
- **References**: [Bet 2](strategic-bets.md) (Pre-Review), [Bet 3](strategic-bets.md) (Standards Knowledge Store as moat).

### Sprint 4+ — Pre-Review depth

- **E. Senior Reviewer Anticipator** (only after labelled markup corpus exists)

### Sprint 5+ — Business tier and Phase-2 prep

- **K. House Rules Authoring Console**
- **L. Audit Log + Reviewer Sign-off — full scope** (core subset ships Sprint 1;
  full scope includes reviewer sign-off, export, retention policies)
- **J. Multi-Document Cross-Check**

### Phase-2 / Parked

- **H. Differing-Site-Conditions Probe** — parked under P-008 (Adversarial Scan engine
  readiness). Confidence is too low to ship before the Standards Knowledge Store matures.
- **I. Indemnification + LoL Auditor** — same as H.
- **C. Standards Lookup Bot** — rejected: GTM Alignment 2/5 (utility, not differentiation),
  and the Standards Knowledge Store is delivered to customers more strategically as a
  silent backbone of A and D than as a standalone Q&A surface.
- **B. Indemnification Clause Flagger as standalone free tool** — deferred. See Sprint 1
  recommendation reasoning below for why I did not pick this as the wedge.

## Sprint 1 Vertical Slice — Recommendation

**Recommendation: Founder is right. Build the GBR Skeleton Generator (A) as the
wedge, with M and a minimum slice of N as the infra spine.**

### Why founder's choice survives the pressure test

I challenged this for the founder. Three counter-wedges were on the table:

1. **B. Indemnification Clause Flagger as a free single-doc scan** — sharper hook,
   instant gratification, partial Adversarial Scan teaser.
2. **Pre-Review Lite** — free upload of one GBR section, returns 5 most likely
   senior-reviewer comments. Directly demonstrates the paid product.
3. **A. Skeleton Generator** — founder's lean.

Where each wins and loses, against the rubric:

| Counter-wedge | Where it beats Skeleton | Where it loses |
|---|---|---|
| B. Indemnification Flagger | Higher Client Impact (4 vs. 3); instant wow | Localisation Penalty 2/5 (clause language is jurisdiction-bound); no quota mechanic; converts to *Adversarial* tier which is Phase-2 ICP |
| Pre-Review Lite | Demonstrates the paid product directly | Chicken-and-egg: user must bring a draft; weak quota mechanic; intermediate engineer's first-use friction is high |
| A. Skeleton Generator | Strong Confidence (5/5) from prior research; clean quota mechanic; produces tangible artifact in 60 seconds; converts to *Pre-Review* tier which **is** the Day-1 ICP path | Lower instant-wow than B; doesn't directly demonstrate the paid product |

### Verdict

A wins on three things that matter more than instant wow at this stage:

1. **Confidence is the highest of any candidate** (5/5). The skeleton-with-placeholders
   pattern is grounded in two prior research files
   (`20260411-gir-skeleton-section-placeholders.md`,
   `20260412-report-drafting-initiation-workflow.md`).
2. **The quota mechanic is the cleanest funnel device.** Generating documents has a
   natural unit (one document = one quota slot). Reviewing or scanning has a fuzzier
   unit (a section? a page? a clause?) that complicates outbound timing.
3. **The conversion path lands on the Day-1 ICP's tier** (Pre-Review / Pro), not on
   a Phase-2 buyer (Adversarial / Business). Wedges that convert into the wrong tier
   waste the funnel.

The cost: A doesn't directly demonstrate the paid product. We solve that in Sprint 2 by
shipping a Pre-Review preview at quota-exhaustion — i.e. when the user hits the wall on
free, the outbound email *also* carries a "try Pre-Review on the skeletons you just
generated" CTA. That sequences the demo to a moment of high intent.

### What this means for Mark

- Mark drafts the Sprint 1 PRD for **A** as the user-visible artifact. **M** and the
  minimum **N** are scoped inside A's PRD as engineering dependencies (do not file
  separately — that fragments accountability).
- Mark drafts the Sprint 2 PRD for **D + G** in parallel, because G's viral mechanic
  needs to be ready when D ships.
- Mark explicitly logs the rejection of B and Pre-Review Lite as Sprint 1 wedges in
  `docs/product/decisions/`, with my reasoning above as the input.

## Mark Handoff (Required Reading)

This is the explicit handoff that closes Ron's H2 strategy pass:

1. **Framework custody.** Per-feature prioritisation is now Mark-owned. Load
   `pm-prioritization` skill before re-scoring this backlog or scoring any new
   feature. The framework lives in `prioritisation-framework.md`.
2. **Sprint 1 PRD.** Draft the PRD for **A. GBR Skeleton Generator** with **M** and
   minimum **N** scoped as engineering dependencies inside the same PRD. Reference
   `20260411-gir-skeleton-acceptance-criteria.md` and
   `20260411-gir-skeleton-section-placeholders.md` as the grounded acceptance basis.
3. **Sprint 2 PRD — Justification Email Generator (G).** Draft as a Sprint 1
   *dependency-mapping* exercise: G's viral mechanic must be ready when D ships in
   Sprint 2–3, so its requirements need to be locked while A is being built.
4. **Dual-persona WTP interview discussion guide.** Draft the discussion guide for
   the KR2 conversations (15 qualified discovery calls in 90 days). Cover both ICPs:
   intermediate engineer (Day-1) and Principal/Partner (Phase-2 signal). Anchor the
   pricing segment on the Van Westendorp module per `pricing-methodology.md` Step 1.
5. **Decision logging.** Any score in this table that Mark disagrees with is logged
   in `docs/product/decisions/` with both scores, both rationales, and the resolution.
   Do not silently overwrite Ron's scores — the audit trail matters.

## Provenance

Scoring is Ron's first pass against the founder's verbatim rubric. Sprint 1 reasoning
synthesis grounded in the prior research files cited inline. Mark handoff is explicit
per the founder's brief this pass.
