# Pricing Methodology — Redline

**Status**: Methodology committed. **All pricing decisions: PARKED.**
**Owner**: Ron, with founder + Mark to close.

> All concrete prices, packaging tiers, and discount mechanics in this document are
> **placeholders for methodology illustration only**. They do not commit Redline to any
> price point and are not to be quoted externally. See `decisions/parked-decisions.md`
> for the parked-decision register.

## Methodology — Ramanujam (*Monetizing Innovation*) Adapted

We adopt the Ramanujam framework because it is the only WTP-first methodology that
explicitly prevents the "build first, price later" trap that kills early SaaS pricing
decisions.

### Step 1 — WTP Interviews Before Build-Out (currently running per KR2)

15 qualified discovery conversations in the first 90 days. Each conversation includes
a structured pricing segment:

- **Van Westendorp Price Sensitivity Meter**: four anchor questions
  (too cheap / cheap / expensive / too expensive) per ICP segment.
- **Feature value-mapping**: rank-order Pre-Review, House Rules, Audit Log, Adversarial
  Scan against willingness-to-pay-per-month.
- **Buyer authority**: who in the firm signs the invoice?

### Step 2 — Segmentation

The Ramanujam framework requires segmenting buyers by *willingness*, not by *ability*.
Redline's plausible segments:

| Segment | Hypothesised pain | Hypothesised authority |
|---|---|---|
| Solo / 2-person geotech consultancy | Reviewer bottleneck = the principal | Principal pays directly |
| 5–20 person firm | Junior throughput; Partner review burden | Partner approves; junior champions |
| 20+ person firm | House Rules consistency; audit trail | Practice Lead / Technical Director |

Segment-specific WTP must be measured, not assumed.

### Step 3 — Packaging (Three Tiers, Hypothesised)

Aligned to the architecture decision (one product, two modes, three tiers):

| Tier | Mode | Hypothesised buyer | Pricing model (illustrative only) |
|---|---|---|---|
| Free | Skeleton Generator (capped 3–5 docs × 100 pages) | Acquisition channel, not a buyer | $0 |
| Pro | Skeleton + Pre-Review | Intermediate engineer, self-serve seat | TBD per WTP outputs |
| Business | Pro + House Rules + Audit Log + (Phase-2) Adversarial Scan | Firm subscription, Partner-approved | TBD per WTP outputs |

### Step 4 — Anchoring Strategy

Three rules carried into pricing conversations once methodology unpacks:

1. **Infrastructure pricing, not SaaS pricing.** Anchor against the cost of a senior
   engineer's review hours, not against per-seat productivity tools.
2. **Per-firm Business tier, not per-seat.** Per-seat caps the price ceiling and
   creates seat-counting friction during firm rollout.
3. **No public price list in H1.** Founder-priced beta only. Public list waits for
   WTP outputs (Step 1) and segment validation (Step 2).

### Step 5 — Decision Gate

Pricing decisions unfreeze when:

- ≥ 10 of the 15 KR2 conversations include a completed Van Westendorp module.
- Segment WTP distributions are documented to `docs/research/`.
- Mark has drafted a packaging proposal grounded in those distributions.
- Founder + Mark + Ron sign off on the packaging proposal.

Until that gate trips, no price is published, quoted in collateral, or committed in writing.

## Fake-Door Tier Discipline

The founder proposes a four-tier pricing page with two real tiers and two fake-door
tiers used to measure latent demand without building. This is a legitimate technique
— "painted-door MVP" / fake-door testing — with documented use at Buffer, Dropbox,
and Slack. It is not inherently dishonest **provided the discipline below is followed**.

### Permitted

- A tier presented as **"closed beta"** or **"join the waitlist"** that captures intent
  via a contact form. The user is told, in plain language, that the tier is not yet
  generally available.
- A tier presented as **"Enterprise — contact us"** that routes to an inbound form,
  provided no specific certifications or guarantees are claimed.
- Tracking waitlist signups as a leading indicator for build-decision unfreezing.

### Forbidden

- **No checkout / credit-card capture for a tier we cannot deliver.** A waitlist is a
  contact form, never a Buy button. Charging a card for a phantom tier is fraud, full
  stop.
- **No false certification claims.** "SOC 2", "ISO 27001", "HIPAA-compliant", or any
  similar specific standard cannot appear unless formally attained. Acceptable
  language: "enterprise security review on request", "contact us about compliance
  requirements". See `non-goals.md` GTM #7.
- **No false delivery promises.** "Available Q3" only if Q3 delivery is genuinely
  scoped. Otherwise: "in development, no committed date".

### Recommended Page Composition (Ron's view, 2026-04-18)

**Free + Pro (paid) + Business (waitlist).** Drop Enterprise from the public page in
H1. Reasons:

1. The Enterprise tier contradicts `non-goals.md` GTM #2 (no enterprise sales motion)
   and the Tier 1 anti-target. Inbound from a Tier 1 firm asking about Enterprise is
   exactly the time-sink we committed to avoiding.
2. "Enterprise — contact us" as a virtue signal that we *might* have guarded capability
   risks the inverse: a Principal at a Tier 1 firm contacts us, gets "no SOC 2 yet,
   come back in a year", and that conversation surfaces in their network. In a small
   market, that is a category-position hit.
3. Implication-by-omission is fine; specific claims are not. Showing Free + Pro +
   Business already implies a higher tier exists "on request" without inviting the
   wrong inbound.

The Enterprise-tier-on-pricing-page question is logged under
`decisions/parked-decisions.md` P-022. Founder decides; Ron's recommendation is on
record.

### Measurement Use

Waitlist conversion on the Business tier is a **leading indicator** for when to actually
build the Business-tier surface (House Rules console, Audit Log, Adversarial Scan).
Track: visitors to pricing page, click-through to Business tier, waitlist completions,
and qualitative notes from any inbound that completes the form.

## Parked Decisions (See `decisions/parked-decisions.md`)

- Specific Pro tier price.
- Specific Business tier price floor.
- Annual vs. monthly billing default.
- Free-tier quota numbers (3 vs. 5 docs; 100 pages cap).
- Discounting policy.
- Founder-pricing comp policy for friends-and-family beta.

## Provenance

Methodology adapted from Madhavan Ramanujam's *Monetizing Innovation*. Adoption is
strategy synthesis. Specific tier mapping aligns with the founder's committed
architecture decision (one product / two modes / three tiers, this pass).
