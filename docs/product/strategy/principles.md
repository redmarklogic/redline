# Product Principles — Redline

**Status**: Committed. **Owner**: Ron.
**Last updated**: 2026-05-04.

> These are settled principles — beliefs firm enough to constrain decisions without
> further debate. Items that are still debatable live in `pricing-methodology.md` as
> hypotheses, not here.

## Principles

### 1. Teach for free, check for pay

The Skeleton Generator teaches the engineer what a well-structured GBR/GIR looks like.
That teaching is free. Pre-Review checks the engineer's own draft against standards and
firm rules. That checking is paid. The free tier educates; the paid tier enforces.

### 2. Gate on depth, not visibility

Do not hide product tiers behind a paywall of ignorance. Every user sees what Redline
can do. The gate is how deep and how much they can use it (quota, document count,
rule library scope), not whether they know it exists.

### 3. Within each product tier, gate by consumption (quota), not by hiding features

The Skeleton Generator is the freemium product — capped by document count and page
limit. Pre-Review is a fully paid product — there is no free Pre-Review tier.
Within each tier, users have access to all features of that tier. The gate is
consumption volume (how many documents, how many reviews), not feature visibility.
Users do not get access to all tools across all tiers — each tier is a distinct product
surface with its own access boundary.

### 4. Dual purchase path

Two distinct buying motions exist and the architecture must support both from Day 1:
(a) an individual engineer buys a personal Pro seat with a credit card, and
(b) a firm Principal approves a Business-tier subscription for the team. These are
not sequential stages of adoption — they are parallel purchase paths that may coexist
within the same firm. A solo consultant and a 30-person firm's team lead have
different budget authority, different procurement friction, and different value
propositions. The product, pricing, and onboarding must accommodate both without
forcing one path to subsidise the other.

### 5. Redline does not author engineering opinions

Redline surfaces gaps, flags deviations, and cites standards. It does not write
recommendations, set design parameters, choose baselines, or express engineering
judgement. Crossing this line forfeits Switzerland-neutrality, exposes Redline to
professional liability, and triggers the political resistance that kills bottoms-up
adoption inside firms. See `non-goals.md` #1.

### 6. The senior reviewer is always right

When Redline flags an issue and the senior reviewer disagrees, the senior reviewer's
judgement prevails. Redline does not adjudicate disputes between author and reviewer.
The tool is subordinate to the human. This is the trust contract that makes the tool
installable inside firms with strong internal review cultures. See `non-goals.md` #3.

## Items Explicitly NOT Principles Yet

The following are active hypotheses being tested through KR2 discovery. They may
become principles after WTP data is collected, or they may be discarded.

- **Per-firm Business tier, not per-seat.** Plausible but unvalidated. Per-seat may
  be the right model for Small firms. Test via KR2 pricing questions.
- **Infrastructure pricing, not SaaS pricing.** Aspirational framing, but the buyer
  may not perceive the distinction. Test via KR2 Van Westendorp and anchoring
  questions.

## Provenance

Principles 1–3 synthesised from founder direction (2026-05-04 session). Principles
5–6 codified from `non-goals.md` and `positioning.md` (established 2026-04-18).
Principle 4 (Dual purchase path) committed as architectural principle by founder
direction (2026-05-04). Demoted items moved to `pricing-methodology.md` as hypotheses.
