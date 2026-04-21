# Pre-Mortem Analysis: Sprint 1 — 30-Day Vertical Slice

**Date:** 2026-04-21
**Author:** Ron (Strategy & GTM Advisor)
**Plan analyzed:** Sprint 1 ships 2026-06-30: free SSO-gated GBR/GIR Skeleton Generator, web platform, document parser, Standards Knowledge Store MVP, audit log core subset. Solo founder, AI coding agents, NZ-only, organic-only acquisition.

**Grounding sources consulted:**
- `docs/product/strategy/strategic-bets.md` (Bets 1-4)
- `docs/product/strategy/gtm/2026-launch-plan.md`
- `docs/product/strategy/pricing-methodology.md` (Ramanujam methodology, parked pricing)
- `docs/product/strategy/non-goals.md`
- `docs/product/strategy/discovery-guide.md`
- `docs/research/20260418-founder-memos-strategy-grounding.md`
- `docs/research/20260413-standards-registry-knowledge-architecture-gaps.md`
- `docs/research/20260420-archie-competitive-intelligence-prompt.md`
- `docs/adr/adr-005-standards-knowledge-store-citation-only-internal-architecture.md`
- Monetizing & Scaling Innovation notebook (session b05f4abb): monetisation failure patterns, buying-center dynamics, free-to-paid conversion baselines, network-effect requirements for PLG

---

## Step 1: The Failure Premise

It is October 1, 2026. Sprint 1 shipped on June 30 as planned. The Skeleton Generator is live. SSO works. The audit log records every generation event. The founder posted LinkedIn content three times a week for 90 days straight.

The kill criterion has tripped. Redline has 19 verified-email signups — well below 50. Of the 6 users who exhausted their quota, 0 responded to the founder's outbound email. The Standards Knowledge Store contains 3 documents, but the skeleton output is too generic to be useful without the clause-level granularity that was deprioritised during the build sprint. Two users who downloaded skeletons described them as "basically just headings I could have typed myself." The founder has burned through 4 months of runway building infrastructure that nobody is using. Bet 1 is dead. There is no paying customer, no pipeline, and no validated willingness-to-pay data to inform what to build next.

---

## Step 2: Root Cause Brainstorm

### Internal / Execution Risks

1. **Solo founder builds five production systems in 30 days.** The sprint asks one person (with AI agents) to ship a skeleton generator, a web platform with SSO, a document parser, a standards knowledge store, and an audit log. Each is a standalone engineering project. Even with AI coding agents, integration testing, deployment, and edge-case handling require human judgement that does not parallelise.

2. **Standards Knowledge Store ships at document level, not clause level.** The knowledge architecture research (`20260413-standards-registry-knowledge-architecture-gaps.md`) explicitly states that document-level storage is a Gap 1 failure — "zero granularity." Clause-level chunking for 3-5 NZ standards is a non-trivial content-engineering task that will be deprioritised under build pressure, producing a skeleton output that cites standards but does not inject actionable placeholder content.

3. **No pricing validation before or during the free-tool build.** The pricing methodology document explicitly parks all pricing decisions until 10+ Van Westendorp interviews are complete. This means Sprint 1 ships with no price, no payment infrastructure, and no willingness-to-pay data. Per Ramanujam, this is the canonical setup for a Minivation (giving away core value) or an Undead (building something nobody will pay for). The 90-day conversion target (KR3: 5 paying customers) depends on pricing decisions that cannot be made until KR2 interviews happen — but KR2 interviews require users, who require the product, which requires Sprint 1. The circular dependency means paid conversion is structurally blocked until month 3 at earliest.

4. **Founder attention is split between building and selling.** The GTM plan requires founder-led LinkedIn content, founder-led outbound emails at quota exhaustion, and founder-led 45-minute discovery interviews — all while the founder is also the sole engineer shipping code with AI agents. There is no slack in the system. If the build takes 35 days instead of 30, the entire acquisition timeline slips.

5. **Document parser is an R&D problem, not a defined implementation task.** Parsing uploaded scope documents to extract project parameters (jurisdiction, soil type, project type) requires NLP or structured extraction from unstructured geotechnical documents. This is a research-grade task disguised as a Sprint 1 deliverable.

### External / Market Risks

