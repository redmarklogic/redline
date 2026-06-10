# Strategic Bets — H2 2026

**Status**: Draft v2. **Owner**: Ron. **Period**: 2026-06-01 → 2026-11-30.

**Constraint**: Founder's first official day is 2026-06-01. All kill-criterion
timelines count from that date.

**Exception (A-13, decided 2026-06-10)**: Bet 1's kill clock anchors to Launch Day
as defined in Bet 1, not 2026-06-01. The 2026-07-31 launch backstop preserves
time-boundedness — the bet cannot drift indefinitely while waiting for launch.

Six bets. Each bet is a falsifiable claim with a kill criterion. If a bet's kill criterion
trips, the bet is dead — we do not revive it without a new grounding pass.

---

## Bet 1 — The Free Skeleton Wedge Beats Paid Acquisition

**Bet**: A free, SSO-gated GBR/GIR Skeleton Generator (capped 3–5 docs × 100 pages per
verified user) acquires intermediate engineers at lower cost than Google Ads or LinkedIn
outbound, *and* converts to paid Pre-Review at a higher rate than cold acquisition would.

**Why it might be true**: Skeleton generation is the natural first step in the GBR
workflow per `docs/research/20260412-report-drafting-initiation-workflow.md`. Quota
exhaustion creates a defensible moment for an outbound conversation. Marginal cost per
quota-exhausted user is $0.10–$1.

**Assumption stack**:

- Intermediate engineers will give a verified work email for a useful skeleton.
- ~~Quota-exhausted users will respond to a founder-led outbound email at ≥ 10%.~~
  **Revised 2026-05-09.** Founder-led outbound is a co-development motion capped at
  10 feedback partners, not a sales-at-scale motion. The founder contacts free-tier
  users via email or LinkedIn to recruit co-development partners. See 10→100→1000
  phasing below.
- ~~At least 1 in 5 responders will book a paid Pre-Review trial.~~ **Revised
  2026-05-09.** Phase 1 goal is 10 active feedback partners (paid or not).
  Monetisation test pushed to Phase 2.
- Target engineers can access `redline.[domain]` from their work machines. *(added
  2026-04-22, enterprise AI blocking risk assessment)* Network-level AI blocking at
  MSP-managed firms or firms using Microsoft Defender for Cloud Apps could prevent
  user acquisition. See `enterprise-ai-blocking-risk-assessment.md`.

