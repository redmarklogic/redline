# PRD: Free Skeleton Generator (Feature A)

**Status**: Draft v1. **Owner**: Mark. **Date**: 2026-04-20.
**Target reader**: Engineering.
**Strategic bet**: [Bet 1 — The Free Skeleton Wedge Beats Paid Acquisition](../strategy/strategic-bets.md)
**Problem statement**: [skeleton-wedge-problem.md](../problems/skeleton-wedge-problem.md)

## Strategic Context

Bet 1 claims that a free, SSO-gated GBR/GIR Skeleton Generator acquires intermediate
engineers at lower cost than paid acquisition and converts to paid Pre-Review at a higher
rate than cold outreach. The skeleton is the natural first step in the GBR workflow per
[report-drafting-initiation-workflow.md](../../research/20260412-report-drafting-initiation-workflow.md).
Quota exhaustion creates a defensible moment for founder-led outbound.

Competitive context: SupaHuman's Archie validates market demand for AI-assisted
geotechnical report drafting, but their delivery model (bespoke $50k+ builds, generalist
RAG with no domain IP) is inaccessible to Tier 2 firms. Redline's PLG advantage is
zero-friction onboarding versus SupaHuman's enterprise sales process.

## Target Segment

Tier 2 NZ/AU geotechnical consultancies (5-50 person firms). Explicitly not Tier 1
(T+T, WSP, Beca) — those firms build internally. The user is the intermediate engineer
(3-7 years post-graduation) who drafts GBRs and GIRs.

## Scope

### In Scope (Sprint 1 — ship by 2026-06-30)

- **GBR skeleton generation**: given a report type (GBR or GIR), jurisdiction (NZ or AU),
  and basic project parameters (site location, client, scope), produce a structured
  document skeleton with section headings, placeholder content, and standard clause
  references.
- **GIR skeleton generation**: same as GBR, adapted for interpretive report structure.
- **SSO-gated signup**: verified work email required. No anonymous access.
- **Quota cap**: 3-5 documents per verified user, 100 pages per document. Quota is
  non-renewable in free tier.
- **Document output**: downloadable Word document (.docx) with the skeleton structure.
- **Standards grounding**: skeleton references drawn from the Standards Knowledge Store
  (MVP subset — 3-5 NZ documents per [feature-backlog.md](../strategy/feature-backlog.md)
  Feature N).
- **Audit trail**: every AI generation event is logged with timestamp, model, input
  parameters, and output hash. Ships with v1, not as Phase-2. See
  [audit-trail-day1-requirement.md](audit-trail-day1-requirement.md).
- **Document Parser (Feature M)**: infrastructure dependency — parses uploaded client
  scope documents to extract project parameters for skeleton generation.
- **Platform and web surface (Feature P)**: SSO-gated web application. See
  [platform-requirements.md](../../specs/003-platform-website/platform-requirements.md).

### Out of Scope

- Pre-Review annotations or inline comments (Bet 2 / Sprint 2-3).
- Adversarial Scan (Phase-2).
- House Rules configuration (Sprint 5+).
- AU standards in the Knowledge Store MVP (NZ-only first; AU follows).
- Word task pane integration (parked — P-024).
- Mobile client (engineering non-goal).
- Firm-specific knowledge ingestion (Business tier).
- Paid tier or revenue collection — the skeleton is free.

## PLG Funnel Mechanics

The skeleton is a product-led growth (PLG) wedge. The funnel:

1. **Acquisition**: intermediate engineer discovers Redline (founder-led content,
   LinkedIn, word-of-mouth within NZ/AU geotech community).
2. **Activation**: engineer signs up with verified work email, generates first skeleton.
   Time-to-value target: under 60 seconds from signup to first skeleton download.
3. **Quota exhaustion**: after 3-5 documents, the free quota is consumed.
4. **Outbound trigger**: quota exhaustion fires a founder-led outbound email offering
   a paid Pre-Review trial on the skeletons the user already generated.
