# Instrumentation — Measurement Spec for the H2 Wedge

**Status**: Draft v2. **Owner**: Ron (spec); founder + Mark (implementation choice).
**Anchored to**: `okrs/2026-h2.md` KR6 (cohort instrumentation in place by 2026-07-01).

> This is a measurement spec, not an implementation plan. It defines *what* we observe
> and *why*, not *how* it is wired up. Implementation choice is the founder's; tooling
> recommendation is below.

## Why Instrumentation Is a KR

Every other KR (signups, qualified conversations, paid conversion, retention) depends
on cohort-level visibility. Without it in week 4, the funnel becomes a gut call and the
founder's outbound loses its qualitative differentiator (junior vs. senior, NZ vs.
AU, repeat visitor vs. one-off). The cost of fixing this in month 3 is at least one
month of unrecoverable cohort data.

## Events to Track (Minimum Viable Set)

| Event | When fired | Why we need it |
|---|---|---|
| `signup_started` | User clicks Generate and is shown SSO prompt | Top-of-funnel; denominator for SSO-completion rate |
| `signup_completed` | SSO returns; work email captured | KR1 numerator |
| `document_uploaded` | File reaches the parser | Activation step 1 |
| `generation_started` | Parser successfully chunks the doc | Activation step 2 |
| `generation_completed` | Skeleton produced and rendered | Activation step 3 |
| `download_completed` | User downloads the generated artifact | Real activation; "did they actually take the value" |
| `quota_consumed` | Each successful generation against the 3–5 cap | Quota mechanic instrumentation |
| `quota_exhausted` | User hits the cap | Outbound trigger event (24-hour SLA per launch plan) |
| `return_visit` | Authenticated user returns ≥ 24 hours later | Engagement signal; feeds KR3/KR4 leading indicator |
| `pricing_page_view` | Pricing page loads (when shipped) | Demand signal for Pro and waitlist tiers |
| `business_waitlist_submitted` | Fake-door Business waitlist form completes | Leading indicator for Business-tier build |

Do **not** track keystrokes, mouse movement, session replay, or any content of the
uploaded document. The zero-training perimeter (engineering non-goal #1) extends to
analytics.

## User Identification

Each user record carries:

1. **SSO-captured work email** (from Google or Microsoft profile at signup).
2. **Display name** (from SSO profile).
3. **LinkedIn URL** — manually populated by the founder via cross-reference, not
   asked of the user. This is the field that distinguishes junior from senior, NZ
   from AU, target firm from non-target.
4. **Distinct user ID** — hashed from the SSO subject identifier; not the email itself
   (so an analytics export does not double as a contact list).

Cohort grouping is by signup week. The founder reviews the previous week's cohort
every Monday during the 30-minute LinkedIn-batch session.

## Privacy Posture

- **Disclose the analytics surface in the privacy policy** by name and purpose.
- **No third-party advertising trackers, ever.** No Google Analytics + Ads remarketing
  pixel, no Meta Pixel, no LinkedIn Insight Tag in H2.
- **Document deletion timeline**: uploaded source documents are deleted within 24
  hours of generation completion. Generated skeletons are retained for the user's
  account access only and deleted on account deletion. State this on the upload page,
  not buried in the privacy policy.
- **Zero training**: stated explicitly on the upload page in plain language ("we do
  not train on your document"). This is the single most reassuring sentence we own.

## Tooling Recommendation

**PostHog** (cloud or self-hosted) for product analytics. Reasons:

- Privacy-respecting by default (no cross-site tracking, no ad-network integrations).
- Self-hostable if regulated customers ask.
- Funnel + cohort + retention dashboards out of the box; matches KR1–KR4 + KR6 needs
  with no custom dashboarding.
- Free tier covers ≥ 1M events/month — comfortably above H2 volume.

**Plausible** is the runner-up — simpler and cheaper, but funnel/cohort tooling is
weaker. Acceptable if the founder wants minimum complexity and is willing to
reconstruct funnels in a spreadsheet.

**GA4** is rejected. Free in dollar terms but expensive in privacy-policy real estate,
adds Google's ad-network surface even if "advertising features" are off, and creates
ongoing GDPR/Privacy-Act compliance overhead disproportionate to the value.

Tooling decision is the founder's. Whichever choice is made, KR6's "definition of
done" must hold: KR1 reproducible from the analytics surface, founder can answer
"of the last 20 signups, how many are senior NZ/AU engineers" in under 5 minutes.

## Out of Scope for H2

- A/B testing infrastructure.
- Server-side event collection (client-side is sufficient at H2 volume).
- Marketing-attribution modelling beyond first-touch (LinkedIn vs. forum vs. direct).
- In-product surveys (founder-led conversations are the H2 qualitative channel).

## Provenance

Event list synthesised from the launch-plan funnel (`gtm/2026-launch-plan.md`) and
the OKR set (`okrs/2026-h2.md`). Tooling recommendation is Ron's view based on
privacy-respecting B2B analytics norms; no notebook query was run for this pass.
