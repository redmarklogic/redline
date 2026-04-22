# GTM — 2026 H2 Launch Plan

**Status**: Draft v2. **Owner**: Ron. **Period**: Jun 1 → Nov 30, 2026.

**Constraint**: Founder is employed until 2026-05-31. No code, servers, or
product research on employer hardware/networks/paid time before June 1.
Strategy planning, NotebookLM research, and LinkedIn content preparation may
proceed on personal time. All GTM clocks start June 1.

## Motion

Single Product-Led Growth funnel with a Business expansion path. No enterprise
sales motion. NZ + AU only. No paid acquisition spend in H2.

```
Free Skeleton Generator (web upload → SSO-gated download, quota-capped)
        |  signup + quota exhaust
        v
Founder-led outbound (within 24 hours of quota exhaustion)
        |  qualifies into Pre-Review trial
        v
Pro tier (self-serve seat) — Pre-Review mode
        |  bottoms-up adoption inside firm
        v
Business tier (firm subscription) — House Rules + Audit Log
```

**Acquisition mechanic (clarified 2026-04-18):** the user uploads a document on the
web, clicks Generate, and is prompted to sign in via Google or Microsoft SSO at the
document-generation moment. The work email is captured silently from the SSO profile.
The founder reaches out manually based on observed usage. The intake is **not** an
email submission — users do not send anything to a Redline mailbox.
`benton@redlinelogic.com` is the bot/system email, never the user-facing intake.

## Funnel Stages and Owner

| Stage | Mechanism | Owner | Conversion target |
|---|---|---|---|
| Awareness | Founder LinkedIn, NZ/AU domain forums, no paid spend | Founder | N/A |
| Acquisition | Free Skeleton Generator at redline.[domain] | Product | KR1: 50 verified-email signups in 60 days |
| Activation | First skeleton generated within 5 minutes of signup | Product | ≥ 80% of signups generate ≥ 1 skeleton |
| Quota event | User exhausts 3–5 doc quota | Product → CRM trigger | Founder-led outbound within 24h |
| Discovery | Founder-led 30-minute call | Founder | KR2: 15 qualified conversations in 90 days |
| Conversion | Pro trial → paid subscription | Founder + product | KR3: 5 paid OR 2 LOIs in 90 days |
| Retention | Active in second billing cycle | Product | KR4: ≥ 60% second-cycle retention |
| Expansion | Pro user requests Business tier for firm | Product (Justification Email Generator) | Tracked, not a KR in H2 |

## Channel Plan

**Channel**: Founder LinkedIn + sparse posting in NZ/AU geotechnical forums (NZGS
chapters, AGS branches), plus referrals from quota-exhausted users.

**The cadence and content rubric for the LinkedIn channel are specified separately in
`content-engine.md`** — Marcus Sheridan's Big 5 framework for content topics, the
10:1 commenting rule, the 4-1-1 mix, and the four-phase Dream 100 outreach mechanic
(LCS warm-up → connection → indirect touch → 4-step DM ask). For Phase-2 buyers
(Principals/Partners) who will not respond to cold DMs, the content-engine playbook
specifies a Carbary *Content-Based Networking* hack: invite them to be interviewed
for a piece of content rather than pitching them.

**Why no paid in H2**: Bet 1 is "free wedge beats paid acquisition". Spending on Google
Ads while the free wedge converts at unknown rate conflates two experiments and
forfeits the falsification value of the bet.

**Channels considered and rejected (or deferred) for H2:**

- **Reddit — rejected as a channel for the ICP.** r/civilengineering and r/geotech
  exist but are dominated by students, US-centric career questions, and memes — not
  practising senior NZ/AU engineers. Reddit is a strong channel for developers,
  hobbyists, and consumer products; it is the wrong audience for senior geotechnical
  practitioners. Logged under `decisions/parked-decisions.md` P-020. May be revisited
  for adjacent personas (e.g. junior engineers in study programmes) at H2 strategy
  refresh, but not for the Day-1 ICP.
