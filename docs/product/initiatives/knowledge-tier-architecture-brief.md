# Initiative: Firm-Specific Knowledge Tier — Architecture Brief

**Status**: Draft v1. **Owner**: Mark. **Date**: 2026-04-20.
**Strategic bet**: [Bet 3 — Standards Knowledge Store Is the Real Moat](../strategy/strategic-bets.md)
**Tier**: Business or higher. Not available in Free or Pro.

## What This Is

A one-page brief describing how firm-specific knowledge ingestion personalises Redline's
output and creates defensible switching costs. This is not a full PRD — it is an
architectural concept to inform Sprint 5+ planning and pricing decisions.

## What Data Goes In

A firm's document controller or technical lead uploads:

| Data type | Examples |
|---|---|
| **Historical reports** | Past GBRs, GIRs, factual reports — the firm's "how we write" corpus |
| **Templates** | Firm-standard document templates with preferred heading structures, boilerplate, and clause language |
| **House style guide** | Naming conventions, abbreviation preferences, preferred phrasing for common clauses |
| **Institutional conventions** | Firm-specific approaches to risk language, limitation-of-liability phrasing, standard disclaimers |

This data is processed into a firm-specific knowledge layer that sits alongside the
universal Standards Knowledge Store. The firm's data is isolated — never shared across
firms, never used for model training (per [non-goals.md](../strategy/non-goals.md):
zero-training perimeter).

## How It Personalises Output

Without firm knowledge, Redline's quality checks are generic: "Does this GBR section
address groundwater per NZGS Module 2?" With firm knowledge, the checks become specific:
"Does this GBR section address groundwater using the firm's preferred baseline statement
format, and does it include the standard disclaimer your firm uses for sites with
perched water tables?"

The personalisation applies to:

- **Skeleton generation**: skeletons reflect the firm's template structure and preferred
  section ordering, not a generic standard.
- **Pre-Review comments**: the Checker agent references the firm's house style when
  flagging issues, not just the jurisdictional standards.
- **House Rules engine** (Feature K, Sprint 5+): firm-configurable QA rules that the
  Checker enforces automatically.

The competitive contrast is sharp. SupaHuman's Archie has no domain IP — the same RAG
architecture that drafts geotech reports also drafts travel RFPs. Redline's firm-specific
knowledge layer means the system gets better the more the firm uses it, creating a
compounding advantage that a generalist RAG agency cannot replicate.

## Why Value Compounds

Once a firm has uploaded its historical reports, templates, and house style, the system's
understanding of their conventions deepens with every report generated through Redline.
After 12 months of use, the knowledge layer reflects not just the firm's static templates
but their evolving practice patterns.

Firms stay because Redline gets better the longer they use it --- not because their data
is trapped. The value is compounding: each new report reinforces the system's grasp of
the firm's conventions, and the cost of re-teaching a new system grows organically over
time. This is retention through accumulated value, not lock-in through dependency.

## The "Standardise" Question

Can a firm's document controller do the initial setup in a week without calling Redline?

This is a critical design question. If setup requires Redline professional services,
the product is not self-serve and the PLG funnel breaks at the Business tier. If setup
is fully self-serve, the onboarding friction is lower but the quality of the initial
knowledge layer may be poor (garbage in, garbage out).

Recommended approach: self-serve upload with guided onboarding. The system ingests
uploaded documents, extracts patterns, and presents a summary back to the document
controller for validation. "We found these 12 conventions in your historical reports.
Are these correct?" The document controller confirms, corrects, or supplements. Target:
a competent document controller completes initial setup in 2-3 days, not weeks.

## Pricing Considerations

Two models under evaluation:

| Model | Pros | Cons |
|---|---|---|
| **One-time setup fee + subscription** | Captures the value of initial knowledge ingestion. Reduces churn (sunk cost). Signals premium positioning. | Higher friction at point of sale. May deter smaller Tier 2 firms. |
| **Pure subscription (knowledge ingestion included)** | Lower friction. Aligns with PLG motion. Easier to trial. | Firms that churn after ingestion capture value without paying for it. Higher subscription price required to amortise ingestion cost. |

Pricing decision deferred to Sprint 5+ planning. The competitive intelligence suggests
that SupaHuman charges $50k+ for bespoke builds — Redline's setup fee for knowledge
ingestion should be a fraction of that to maintain the PLG advantage while still
capturing the ingestion value.

## Open Questions

1. What is the minimum corpus size for useful personalisation? Can a firm with 5
   historical reports get meaningful value, or does it require 50?
2. How does the system handle conflicting conventions across a firm's historical reports
   (e.g., two different disclaimer formats used in different years)?
3. What is the data retention and deletion policy when a firm churns? The zero-training
   perimeter means we don't retain data for model improvement, but do we retain the
   processed knowledge layer for potential re-activation?
4. Can the knowledge ingestion pipeline be reused for the Standards Knowledge Store
   maintenance workflow, or are they architecturally separate?

## Risks

| Risk | Mitigation |
|---|---|
| Firms reluctant to upload proprietary reports | Zero-training perimeter, data isolation, and clear contractual terms. Position as "your data stays yours — we never train on it." |
| Poor-quality uploads degrade output quality | Guided onboarding with validation step. System flags low-confidence extractions for human review. |
| Setup effort deters adoption | Target 2-3 day self-serve setup. If this is not achievable, the feature is not ready to ship. |
| Knowledge layer becomes stale as firm practices evolve | Continuous learning from new reports generated through Redline (without model training — pattern extraction only). Annual refresh prompt to document controller. |

## References

- [strategic-bets.md](../strategy/strategic-bets.md) — Bet 3 (Standards Knowledge Store is the moat)
- [feature-backlog.md](../strategy/feature-backlog.md) — Feature K (House Rules Authoring Console), Sprint 5+
- [non-goals.md](../strategy/non-goals.md) — zero-training perimeter, no data retention for fine-tuning
- [positioning.md](../strategy/positioning.md) — Switzerland-neutral, infrastructure not SaaS
- Archie competitive intelligence (2026-04-20) — SupaHuman has no domain IP