**Kill criterion** *(re-anchored 2026-06-10, A-13)*: 90 days after Launch Day, fewer
than 50 verified-email signups. **Launch Day** is the first day the Skeleton Generator
is publicly reachable in production **AND** the SSO-gated verified-email signup flow
(B-1b, issue #73) is live — the day the kill metric becomes measurable. The
skeleton-ship date alone does not start the clock. **Launch backstop**: if Launch Day
has not occurred by **2026-07-31**, Bet 1 enters a mandatory bet review (founder, Ron,
Peter) with the same standing as a tripped kill criterion, ending in either a single
re-committed Launch Day or a kill decision. The 90-day clock starts once and cannot be
reset by re-launching. *(Ron, 2026-06-11: founder briefly set the backstop to
2026-06-29; I flagged that date precedes the 2026-06-30 skeleton ship target and would
fire in every realistic scenario. Founder reverted to 2026-07-31 the same day.)* The signup count is
the authoritative trigger; the activation rate in KR1 is a
product-quality metric that informs iteration, not a bet-kill signal. ~~The outbound
response rate criterion has been removed~~ *(revised 2026-05-09)* — the founder-led
outbound motion is a co-development partnership recruitment (capped at 10), not a
scalable sales motion. Outbound response rate is not a meaningful kill signal at
this scale.

**10→100→1000 phasing** *(added 2026-05-09, founder brainstorm)*:

- **Phase 1 (10 customers)**: Founder personally recruits up to 10 feedback partners
  from free-tier users via email or LinkedIn. Goal is co-development and removing
  roughness. Paid or not — partnership for feedback is the priority. Duration: ~90
  days from launch.
- **Phase 2 (100 customers)**: Opens up acquisition. Referral/viral loop hypothesis:
  users can share the tool and earn extra credits when their referral logs in.
  Monetisation test begins. Self-serve Pro purchase path activates.
- **Phase 3 (1000 customers)**: Full scale.

**Phase 1 → Phase 2 transition gate** *(added 2026-05-09)*:

- **Hard gate (Repeat Usage)**: By day 90 of Phase 1, at least 7 of 10 feedback
  partners have returned unprompted to generate a skeleton for a second distinct
  project within 30 days of their first generation.
- **Supporting signal (Senior Endorsement)**: By day 90, at least 3 distinct firms
  among the 10 have a senior/principal engineer who has reviewed a Redline-generated
  skeleton and confirmed it met their firm's structural and legal standards without
  requiring structural rework.

**Competitive validation** *(added 2026-04-20, Archie CI session)*: Archie (NZ-based
AI geotechnical report tool) validates that AI-driven geotechnical report tooling has
real market demand. Archie writes drafts; Redline checks them — different jobs, same
market signal. PLG vs enterprise sales is a durable acquisition advantage: zero-friction
onboarding (upload report, see skeleton) reaches engineers that bespoke agency models
(SupaHuman's sales-call-plus-contract) will never talk to. Provenance:
`docs/research/20260420-archie-competitive-intelligence-prompt.md`.

**One-click UX decision** *(added 2026-04-22, founder-approved)*: Sprint 1 UX confirmed
as one-click LOE upload with LLM metadata extraction and live progress indicator. No
manual-input form. This reinforces the PLG acquisition advantage — every form field is
an abandonment point; one-click upload is the only version that delivers the zero-friction
onboarding this bet depends on. The progress indicator ("Extracting metadata... Building
sections... Applying standards...") doubles as in-product marketing copy, teaching users
what Redline does while it works. See PRD decision log (2026-04-22).

**OKR ladder**: `okrs/2026-h2.md` → KR1 (signups — warning signal at 60 days; kill
criterion at 90 days), KR2 (founder-led qualified conversations for co-development),
KR3 (10 active feedback partners).

---

## Bet 2 — Pre-Review Mode Is the Paid Product Day-1

**Bet**: Intermediate engineers will pay for an inline annotation engine (Pre-Review)
that flags what a senior reviewer would mark up, *before* we have an Adversarial Scan
or House Rules engine.

**Why it might be true**: Day-1 ICP pain is reviewer-bottleneck pain (per
`jtbd.md`). Pre-Review attacks that bottleneck directly. Adversarial Scan attacks a
Phase-2 buyer (Partner) we are not yet credible to.

**Assumption stack**:

- A rule library covering 20-30 common reviewer markup patterns is sufficient to deliver
  perceived value (we do not need 200).
- ~~Word task pane integration is acceptable to the engineer's workflow.~~ **Parked
  (2026-04-19).** Web interface only in H2. Word task pane desirability will be
  re-evaluated during KR2 discovery interviews. See `decisions/parked-decisions.md`
  P-024.
- Firm IT will permit the integration without a 6-month security review for self-serve
  Pro-tier seats. *(Risk upgraded 2026-04-22)*: Microsoft Defender for Cloud Apps
  provides exactly the kind of automated security review that could block Pre-Review
  before anyone requests a trial. An IT Justification Brief (see
  `enterprise-ai-blocking-risk-assessment.md` section 2.3) mitigates this directly.

**Rule taxonomy refinement — structural presentation completeness** *(added
2026-04-23)*: Government procurement debrief feedback from the NZ engineering sector
confirms a recurring failure mode: engineers have the right technical content but lose
marks because they don't articulate it with sufficient structural specificity. Panels
penalise missing worked examples, missing decision matrices, missing severity
taxonomies, and missing governance diagrams — even when the underlying reasoning exists
in the narrative. This pattern maps directly to GBR/GIR senior review: intermediates
draft risk assessments without severity classifications, compare options without
decision matrices, and describe QA processes without distinguishing automated from
manual controls. The initial 20-30 rule library should therefore include not only
*technical correctness* checks (wrong standard cited, missing reference) but also
*structural completeness* checks — rules that flag when a section makes a claim or
describes a process without the structural artefact a senior reviewer would expect to
accompany it. Validate via KR2 discovery interviews (see `discovery-guide.md`,
structural completeness probe).

**Scope-limitation rule pattern** *(added 2026-05-10, Graeme/Ron)*: CEAS Indemnity
Matters Issue 88 (April 2026) issued a PS4 Practice Advisory on altered Producer
Statements with unclear scope definitions for construction monitoring. Graeme confirms
this maps directly to a recurring GBR/GIR quality failure: conclusions sections that
make claims about site conditions without qualifying investigation scope. The risk
literature identifies this as one of the two primary categories of professional liability
claims --- "improper use of information and advice is a more frequent cause of claims
than inaccurate information or wrong advice." Pre-Review rules address this through
three mechanisms: (1) mandatory clause presence checks (inferred conditions caveat,
temporal boundaries, groundwater, changed conditions, third-party reliance,
standard-of-care), (2) scope-conclusion consistency checks (LLM-assisted: flag
conclusions that extend beyond stated scope), and (3) taboo word detection in
conclusions (absolute/subjective words that imply completeness the investigation cannot
support). Candidate rule shape: *"when section type = Conclusions or Limitations and
report scope includes ground investigation, construction monitoring, or foundation
design, flag if no explicit scope limitation statement is present."* The 1979 CEAS case
study reprinted in the same issue --- engineer sued for failing to qualify investigation
limitations --- validates that this failure mode has persisted for nearly 50 years.
Provenance: CEAS Indemnity Matters Issue 88; Graeme notebook-grounded assessment
(Risk Assessment in Engineering, GBR, Report Workflows notebooks).

**Kill criterion**: After Sprint 4, ≥ 50% of free-tier Skeleton converters refuse to
trial Pre-Review when prompted. Indicates the value prop does not extend from skeleton
to review.

**Insurance bifurcation** *(added 2026-04-20, Archie CI session)*: Some NZ insurers are
offering affirmative AI policies; others are inserting absolute exclusion clauses. This
bifurcation upgrades audit trail from a Phase-2 feature to a Day-1 product requirement.
GTM angle: "Redline gives you the audit trail your insurer will ask for." Feature L
(Audit Log) core subset elevated to Sprint 1 accordingly --- see `feature-backlog.md`.

**AI report review — compounding cognitive load** *(added 2026-05-14, Graeme + Ron)*:
Reviewing AI-generated reports carries a higher per-sentence cognitive load than
reviewing human-written reports — even when the English is perfect. With a known human
author, the reviewer applies a trust model built over time and uses pattern recognition
to allocate attention. With AI, that model does not exist. Errors are not correlated
with style, confidence, or fluency. The reviewer cannot skim. Every sentence is, in
effect, from an unknown author with no track record.

The class of errors AI introduces is specifically difficult to catch: fabricated
citations that look authoritative (e.g., NZS 4407:2015 for SPT — a roading standard),
correct-range-but-wrong values (plausible SPT N-value, wrong borehole), method-correct
but context-wrong (valid design method applied to wrong soil classification), and fluent
interpolation beyond the data (ground conditions between investigation points stated as
fact, not inference).

**Strategic implication**: as AI-generated report volume increases, the "without
Redline" baseline worsens — not stays constant. The senior engineer's total review
time for an AI-written report is higher than for a human-written report. Redline's
delta therefore grows with AI adoption. This is a compounding value story, not a
one-time efficiency story. The before/after value framing should reflect three
scenarios: (1) human-written report, (2) AI-written report without Redline, (3)
AI-written report with Redline. Scenario 2 is the ceiling that makes the Redline
pitch largest.

**Scope of the compounding story (important constraint):** Redline eliminates the
harder compliance mechanics in AI-written reports. It does not reduce the difficulty
of the engineering judgment layer — that remains harder than for human-written reports
because the reviewer still cannot apply a trust model to AI output. After Redline
runs, the senior engineer reviewing an AI-written report is back to doing their real
job — but their real job is harder when the input was AI-generated. Do not present
the compounding value story in a way that implies Redline fully normalises an
AI-written report's review burden back to the human-written baseline. It does not.
Provenance: `docs/research/20260420-archie-competitive-intelligence-prompt.md`.

**Insurance-industry AI scrutiny signal** *(added 2026-05-10, Ron)*: CEAS Indemnity
Matters Issue 88 (April 2026) directly asks NZ consulting engineers: "How open are you
with your clientele about your use of AI? And are your reports factually correct?" This
question comes from Aon --- the engineers' PI insurance provider. Two cautionary tales
cited: Deloitte repaying part of a $440k AI-error report; a WA lawyer referred to the
regulator for AI-generated fake citations. The tone is cautionary, not exclusionary ---
but the direction of travel is clear. This is a leading indicator for the insurance
bifurcation thesis: the insurance industry is actively asking engineers about AI usage
and report accuracy. If more engineering-specific cases emerge, the industry could shift
from cautionary questions to explicit exclusion clauses or premium increases for firms
that disclose AI usage without a demonstrable QA layer. Favourable for Redline if the
audit trail exists. Provenance: CEAS Indemnity Matters Issue 88, April 2026.

**Sign-off via OOXML metadata** *(added 2026-05-06)*: Feature L full scope (Sprint 5+)
will implement reviewer sign-off using OOXML document metadata (`customXmlParts`)
embedded in the .docx itself --- not a separate database record. This stores the
sign-off audit trail inside the document, making it portable and insurer-readable.
Conditional on P-024 (Word task pane) unfreezing, since the sign-off interaction
requires an in-Word surface.

**Adjacent-market watch item — legal AI playbooks** *(added 2026-04-26)*: Leya's
playbook-driven review (firm legal teams encode rules with approved language and
fallback positions; AI marks up deviations; lawyer approves) validates the House Rules
concept. Legal playbooks create compounding value through accumulated configuration ---
the same dynamic Redline expects from firm-specific House Rules. Validate playbook
adoption appetite via KR2 discovery: "Would your firm encode its review standards in a
tool, or is that knowledge too tacit?" Provenance:
`docs/research/20260426-legal-ai-adjacent-market-signal.md`.

**Adjacent-market watch item — Word-native integration** *(added 2026-04-26)*: Leya's
Word add-in (right-hand pane, reads document, creates edits, applies playbooks) is
central to adoption because lawyers live in Word. Engineers also live in Word/PDF.
**Adjacent-market watch item — starter rules framing** *(added 2026-04-27, Leya internet
research)*: Leya ships standard playbooks out of the box that firms can immediately use
or customise. Redline's 20–30 rule library IS a starter playbook by another name. The
framing matters: (1) it signals rules are customisable, not fixed vendor decisions;
(2) it creates a natural upgrade path to House Rules ("you've been using our starter
rules — now encode your own"); (3) it anchors KR2 discovery ("here are our starter
rules — which would you change?"). Action: position the Pre-Review rule library as
"starter rules" in product copy and onboarding from Sprint 1. Naming change only; no
scope change. Provenance:
`docs/research/20260426-legal-ai-adjacent-market-signal.md`.

**Architecture watch item — model-agnostic LLM routing** *(added 2026-04-27, Leya
internet research)*: Leya routes queries to OpenAI and Anthropic, selecting the best
model per task type (not single-vendor). When formalising LLM infrastructure in
Sprint 1–2, model-agnostic routing should be the default posture — different models
for rule-matching, linguistic analysis, and summarisation. Avoids vendor lock-in and
enables per-query-type cost optimisation. No H2 scope change; implementation decision
only. Provenance:
`docs/research/20260426-legal-ai-adjacent-market-signal.md`.

**Adjacent-market convergence note** *(added 2026-04-27)*: Legal and geotechnical
engineering have independently converged on the same document-review interaction
pattern: select rule set → run against document → review flagged deviations. This is
not an analogy — it is a confirmed interaction model. "Playbook" is the correct
abstraction for what the Pre-Review rule library does. Strengthens conviction that
the Pre-Review → House Rules upgrade path is architecturally correct.

**Adjacent-market watch item — Legora/Microsoft comparable** *(added 2026-05-03;
updated 2026-05-04: Robin AI dropped per founder direction)*:
Legora and Microsoft Word Legal Agent strengthen the Pre-Review → House Rules
hypothesis. They validate playbook-driven review, source-linked markup, preserved
document fidelity, and human approval as the interaction model for high-liability
document work. They do not change the product problem. For H2, Redline should test
whether high-fidelity DOCX output, comments, tracked changes, and source-linked
review notes are sufficient before unfreezing the Word task pane. No scope change.

**Professional-boundary guardrail** *(added 2026-05-03, Graeme)*: Legal-AI-style
workflow expansion is allowed only where Redline remains a quality and traceability layer.
Safe expansion includes document-native review, comments, tracked changes,
source-linked flags, audit trail, standards references, and House Rules. Unsafe expansion
includes autonomous engineering recommendations, GBR baseline setting, compliance
attestation, or arbitration between author and reviewer. Provenance:
`docs/knowledge/geotechnical/contracts-and-risk/ai-workflow-expansion-boundaries.md`.

**OKR ladder**: KR3 (paid conversion), KR4 (retention).

**Pre-Submission freemium angle** *(added 2026-05-13, checklist collection analysis)*:
Council lodgement checklists (CERT 10a, Lodgement Checklist Commercial, Mason County) are
public, non-copyrighted documents defining the minimum submission bar. A free Pre-Submission
checker that validates against council-specific checklists would acquire users at zero CAC
and create a natural upsell path to Pre-Review: "Your report passes the council gate, but
here are 12 quality issues a peer reviewer would find." This is a Phase 2 product surface
that reuses the Pre-Review parsing pipeline at Depth 1 only (presence checks). Council
checklists are copyright-free rule sources. See
`docs/product/initiatives/pre-submission-council-compliance-checker.md`. Provenance:
`docs/research/20260513-checklist-collection-analysis.md`.

---

## Bet 3 — Standards Knowledge Store Is the Real Moat

**Bet**: A curated, versioned, jurisdictional Standards Knowledge Store (NZS 3910, AS
4000, AS/NZS 4122, NZGS, ACENZ guidance) is the asset competitors cannot replicate in
under 12 months. Every paid feature compounds on it.

**Why it might be true**: Per
`docs/research/20260413-standards-registry-knowledge-architecture-gaps.md`, standards
knowledge is fragmented, jurisdiction-bound, and underspecified in public LLMs. A
curated registry is a defensible asset.

**Assumption stack**:

- A small standards corpus (10–15 documents) is enough to materially improve skeleton
  and Pre-Review output for NZ GBR work.
- Maintenance load is hours per quarter, not weeks per month.
- Standards licensing does not block resale of derived guidance.

**Architecture decision (locked 2026-04-19)**: The Standards Knowledge Store is
**internal-only and citation-only**. It stores clause references and applicability
mappings — never full proprietary text. It is never exposed as a public-facing query
interface. This is confirmed professionally defensible by Graeme (high confidence).
See `docs/adr/adr-006-standards-knowledge-store-citation-only-internal-architecture.md`
and `docs/knowledge/geotechnical/standards-and-codes/nz-au-standards-ip-classification.md`.

**Mode-neutral data model requirement** *(added 2026-05-03)*: The Standards Knowledge
Store data model must not embed new-design-only assumptions. In H2, the store serves
"before the fact" (new design) only, but the schema must accommodate "after the fact"
(assessment of existing infrastructure) in Phase 2 — including historical standard
versions, reduced compliance thresholds (%NBS), and legislative definitions. Project
type is stored as a metadata field from Sprint 1 for future routing. See
`docs/product/strategy/decisions/decision-002-before-vs-after-the-fact.md`.

**House Rules shape — conditional structural expectations** *(added 2026-04-23)*:
Debrief analysis of lost NZ government engineering procurements reveals that firm-level
quality expectations are not flat checklists but **conditional structural requirements**:
"every risk section must include a severity classification", "every options analysis
must include a decision matrix", "every QA description must distinguish automated from
manual controls." These expectations live in senior engineers' heads and are enforced
inconsistently through ad-hoc review markup. The House Rules engine data model must
support conditional rules of the form *"when section type = X and claim type = Y,
require artefact Z"* --- not just global toggles. This gives House Rules a concrete
first use case: encoding the structural presentation standards that differentiate a
draft that survives senior review from one that gets sent back. Firms that encode
these rules experience compounding value through accumulated configuration (per
`knowledge-tier-architecture-brief.md`) --- the system gets better the longer they
use it, and the cost of re-teaching a new system grows over time.

**Kill criterion**: Licensing review (P-026) concludes that even citation-only internal
use of NZS/AS standards content requires a licence Redline cannot obtain or afford.
Bet dies; refactor to public-LLM-only grounding with no curated corpus.

**Adjacent-market watch item — point solutions collapse** *(added 2026-04-26)*: In
legal tech, fragmented point solutions (templating, translation, redlining, research)
became obsolete when generative AI could cover all text-processing workflows. The
Standards Knowledge Store is what prevents Redline from being a point solution ---
without it, any generic LLM wrapper could replicate Pre-Review output. The curated,
jurisdictional, versioned corpus is what makes the quality layer domain-specific and
defensible. Provenance:
`docs/research/20260426-legal-ai-adjacent-market-signal.md`.

**OKR ladder**: Underwrites all KRs; not directly metered.

**Council checklist catalogue as sourcing strategy** *(added 2026-05-13, checklist
collection analysis)*: NZ/AU/US council geotechnical checklists are public, non-copyrighted
documents. They provide a free, low-risk starting corpus for the Standards Knowledge Store:
encode council checklist rules as Depth 1 (presence) checks, then layer Depth 2 (content
quality) rules from professional standards on top. This avoids the licensing risk (P-026)
for the initial rule library while still demonstrating the Knowledge Store architecture.
Council checklists also validate the shared taxonomy (ADR-007) empirically --- 10 checklists
from 5 jurisdictions converge on the same 10-node taxonomy. Provenance:
`docs/research/20260513-checklist-collection-analysis.md`.

---

## Bet 4 — Switzerland-Neutral Positioning Wins Inside Firms

**Bet**: Positioning Redline as a *neutral quality layer* (does not author, does not
opine, does not arbitrate) — rather than as an "AI engineer" or "AI reviewer" —
removes the political resistance that kills bottoms-up SaaS adoption inside
professional-services firms.

**Why it might be true**: Senior engineers feel threatened by tools that author content;
they do not feel threatened by tools that surface issues for human resolution.
Procurement gatekeepers approve infrastructure faster than they approve "AI tools".

**Assumption stack**:

- Junior/intermediate engineers will champion a tool framed as a self-check rather than
  hide it from seniors.
- Firm Principals will allow the tool when the framing is "checks our house standards"
  rather than "writes reports".

**Kill criterion**: After 30 founder-led conversations, < 30% of intermediate engineers
say they would tell their senior they use it. Indicates the positioning does not survive
contact with the actual buying committee.

**Enterprise IT survival** *(added 2026-04-22, enterprise AI blocking risk assessment)*:
The Switzerland-neutral positioning must survive not just the buying committee but also
the IT committee. Microsoft Defender for Cloud Apps categorises tools by perceived
function; if Redline lands in the "Generative AI" category, IT teams will default-block
it regardless of the positioning's success with engineers. The lexicon ("quality layer",
"infrastructure, not SaaS") is now blocking-survival language, not just sales language.
See `enterprise-ai-blocking-risk-assessment.md` section 2.1.

**Adjacent-market watch item — senior-sponsor GTM** *(added 2026-04-26)*: Leya's
GTM confirms that bottom-up adoption is blocked in high-liability professional firms
(procurement, security, privacy gates). Their playbook: sell to a senior partner or
innovation lead, make one team visibly successful ("rock stars"), let others follow.
This reinforces Switzerland-neutral positioning --- the tool must be something a
principal would endorse, not something a junior hides. First login impression is
critical. Provenance:
`docs/research/20260426-legal-ai-adjacent-market-signal.md`.

**OKR ladder**: KR2 (qualified-conversation rate).

---

## Bet 5 — NZ + AU Year One, No Geographic Expansion (Beachhead Doctrine)

**Bet**: Concentrating Year-1 GTM on NZ and AU markets (shared standards heritage,
proximate procurement culture, founder's network) outperforms any attempt to add a third
geography in the same window.

**Why it might be true**: Localisation Penalty (per the prioritisation framework) is the
single highest scalability risk in this product. Each new geography requires a Standards
Knowledge Store rebuild and contract-law context shift.

**Reinforcement (Moore, *Crossing the Chasm*)**: Pragmatist buyers in professional
services rely on within-segment word-of-mouth; they will not reference a vendor whose
customers are scattered across geographies and disciplines. Moore's threshold for
"dominating" a beachhead is **≥ 50% of new sales in that segment over a year**. Until
that threshold trips for NZ + AU geotech, every cross-segment opportunity dilutes the
reference base that mainstream pragmatists demand. Adjacent segments come later via the
*bowling pin* path (Moore): expand from geotech-NZ-AU into either (a) AU adjacent
disciplines that share the same firms, or (b) a third geography that shares NZ/AU
standards heritage. Both paths are Phase-2 conversations, not H2.

**Kill criterion**: A non-NZ/AU prospect signs an LOI worth ≥ $50k ARR before Sprint 6.
At that point, re-evaluate. Until then, decline the geography.

**OKR ladder**: Implicit constraint on KR1 and KR3.

---

## Bet 6 — New-Market Disruption Against Nonconsumption (Christensen Frame)

**Bet**: Redline competes against *nonconsumption* — geotechnical consultancies do not
currently buy software for the senior-review / quality-layer job; they consume senior
engineer hours. Framing Redline as a *new-market disruption* (Christensen) — rather than
as a feature competing against ChatGPT, Microsoft Copilot, or Autodesk — is what keeps
incumbents asleep long enough for the wedge to mature.

**Why it might be true**: New-market disruptions take root in segments invisible to
incumbent P&Ls. A senior-review-quality-layer for NZ/AU geotechnical reports is too
specific and too small to register on Autodesk's or Bentley's roadmap. By the time it
is large enough to register, the Standards Knowledge Store and House Rules moat
(Bet 3) is years deep.

**Assumption stack**:

- The job is genuinely "nonconsumption" today (validated through KR2 — confirm engineers
  are paying for senior review hours, not for tooling).
- No incumbent (Autodesk, Bentley, Microsoft, OpenAI) treats geotech-specific QA as a
  *sustaining* innovation worth a roadmap line in the next 24 months.
- The wedge can grow within the beachhead before incumbent attention arrives.

**Kill criterion (the Christensen litmus)**: An incumbent (Autodesk, Bentley,
Microsoft, OpenAI, or a geotech-vertical SaaS) publicly announces or ships a feature
that addresses the senior-review-quality job for geotechnical reports as a sustaining
innovation in their existing product line. At that point, Redline is in a sustaining
fight against a well-resourced incumbent — Christensen's theory predicts we lose. We
then pivot positioning to a defensible adjacent (Adversarial Scan / litigation
surface, where incumbents have no posture).

**Named watch item: Beca / Frankly.AI** *(added 2026-04-20, Archie CI session)*:
Beca built Frankly.AI as an in-house AI project and launched it as a commercial service via
Microsoft Teams globally. It has since been discontinued. Assessed as non-threatening for
three reasons: (1) cannibalisation problem — selling the tool helps competitors; (2)
asymmetric motivation — Beca's infrastructure cost structure cannot serve
residential/commercial geotech; (3) Frankly.AI is now discontinued, confirming that
engineering consultancies lack the DNA to sustain AI product commercialisation alongside a
billable-hours business model. If Beca or another Large firm reverses this pattern and
ships a commercially available geotech QA tool, this kill criterion trips.

**Market segmentation clarification** *(updated 2026-05-03, canonical naming)*:
Large firms (T+T, WSP, Beca — 500+ employees, government projects, high overhead)
will build their own AI and require enterprise SOC2. They are not Redline's market.
Small firms (Soil & Rock, EGL — 5-50 employees, residential/commercial geotech) must
buy. This is Redline's market. Current Small-firm alternatives: manual review, SupaHuman
bespoke ($50k+), or ChatGPT (no jurisdiction, no audit trail). SupaHuman is a generalist
agency (same RAG does travel and geotech) with one named engineering client after 2+
years and potential exclusivity with Soil & Rock. Provenance:
`docs/research/20260420-archie-competitive-intelligence-prompt.md`.

**Litmus uncertainty**: Whether each incumbent would *actually* see this as sustaining
is itself a contested question. Logged under `decisions/parked-decisions.md` P-018.

**Incumbent signal — Microsoft Word Legal Agent** *(added 2026-05-03)*: Microsoft
shipping a legal workflow agent inside Word is a platform-incumbent signal, but it does
not trip this bet's kill criterion. The kill criterion is geotech-specific senior-review
quality for GBR/GIR documents, not generic legal redlining or Word-native document
assistance. Treat Microsoft as proof that generic Word review will commoditise, and keep
Redline focused on geotechnical standards, House Rules, audit trail, and NZ/AU beachhead
workflows. Provenance:
`docs/research/20260503-microsoft-word-legal-agent-robin-ai-legora-signal.md`.

**OKR ladder**: Underwrites Bet 4 (positioning) and Bet 5 (beachhead).

---

## Bet 7 — "The Verification Shift" Positions Redline as the Category-Defining AI Review Platform for Civil Engineering

**Bet**: The problems AI is creating for software development teams today (verification
bottleneck, batch size inflation, expertise paradox, culture amplification) will manifest
in civil engineering report production within 12-18 months. Firms that recognise this
pattern and invest in verification infrastructure now will have competitive advantage.
Redline, positioned at the intersection of geotechnical engineering and AI workflow
expertise, becomes the category-defining verification platform by translating lessons
from software (DORA 2024-2026) into actionable tools and thought leadership for civil
engineers.

**Why it might be true**: Ground Engineering magazine (March 2026) documents that Mott
MacDonald (EMMA), Arup (ProjectGPT), and A-squared Studio are already deploying AI for
report generation. The "intelligent editor" role shift is named explicitly in the
industry press. Jim De Waele (BGA) and Domenico Lombardi (A-squared) have publicly
raised the junior engineer training gap. A leading NZ consultancy is already building
an automated pre-review tool ("Faultless"). The pattern mirrors DORA's finding that AI
adoption increases throughput while degrading stability -- and Redline's Pre-Review
product directly addresses the verification bottleneck this creates.

**Assumption stack**:

- The DORA-documented pattern (increased throughput + decreased stability from AI
  adoption) transfers from software development to civil engineering report production.
- Civil engineering firms will experience reviewer strain from AI-generated report
  volume within 12-18 months of adopting AI writing tools.
- Thought leadership positioning at the software-engineering intersection is credible
  and differentiated -- few people have expertise in both domains.
- LinkedIn content translating DORA findings into civil engineering terms will generate
  engagement and inbound interest from engineering leaders.

**Kill criterion**: After 6 months of consistent LinkedIn content (by 2027-01-01),
fewer than 3 inbound enquiries or speaking invitations from engineering firms or
industry bodies referencing the "verification shift" framing. Indicates the theory
resonates in software circles but does not transfer to the civil engineering audience.

**Cross-references**: See
`docs/knowledge/geotechnical/report-writing/ai-verification-shift-evidence.md` for GE
magazine evidence. See
`docs/research/software-development/20260526-accelerate-problem-diagnosis-ai-era.md`
for the DORA structural mapping. Reinforces Bet 2 (Pre-Review as paid product) -- this
bet provides the thought leadership and market education that makes Bet 2's value
proposition legible to buyers.

**OKR ladder**: KR5 (thought leadership engagement -- to be defined).

---

## Provenance

Bet 1, 2, 4, 5 are strategy synthesis grounded in
`docs/research/20260418-founder-memos-strategy-grounding.md`. Bet 3 is grounded in the
standards-registry research files cited inline. Bet 5 reinforcement (Moore beachhead
doctrine) and Bet 6 (Christensen new-market disruption framing) grounded in queries
against the entrepreneurship-startup-strategy notebook on 2026-04-18. Bet 1 competitive
validation, Bet 2 insurance bifurcation, and Bet 6 named watch items and market
segmentation added 2026-04-20 from Archie competitive intelligence session;
see `docs/research/20260420-archie-competitive-intelligence-prompt.md`.
Bet 7 grounded in DORA 2024-2026 research
(`docs/research/software-development/20260526-accelerate-problem-diagnosis-ai-era.md`)
and Ground Engineering magazine March 2026 AI coverage
(`docs/knowledge/geotechnical/report-writing/ai-verification-shift-evidence.md`).
