# Positioning — Redline

**Status**: Draft v1. **Owner**: Ron.

## One-Sentence Positioning

> For NZ and AU geotechnical engineers, Redline is the neutral quality layer that catches
> what a senior reviewer would catch — without writing the report, taking a position, or
> arbitrating disputes.

## Positioning Frame

We position Redline against three categories of incumbent, deliberately:

| Category | Incumbent example | How Redline differs |
|---|---|---|
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
- "Productivity tool", "writing assistant" — wrong category, wrong price ceiling.
- "Compliance" as a noun for what we deliver. We assist compliance work; we do not
  attest to compliance.

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
("what a senior reviewer would catch") rather than the *product category* ("AI
assistant"). Head-on comparisons invite the incumbent's attention; job-framing keeps
us invisible until the beachhead is dominated.

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
