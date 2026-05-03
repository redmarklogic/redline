# Strategy Memo: Enterprise AI Blocking Risk Assessment

**Date**: 2026-04-22. **Author**: Ron (Strategy & GTM Advisor).
**Status**: Active. **Provenance**: See bottom.

---

## Executive Summary

Microsoft Defender for Cloud Apps provides a framework that makes it easy for enterprise
IT teams to discover and block web-based "Generative AI" tools. A large NZ civil
engineering consultancy has already used this framework to propose blocking ~44 of 47
generative AI tools on their network. This creates a new risk vector for Redline's
Product-Led Growth (PLG) go-to-market (GTM): if engineers cannot access
`redline.[domain]` from their work machines, the free Skeleton Generator wedge (Bet 1)
cannot acquire users organically.

**Severity: Tier 2 -- serious but manageable.** Not existential, because our primary
target market (Small firms, 5-50 people) mostly lacks the Microsoft 365 E5
licensing and dedicated IT teams required to deploy Defender for Cloud Apps blocking.
But this risk upgrades from "manageable friction" to "Tier 1 strategic threat" if the
blocking pattern cascades from large consultancies into MSP-managed IT environments
that service mid-market firms — and that cascade is plausible within 12-18 months.

---

## 1. Risk Assessment

### 1.1. What is actually happening

Microsoft Defender for Cloud Apps scores 31,000+ cloud applications on ~90 risk factors
and assigns a 1-10 score (10 = lowest risk). Enterprise IT teams use this catalog to
discover "Shadow IT" on their networks, then tag apps as "Sanctioned" (allowed) or
"Unsanctioned" (blocked). Unsanctioned apps are auto-blocked via Defender for Endpoint
or firewall scripts. Microsoft also maintains a "Generative AI" category that flags any
AI content-generation tool for heightened scrutiny.

The decision to block is made by each organisation's IT team, not by Microsoft. But
the framework creates a strong default toward blocking: if a tool has a low risk score
and nobody complains, it gets blocked.

### 1.2. Why this matters for Redline

Bet 1 (the Free Skeleton Wedge) depends on a single acquisition mechanic: an
intermediate engineer visits `redline.[domain]`, uploads a document, and generates a
skeleton. If their employer's network blocks the domain, the engineer never reaches the
upload page.

The founder's Trojan Horse strategy — as grounded in the Founder Memos — assumes
individual engineers at SME firms will independently try the tool. The memos explicitly
state the target is "mid size and small size" consultancies that "don't have a dedicated
legal team." The founder did not contemplate corporate IT blocking as a barrier, because
the SME firms he targets mostly do not have enterprise IT security infrastructure.

That assumption is correct for most Small firms today. But three things could change it:

1. **Cascade from large to mid-market via MSPs.** Many Small firms outsource IT to
   Managed Service Providers (MSPs). MSPs manage Microsoft 365 tenants at scale and may
   apply Defender for Cloud Apps policies as a default template across all their clients.
   When one MSP blocks "Generative AI" tools, every client inherits the block — including
   20-person geotechnical firms that never asked for it.

2. **Industry narrative contagion.** When large consultancies like the one in this
   assessment adopt "Microsoft recommends blocking AI tools" as an internal policy, that
   narrative leaks into professional networks (NZGS chapters, AGS branches, LinkedIn
   threads). Mid-market firms that do not use Defender may still adopt informal "no AI
   tools" policies in response to the narrative — blocking access at the cultural level
   rather than the network level.

3. **Insurance pressure.** The insurance bifurcation identified in Bet 2 (some insurers
   inserting absolute AI exclusion clauses) could reinforce IT blocking. A firm whose
   Professional Indemnity (PI) insurer excludes AI tools has a financial incentive to
   block all AI-categorised software, regardless of the tool's actual risk profile.

### 1.3. Severity assessment

| Factor | Assessment |
|---|---|
| **Primary target (Small firms, 5-50 people)** | Low exposure today. Most lack M365 E5 + Defender for Cloud Apps. Risk upgrades if MSPs cascade policies. |
| **Secondary audience (large consultancy engineers)** | High exposure. The PDF is direct evidence of blocking at a large consultancy. Engineers at these firms will not reach Redline. |
| **Word-of-mouth channel** | Moderate impact. If early advocates at large firms are blocked, the word-of-mouth flywheel that accelerates beachhead adoption loses one channel — but not the primary channel (LinkedIn + NZ/AU forums). |
| **Narrative contagion** | The most dangerous vector. "Microsoft says block AI tools" becomes an industry talking point that poisons Redline's category before engineers even try it. |
| **Timeline** | 6-18 months for cascade to reach Small MSP-managed firms. Immediate for large consultancies. |

