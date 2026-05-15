# Marketing Instrumentation Input — PostHog Event Taxonomy & Dashboards

**Status**: Input for Mark's discovery phase (June 2-14).
**Owner**: John (marketing perspective). Ron owns the measurement spec at
`docs/product/strategy/instrumentation.md`; this document supplements it with the
marketing-specific layer.
**Date**: 2026-04-19.
**Anchored to**: Strategic Bet 1 (kill criterion), `gtm/2026-launch-plan.md` funnel,
`pricing-methodology.md` (WTP interview instrumentation).

> This is John's marketing input, not a replacement for Ron's spec. Ron defines *what*
> we observe and *why* at the product level. This document adds: content attribution,
> firm-level segmentation, dashboard specifications, UTM conventions, and the
> kill-criterion tracking layer a solo founder can implement in a few hours.

---

## 1. Event Taxonomy

### 1A. Website / Landing Page Events (PostHog)

These fire on the public marketing surface — the landing page, pricing page, and any
content pages. They answer: "who is coming, from where, and what do they do before
signing up?"

| Event Name | Trigger | Properties | Priority |
|---|---|---|---|
| `page_viewed` | Any page load (PostHog autocapture handles this, but name it explicitly for dashboards) | `path`, `referrer`, `utm_source`, `utm_medium`, `utm_campaign`, `utm_content` | Must |
| `cta_clicked` | User clicks any call-to-action button (e.g. "Try the Skeleton Generator", "See Pricing") | `cta_id`, `cta_text`, `page_path` | Must |
| `pricing_page_viewed` | Pricing page loads (Ron's spec includes this) | `referrer`, `utm_source`, `utm_campaign` | Must |
| `business_waitlist_submitted` | Fake-door Business waitlist form completes (Ron's spec includes this) | `email_domain`, `utm_source`, `utm_campaign` | Must |
| `trust_doc_downloaded` | User downloads the Principal-facing trust document | `referrer`, `page_path` | Should |
| `faq_expanded` | User expands an FAQ accordion item | `question_text` | Could |
| `scroll_depth_reached` | User scrolls past 25%, 50%, 75%, 100% of the landing page | `depth_percent`, `page_path` | Could |

**Note on `page_viewed`:** PostHog's autocapture tracks pageviews automatically. The
explicit event lets us attach UTM properties cleanly for attribution dashboards. If
autocapture is sufficient, skip the custom event and use PostHog's built-in `$pageview`
with UTM properties parsed from the URL.

### 1B. Tool Usage Events (PostHog)

These fire inside the Skeleton Generator tool. They answer: "once someone signs up, do
they actually use the tool, and do they come back?"

Ron's spec already defines these. I am reproducing them here with the marketing-relevant
properties added, not changing the event names.

| Event Name | Trigger | Properties | Priority |
|---|---|---|---|
| `signup_started` | User clicks Generate and is shown SSO prompt | `referrer`, `utm_source`, `utm_campaign`, `utm_content` | Must |
| `signup_completed` | SSO returns; work email captured | `email_domain`, `signup_method` (google/microsoft), `utm_source`, `utm_campaign`, `utm_content` | Must |
| `document_uploaded` | File reaches the parser | `file_type`, `page_count_bucket` (1-10, 11-50, 51-100) | Must |
| `generation_started` | Parser successfully chunks the doc | `document_id` (hashed) | Must |
| `generation_completed` | Skeleton produced and rendered | `document_id`, `generation_time_seconds` | Must |
| `download_completed` | User downloads the generated artifact | `document_id`, `format` (docx/pdf) | Must |
| `quota_consumed` | Each successful generation against the cap | `current_count`, `quota_limit` | Must |
| `quota_exhausted` | User hits the cap | `email_domain`, `days_since_signup` | Must |
| `return_visit` | Authenticated user returns 24+ hours later | `days_since_last_visit`, `total_visits` | Must |
| `outbound_sent` | Founder sends outbound email to a quota-exhausted user | `days_since_exhaustion`, `email_domain` | Must |
| `outbound_responded` | Quota-exhausted user replies to outbound email | `days_since_outbound`, `email_domain` | Must |

**Properties I added to Ron's event list** (marketing-relevant, not in the original spec):

- `utm_source`, `utm_campaign`, `utm_content` on signup events — so we can attribute
  signups to the LinkedIn post or outbound email that drove them.
- `email_domain` on signup and quota events — feeds Group Analytics (Section 3).
- `days_since_signup` / `days_since_exhaustion` — time-to-event metrics for funnel
  velocity analysis.
- `page_count_bucket` on upload — tells us what size documents users actually bring,
  which informs the quota cap tuning.
- `signup_method` — tells us whether Google or Microsoft SSO dominates, which matters
  for the firm IT security question in Bet 4.

### 1C. Events NOT to Track

Per Ron's spec and the privacy posture:

- No keystroke or mouse-movement tracking.
- No content of uploaded documents (zero-training perimeter).
- No session replay of document content (if session replay is enabled, mask the
  document content area).
- No LinkedIn Insight Tag, Meta Pixel, or Google Ads remarketing pixel. Ever.

---

## 2. Firm-Level Analytics (PostHog Group Analytics)

PostHog Group Analytics lets us track metrics at the "firm" level, not just the
individual user level. Since SSO captures work email domains, the email domain is our
firm identifier.

### Setup

1. **Define a Group Type** called `firm` in PostHog.
2. **On `signup_completed`**, associate the user with a group using the email domain:
   ```
   // Conceptual — not code, just the PostHog call shape
   posthog.group('firm', emailDomain, {
     name: emailDomain,        // e.g. "tonkintaylor.co.nz"
     first_seen: timestamp,
     country: derivedFromDomain // "NZ" or "AU" — derive from TLD or lookup
   })
   ```
3. **Every subsequent event** from that user is automatically attributed to the firm
   group.

### Firm-Level Metrics to Track

| Metric | How to compute | Why it matters |
|---|---|---|
| Users per firm | Count of distinct users in a `firm` group | Bottoms-up adoption signal (Bet 4). A firm with 3+ users is a Business-tier candidate. |
| Generations per firm | Sum of `generation_completed` per firm | Usage intensity. High-generation firms are warm leads for outbound. |
| Quota exhaustion rate per firm | Count of `quota_exhausted` / count of users in firm | Firms where multiple users exhaust quota = strongest upgrade signal. |
| Time to first generation per firm | Min of (`generation_completed.timestamp` - `signup_completed.timestamp`) per firm | Activation speed. Slow firms may need onboarding help. |
| Firm country | Derived from email domain TLD (.co.nz, .com.au) or manual enrichment | NZ vs AU segmentation for KR reporting. |

### Firm Properties to Set

| Property | Source | Purpose |
|---|---|---|
| `domain` | Email domain from SSO | Primary firm identifier |
| `country` | TLD heuristic (.co.nz = NZ, .com.au = AU) or founder manual tag | Geo segmentation |
| `firm_size_estimate` | Founder manually tags after LinkedIn cross-reference | Segment into solo/small/medium (per pricing methodology) |
| `first_signup_date` | Timestamp of first user signup in the firm | Cohort analysis at firm level |
| `is_target_firm` | Boolean, founder-tagged | Prioritise outbound and dashboard filtering |

**Implementation note for the founder:** Group Analytics is a PostHog paid feature on
their Cloud plan (free up to 1M events/month, but Groups requires the Teams add-on or
self-hosted). Confirm the plan tier covers this. If not, the fallback is to track
`email_domain` as a user property and filter/group in PostHog dashboards manually —
less elegant but functional for H2 volume.

---

## 3. Kill Criterion Tracking

**Bet 1 kill criterion (from `strategic-bets.md`):**

> After 90 days from launch (2026-09-01), fewer than 50 verified-email signups OR
> fewer than 5% of quota-exhausted users respond to outbound. Either kills the wedge.

### Events That Feed the Kill Criterion

| Kill leg | Numerator event | Denominator | Target |
|---|---|---|---|
| Leg 1: Signups | `signup_completed` (cumulative count) | Calendar time (90 days from June 2) | ≥ 50 by Sep 1 |
| Leg 2: Outbound response rate | `outbound_responded` | `outbound_sent` | ≥ 5% |

### PostHog Dashboard: "Bet 1 Kill Criterion Tracker"

Build one dashboard with these panels:

1. **Cumulative Signups (line chart)**
   - Insight type: Trends
   - Event: `signup_completed`, cumulative count
   - Time range: June 2 - Sep 1
   - Add a horizontal reference line at 50 (the kill threshold)
   - Add a diagonal "pace line" showing the required 0.56 signups/day to hit 50 by
     Sep 1 (50 signups / 90 days)
   - Warning signal: if below pace at day 60 (Aug 1), per Ron's OKR spec

2. **Signups by Week (bar chart)**
   - Insight type: Trends
   - Event: `signup_completed`, weekly count
   - Shows acceleration or deceleration

3. **Outbound Response Rate (number)**
   - Insight type: Trends → Formula
   - Formula: `outbound_responded` / `outbound_sent` * 100
   - Display as a single number with a threshold indicator at 5%

4. **Funnel: Visit → Signup → Generation → Download → Quota Exhaustion**
   - Insight type: Funnel
   - Steps: `page_viewed` (landing) → `signup_started` → `signup_completed` →
     `generation_completed` → `download_completed` → `quota_exhausted`
   - Conversion window: 7 days
   - Shows where the funnel leaks

5. **Days to Quota Exhaustion (histogram)**
   - Insight type: Trends
   - Event: `quota_exhausted`, property `days_since_signup`
   - Shows whether users exhaust quickly (good — high engagement) or slowly
     (may indicate low perceived value)

### Kill Criterion Review Cadence

The founder reviews this dashboard every Monday morning during the LinkedIn-batch
session (per Ron's cohort review cadence). The two signals to watch:

- **Day 60 (Aug 1) warning**: If cumulative signups < 33 (two-thirds of 50), the
  founder should escalate to Ron. Recovery options include switching to paid
  acquisition (parked decision P-016/P-021) or revisiting the free wedge value
  proposition.
- **Day 90 (Sep 1) kill**: If signups < 50 OR outbound response < 5%, Bet 1 is dead.
  Ron decides next move.

---

## 4. Dashboards to Build (PostHog)

A solo founder needs at most 4–5 dashboards. More than that and nobody looks at them.

### Dashboard 1: "Weekly Pulse" (the Monday morning dashboard)

The founder opens this every Monday. Five minutes, in and out.

| Panel | Insight type | What it shows |
|---|---|---|
| Signups this week | Trends (number) | `signup_completed` count, last 7 days |
| Cumulative signups | Trends (line, cumulative) | Running total vs. pace line to 50 |
| Generations this week | Trends (number) | `generation_completed` count, last 7 days |
| Quota exhaustions this week | Trends (number) | `quota_exhausted` count, last 7 days |
| Outbound pipeline | Trends (number) | `outbound_sent` - `outbound_responded` (outstanding) |
| Return visitors | Trends (number) | `return_visit` count, last 7 days |

### Dashboard 2: "Acquisition Funnel"

| Panel | Insight type | What it shows |
|---|---|---|
| Full funnel | Funnel | `page_viewed` → `signup_started` → `signup_completed` → `generation_completed` → `download_completed` → `quota_exhausted` |
| Signup conversion by source | Funnel, breakdown by `utm_source` | Which channel converts best |
| Time to first generation | Distribution | Seconds between `signup_completed` and first `generation_completed` |
| SSO method split | Trends, breakdown by `signup_method` | Google vs Microsoft SSO adoption |

### Dashboard 3: "Content Attribution"

| Panel | Insight type | What it shows |
|---|---|---|
| Signups by UTM source | Trends, breakdown by `utm_source` | LinkedIn vs direct vs forum vs outbound-email |
| Signups by UTM campaign | Trends, breakdown by `utm_campaign` | Which LinkedIn post or campaign drove signups |
| Landing page views by source | Trends, breakdown by `utm_source` | Traffic volume per channel |
| Conversion rate by source | Formula | `signup_completed` / `page_viewed`, grouped by `utm_source` |

### Dashboard 4: "Firm Adoption" (requires Group Analytics)

| Panel | Insight type | What it shows |
|---|---|---|
| Active firms this week | Trends (number) | Distinct `firm` groups with any event, last 7 days |
| Top firms by usage | Table | Firm groups ranked by `generation_completed` count |
| Multi-user firms | Table | Firms with 2+ distinct users (Business-tier candidates) |
| Firm geography | Trends, breakdown by `country` | NZ vs AU adoption |

### Dashboard 5: "Bet 1 Kill Criterion Tracker"

Described in Section 3 above. This is the dashboard Ron and the founder review at
day-60 and day-90 checkpoints.

---

## 5. UTM and Content Attribution Strategy

### UTM Parameter Convention

Every link the founder shares externally gets tagged. No exceptions. Use these
conventions:

| Parameter | Convention | Examples |
|---|---|---|
| `utm_source` | The platform where the link is posted | `linkedin`, `email`, `nzgs-forum`, `ags-forum`, `direct` |
| `utm_medium` | The content type | `post`, `comment`, `dm`, `outbound-email`, `referral`, `signature` |
| `utm_campaign` | A short slug identifying the campaign or content piece | `launch-announce`, `big5-pricing`, `skeleton-demo`, `quota-followup` |
| `utm_content` | Optional. Distinguishes variants within the same campaign | `cta-top`, `cta-bottom`, `version-a` |

### Tagging Playbook

**LinkedIn posts:**
Every LinkedIn post includes a link to the Skeleton Generator. Tag it:
```
https://redline.[domain]/skeleton?utm_source=linkedin&utm_medium=post&utm_campaign=<slug>
```
Where `<slug>` is a short descriptor of the post topic (e.g. `gbr-skeleton-demo`,
`pricing-transparency`, `nzgs-gap-analysis`).

**LinkedIn comments (on others' posts — the 10:1 LCS rule):**
When the founder comments on someone else's post and includes a link:
```
https://redline.[domain]/skeleton?utm_source=linkedin&utm_medium=comment&utm_campaign=lcs-outreach
```

**LinkedIn DMs (Dream 100 outreach):**
```
https://redline.[domain]/skeleton?utm_source=linkedin&utm_medium=dm&utm_campaign=dream100-<firm-slug>
```

**Outbound emails (quota-exhaustion follow-up):**
```
https://redline.[domain]/skeleton?utm_source=email&utm_medium=outbound-email&utm_campaign=quota-followup
```

**Email signature:**
The founder's email signature links to Redline. Tag it:
```
https://redline.[domain]?utm_source=email&utm_medium=signature&utm_campaign=founder-sig
```

**Forum posts (NZGS, AGS):**
```
https://redline.[domain]/skeleton?utm_source=nzgs-forum&utm_medium=post&utm_campaign=<topic-slug>
```

### Link Shortening

Do NOT use generic URL shorteners (bit.ly, t.ly) — they look spammy to engineers.
Options:

1. **Best**: Use a custom short domain (e.g. `go.redline.[domain]/skeleton`) with a
   redirect that preserves UTM parameters.
2. **Acceptable**: Post the full URL with UTM parameters. LinkedIn truncates long URLs
   in the display but preserves them in the `href`. Engineers do not care about ugly
   URLs.
3. **Avoid**: bit.ly or similar — signals consumer marketing, not professional tooling.

### First-Touch Attribution

PostHog captures `$referrer` and `$referring_domain` automatically. Combined with UTM
parameters on `signup_completed`, we can answer:

- "What percentage of signups came from LinkedIn?" (filter by `utm_source = linkedin`)
- "Which LinkedIn post drove the most signups?" (breakdown by `utm_campaign`)
- "Did forum posts convert better than LinkedIn?" (compare `utm_source` values)

For H2, **first-touch attribution is sufficient**. The buyer journey is short (one or
two touchpoints before signup). Multi-touch attribution modelling is out of scope and
would be over-engineering at this volume.

### What About Signups With No UTM?

Some users will arrive with no UTM parameters — they typed the URL directly, clicked a
non-tagged link, or came from organic search (if any). PostHog still captures:

- `$referrer` — the referring page URL
- `$referring_domain` — the referring domain (e.g. `linkedin.com`, `google.com`)

These give a reasonable fallback. If `$referring_domain = linkedin.com` but there is no
`utm_source`, the signup is "LinkedIn (untagged)". Track the percentage of untagged
signups — if it exceeds 30%, the tagging discipline is slipping.

---

## 6. Privacy Considerations

### NZ Privacy Act 2020

Redline's primary market is NZ, with AU as secondary. The NZ Privacy Act 2020 governs
collection, use, and disclosure of personal information. Key obligations for analytics:

- **Information Privacy Principle 1 (Purpose of collection)**: Only collect personal
  information for a lawful purpose connected with a function of the agency. Analytics
  for product improvement qualifies. Advertising-network data-sharing does not.
- **IPP 3 (Collection from the individual)**: Inform users what is collected, why, and
  who will see it. A clear privacy policy and analytics disclosure covers this.
- **IPP 5 (Storage and security)**: Protect collected data. PostHog Cloud stores data
  in the US (standard) or EU (on request). Self-hosted is NZ/AU if needed. For H2
  volume, Cloud is fine — but disclose the data location.
- **IPP 12 (Cross-border disclosure)**: If using PostHog Cloud (US-hosted), disclose
  this in the privacy policy. No consent required for cross-border transfer under the
  2020 Act, but disclosure is required.

### Consent and Cookieless Tracking

PostHog supports **cookieless tracking mode**, which uses a session hash instead of
persistent cookies. This means:

- **No cookie consent banner required** if cookieless mode is enabled.
- Users are identified by their SSO login, not by a cookie.
- Session-level analytics (pageviews, clicks) work without cookies.
- Cross-session identification relies on the SSO-authenticated user ID, not a cookie.

**Recommendation**: Enable PostHog in cookieless mode from day one. This eliminates
the cookie consent banner (which engineers hate and which reduces tracking coverage)
and aligns with the "privacy-first" brand positioning. Once a user signs in via SSO,
PostHog can link their pre-auth pageviews to their authenticated identity via the
`posthog.identify()` call — no cookie needed.

### What to Disclose

The privacy policy must state:

1. **What analytics tool** is used (PostHog) and its purpose (product improvement,
   not advertising).
2. **What is collected**: page views, button clicks, feature usage, signup method,
   email domain (not email address in analytics — per Ron's spec, user ID is a hash).
3. **What is NOT collected**: document content, keystrokes, mouse movement (unless
   session replay is enabled, in which case mask the document area).
4. **Where data is stored**: PostHog Cloud (US) or self-hosted (specify).
5. **No third-party advertising trackers**: state this explicitly. It is the single
   most trust-building line in the privacy policy for this audience.

### Session Replay

PostHog offers session replay. If enabled:

- **Mask** the document upload area and generated skeleton content. Engineers must not
  see their documents appear in a vendor's replay tool.
- **Do NOT enable session replay on day one.** It is a "Could" priority. Enable it
  after the first 20 signups to diagnose UX friction, with the document area masked.
- Disclose session replay in the privacy policy if enabled.

---

## 7. Implementation Priority

The founder is a solo technical founder. Everything here is prioritised for "what can
one person wire up in a few hours."

### Must (before launch)

1. PostHog JS SDK on the frontend, cookieless mode enabled.
2. PostHog Python SDK on the backend for server-side events (`generation_completed`,
   `quota_consumed`, `quota_exhausted`, `outbound_sent`, `outbound_responded`).
3. UTM parameter parsing on all entry points — store as user/event properties.
4. `signup_completed` event with `email_domain`, `signup_method`, UTM properties.
5. All events in Ron's "Events to Track" table (Section 1B above).
6. Dashboard 1 ("Weekly Pulse") and Dashboard 5 ("Kill Criterion Tracker").
7. Privacy policy with analytics disclosure.

### Should (first two weeks post-launch)

1. PostHog Group Analytics for `firm` type (if plan tier supports it).
2. Dashboard 2 ("Acquisition Funnel") and Dashboard 3 ("Content Attribution").
3. Dashboard 4 ("Firm Adoption") — requires Group Analytics.
4. `trust_doc_downloaded` event.
5. UTM tagging discipline for all LinkedIn posts (every post, no exceptions).

### Could (after first 20 signups)

1. Session replay (with document masking).
2. `faq_expanded` and `scroll_depth_reached` events.
3. Conversion-rate-by-source analysis.
4. Firm-size enrichment via LinkedIn cross-reference.

---

## 8. What This Does NOT Cover

- **Langfuse / AI observability metrics** — covered separately by the engineering spec.
  Langfuse tracks token consumption, latency, prompt versions, and output quality.
  PostHog tracks the marketing and product funnel. They do not overlap.
- **A/B testing** — out of scope for H2 (per Ron's instrumentation spec).
- **Multi-touch attribution modelling** — over-engineering at H2 volume.
- **In-product surveys** — founder-led conversations are the qualitative channel in H2.
- **Marketing automation** — no drip campaigns, no email sequences. The founder sends
  outbound manually. If this becomes unsustainable, revisit.

---

## Provenance

Grounded in: `docs/product/strategy/instrumentation.md` (Ron's measurement spec),
`docs/product/strategy/strategic-bets.md` (Bet 1 kill criterion),
`docs/product/strategy/gtm/2026-launch-plan.md` (funnel stages and channel plan),
`docs/product/strategy/pricing-methodology.md` (WTP interview cadence),
`specs/003-platform-website/platform-requirements.md` (PostHog + Langfuse confirmation).

No notebook queries were run for this pass — the existing strategy artifacts provided
sufficient grounding. If Mark's discovery interviews surface new funnel stages or user
behaviours, this document should be updated.

**Next step**: Hand to Mark for integration into the platform discovery phase (June
1-14). Mark decides which events are Sprint 1 engineering scope vs. later sprints.
