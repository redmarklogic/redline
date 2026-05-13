# Personas — Small Firm Segment (5-50 people)

**Status**: Pre-discovery draft v1. **Owner**: Mark (co-owned with Ron).
**Segment**: Small (5-50). **Beachhead**: Yes.
**Last updated**: 2026-05-03.

> **Pre-discovery notice.** These personas are grounded in Graeme's domain expertise
> and the founder's strategic direction, not in validated customer interviews. They are
> hypotheses. The KR2 discovery conversations (see `discovery-guide.md`) will validate,
> revise, or kill them. Names are synthetic placeholders — replace with real names when
> interview evidence exists.

**Firm archetype for all three personas**: A geotechnical consultancy with 10-30 staff.
One to three directors, two to five seniors, five to twenty intermediates. NZ examples:
Engeo NZ, CMW Geosciences, Riley Consultants, HD Geo, Geotechnics. UK parallel:
Piledesigns (11 engineers, 1,700+ instructions/year). These firms have enough report
volume to feel the review bottleneck but no budget for dedicated QA staff or R&D.

---

## 1. Perrie — Day-1 User (Intermediate Engineer)

### Identity

- **Name**: Perrie (synthetic)
- **Role**: Intermediate Geotechnical Engineer, 4 years post-graduation, working toward
  Chartered Professional Engineer (CPEng) status
- **Firm context**: 15-person NZ consultancy. Perrie reports to a Senior Engineer and has
  work reviewed by one of two seniors before the Director signs off
- **Digital maturity**: Comfortable with Word, Teams, and basic cloud tools. Has used
  ChatGPT privately but would never admit it at work because the Director has not
  sanctioned it

### Evidence Anchors

1. Graeme's domain grounding (2026-05-03): "five to twenty intermediates" in Small firms;
   "each senior reviews work from 5-7 people"
2. JTBD (`jtbd.md`): "Intermediate civil/geotechnical engineer (3-7 years
   post-graduation)... draft is due, senior reviewer is bottlenecked, engineer has run out
   of self-check options"
3. Bet 1 (`strategic-bets.md`): Free Skeleton Generator acquires intermediate engineers
   via PLG; quota exhaustion creates the outbound conversation

### Jobs to Be Done

1. **Draft a GBR/GIR that survives senior review in one round** — so I stop losing
   evenings to rework and stop feeling like I'm wasting my reviewer's time.
2. **Get the report structure right before I start writing** — so I don't discover
   halfway through that I've missed a section the client scope required.
3. **Reference the correct standards without memorising every update** — so my reviewer
   stops marking up "wrong standard cited" and I stop looking careless.

### Pains (observed, not assumed)

| Pain | Source |
|---|---|
| Copy-paste errors: previous project name left in headers, wrong site description carried over | Graeme grounding: most common quality failures |
| Wrong or missing standard references — "standards keep updating and nobody remembers all of it" | Graeme grounding |
| Conclusions introduce new information not supported by the body | Graeme grounding |
| Self-review against the firm's checklist is partial and stale — "checklists are tribal" | JTBD (`jtbd.md`) |
| Submitting a draft I know is incomplete because the reviewer is bottlenecked and I have no other option | JTBD trigger event |
| Cannot use ChatGPT because it has no jurisdictional grounding and the partner would not approve it | JTBD current alternatives |

### Gains (what success looks like, in Perrie's words)

- "My reviewer came back with five comments instead of twenty. That's never happened."
- "I used the skeleton and it already had the right section structure for an NZ residential
  GIR. I didn't have to guess."
- "It flagged that I'd referenced a superseded standard. I would have missed that."

### Adoption Journey

1. **Discovery**: Perrie finds the free Skeleton Generator through a colleague or a Google
   search for "GBR template NZ." Uploads a Letter of Engagement. Gets a structured
   skeleton in one click. (Bet 1 acquisition)
2. **Activation**: Perrie uses the skeleton 2-3 times. Quota exhausts. Founder reaches out
   with a Pre-Review trial offer. (Bet 1 → Bet 2 conversion)
3. **Retention**: Perrie submits a Pre-Reviewed draft. Reviewer returns fewer comments.
   Perrie tells a colleague. (Bet 2 validation)

### Adoption Risks

- **Variable digital maturity** — Perrie might not trust a web tool with a draft report
  containing client data. Data sensitivity is real for engineers handling site
  investigation results.