5. **Conversion**: at least 1 in 5 outbound responders books a paid Pre-Review trial
   (Bet 1 assumption stack).

GTM angle for outbound: "Your AI wrote it. Who checked it? Redline gives you the audit
trail your insurer will ask for."

## Success Definition

Per Bet 1's kill criterion:

| Metric | Target | Kill threshold |
|---|---|---|
| Verified-email signups (90 days) | 50+ | < 50 kills the wedge |
| Outbound response rate (quota-exhausted users) | 5%+ | < 5% kills the wedge |
| 60-day warning signal | 30+ signups by Day 60 | Below 30 triggers course correction |

Product-quality metric (informing iteration, not bet-kill): activation rate
(signup-to-first-skeleton-download).

## Acceptance Criteria (MVP)

1. Given a verified user selects GBR or GIR and provides jurisdiction (NZ) and basic
   project parameters, the system generates a structured skeleton document within
   30 seconds.
2. The skeleton contains section headings consistent with
   [GIR skeleton acceptance criteria](../../research/20260411-gir-skeleton-acceptance-criteria.md)
   and [section placeholders](../../research/20260411-gir-skeleton-section-placeholders.md).
3. The skeleton includes placeholder text that references applicable NZ standards from
   the Standards Knowledge Store.
4. The output is a downloadable .docx file with proper heading hierarchy.
5. Each generation event is logged in the audit trail with timestamp, user ID, model
   version, input parameters, and output document hash.
6. Quota enforcement: after 3-5 documents (configurable), further generation is blocked
   and the user sees a quota-exhaustion message with a CTA for Pre-Review trial.
7. SSO gating: no skeleton generation without a verified work email.
8. The system does not author engineering opinions, recommendations, or interpretive
   content (per [non-goals.md](../strategy/non-goals.md)).

## Constraints

- Switzerland-neutral: the skeleton is structural scaffolding, not engineering content.
- Zero-training perimeter: no customer data is retained for model fine-tuning.
- NZ jurisdiction only in Sprint 1. AU standards follow.
- Audit trail is a Day-1 requirement, not Phase-2 (see
  [audit-trail-day1-requirement.md](audit-trail-day1-requirement.md)).

## Engineering Dependencies

- **Feature M — Document Parser**: required to extract project parameters from uploaded
  scope documents. Scoped inside this PRD, not filed separately.
- **Feature N — Standards Knowledge Store (MVP)**: NZ-only subset (3-5 documents).
  Scoped inside this PRD. Architecture per
  [ADR-005](../../adr/adr-005-standards-knowledge-store-citation-only-internal-architecture.md):
  citation-only, internal, never exposed as a public query interface.

## Open Questions

1. What is the exact quota cap — 3 or 5 documents? Needs founder input on the
   friction/value tradeoff.
2. Should the quota-exhaustion outbound email be automated or manually triggered by
   the founder in the first 90 days?
3. What project parameters are required vs. optional for skeleton generation? Needs
   Graeme's input on minimum viable inputs for a structurally sound GBR skeleton.
4. How does the skeleton handle multi-discipline reports (e.g., combined geotech +
   environmental)? Per non-goals, we refuse environmental — but what happens when a
   user tries?

## Risks

| Risk | Mitigation |
|---|---|
| Skeleton quality too low — engineers don't trust it | Grounded in prior research (acceptance criteria + section placeholders). Iterate based on Day 1-30 feedback. |
| Quota cap too generous — no conversion pressure | Start at 3 documents. Increase only if activation rate is low. |
| SSO gating loses casual users | Acceptable tradeoff — unverified signups have no outbound path. |
| Insurance liability for AI-generated skeleton content | Audit trail ships Day-1. Switzerland-neutral framing: skeleton is structural, not advisory. |

## Next Step

Sprint 2 PRD for D (Inline Annotation Engine) + G (Justification Email Generator) is
drafted in parallel, per the [feature-backlog.md](../strategy/feature-backlog.md) handoff.