- **Google Ads — not committed in H2.** Founder raised re-opening this in 2026-04-18 review.
  Holding to the original commitment for H2 (non-goal #3): Bet 1 must produce a
  falsifiable organic CAC before we add paid as a second variable. If Bet 1 trips its
  kill criterion (KR1 < 50 signups in 60 days), paid acquisition becomes the recovery
  path — see P-016 and the new P-021 entry.
- **Geographic expansion via paid Reddit/Google in AU/UK/CA — not needed.** LinkedIn is
  global; the founder LinkedIn channel reaches AU/UK/CA practitioners at zero marginal
  cost. Adding paid English-speaking-market channels in H2 is premature.

**Product-Led SEO (Schwartz) — not committed in H2**: The Skeleton Generator is
structurally compatible with the Product-Led SEO pattern (a *product*, not blog posts,
as the SEO surface). Not committed in H2 — patience requirement conflicts with KR1's
60-day window, and customer-document privacy bleeds into a zero-publication default.
Logged under `decisions/parked-decisions.md` P-019.

**What we measure on the channel**: LinkedIn-attributed signups (target: ≥ 50% of
KR1) and LinkedIn-sourced KR2 conversations (target: ≥ 50% of KR2). Followers and
impressions are tracked but not targeted — they are vanity metrics in Lean Startup
terms unless they convert.

## Pricing

Pricing is parked. See `pricing-methodology.md`. For H2 launch, Pro tier is positioned
as "founder-priced beta" with explicit price-discovery framing during founder
conversations. No public price list in H2.

**Landing page business model statement (locked 2026-04-19).** The landing page must
explain the business model on day one — withholding it causes professional engineers
with procurement instincts to assume their data is the product. Approved framing:

> "The Skeleton Generator is free. We are building a paid professional tier — pricing
> will be set after we have understood how the market values it."

This addresses the data-harvesting concern, explains the freemium model, and does not
conflate the surface-display choice with the parked pricing decisions (P-002, P-003).
No specific price points until P-002 and P-003 unfreeze.

## Trust and Privacy

**Principal-facing trust document (required before first quota-exhaustion event).**
Intermediate engineers cannot approve Redline for firm-wide use — that requires a
Principal or Partner. The intermediate engineer needs a forwardable one-page document
to escalate upward. Without it, adoption stalls at the firm boundary.

The trust document answers five questions, in this priority order:
1. **Data residency** — which country processes and stores uploaded documents? (NZ
   Privacy Act 2020 IPP 12 and Australian Privacy Act 1988 APP 8 both have cross-border
   transfer requirements that Principals at regulated firms will ask about.)
2. **Zero-training guarantee** — documents are never used to train models. Lead with this.
3. **Deletion timeline** — specific hours, not "in accordance with our policy."
4. **Sub-processor transparency** — name every service that touches customer data.
   Do not say "cloud infrastructure providers."
5. **Infrastructure certifications** — what the named sub-processors hold.

**SOC 2 framing (binding).** Redline does not hold SOC 2 certification. The trust
document must not claim it. The approved framing for sub-processor certifications:

> "Redline processes your documents on [AWS / Vercel / Supabase / OpenAI API]. Each
> of these providers holds an independent SOC 2 Type II certification, with reports
> available on request from those providers. Redline is not yet independently SOC 2
> certified. We are planning independent certification as the business scales."

Before this framing is published, an exhaustive sub-processor audit must be completed
(every service touching customer data, including logging, error tracking, analytics,
email, and CI/CD). See `decisions/parked-decisions.md` P-027. No trust document
publishes before that audit is complete.

## Customer Onboarding

Self-serve for free tier. White-glove for Pro:

- Founder runs 30-minute setup call.
- Customer brings one in-flight GBR section.
- Founder demonstrates Pre-Review on the customer's own document.
- This call **is** the close.

## Risks and Mitigation

| Risk | Mitigation |
|---|---|
| Quota cost exceeds $1/user | KR5 ceiling enforced; rate-limit before KR5 trips |
| Email-verified signup does not equal buying intent | KR2 (qualified conversations) and KR3 (paid) catch this |
| Founder bandwidth caps qualified conversations at 15 | If KR1 over-delivers, batch outbound and prioritise the 15 highest-fit signups |
| Pricing discovery delays paid conversion | Accept; KR3 allows LOIs as substitute for paid revenue |
| Enterprise AI blocking prevents user acquisition at MSP-managed firms | Category positioning ("quality tool", not "AI tool"); risk-score hygiene; email-based fallback channel; IT Justification Brief. See `enterprise-ai-blocking-risk-assessment.md`. *(added 2026-04-22)* |

## Phase-2 GTM (Out of Scope, but Documented)

- Adversarial Scan to Partner-level buyer.
- House Rules authoring console as Business-tier hook.
- Indirect channel partnerships with NZ/AU PM-software vendors.
- Conference presence (NZGS, AGS).

## Provenance

PLG-with-bottoms-up framing is strategy synthesis, informed by standard SaaS expansion
playbooks. Founder-led-outbound mechanic is the founder's hypothesis (Bet 1) — being
tested, not assumed.