**Overall: Tier 2 risk (serious, needs strategic response, not existential today).**
Escalates to Tier 1 if: (a) a major NZ/AU MSP applies blanket Generative AI blocking
across its client base, OR (b) PI insurers begin requiring firms to demonstrate they
block AI tools as a condition of coverage.

---

## 2. Strategic Recommendations

These recommendations are about positioning, architecture, and messaging — not about
contacting organisations directly.

### 2.1. Win the category label war

This is the single most important action. The Microsoft Cloud App Catalog assigns each
app to a category. If Redline lands in "Generative AI", it will be default-scrutinised
and default-blocked by every enterprise IT team that follows Microsoft's framework.

**Action: Position Redline for the catalog as a "Document Management" or "Productivity"
or "Content Management" tool — not "Generative AI."**

This is not dishonest. Redline does not generate engineering opinions, does not author
report content, does not produce images or media. Redline is a quality-checking layer
that reads documents and surfaces issues. The "Generative AI" label is factually wrong
for what Redline does — we use AI, but the output is annotations and structured
metadata, not generated content.

The Monetizing & Scaling Innovation notebook confirms this principle: "it is truly
impossible to separate pricing from positioning." The Tata Nano example is instructive —
it was a good car killed by the wrong category label ("world's cheapest car"). Redline
must not become a good tool killed by the wrong category label ("Generative AI").

Our existing strategic lexicon already points in the right direction:
- "Infrastructure, not SaaS" (from `positioning.md`)
- "Quality layer" (from `positioning.md`)
- "Switzerland-neutral" (from `positioning.md`)

These framings are not just marketing — they are category-survival language. They need
to extend from our sales messaging into our technical metadata: website meta tags, API
descriptions, privacy policy language, and any submission to app catalogs.

### 2.2. Invest in risk-score hygiene from Day 1

The Microsoft risk score is calculated from ~90 factors across Security, Compliance,
General, and Legal categories. Many of these are achievable at launch without
enterprise-grade investment:

**Day-1 achievable (Sprint 1-2):**
- HTTPS everywhere with proper security headers (TLS 1.2+, HSTS)
- Published privacy policy, terms of service, data retention policy
- Data-at-rest encryption (standard with any cloud provider)
- Clear data ownership statement ("customer owns all uploaded data")
- Published sub-processor list (already committed in the GTM trust document)

**Near-term achievable (H2 2026):**
- Admin audit trail (Feature L core subset is already elevated to Sprint 1)
- User audit trail
- MFA / SSO support (already planned — Google and Microsoft SSO)
- RBAC (Role-Based Access Control) for Business tier
- GDPR-aligned data processing agreement

**Medium-term (2027):**
- SOC 2 Type II certification
- ISO 27001 certification

The goal is not to get a perfect 10 score. It is to get above the blocking threshold
(score 7+) so that IT teams reviewing Redline see a "reasonable" risk profile and move
on, rather than defaulting to block.

### 2.3. Build the "business justification" toolkit

The CoTE conversation reveals the real decision dynamic: "the consensus in the CoTE
meeting was that this should be controlled procedurally and, at the very least, the
consulting business should have the opportunity to object to blocking any tools they use
actively."

This means blocking decisions are negotiable. The consulting business (the engineers)
can push back. But they need ammunition.

**Action: Prepare a one-page "IT Justification Brief" that an intermediate engineer
can forward to their IT team when Redline is flagged for blocking.**

This document should cover:
1. What Redline does (quality checking, not content generation)
2. What data flows where (zero-training guarantee, deletion timeline, sub-processors)
3. Why it is not a "Generative AI" risk (does not generate engineering opinions; output
   is structured annotations, not free-form generated text)
4. What security controls are in place (encryption, audit trail, SSO, data ownership)
5. Business value statement (reduces review rounds, improves report quality)

This toolkit is different from the "Principal-facing trust document" already planned in
the GTM. That document answers "should our firm use this?". The IT Justification Brief
answers "should IT allow this on our network?" — a different audience with different
concerns.

### 2.4. Architectural hedges

Two architectural choices reduce exposure to network-level blocking:

**a) Email-based interface as a blocking bypass.**
The founder's original "Burton" concept — interacting with Redline via email — is
accidentally a brilliant anti-blocking mechanism. Email is never blocked by Defender
for Cloud Apps. If a user emails a document to `burton@redline.[domain]` and receives
annotated results back, no web traffic is generated to a domain that could be blocked.
This does not mean we should abandon the web interface. But maintaining the email
channel as a parallel intake path provides a fallback that bypasses network-level
blocking entirely.

