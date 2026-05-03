# Positioning — Redline

**Status**: Draft v1. **Owner**: Ron.

## One-Sentence Positioning

> For NZ and AU geotechnical engineers, Redline is the neutral quality layer that handles
> the routine compliance checks so your senior reviewers can focus on engineering
> judgment — without writing the report, taking a position, or arbitrating disputes.

## Positioning Frame

We position Redline against three categories of incumbent, deliberately:

| Category | Incumbent example | How Redline differs |
| --- | --- | --- |
| Generic AI assistants | ChatGPT, Microsoft 365 Copilot | Jurisdictional grounding (NZS / AS / NZGS), zero-training perimeter, partner-safe to admit using. |
| Document QA / linting tools | Generic grammar / clause-flagger SaaS | Domain-specific to geotechnical reports; Switzerland-neutral; firm-configurable house rules. |
| Senior peer review | The senior engineer | Compresses the review loop; never replaces the human reviewer's judgement. |

## Lexicon

These words appear in every external surface (web, sales, docs):

- **Quality layer** — what we are. Not a tool, not an assistant, not a reviewer.
- **Infrastructure, not SaaS** — what category we sell into. Protects pricing power.
- **Switzerland-neutral** — what we promise. We surface; the human resolves.
- **Pre-Review** and **Adversarial Scan** — the two product modes. Used as proper nouns.
- **House Rules** — firm-configurable QA standards. Used as a proper noun.
- **Standards Knowledge Store** — our defensible asset. Used as a proper noun.

These words **never** appear:

- "AI engineer", "AI reviewer", "autonomous", "agentic" — all imply replacement,
  trigger Partner resistance, and forfeit neutrality.
- "AI-powered", "AI" as a value-proposition qualifier — permitted only in
  explanatory and discovery content, never in positioning (see AI Language Policy
  below).
- "Productivity tool", "writing assistant" — wrong category, wrong price ceiling.
- "Compliance" as a noun for what we deliver. We assist compliance work; we do not
  attest to compliance.

## AI Language Policy *(added 2026-04-30, founder + Ron + John consensus)*

**Decision:** AI is the engine, never the brand. The word "AI" follows a three-layer
rule across all external surfaces.

- **Positioning** (tagline, homepage hero, pitch deck cover, elevator pitch, value
  proposition): no "AI". No "machines". Lead with the job: "handles the routine checks
  so your senior reviewers can focus on the judgment that matters."
- **Explanatory** (how-it-works page, product tour, onboarding, sales Q&A): use "AI"
  factually and sparingly when explaining how the product works. Never as a selling
  point — as a technical fact. Example: "Yes, AI is the engine. It's trained specifically
  on geotechnical standards — not general-purpose."