- **No internal champion to validate output** — Perrie cannot independently judge whether
  the tool's suggestions are correct. If the tool gives bad advice once, Perrie loses trust
  permanently.

### Anti-Persona (who Perrie is NOT)

- Perrie is not a graduate (0-2 years). Graduates do not draft full GBRs independently; they
  assist seniors. A graduate has no "review bottleneck" pain because they are not the
  bottleneck — they are the cause of it.
- Perrie is not a tech enthusiast adopting AI tools for fun. Perrie is a pragmatist who wants
  fewer review comments, not a better AI experience.
- Perrie is not at a Large firm (500+). Large firms have internal QA teams, templates, and
  dedicated technical writers. Perrie's pain exists because the firm is too small for those.

---

## 2. Anna — Day-1 Buyer (Director / Practice Lead)

### Identity

- **Name**: Anna (synthetic)
- **Role**: Technical Director and co-owner of the firm. 18 years post-graduation, CPEng.
  Responsible for business development, client relationships, and final sign-off on major
  reports
- **Firm context**: 20-person NZ consultancy. Anna manages a practice of 12 people
  (3 seniors, 9 intermediates). She still does some hands-on review but is increasingly
  pulled into BD and management
- **Decision authority**: Anna can approve a SaaS subscription under $500/month without
  board approval. Above that, she needs her co-director's sign-off

### Evidence Anchors

1. Graeme's domain grounding (2026-05-03): "One to three directors... tight margins make
   time savings valuable"; "PI premiums are 3-8% of revenue"; "Insurers evaluate QA
   systems when setting premiums"
2. JTBD Phase-2 (`jtbd.md`): "Principal engineer or technical Partner with sign-off
   authority and litigation exposure"
3. Bet 2 (`strategic-bets.md`): Pre-Review mode is the paid product Day-1; buyer pain is
   reviewer-bottleneck pain

### Jobs to Be Done

1. **Reduce the review bottleneck so my seniors can do project work** — every hour a
   senior spends correcting copy-paste errors is an hour they are not billing or winning
   work.
2. **Improve junior report quality without hiring dedicated QA staff** — I don't have
   the budget for a QA manager, but I need the quality to stop slipping.
3. **Strengthen the firm's PI insurance story** — if I can show insurers a systematic
   QA layer, I might hold premiums steady instead of watching them climb 5% a year.

### Pains (observed, not assumed)

| Pain | Source |
|---|---|
| Each senior reviews 15-25 reports/month at 1-3 hours each, on top of their own project work, BD, and management | Graeme grounding: reviewer bottleneck |
| The same mistakes repeat across intermediates — copy-paste errors, wrong standards, missing caveats | Graeme grounding: most common quality failures |
| PI premiums are 3-8% of revenue; even minor disputes cost at least $10,000 from profits | Graeme grounding: liability context |
| Talent shortage means intermediates are less experienced than a decade ago, but report volumes have not dropped | Graeme grounding: "talent shortage causes the liability exposure" |
| No dedicated QA staff or R&D budget — "we don't have the budget for R&D" | Graeme grounding |
| Disputes Tribunal ceiling doubled to $60k; minor quality failures now carry material financial exposure without legal representation | CEAS Indemnity Matters Issue 88, April 2026 |
| Multiple PS4 / scope-qualification advisories in 18 months from CEAS, EngineeringNZ, and ACENZ; directors who sign off reports are receiving industry-wide warnings about inadequate limitation clauses | CEAS Indemnity Matters Issue 88, April 2026 |

### Gains (what success looks like, in Anna's words)

- "My seniors are reviewing faster because the basic stuff is already caught. They can
  focus on the engineering judgment, not the formatting."
- "New hires are learning the firm's standards through the tool instead of through
  painful review cycles. Onboarding time is dropping."
- "I can tell our insurer we have a systematic pre-review layer. That's a conversation
  I couldn't have before."

### Buying Triggers

- A senior leaves and review capacity drops overnight. Anna feels the bottleneck
  personally — she has to pick up reviews she had delegated.
- A near-miss: a report goes to a client with the wrong project name in the header.
  The client notices. Anna is embarrassed and angry.
- PI renewal: the insurer asks what QA systems the firm has. Anna's answer is "our
  seniors check everything." She knows that is not a system.