6. **The total addressable user pool at Tier 2 NZ geotech firms is very small.** New Zealand has approximately 40-60 geotechnical consultancies in the 5-50 person range. At 3-7 year experience, the number of intermediate engineers across all these firms is perhaps 200-400 people nationally. Acquiring 50 verified emails from this pool using only LinkedIn content and word-of-mouth in 60 days requires reaching and converting roughly 12-25% of the entire national ICP — an extraordinarily high market-penetration rate for a brand-new, unknown product with no paid amplification.

7. **The buying-center problem blocks 90-day paid conversion.** Per the Monetizing & Scaling Innovation notebook, B2B SaaS is never adopted by a single individual — it is sold to a "buying center." The Sprint 1 ICP (intermediate engineer, 3-7 years) does not hold budget authority. The Partner or Practice Lead approves spend. Even if an intermediate engineer loves the skeleton, converting to paid Pre-Review requires the Partner to evaluate liability risk, audit-trail sufficiency, and firm policy on AI tools. In NZ professional services, this approval cycle runs 6-8 weeks minimum. The plan assumes a 90-day funnel from first signup to 5 paying customers — which allows roughly 2 weeks for the user to exhaust quota, respond to outbound, book a call, trial Pre-Review, and get Partner sign-off. This timeline does not fit the market's actual buying behaviour.

8. **No network effects to drive viral organic growth.** The Monetizing & Scaling Innovation notebook emphasises that free-tool PLG works best when the product benefits from network effects — the product's value increases as more people use it. A geotechnical skeleton generator is a single-player tool. There is no sharing mechanic, no collaboration feature, no reason for one engineer's usage to drive another's signup. Word-of-mouth will be linear, not exponential. This means the 50-signup target depends entirely on the founder's personal LinkedIn reach and direct outreach, with no product-driven amplification.

9. **Archie validates market demand but also compresses the window.** The competitive intelligence research (`20260420-archie-competitive-intelligence-prompt.md`) confirms Archie is live and shipping AI-generated geotechnical reports in NZ. Redline's PLG positioning (zero-friction onboarding, self-serve) is genuinely differentiated from Archie's bespoke agency model. But Archie's existence means the "first mover" narrative is already taken. If Archie announces a free-tier or self-serve option before September 2026, Redline's wedge advantage evaporates before Bet 1 is evaluated.

### Technical / Operational Risks

10. **SOC 2 "shadow" compliance on Day 1 adds significant infrastructure overhead.** Shadow compliance means building as if SOC 2 were required — audit logging, access controls, encryption at rest and in transit, incident-response documentation — without formal certification. This is the right posture for the insurance-bifurcation context (Bet 1, Archie CI session), but it adds 20-30% engineering overhead to every Sprint 1 deliverable. For a solo founder in a 30-day sprint, this overhead may be the difference between shipping and not shipping.

11. **PostHog + Langfuse + audit log = three observability systems on Day 1.** The plan requires product telemetry (PostHog), LLM observability (Langfuse), and a custom audit log — three distinct instrumentation stacks. Each requires integration, testing, and operational monitoring. This is infrastructure that mature teams take weeks to set up correctly.

12. **SSO with verified work email has non-trivial edge cases.** Google and Microsoft OAuth return different email claim structures, may return personal rather than work emails, and have varying consent-screen requirements. Email verification for "is this a real company?" requires domain-allow/block-list logic or MX-record validation. These are solvable problems, but they consume engineering days that compete with feature work.