**b) API-first architecture.**
If Redline operates as an API that third-party tools call (e.g., a Word add-in, a
Teams integration, or a CI/CD pipeline), the traffic pattern looks different from
"user visits an AI website." Defender for Cloud Apps discovers apps via HTTP traffic
logs — API calls from sanctioned tools (Microsoft Word, Microsoft Teams) are less
likely to be flagged as Shadow IT.

Neither of these is a Sprint 1 action. But the architecture should not close the door
on them.

### 2.5. The "10 angry users" strategy

The exceptions in the PDF reveal the real blocking-override mechanism: user advocacy.
BeyondWords survived with 250 users. Scite survived with 30. The Enterprise Architect
did not block these because people would fight back.

**Implication for Bet 1:** The free wedge is not just an acquisition mechanic — it is a
blocking-resistance mechanic. Every user who generates a skeleton and finds it useful
becomes one more person who will object when IT proposes blocking the tool. The quota
is designed to create dependency before the outbound conversation. That same dependency
creates advocacy when IT threatens to block.

This means the Trojan Horse strategy is more important, not less. The blocking risk
does not invalidate the wedge — it makes the wedge's speed matter more. We need to
acquire users and build dependency faster than IT can discover and block the tool.

---

## 3. Lessons from the Exceptions

Three apps survived blocking in the PDF. Each teaches something:

### BeyondWords (not blocked, score 5, 250 users)

- **Lesson:** User count is the strongest protection. 250 users made the Enterprise
  Architect pause ("need to understand why so many users"). IT does not block tools
  that will generate 250 complaints.
- **Application:** Bet 1's quota-capped free tier should be designed for maximum user
  count, not maximum per-user depth. More users at shallow usage beats fewer users at
  deep usage — for blocking resistance, not just for conversion.

### Scite (not blocked, score 5, 30 users)

- **Lesson:** A tool perceived as "scientific verification" rather than "AI content
  generation" survives. The note says "valid use?" — the IT team recognised the tool
  serves a legitimate professional function.
- **Application:** Redline's "quality layer" positioning maps directly to this pattern.
  We check reports; we do not generate them. If an IT admin asks "what does this tool
  do?", the answer must be "it verifies engineering reports against standards" — not
  "it uses AI to help write reports."

### Quizlet (not blocked, score 7, 4 users)

- **Lesson:** Being perceived as "not really a Generative AI tool" is the ultimate
  protection. The note says: "Not really a Generative AI tool. Legitimate uses for
  learning and development, don't block."
- **Application:** If Redline can achieve the perception of "this is an engineering
  quality tool that happens to use AI under the hood" — the same way Quizlet is "a
  learning platform that happens to have some AI features" — it exits the danger zone
  entirely. The AI is an implementation detail, not the product category.

### Synthesised principle

**The blocking-survival formula: Business Utility + Non-AI Primary Identity +
User Advocacy = Unblockable.**

Any two of three is probably sufficient. All three is the target state.

---

## 4. Impact on Existing Strategy Artifacts

### 4.1. Strategic Bets

**Bet 1 (Free Skeleton Wedge):** Add a new assumption to the assumption stack: "Target
engineers can access `redline.[domain]` from their work machines." Add a new risk item:
"Network-level AI blocking at MSP-managed firms could prevent user acquisition." The
kill criterion does not change — if engineers cannot access the site, KR1 (50 signups
in 60 days) will fail on its own, and the bet dies.

**Bet 2 (Pre-Review as Paid Product):** The existing assumption "Firm IT will permit the
integration without a 6-month security review" is now more fragile. The Defender for
Cloud Apps framework is exactly the kind of automated security review that could block
Pre-Review before anyone even requests a trial. The IT Justification Brief (2.3 above)
directly mitigates this.

**Bet 4 (Switzerland-Neutral Positioning):** This bet is strengthened, not weakened. The
blocking risk validates that positioning matters at the infrastructure level, not just
the sales conversation level. "Infrastructure, not SaaS" and "quality layer, not AI
tool" are no longer just messaging — they are blocking-survival language. Bet 4's
assumption stack should add: "The Switzerland-neutral positioning must survive not just
the buying committee but also the IT committee."

**Bet 6 (Christensen Disruption):** The blocking risk adds a new dimension to the
"nonconsumption" framing. IT teams are not blocking Redline because they think it is bad
— they are blocking it because they cannot distinguish it from ChatGPT. This is a
categorisation failure, not a product failure. Bet 6's watch item on Beca/Frankly.AI
is informative: Beca's internal AI was never blocked because it was sanctioned
internally. Redline, as an external tool, faces the same scrutiny that Frankly.AI
would have faced if it had been sold to other firms.

### 4.2. GTM Plan