- PI renewal: the insurer asks specifically about AI usage in report preparation.
  Anna does not have a policy, a disclosure statement, or a record of which reports
  used AI assistance. The question makes her realise the firm is exposed on a dimension
  she had not considered. *(Added 2026-05-10. Treat as a distinct buying trigger from
  the general QA systems question above — AI disclosure is a newer and more specific
  insurer concern.)*
- Disputes Tribunal ceiling doubles to $60k (January 2026). Report quality failures
  that previously fell below the threshold for formal action are now firmly within
  Tribunal reach. The blowback risk --- chasing unpaid fees and facing a quality
  counterclaim without legal representation --- makes Anna re-evaluate what "good
  enough" QA looks like. Source: CEAS Indemnity Matters Issue 88, April 2026.

### Adoption Risks

- **Cost sensitivity** — Anna will compare the subscription cost to a senior's hourly
  rate and ask "how many review hours does this save me per month?" The ROI must be
  obvious and demonstrable within the first month.
- **Conservatism** — Anna has run the firm successfully for 15 years without this tool.
  The status quo is uncomfortable but familiar. She needs a trigger event (above) to move.
- **Agility cuts both ways** — Anna can decide in a day, but she can also cancel in a
  day. Retention depends on visible, recurring value — not a one-time "wow" moment.

### Anti-Persona (who Anna is NOT)

- Anna is not a technology buyer. She is not evaluating Redline against other SaaS
  tools. She is evaluating it against "hire another senior" or "accept the current
  quality level."
- Anna is not at a Micro firm (1-4). A sole practitioner reviews their own work and
  has no delegation bottleneck. Anna's pain exists because she has intermediates
  producing volume she cannot review fast enough.
- Anna is not at a Large firm (500+) where a Head of Technical Excellence or a QA
  department already exists. Anna IS the QA department.

---

## 3. Prisca — Gatekeeper (Senior Reviewer)

### Identity

- **Name**: Prisca (synthetic)
- **Role**: Senior Geotechnical Engineer, 10 years post-graduation, CPEng. Prisca is the
  primary reviewer for 6 intermediates. She is technically excellent, respected by the
  team, and protective of the firm's technical reputation
- **Firm context**: Same 20-person firm as Anna. Prisca reports to Anna but has
  significant autonomy on technical matters. Anna trusts Prisca's judgment — if Prisca says
  a report is not ready, it does not go to the client

### Evidence Anchors

1. Graeme's domain grounding (2026-05-03): "Each senior reviews work from 5-7 people...
   15-25 reports per month per senior needing substantive technical review, at 1-3 hours
   each"; "Reviewer ego" as adoption resistance factor
2. Graeme grounding, adoption factors: "do NOT say 'catches what a senior reviewer would
   catch'" — explicit warning about messaging that threatens reviewer identity
3. Positioning (`positioning.md`): Redline is positioned against "the senior engineer" —
   "compresses the review loop; never replaces the human reviewer's judgment"

### Jobs to Be Done

1. **Maintain the firm's technical standard** — every report with Prisca's review carries
   her professional reputation. She will not lower the bar.
2. **Stop correcting the same basic mistakes** — Prisca is tired of marking up copy-paste
   errors and missing caveats. She wants to spend review time on engineering judgment, not
   proofreading.
3. **Develop the intermediates** — Prisca genuinely wants her team to improve. She just does
   not have time to teach when she is buried in reviews.

### Pains (observed, not assumed)

| Pain | Source |
|---|---|
| Reviews 15-25 reports/month at 1-3 hours each while also managing her own project work | Graeme grounding |
| The same corrections repeat — copy-paste errors, wrong standards, missing caveats — and Prisca feels like nobody learns | Graeme grounding: most common quality failures |
| Prisca carries the cognitive load of remembering which standards have been updated, which caveats apply to which soil conditions, and which client has specific reporting requirements | Graeme grounding: "standards keep updating and nobody remembers all of it" |
| Prisca's review time is not valued as a line item — it is absorbed into project overhead, making it invisible to management until a senior leaves | Structural inference from Graeme's bottleneck description |

### Resistance Profile

Prisca is the persona most likely to resist Redline. Her resistance is not irrational — it
is identity-based. Understanding it is critical to adoption.