13. **Skeleton output quality depends on the Standards Knowledge Store quality.** If the Standards Knowledge Store ships at document-level granularity (risk #2), the skeleton generator cannot inject standards-specific placeholder content. The output degrades to a generic heading structure that any engineer could produce in Word in 10 minutes. The value proposition collapses: "generate a skeleton" becomes "generate a table of contents," which is not worth an SSO signup.

---

## Step 3: Prioritized Risks

1. **Solo-founder scope overload: five production systems in 30 days** (Category: Internal/Execution)
   - Likelihood: **High** — The plan names five distinct deliverables (skeleton generator, web platform with SSO, document parser, standards knowledge store, audit log) plus three observability stacks (PostHog, Langfuse, custom audit log) plus SOC 2 shadow compliance. AI coding agents accelerate implementation but do not eliminate integration, testing, deployment, and edge-case resolution. The founder has no prior production-deployment track record with this stack.
   - Impact: **High** — If Sprint 1 slips past June 30, every downstream KR timeline shifts. The kill criterion at September 1 becomes unreachable because the 90-day clock has not started.

2. **Organic-only acquisition cannot reach 50 signups in 60 days in a pool of 200-400 people** (Category: External/Market)
   - Likelihood: **High** — The NZ intermediate geotechnical engineer population at Tier 2 firms is very small. LinkedIn organic reach for a new account with no established audience in a niche B2B vertical typically converts at 0.5-2% of impressions. With no paid amplification, no product-driven virality, and no network effects, linear word-of-mouth must do all the work. The plan acknowledges "no paid in H2" as a non-goal — but the constraint may be too tight for the market size.
   - Impact: **High** — Missing KR1 is the kill criterion for Bet 1. If the wedge does not attract users, there are no quota-exhausted users to trigger outbound, no discovery interviews, no WTP data, and no path to paid conversion. The entire strategy collapses.

3. **90-day paid conversion (KR3: 5 customers) is structurally blocked by buying-center dynamics and deferred pricing** (Category: External/Market)
   - Likelihood: **High** — Pricing is parked until 10+ Van Westendorp interviews are complete. Payment infrastructure is out of scope. The ICP (intermediate engineer) lacks budget authority; the buyer (Partner) has a 6-8 week approval cycle. Even in the best case — quota exhaustion at Day 14, outbound response at Day 15, discovery call at Day 20, trial at Day 30 — the Partner approval gate consumes all remaining time before September 1. Five paying customers in 90 days requires five independent buying-center approvals to complete in parallel. This is implausible without an existing relationship network.
   - Impact: **High** — KR3 is the revenue proof-point. Missing it does not kill Bet 1 (the kill criterion is signups + outbound response rate), but it kills the path to Bet 2 (Pre-Review as paid product). Without paying customers, the founder cannot validate willingness-to-pay, cannot fund continued development, and cannot demonstrate traction to any future hire or investor.

4. **Standards Knowledge Store ships at document level, making skeleton output undifferentiated** (Category: Internal/Execution)
   - Likelihood: **Medium** — The knowledge architecture gap analysis (`20260413`) explicitly warns that document-level storage is a "Gap 1 failure." Clause-level chunking for 3-5 NZ standards is feasible but time-consuming. Under 30-day build pressure, it will be deprioritised to "document-level citations with a TODO for granular chunking."
   - Impact: **High** — If the skeleton output is just headings with "refer to NZS 3910" rather than actionable placeholder content derived from specific clauses, the free tool delivers no value beyond what an engineer already knows. Activation rate (KR1 sub-metric: 60% weekly cohort activation) collapses. Users generate one skeleton, find it useless, and never return. The quota-exhaustion trigger never fires because users do not care enough to generate 3-5 documents.

5. **Founder attention is irreversibly split between building, selling, and discovering** (Category: Internal/Execution)
   - Likelihood: **High** — The plan requires the founder to simultaneously ship code (Sprint 1), create LinkedIn content (GTM), respond to quota-exhausted users within 24 hours (outbound), and run 45-minute discovery interviews (KR2). These are four full-time jobs. The discovery guide (`discovery-guide.md`) explicitly states "the founder runs the interview — not delegated." There is no delegation path.
   - Impact: **Medium** — The founder will rationally prioritise whichever activity feels most urgent (likely build), starving the others. If build is prioritised, acquisition stalls. If acquisition is prioritised, build quality degrades. The system has no buffer.

---

## Step 4: Reinforcement and Mitigation

### Risk 1: Solo-founder scope overload

- **Action A: Cut the document parser from Sprint 1.** The document parser (parsing uploaded scope docs to extract project parameters) is the least essential deliverable for Bet 1 validation. Replace it with a simple manual-input form: the user selects jurisdiction, report type, and project parameters from dropdowns. This removes an R&D-grade task and converts it to a well-defined UI problem. Scope-document parsing moves to Sprint 2 or later. **Who:** Founder, before June 1. **When:** Now — amend the Sprint 1 scope document immediately.

- **Action B: Define a "shippable minimum" for each deliverable with explicit cut-lines.** For each of the remaining four deliverables, write a one-paragraph "what ships" vs. "what's deferred" definition. Example: Audit log ships timestamp + user ID + input hash + output hash — nothing else. Standards Knowledge Store ships with document-level citations (accepting risk #4 partially) and a concrete Sprint 2 commitment to clause-level granularity. This forces scope discipline before the build begins. **Who:** Founder + Mark. **When:** Before June 1.

### Risk 2: Organic-only acquisition cannot reach 50 signups

- **Action A: Pre-build a warm audience before June 1.** The founder has 5 weeks before the official start date. Strategy and LinkedIn content preparation are permitted on personal time (per `non-goals.md` Engineering #4). Use this window to grow the founder's LinkedIn network from its current size to 200+ connections in the NZ/AU geotechnical community. Post 2-3 "problem-aware" articles per week (not product announcements — per Big 5 methodology). This builds an organic audience that is ready to convert on Day 1 of launch, rather than starting audience-building and product-building simultaneously. **Who:** Founder. **When:** May 1 - May 31.

- **Action B: Identify 10 specific firms and 30 specific intermediate engineers by name before launch.** Do not rely on "LinkedIn will find them." Build a target list of named individuals at named Tier 2 NZ/AU firms. Use NZGS membership directories, LinkedIn Sales Navigator (free trial), and AGS branch lists. If the list cannot reach 100 named individuals, the TAM is too small for Bet 1 as designed, and the kill criterion should be revised downward before launch. **Who:** Founder. **When:** Before June 1.

### Risk 3: 90-day paid conversion is structurally blocked

- **Action A: Separate the kill criterion from the conversion target.** The kill criterion is already correctly defined (50 signups + 5% outbound response rate — not 5 paying customers). But the plan's KR ladder presents KR3 (5 paying customers by Sept 1) with equal weight, creating an implicit expectation that paid conversion will happen in 90 days. Explicitly document that KR3 is a stretch indicator, not a kill signal. The real question Bet 1 must answer by September 1 is: "Do intermediate engineers at Tier 2 NZ firms care enough about AI-generated skeletons to give us a verified work email and generate multiple documents?" Revenue validation is a Bet 2 question (Pre-Review), not a Bet 1 question (free wedge). **Who:** Ron, amend `strategic-bets.md`. **When:** Before June 1.

- **Action B: Start 3-5 WTP conversations during the pre-build window (May).** Do not wait for the product to exist. The discovery guide allows conducting Switch-timeline interviews without a product demo. Recruit 3-5 intermediate engineers through the founder's existing NZ network for informal conversations about their GBR workflow. This gives early WTP signal before the build starts and creates 3-5 warm leads who will be the first to try the product on Day 1. **Who:** Founder. **When:** May.

### Risk 4: Standards Knowledge Store ships at document level

- **Action A: Manually chunk 1 standard (NZS 3910) to clause level before build, as a design spike.** Take NZS 3910 (the most commonly referenced NZ construction standard in geotechnical work) and manually produce a clause-level applicability map for GBR sections. This forces the founder to confront the content-engineering effort required, produces a reusable reference for the AI agents to follow, and ensures at least one standard ships at actionable granularity. The remaining 2-4 standards can ship at document level with a Sprint 2 chunking commitment. **Who:** Founder, with Graeme advisory. **When:** June 1-7, first week of sprint.

### Risk 5: Founder attention is irreversibly split

- **Action A: Time-block the sprint into build-only and sell-only phases.** Days 1-25: build. Days 26-30: launch prep and first LinkedIn announcements. Post-launch (July 1 onward): founder-led content and outbound. Do not attempt to run acquisition and build in parallel during June. The GTM plan's 60-day clock for KR1 starts at launch (June 30), not at the founder's first day (June 1). This gives 60 days of focused selling after 30 days of focused building, rather than 90 days of doing both badly. **Who:** Founder. **When:** Before June 1 — commit to the time-block in writing.

---

**Next step for Mark:** Frame a problem statement for the document-parser scope cut (Risk 1, Action A) — specifically, define what the manual-input form must capture to produce a useful skeleton, and confirm with Graeme that dropdown-based parameter selection is sufficient for NZ GBR/GIR jurisdiction mapping. This is the most impactful scope-reduction decision in the sprint and it needs product sign-off before build begins.
