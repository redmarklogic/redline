# Launch Perimeter Constraints

**Status**: Final v1.
**Owner**: Mark.
**Source**: Item 1, Launch Planning Session — 2026-05-14.
**Downstream consumers**: John (Item 4 — Market Activation Sequencing), Matt (website design brief).

---

## 1. Dependency Chain

Each step must exist before the next begins. No step is optional.

**Step 0 — Silent setup (now, no deadline).**
Company LinkedIn profile created. Founder profile optimised. Connections built with known contacts only. Content drafted and batched. No public posting, no public commenting, no activity that surfaces to strangers. This step has no dependency and can begin immediately.

**Step 1 — Website goes live.**
Minimum viable state: see Section 2 below. This is the gate. Nothing public on LinkedIn until this step is complete.

**Step 2 — Founder LinkedIn narrative content begins publicly.**
Educational content grounded in NZ geotechnical dispute patterns (court cases, standards analysis, observed failure modes). CTA changes to the waitlist URL immediately. Purpose: drive profile visitors directly to the waitlist. The website must exist before any public activity creates profile visitors.

**Step 3 — Skeleton generator is demo-able.**
Does not need to be production-ready. Must be demo-able in a co-development recruitment conversation. LinkedIn content mix shifts to include product demonstrations. Full media wing tempo activates.

**Step 4 — LinkedIn media wing at full tempo.**
10:1 commenting rule, Dream 100 direct motion, full cadence. Activates only when Step 3 is live. John owns the mechanics (Item 4).

---

## 2. Minimum Viable Website

**Required at Step 3:**

1. Headline that states what Redline is (using the quality-layer positioning — no "AI" in the headline).
2. Two-sentence description of who it is for and what job it does.
3. One concrete domain-specific credibility signal — a real standards example demonstrating that Redline is grounded in the practitioner's world (e.g., a wrong-standard-detection example using actual NZS/NZGS version references). Does not require a working tool — can be static prose or a screenshot.
4. Waitlist form (work email capture — SSO prompt deferred to first generation moment, as per Bet 1 UX decision 2026-04-22).
5. Beta framing — explicit statement that the product is in beta.

**Not required at Step 3 (scope-locked):**

- Working tools of any kind.
- Blog or domain authority content section.
- Demo video (desirable if skeleton generator is demo-able before Step 3; not blocking if it is not).
- Pricing page.
- Case studies or testimonials.
- Any navigation beyond a single landing page.

---

## 3. Demo Strategy

These are separate decisions. Do not conflate them.

| | Skeleton Generator | Wrong-Standard-Detection |
|---|---|---|
| **Role** | Acquisition product — Bet 1 wedge, usage loop, quota exhaustion trigger | Demo narrative — website credibility signal, LinkedIn story, co-development conversation script |
| **When required** | Step 4 (working demo-able version) | Step 3 (static example sufficient) |
| **Wow factor** | Moderate — engineers can structure reports themselves | High — catches something a human would likely miss and explains the legal exposure |
| **Live tool required?** | Yes (at Step 4) | No (can be presented as a case study or screenshot at Step 3) |

**Decision**: The skeleton generator is the first product to ship and the acquisition wedge. Wrong-standard-detection is the first story to tell and the launch narrative. Both are required; they serve different jobs.

---

## 4. LinkedIn Constraint

The company LinkedIn profile (Step 0) is live immediately as silent infrastructure.

Before website live (Step 1): no public posting, no public commenting, no activity that surfaces to strangers. Silent profile setup and connection-building with known contacts is permitted. Rationale: NZ geotechnical is a small professional market of a few hundred practitioners. A profile visit that finds no destination forms a sticky "nothing here yet" impression. Repeat attention is harder to earn than first attention. The cost of waiting two to three weeks for the website is negligible; the cost of a wasted first impression is not recoverable.

After website live (Step 2): public content begins. CTA is the waitlist URL from the first post — no "follow for updates" phase.

John owns all LinkedIn mechanics. This constraint is the handoff boundary from Ron/Mark to John.

---

## 5. Named Risk — Waitlist Gap

**Risk 1 — Waitlist gap**: The website goes live (Step 1) and converts LinkedIn traffic into waitlist signups. The skeleton generator (Step 3) takes additional weeks to become demo-able. In that gap, waitlist members lose context and brand familiarity, degrading the first product experience.

**Owner**: John.

**Status**: Unaddressed. John must produce a waitlist nurture sequence — 2–3 emails delivering the same standards insight content as the LinkedIn posts — to keep the brand present between Step 1 and Step 3. This is a GTM instrument, not a website feature. It should be scoped in Item 4.

---

**Risk 2 — Small-market first-impression**: NZ geotechnical consulting is a market of a few hundred relevant practitioners who operate in overlapping professional networks. A profile visit that finds no destination (no website, no product) forms a sticky "nothing here yet" impression. Repeat attention from the same person is harder to earn than first attention — LinkedIn algorithm deprioritises re-engagement with profiles that generated no click or follow on first visit, and in a small social graph a casual remark travels faster than the content will.

**Mitigation**: The revised dependency chain (website before any public posting) is the mitigation. Do not revert Step 0/Step 1 ordering under time pressure.

**Owner**: Ron (sequencing discipline).

---

## 6. Co-Development Partner Outreach — Guardrail

**Rule**: Co-development partner outreach starts only after the website is live (Step 1) and the skeleton generator is demo-able (Step 3). Recruitment comes from free-tier waitlist signups who have activated the product — not from LinkedIn audience or cold outreach.

**Pre-website exception (tightly scoped):**
Up to three private discovery conversations with existing professional contacts (people the founder has personally worked alongside, supervised, or trained) are permitted before the website goes live, subject to:

- Known contacts only — not people the founder merely recognises from the NZ geotech network.
- Framing is discovery, not product demonstration — the skeleton generator is not shown; no sales language.
- The ask is: "I'm designing something and I want twenty minutes of your honest reaction to the problem I'm trying to solve."
- If findings from these conversations change the positioning or the website headline, Mark must see them before the website goes live.

**Co-development recruitment motion:**
The first co-development partner invitations are sent from waitlist signups who have activated the free-tier skeleton generator — approximately two to four weeks after Step 3 goes live. Email 2 of the nurture sequence (see `docs/product/marketing/content/waitlist-nurture-sequence.md`) carries the soft co-development ask. Mark must verify that the Email 2 trigger (14 days from signup) aligns with the expected time for a free-tier user to activate the skeleton generator — the ask must not land before the prospect has used the product.

**Owner**: Ron (sequencing discipline). Mark (Email 2 trigger alignment check).