**Add a "Blocking Risk" row to the Risks and Mitigation table:**

| Risk | Mitigation |
|---|---|
| Enterprise AI blocking prevents user acquisition at MSP-managed firms | Category positioning ("quality tool", not "AI tool"); risk-score hygiene; email-based fallback channel; IT Justification Brief |

**Add a note to the Trust and Privacy section:** The Principal-facing trust document
should be complemented by an IT-facing justification brief. Different audience,
different concerns, different document.

### 4.3. Positioning

**Add a "Category Defence" section to `positioning.md`** that makes explicit: Redline
must never self-identify as a "Generative AI" tool in any technical metadata, app-store
listing, API description, or catalog submission. The lexicon already forbids "AI
engineer", "AI reviewer", and "autonomous". It should also forbid "Generative AI" as
a product category label.

### 4.4. Non-Goals

No change needed. The existing non-goals are consistent with this risk assessment.

---

## 5. Trojan Horse Strategy: Validated with a Caveat

The Trojan Horse strategy is validated by this analysis, with one important caveat.

**Validated:** The exceptions in the PDF confirm that widely-used tools with clear
business utility survive blocking. The free wedge is designed to create exactly this
dynamic — build user dependency before the firm's IT team or management notices. The
CoTE conversation confirms that the consulting business can object to blocking tools
they actively use. Users who depend on Redline will push back.

**Caveat:** The Trojan Horse has a race condition. Defender for Cloud Apps discovers
Shadow IT via traffic log analysis. If IT discovers Redline before enough users depend
on it, it gets blocked before the advocacy base exists. The "10 angry users" threshold
(borrowing from BeyondWords and Scite) must be reached before IT's next quarterly
Shadow IT review.

For Small firms without Defender, this race condition does not exist — and those
firms are our primary target. For large consultancies and MSP-managed mid-market firms,
the race condition is real.

**Strategic implication:** The free tier should optimise for rapid user acquisition
breadth (many firms, one or two users each) rather than depth (a few firms, many users
each). Breadth means more firms reach the "angry users" threshold independently.

---

## 6. What I Am Not Recommending

- I am not recommending we contact IT departments at target firms. That breaks the
  bottoms-up PLG motion and signals to IT that we are a tool worth scrutinising.
- I am not recommending SOC 2 certification in H2. It is expensive and premature. We
  should invest in the low-cost risk-score factors (policies, encryption, audit trails)
  that move the needle on the Microsoft score without the certification overhead.
- I am not recommending we abandon the web interface for email-only. The web interface
  is the PLG funnel. Email is a fallback channel, not the primary channel.
- I am not recommending we hide the fact that Redline uses AI. Concealment would be
  dishonest and would destroy trust if discovered. The recommendation is to position
  accurately: Redline is a quality-checking tool that uses AI internally — it is not a
  "Generative AI" tool that creates content.

---

## 7. Next Steps

| Action | Owner | Priority |
|---|---|---|
| Update Bet 1 assumption stack with network-access assumption | Ron | Now |
| Update Bet 4 assumption stack with IT committee survival | Ron | Now |
| Add "Blocking Risk" row to GTM Risks table | Ron | Now |
| Add "Category Defence" section to positioning.md | Ron | This week |
| Review Redline's planned website meta tags and API descriptions for "Generative AI" language | Mark / Engineering | Before launch |
| Prepare IT Justification Brief template | Mark | Before first quota-exhaustion event |
| Evaluate email-based intake channel as architectural hedge | Mark / Engineering | Sprint 2-3 |
| Monitor MSP AI-blocking policies in NZ/AU market | Ron | Quarterly |

**The next step for Mark:** Frame a problem statement for the IT Justification Brief,
linked to Bet 4 (Switzerland-neutral positioning). The brief is a product artifact, not
a strategy artifact — it needs Mark's problem-framing rigour, not just a marketing
one-pager.

---

## Provenance

- Founder Memos notebook (queried 2026-04-22): confirmed Trojan Horse strategy targets
  SME firms; confirmed founder did not contemplate IT blocking risk; confirmed founder
  plans Microsoft Teams integration.
- Monetizing & Scaling Innovation notebook (queried 2026-04-22): confirmed that product
  category perception is inseparable from pricing and adoption; Tata Nano analogy
  (wrong category label kills a good product); Superhuman analogy (right category
  label enables premium pricing).
- Research document: `docs/research/20260422-enterprise-ai-blocking-risk.md` (technical
  analysis of the Microsoft Defender for Cloud Apps framework and the PDF assessment).
- Existing strategy artifacts: `strategic-bets.md`, `positioning.md`, `vision.md`,
  `non-goals.md`, `gtm/2026-launch-plan.md`.
