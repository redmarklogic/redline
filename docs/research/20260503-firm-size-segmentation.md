# Firm Size Segmentation — Strategic Analysis

**Date**: 2026-05-03
**Author**: Ron (Strategy & GTM Advisor)
**Agenda item**: Founder Brain Dump 1.4 — Segment by Company Size
**Notebooks queried**: Founder Memos, Professional Services Firm Management, Entrepreneurship & Startup Strategy

---

## Research Question

How should Redline segment the geotechnical consulting market by firm size? What
thresholds define each tier? Who should we target first and why? How does the CEO
priority hierarchy vary by tier?

## Proposed Tier Definitions

The PSF Management literature identifies structural thresholds where firm behaviour
changes. Combined with the founder's memos and the tier model already in `strategy-psf-domain`,
I propose three tiers defined by **headcount** — the simplest metric an engineer or a
founder can estimate without asking for revenue figures.

| Tier | Headcount | Label | Structural characteristics |
|---|---|---|---|
| Tier 3 | 5–50 staff | Small / niche firms | No dedicated legal, BD, or R&D teams. QA is informal — email or face-to-face review between PM and engagement director. Independent review is structurally difficult because "everyone in the firm may have been involved in the project." Invest almost exclusively in base technologies (word processing, CADD). Pacing technologies viewed as too expensive and too high-risk. Decisions made in days, not months. |
| Tier 2 | 50–500 staff | Mid-size firms | Matrix management emerges (~40–50 staff). Formal monthly procedures and reporting appear at ~40 staff. Technology budget exists but is limited. Firm can evaluate before buying but lacks R&D capacity. Some innovation budget. QA is more formalised but still not fully independent. Overhead jumps sharply at the ~150 staff threshold. |
| Tier 1 | 500+ staff | Large infrastructure firms | Dedicated bidding, legal, and R&D teams. In-house AI/tool-building capability. Formal practice guides, independent review staff. Government and mega-project portfolios. Build bespoke tools. No incentive to sell tools externally (cannibalisation). |

**Why headcount, not revenue?** Revenue thresholds vary by jurisdiction and are rarely
disclosed by private firms. Headcount is observable (LinkedIn, company website, industry
directories) and correlates directly with the structural transitions the PSF literature
identifies. The founder can estimate a firm's tier during a LinkedIn prospecting session
without asking for financials.

**Why not project type as the primary axis?** Project type (residential vs infrastructure
vs mega-project) correlates with firm size but does not cause the structural differences
that matter for buying behaviour. A 20-person firm doing residential and a 20-person
firm doing small commercial projects have the same QA constraints, the same thin
management layer, and the same technology budget. Project type is a secondary filter
within a tier, not the segmentation axis.

## CEO Priority Hierarchy by Tier

Already resolved in item 1.2. Reproduced here with segmentation detail.

| Tier | #1 Priority | #2 Priority | #3 Priority | Notes |
|---|---|---|---|---|
| Tier 3 (5–50) | Financial Performance | Liability | Talent | Thin margins; one slow month threatens payroll. No legal team to mitigate PI exposure. Fewer seniors to lose — but losing one is existential. |
| Tier 2 (50–500) | Financial Performance | Talent | Liability | More financial resilience, but acute talent competition at the ~150 threshold where overhead spikes. PI exposure grows with project diversity. |
| Tier 1 (500+) | Talent | Financial Performance | Liability | Knowledge drain from retiring principals is the existential risk. Financial resilience is higher. Dedicated legal and QA teams manage liability internally. |

**Key refinement from this analysis**: For Tier 3 firms, I would argue liability sits
higher than talent as priority #2 — not because they have more claims, but because they
have **zero buffer** against a claim. A Tier 1 firm absorbs a $50k dispute from overhead.
A Tier 3 firm absorbs it from the owner's mortgage. The PSF literature confirms that
some small start-up firms skip professional liability insurance entirely due to cost,
which paradoxically increases their exposure. This makes the audit trail value proposition
("Redline gives you the audit trail your insurer will ask for") sharper for Tier 3 than
for any other tier.

## Beachhead Recommendation: Tier 3 First, Then Bowling-Pin into Tier 2

### Why Tier 3 is the beachhead

Crossing the Chasm (Moore) says the beachhead must be "big enough to matter, small
enough to win, and a good fit with your crown jewels." Applied to our tiers:

| Criterion | Tier 3 assessment | Tier 2 assessment |
|---|---|---|
| **Big enough to matter** | NZ alone has hundreds of small geotechnical firms. AU is an order of magnitude larger. Even a fraction of this segment sustains early revenue. | Fewer firms in absolute count, but larger deal sizes. |
| **Small enough to win** | Yes. No competitor serves this niche. Archie targets AI drafting, not quality review. ChatGPT has no jurisdictional grounding. Bespoke agencies (SupaHuman) price Tier 3 firms out at $50k+. | Harder. Mid-size firms may have enough IT staff to evaluate and reject, and the sales cycle is longer. |
| **Good fit with crown jewels** | Perfect. The Standards Knowledge Store and zero-training perimeter solve Tier 3's exact pain: they cannot build these tools and cannot afford consultants who build them. | Good, but Tier 2 firms may demand integrations, SSO, procurement processes we cannot yet deliver. |
| **Self-referencing** | Geotechnical engineers in NZ/AU are a tight community. They attend the same NZGS conferences, read the same Ground Engineering magazine, and move between firms. Word-of-mouth is fast. | Also self-referencing, but with more formal procurement gates. |
| **Compelling reason to buy** | Acute. No dedicated review staff, no R&D budget, informal QA that would not survive a PI insurer's audit. Every uncaught error is a direct threat to the owner's personal finances. | Present but less acute. They have some review infrastructure. |
| **Whole product feasible in 3 months** | Yes. Skeleton Generator + Pre-Review on web interface is the whole product for a Tier 3 engineer drafting a GBR. | Possibly not. Tier 2 firms may require Word integration, SSO, or admin dashboards before they consider it "complete." |
| **No entrenched competition** | Confirmed. No competitor occupies this space. | Same. |

The founder's memos confirm this: Redline exists to bring "technology available in large
civil engineering consultancies to small and medium size" firms. The founder explicitly
identifies that large firms "have no incentive to sell" their proprietary tools to
smaller competitors, and that small firms "don't have a dedicated legal team to help
them reduce the risk." This is a classic new-market disruption against nonconsumption.

### The bowling-pin path to Tier 2

Once Tier 3 is dominated — meaning we hold >50% of new orders in NZ geotechnical
small-firm quality tools within 12 months of launch — the bowling-pin path into Tier 2
is natural:

1. **Word-of-mouth bridge**: Engineers move from small firms to mid-size firms (and
   back). A Tier 3 engineer who used Redline at a 15-person firm and moves to a
   100-person firm becomes an internal advocate.
2. **Whole product extension**: By the time we cross into Tier 2, we will have sprint
   cycles behind us to add SSO, admin dashboards, and any integration the discovery
   interviews surface.
3. **Reference base**: Tier 2 pragmatist buyers want references from their own world.
   A portfolio of Tier 3 references in geotechnical is more credible to a Tier 2
   geotechnical firm than references from a different industry entirely.

### Tier 1 is explicitly out of scope

Large firms build their own tools. They have R&D budgets, dedicated legal teams, and
the incentive structure to keep proprietary advantages internal. Targeting Tier 1 firms
would mean competing with their in-house capability — a fight we would lose and should
not enter. Tier 1 is a **non-goal** (see `non-goals.md`).

One exception to monitor: Tier 1 firms may become *channel partners* or *referral
sources* if their senior engineers use Redline at a side gig or recommend it to
subconsultants. This is an organic path, not a GTM motion.

## Risks and Open Questions

1. **Tier 3 willingness to pay**: Small firms are price-sensitive. The PLG wedge
   (free skeleton, paid Pre-Review) mitigates this, but the price point for Pre-Review
   must be validated in KR2 discovery conversations. The founder should probe
   willingness-to-pay in the first five conversations using the Monetizing Innovation
   methodology (Van Westendorp or Gabor-Granger).

2. **Enterprise AI blocking in Tier 2**: The `enterprise-ai-blocking-risk-assessment.md`
   flags that mid-size firms with MSP-managed IT may block web tools. This is a Tier 2
   problem, not a Tier 3 problem — most Tier 3 firms manage their own IT or use a
   light-touch MSP that does not deploy application-level filtering.

3. **"Firm size" vs "project size"**: Within Tier 3, a firm doing residential
   geotechnical work and a firm doing small commercial work may have different report
   types. The skeleton generator handles this through standards configuration, but the
   discovery guide should include a project-type filter to validate.

4. **Tier 3 buying authority**: In a 10-person firm, the founder/principal *is* the
   economic buyer, the TD, and often the senior reviewer. This collapses the buying
   committee to one person — which accelerates sales but means one veto kills the deal.
   The positioning language sensitivity rules (no "catches what a reviewer would catch")
   are critical here because the buyer IS the reviewer.

## Recommendation for Agenda Resolution

**Define the size buckets**: Tier 3 (5–50 staff), Tier 2 (50–500 staff), Tier 1 (500+ staff).
Segmented by headcount.

**Primary target**: Tier 3 first — the beachhead. These firms cannot build, cannot afford
bespoke, and have the most acute pain-to-resource ratio.

**Secondary target**: Tier 2 via bowling-pin expansion after Tier 3 beachhead is secured.

**Explicitly out of scope**: Tier 1 — they build their own tools.

## Provenance

- Founder Memos notebook (citations [1]–[12] from query session)
- Professional Services Firm Management notebook (citations [1]–[39] from query session)
- Entrepreneurship & Startup Strategy notebook, Crossing the Chasm (citations [1]–[26])
- Existing strategy docs: `positioning.md`, `strategic-bets.md`, `jtbd.md`
- Domain grounding: `strategy-psf-domain` skill (Tier definitions, cannibalisation model)