| Resistance factor | Root cause | What would shift it |
|---|---|---|
| **Ego**: "I am the quality standard here" | Prisca's professional identity is built on being the person who catches mistakes. A tool that catches mistakes threatens that identity. | Position the tool as catching the *routine* stuff (copy-paste, standards references) so Prisca can focus on the *hard* stuff (engineering judgment, risk assessment). Never say "catches what Prisca would catch." Say "handles the checklist so Prisca can focus on the judgment." |
| **Trust**: "What if it's wrong?" | Prisca knows that a bad suggestion accepted by an intermediate is worse than no suggestion at all. She has seen juniors trust ChatGPT output uncritically. | Show Prisca the tool's reasoning. Let her see *why* it flagged something. Transparency converts skeptics faster than accuracy metrics. |
| **Control**: "I haven't approved this" | Prisca was not consulted when Anna bought the tool. She feels bypassed. | Involve Prisca in the trial. Ask her to configure the house rules. Make her the expert on the tool, not the subject of it. |

### Conversion Path (Gatekeeper to Champion)

Prisca does not convert because she is told to. She converts through one of two experiences:

1. **The tool catches something Prisca missed.** This is rare but transformative. Prisca
   respects competence. If the tool flags a superseded standard that Prisca did not notice,
   Prisca's resistance drops sharply.
2. **The tool eliminates the drudge work.** Prisca realises she has not marked up a single
   copy-paste error in two weeks because the intermediates are catching them before
   submission. Prisca's reviews are now 45 minutes instead of 2 hours, and the review
   quality is higher because she is not fatigued by the time she gets to the hard sections.

### Anti-Persona (who Prisca is NOT)

- Prisca is not a Luddite. She uses engineering software daily (gINT, LPILE, PLAXIS). Her
  resistance is not about technology — it is about a tool entering *her* domain of
  expertise.
- Prisca is not the buyer. She does not care about the subscription cost or the PI insurance
  story. She cares about whether the tool makes her intermediates' reports better or worse.
- Prisca is not the user. She does not run Pre-Review on her own reports. She sees the
  *output* of Pre-Review in the drafts her intermediates submit.

---

## Segment Context — Why Not the Other Segments?

| Segment | Size | Why not Day-1 |
|---|---|---|
| **Micro** (1-4) | Solo CPEng or tiny partnership | Principal IS the reviewer — no delegation bottleneck. Too few reports to justify a subscription. Not our target. |
| **Medium** (50-500) | Multi-office, departmental structure | Longer procurement cycles, IT security review requirements (see `enterprise-ai-blocking-risk-assessment.md`), internal QA staff may already exist. Phase-2 expansion target, not beachhead. |
| **Large** (500+) | National/multinational | Dedicated QA teams, templates, technical writers, enterprise procurement. 6-month security review minimum. Phase-3 at earliest. |

---

## Provenance

- **Domain grounding**: Graeme's firm-size segmentation analysis (2026-05-03), grounded
  in 25+ years of consultancy experience across NZ and UK geotechnical firms.
- **JTBD**: `docs/product/strategy/jtbd.md` (Draft v1).
- **Positioning**: `docs/product/strategy/positioning.md` (Draft v1).
- **Strategic bets**: `docs/product/strategy/strategic-bets.md` (Draft v2) — Bet 1
  (Free Skeleton Wedge) and Bet 2 (Pre-Review Day-1).
- **Adoption resistance factors**: Graeme grounding, specifically the "do NOT say 'catches
  what a senior reviewer would catch'" warning.

## Validation Plan

These personas are hypotheses. They will be validated or revised through:

1. **KR2 discovery conversations** (15 planned) using the Switch interview structure.
   Each conversation should produce a Four-Forces map. See `discovery-guide.md`.
2. **Name replacement**: Replace synthetic names (Perrie, Anna, Prisca) with real names from
   interviews when evidence exists.
3. **Staleness rule**: These personas expire 12 months from creation (2027-05-03) and
   must be revisited before reuse.

## Next Steps

- **Ron**: Review for alignment with strategic bets and positioning. Confirm the
  archetype-level segment definition is consistent with GTM motion.
- **John**: Use these personas to ground content marketing topics (Big 5 framework) and
  LinkedIn targeting. Do not publish persona names externally.
- **Mark**: Reference these personas in all PRDs targeting the Small segment. Load
  `pm-prd-builder` when the first PRD is ready for engineering handoff.