- **Discovery** (blog posts, SEO content, FAQ, meta descriptions, LinkedIn content): use
  "AI" where it serves discoverability. John owns this via content strategy. The
  specialised-AI thesis ("People using specialised AI will replace people using generic
  AI") lives here.

**Rationale:**

- Pragmatist buyers (Moore, *Crossing the Chasm*) want "industry standard," not
  "state-of-the-art." Technology labels work on enthusiasts, not on engineering CEOs.
- A blanket ban on "AI" across all content creates a credibility gap (engineers know
  it's AI) and SEO invisibility (buyers search "AI for geotechnical reports").
- "Machines" as a replacement word triggers the wrong mental image for geotechnical
  engineers (excavators, CPT rigs, pile drivers — not software). Dropped.

**Enforcement:** Every piece of external copy must be reviewed against this table.
John owns discovery-layer usage. Ron owns positioning-layer compliance. Mark owns
explanatory-layer accuracy.

## Day-1 Buyer Story (Intermediate Engineer)

> "I drafted a GBR section, hit Redline, it flagged that I had not addressed the soil
> shear-strength assumption that NZGS guidance expects in this scenario. Saved me a
> review round."

## Phase-2 Buyer Story (Principal / Partner)

> "Before we ship a final-draft GBR on a contentious tender, we run Adversarial Scan to
> see how a contractor's claim engineer would attack the baseline language. We close the
> gap before it becomes a Differing Site Conditions claim."

## Anti-Positioning (What We Refuse to Be)

We refuse to be sold as: an AI engineer, a productivity tool, a writing assistant, a
compliance certifier, a chatbot, or an enterprise platform. Every one of those framings
costs us a Strategic Bet.

## Competitive Positioning *(added 2026-04-20, Archie CI session)*

**Against upstream AI drafting tools (Archie and similar):**

> "Your AI wrote it. Who checked it?"

Archie and similar tools generate report drafts. Redline checks them. These are
complementary, not competing jobs. As AI-drafted reports proliferate, the review job
grows — every AI-generated GBR still needs a quality layer before a senior signs it.
Redline is positioned downstream of any drafting tool, not against it.

**Generic LLM and drafting-tool objection:**

Generic AI is useful for early thinking, drafting assistance, and summarisation. Redline
is not trying to be a better chatbot. It is the quality layer after the draft: it checks
whether the document follows the standards, firm rules, and review expectations the firm
is prepared to stand behind.

Approved softer phrasing for this objection:

> "The draft can come from anywhere. The check still has to happen."

**Against bespoke AI agencies (SupaHuman and similar):**

SupaHuman delivers bespoke RAG implementations at $50k+ with a sales-call-plus-contract
acquisition model. Redline delivers a productised quality layer with zero-friction PLG
onboarding (upload report, see skeleton). SupaHuman reaches firms willing to buy a
custom project; Redline reaches every engineer willing to try a free tool.

**Insurance GTM angle:**

NZ insurance market is bifurcating on AI coverage — some insurers offering affirmative
AI policies, others inserting absolute exclusion clauses. GTM message for firms
navigating this uncertainty: "Redline gives you the audit trail your insurer will ask
for." Audit trail is baked into the product from Day 1 (see `feature-backlog.md`,
Feature L core subset elevated to Sprint 1).

Provenance: `docs/research/20260420-archie-competitive-intelligence-prompt.md`.

## Disruption Frame (Christensen — see `strategic-bets.md` Bet 6)

Redline is a **new-market disruption against nonconsumption**. We are not picking a
fight with Autodesk, Bentley, ChatGPT, or Microsoft Copilot — we are addressing a job
none of them currently sell into (the senior-review quality layer for geotechnical
reports). Positioning consequence: in any external surface where we are tempted to
compare ourselves head-on with a large incumbent, we instead reframe to the *job*
("the routine compliance checks that consume senior review time") rather than the
*product category* ("AI assistant"). Head-on comparisons invite the incumbent's
attention; job-framing keeps us invisible until the beachhead is dominated.

## CEO Priority Hierarchy *(added 2026-04-30, Ron + Graeme consensus)*

The top-three priorities of a geotechnical engineering firm CEO, in agreed order.
This ordering drives how we pitch to different buyer roles.

| # | Priority | What the CEO thinks about | Source |
| --- | --- | --- | --- |
| 1 | **Financial Performance** (utilisation, cash flow, revenue per employee) | "Are we getting paid for the engineering we are doing?" Utilisation must be ~85-90% for technical staff; missing payroll is the most stressful aspect of firm leadership. | PSF Management literature; Graeme (25yr practitioner) |
| 2 | **Talent** (recruitment, retention, knowledge transfer, leverage) | Skills shortage ranked #1 industry concern in the GSF survey every year (74.6% in 2024). University geoscience enrolments down 45% since 2014. Seniors doing work graduates could handle (systemic underdelegation). | Ground Engineering GSF surveys 2018-2025; PSF Management |
| 3 | **Liability** (PI insurance, claims, QA/QC) | PI premiums up to 1,000% increases; coverage cut from per-claim to aggregate caps. Even a minor dispute costs $10k+ unbillable time. Insurers evaluate QA procedures when setting premiums. | Ground Engineering 2019-2024; Risk Assessment literature |

**Context-dependence by firm size:**

| Firm tier | Binding constraint | Notes |
| --- | --- | --- |
| Tier 3 (5-50 staff) | Financial Performance firmly #1; Liability #2 | Thin margins; one slow month threatens payroll. Zero buffer against a PI claim — absorbed from the owner's personal finances. No legal team; some skip PI insurance entirely due to cost. |
| Tier 2 (50-500 staff) | Financial Performance #1, Talent closing fast | More financial resilience, but acute talent competition. PI exposure grows with project diversity. |
| Tier 1 (500+ staff) | Talent can overtake Financial Performance | Financial resilience is higher; existential risk is knowledge drain from retiring principals. Dedicated legal and QA teams manage liability internally. |
| Any firm during PI crisis | Liability jumps temporarily to #1 | When premiums spike or coverage shifts, ability to trade is threatened |

**Pitch rule:** When positioning to CEOs, lead with financial performance (write-off
reduction, capacity, utilisation). When positioning to practice leads and senior
engineers, lead with talent and leverage. Always frame the quality layer as solving
downstream consequences (claims, client loss, capacity), not "better reports."

**Key vocabulary correction:** "Efficiency" is a lever, not a CEO-level priority.
Never use "efficiency" as a selling point. Use specific consequences instead:
capacity, write-off reduction, leverage, recovered senior hours.

## Positioning Language Sensitivity *(added 2026-04-30, Graeme + John)*

**Problem:** The original supporting tagline "catches what a senior reviewer would
catch" implies current reviewers are missing things. The Technical Director (TD) —
often the veto holder on tool purchases — will feel their competence is questioned
and kill the deal.

**Principle:** The tool is subordinate. It does the tedious part. The human does the
important part. No engineer resents a tool that removes drudgery. Every engineer
resents a tool that implies they need supervision.

**Approved phrasings (TD sniff test passed):**

| Context | Phrasing |
| --- | --- |
| Canonical supporting tagline | "Handles the routine checks so your senior reviewers can focus on the judgment that matters." |
| Conversational (sales calls, LinkedIn) | "Takes the checklist off your senior reviewer's desk — so they can do the work only they can do." |
| High-impact (landing pages, demos) | "Your pre-review grunt work, handled — before your senior reviewer even opens the file." |

**Banned phrasing:** "Catches what a senior reviewer would catch" — retired.
Implies reviewers are failing. Confrontational to the TD gatekeeper.

Provenance: Graeme memo on reviewer sensitivity (2026-04-30); John copy review.

## Credibility Boundaries (Founder Voice)

The founder is the product's public face. He is **not** a geotechnical engineer and has
never drafted or reviewed an engineering document. He was lead data scientist for 3.5
years inside a NZ geotechnical consultancy, formally part of the discipline
organisationally. Product domain knowledge derives from the curated NotebookLM corpus
(CIRIA, ASCE, NZGS guidance, Eurocode 7, BS 5930 and the founder memos), not from
personal engineering practice.

**Permitted founder framings (LinkedIn bio, talks, web copy):**

- "Data scientist embedded in a major NZ geotechnical consultancy for 3.5 years."
- "Building Redline against the canonical literature of the discipline (CIRIA, ASCE,
  NZGS, Eurocode 7, BS 5930)."
