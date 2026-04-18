# GTM — 2026 H1 Launch Plan

**Status**: Draft v2. **Owner**: Ron. **Period**: Jun 1 → Nov 30, 2026.

**Constraint**: Founder is employed until 2026-05-31. No code, servers, or
product research on employer hardware/networks/paid time before June 1.
Strategy planning, NotebookLM research, and LinkedIn content preparation may
proceed on personal time. All GTM clocks start June 1.

## Motion

Single Product-Led Growth funnel with a Business expansion path. No enterprise
sales motion. NZ + AU only. No paid acquisition spend in H1.

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
| Expansion | Pro user requests Business tier for firm | Product (Justification Email Generator) | Tracked, not a KR in H1 |

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

**Why no paid in H1**: Bet 1 is "free wedge beats paid acquisition". Spending on Google
Ads while the free wedge converts at unknown rate conflates two experiments and
forfeits the falsification value of the bet.

**Channels considered and rejected (or deferred) for H1:**

- **Reddit — rejected as a channel for the ICP.** r/civilengineering and r/geotech
  exist but are dominated by students, US-centric career questions, and memes — not
  practising senior NZ/AU engineers. Reddit is a strong channel for developers,
  hobbyists, and consumer products; it is the wrong audience for senior geotechnical
  practitioners. Logged under `decisions/parked-decisions.md` P-020. May be revisited
  for adjacent personas (e.g. junior engineers in study programmes) at H2 strategy
  refresh, but not for the Day-1 ICP.
- **Google Ads — deferred to H2.** Founder raised re-opening this in 2026-04-18 review.
  Holding to the original commitment for H1 (non-goal #3): Bet 1 must produce a
  falsifiable organic CAC before we add paid as a second variable. If Bet 1 trips its
  kill criterion (KR1 < 50 signups in 60 days), paid acquisition becomes the recovery
  path — see P-016 and the new P-021 entry.
- **Geographic expansion via paid Reddit/Google in AU/UK/CA — not needed.** LinkedIn is
  global; the founder LinkedIn channel reaches AU/UK/CA practitioners at zero marginal
  cost. Adding paid English-speaking-market channels in H1 is premature.

**Product-Led SEO (Schwartz) — deferred to H2**: The Skeleton Generator is
structurally compatible with the Product-Led SEO pattern (a *product*, not blog posts,
as the SEO surface). Not committed in H1 — patience requirement conflicts with KR1's
60-day window, and customer-document privacy bleeds into a zero-publication default.
Logged under `decisions/parked-decisions.md` P-019.

**What we measure on the channel**: LinkedIn-attributed signups (target: ≥ 50% of
KR1) and LinkedIn-sourced KR2 conversations (target: ≥ 50% of KR2). Followers and
impressions are tracked but not targeted — they are vanity metrics in Lean Startup
terms unless they convert.

## Pricing

Pricing is parked. See `pricing-methodology.md`. For H1 launch, Pro tier is positioned
as "founder-priced beta" with explicit price-discovery framing during founder
conversations. No public price list in H1.

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
| Email-verified signup ≠ buying intent | KR2 (qualified conversations) and KR3 (paid) catch this |
| Firm IT blocks Word task pane | Sprint 1 ships browser upload as fallback, not Word add-in |
| Founder bandwidth caps qualified conversations at 15 | If KR1 over-delivers, batch outbound and prioritise the 15 highest-fit signups |
| Pricing discovery delays paid conversion | Accept; KR3 allows LOIs as substitute for paid revenue |

## Phase-2 GTM (Out of Scope, but Documented)

- Adversarial Scan to Partner-level buyer.
- House Rules authoring console as Business-tier hook.
- Indirect channel partnerships with NZ/AU PM-software vendors.
- Conference presence (NZGS, AGS).

## Provenance

PLG-with-bottoms-up framing is strategy synthesis, informed by standard SaaS expansion
playbooks. Founder-led-outbound mechanic is the founder's hypothesis (Bet 1) — being
tested, not assumed.
