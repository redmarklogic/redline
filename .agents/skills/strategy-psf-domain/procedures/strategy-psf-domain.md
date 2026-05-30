# Strategy Psf Domain — Detailed Reference

### Inputs
- Strategic question involving PSF/A/E/C firms (competitor analysis, market segmentation,
  product positioning, build-vs-buy)
- Professional Services Firm Management notebook via `redline-research`

### Outputs
- Domain-grounded strategic analysis that reflects PSF economics, not generic SaaS assumptions

### Out of Scope
- Geotechnical engineering theory (use the Domain Expert and engineering notebooks)
- Code implementation
- PRD writing (`pm-prd-builder`)

### 1. Billable Hours Business Model

**Generic assumption that fails:** Firms generate revenue through product sales, subscriptions,
or licensing.

**PSF reality:** Engineering consultancies generate revenue through billable hours — time spent
by qualified professionals on client projects. Overhead (office, admin, marketing) is funded
from the margin between billing rate and salary cost. Every strategic decision filters through
the question: "Does this increase or protect billable hours?"

**Implication for strategy:** A tool that reduces billable hours is not "efficiency" — it is
revenue destruction unless the firm can redeploy freed hours to higher-value work. Never assume
PSFs want to automate their core deliverables.

### 2. [Cannibalisation Dynamics](../mental-models/strategic_decisions/cannibalisation-dynamics.md)

**Generic assumption that fails:** A company with a strong internal tool can sell it externally
to generate a new revenue stream.

**PSF reality:** An engineering firm that sells a tool automating report production gives
competitors the ability to produce equivalent reports faster and cheaper. The firm loses more
in competitive advantage than it gains in licensing revenue. Cannibalisation is structural,
not optional — it follows directly from the billable hours model.

**Implication for strategy:** When analysing whether an engineering firm will commercialise an
internal tool, default to "no" unless the firm is exiting that service line entirely. This
applies to bespoke AI tools, proprietary calculation sheets, and template libraries.

### 3. Market Segmentation by Firm Tier

**Generic assumption that fails:** All companies in an industry have roughly equivalent
technology capability and would respond similarly to new tools.

**PSF reality:** Civil engineering consultancies segment sharply by size and project type:

| Tier | Staff | Typical projects | AI/tech capability | Build-vs-buy |
|---|---|---|---|---|
| Tier 1 (>500 staff) | Large infrastructure firms | Government, transport, mega-projects | In-house R&D teams, can build | Builds bespoke tools |
| Tier 2 (50-500 staff) | Mid-size firms | Commercial, mixed portfolio | Limited IT, some innovation budget | Evaluates before buying |
| Tier 3 (5-50 staff) | Small/niche firms | Residential, small commercial | No internal AI capability | Buys if affordable, or does without |

**Implication for strategy:** Tier 1 firms are not the target market — they build their own.
Tier 3 firms are the primary market — they cannot build and will buy tools that reduce risk
and increase consistency. Never assume capability is uniform across tiers.

### 4. Professional Indemnity Insurance

**Generic assumption that fails:** Product liability is a downstream legal concern handled by
terms of service.

**PSF reality:** Every engineering consultancy carries professional indemnity (PI) insurance.
PI insurers are actively developing positions on AI-assisted engineering work. Some insurers
may require audit trails showing which content was AI-generated, which was human-reviewed, and
who approved the final output. This is not a Phase 3 concern — it is a Day-1 product
requirement.

**Implication for strategy:** Any product touching engineering deliverables must include audit
trail functionality from inception. Position audit trails as a feature, not compliance
overhead. Query the Risk Assessment in Engineering notebook for the current insurer landscape.

### 5. Engineering Review Workflows

**Generic assumption that fails:** Quality assurance requires separation of duties — the entity
that produces content must not review it (the "who watches the watchmen" objection).

**PSF reality:** Engineering firms routinely use internal review: a senior engineer reviews a
junior engineer's draft within the same organisation. The review is not independent
verification — it is attention-directing. Marked-up drafts with comments (in Word, PDF, or
Bluebeam) are the standard review mechanism. The reviewer and the author work for the same
firm.

**Implication for strategy:** A tool that generates content and then highlights areas requiring
attention mirrors existing engineering practice. The "maker-checker" pattern (generate then
review) is natural to engineers if the review layer directs attention rather than claiming
independent verification. Do not oppose maker-checker on abstract governance grounds.

### 6. Positioning Must Follow Workflow

**Generic assumption that fails:** Product positioning should be pure and focused — do not
claim to do what you aspire to do later.

**PSF reality:** Engineering practitioners work with combined draft-and-review tools daily
(Word with track changes, Bluebeam with markups). A tool that both drafts and reviews is not
a positioning stretch — it reflects how engineers already work. Sequencing features based on
positioning purity rather than practitioner workflow creates artificial gaps that competitors
will fill.

**Implication for strategy:** Sequence product features by practitioner workflow fit, not by
positioning category. If engineers expect draft + review in one tool, deliver draft + review
in one tool, even if it means expanding the initial scope.

## Anti-Patterns

| Anti-pattern | Why it fails | Correct approach |
|---|---|---|
| Treating an engineering firm's internal tool as a competitive product launch | Cannibalisation prevents commercialisation | Query PSF notebook for firm incentive structure |
| Assuming all firms can "just build their own" | Tier 3 firms have zero AI capability | Segment by firm tier before assessing build-vs-buy |
| Applying separation-of-duties to maker-checker | Engineering review is attention-directing, not independent audit | Query PSF notebook for engineering review workflows |
| Treating PI insurance as a downstream concern | Insurers are developing AI-specific positions now | Include audit trail as Day-1 feature requirement |
| Sequencing features by positioning purity | Engineers expect combined draft+review tools | Align product sequencing with practitioner workflow |
| Flagging large firms as competitive threats to a niche product | Large firms serve different project types with different cost structures | Segment by project type and firm overhead before threat assessment |