- "Watched the senior-review process from the inside as the team's data scientist."
- Commentary on *publicly available* cases (NZ court judgements, Ground Engineering
  magazine case studies, published guidance updates).
- Pattern observations grounded in publicly available industry discourse — framed as
  "a pattern I keep seeing in how the industry discusses this problem", not as a citation
  of a personal corpus. The source of the pattern (the Ground Engineering archive; see
  `docs/product/marketing/archive-intelligence.md`) is never disclosed. Insights surface
  in content; the archive remains invisible.

**Forbidden founder framings (reputational and legally adjacent):**

- "I have reviewed GBRs / GIRs." (False.)
- "From experience, I know what senior engineers look for." (False; the source is the
  literature, not practice.)
- "In my projects we found that..." (Implies engineering project ownership he did not
  hold.)
- Any first-person engineering opinion on a specific design, calculation, or
  interpretive matter.
- The shorthand "engineer who watched 500 reports get reviewed" — only viable if
  reframed as "data scientist who watched the process from inside the team".

Misrepresenting professional credentials in a market this small is irrecoverable.
This section is binding on every external surface — web, LinkedIn, sales decks,
podcast appearances, conference panels.

**Founder persona framing (internal):** The founder's LinkedIn presence is grounded in
the credibility boundaries above, not in a performed "actor" character. The mental model
that fits the boundaries is "authentic positioned voice" — the founder is genuinely a
data scientist who read deeply, watched the process, and is building against the
literature. That is not a performance; it is an honest positioning. Ron's recommendation
(2026-04-19): drop the "actor" framing internally. In a market of practitioners who talk
to each other, a performed persona is terminal if it ever reads as inauthentic. Founder
decision pending; see `docs/product/strategy/decisions/parked-decisions.md` P-028.

## Provenance

Switzerland-neutral framing and Infrastructure-not-SaaS lexicon are strategy synthesis;
not memo-grounded. Domain pain framing draws on prior research files catalogued in
`docs/research/20260418-founder-memos-strategy-grounding.md`. Credibility Boundaries
section added 2026-04-18 per founder correction (he is a data scientist, not an
engineer). Archive citation rule and founder persona framing note added 2026-04-19
following Ron + John advisory session on the Ground Engineering archive as a stealth
intelligence asset. Competitive Positioning section and Insurance GTM angle added
2026-04-20 from Archie competitive intelligence session;
see `docs/research/20260420-archie-competitive-intelligence-prompt.md`.
