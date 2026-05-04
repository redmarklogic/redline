# Parameter Completeness Checking — Advisory Board Session

**Date**: 2026-05-04
**Status**: Final
**Participants**: Founder, Graeme (Principal Geotechnical Engineer), Ron (Strategy & GTM Advisor), Mark (Principal Product Manager), John (Head of Marketing)
**Purpose**: Determine whether parameter completeness checking is in scope for Redline and, if so, how it should be structured, gated, and documented.

---

## Session Purpose

The advisory board convened to resolve a scoping question: should Redline check that geotechnical reports mention all required input/output parameters for a given design type? The session covered taxonomy structure, regional variation, pricing implications, anti-scraping posture, marketing strategy, and integration with the existing Skeleton Generator and Pre-Review products.

## Key Decisions

### 1. Parameter completeness checking is in scope

Redline checks that reports mention all required input/output parameters for the specific design type. This is a presence check, not numeric validation. Both under-inclusion (missing a required parameter) and over-inclusion (including irrelevant parameters that signal copy-paste from a different design type) are failure modes.

### 2. Design-type taxonomy required

Approximately 11 top-level categories and 30 sub-types, each with distinct parameter sets. The Pareto 20% that covers the majority of New Zealand practice: shallow foundations, timber pole retaining walls, slope stability, liquefaction assessment, piled foundations.

### 3. Regional overlays

Canterbury, Auckland, and Wellington have different requirements driven by local seismicity, liquefaction susceptibility, and council-specific standards. Regional variation is an overlay on the base taxonomy, not the primary axis of organisation.

### 4. Parameter placement awareness

Parameters may appear in the report body, appendices, or calculation files. Firms have different conventions for where specific parameters are documented. The completeness checker must be aware of placement context, not just presence in the document.

### 5. Input vs output parameters

Both require checking. Input completeness prevents errors (e.g., a shallow foundation design that never states the bearing capacity assumption). Output completeness prevents ambiguity (e.g., a report that recommends a foundation depth but never states the assumed groundwater level).

### 6. Configurability as business-tier upsell

House Rules (Business tier) allow firms to toggle which parameters to flag. This lets firms encode their internal QA expectations into the tool without Redline dictating a single standard of care.

### 7. Tool A (interactive checklist) rejected

An interactive web checklist that lets users explore the taxonomy was rejected. It exposes the full taxonomy to scraping, undermining Redline's competitive moat.

### 8. Tool B (parameter quick-scan) refined

The free tier shows what parameters are missing. Contextual analysis (where in the report the parameter should appear, why it matters, and how to fix the gap) is paid. The LinkedIn Premium "curiosity gap" model was initially proposed but rejected after Graeme flagged it as a dark pattern inappropriate for engineering practitioners who need actionable information.

### 9. Skeleton Generator integration

The Skeleton Generator embeds parameter prompts as part of its section placeholders (free = teaching the engineer what to include). Pre-Review checks compliance against the taxonomy (paid = verifying completeness after the report is drafted). This separation reinforces the "teach for free, check for pay" principle.

### 10. Robin AI / Lagura analogy dropped

The analogy to Robin AI (legal contract review) and Lagura was useful as an internal mental model during early ideation. It is not appropriate for external communication and has been dropped from all documentation.

### 11. Persona rename: Dave to Prisca

The persona previously named "Dave" has been renamed to "Prisca" across all product documents.

### 12. Anti-scraping triple approach (P-034)

Three-layered defence against taxonomy extraction:

1. Terms of Service prohibition on systematic extraction
2. Detection mechanism for bulk download patterns
3. Anomalous upload pattern detection

Trigger threshold during beta: more than 20 uploads per month per account.

### 13. Taxonomy Query Channel (P-035)

Internal sales enablement tool codenamed "Benton". Three-tier exposure model:

- **Public**: category-level information only (e.g., "foundations")
- **Sales**: family and type-level (e.g., "shallow foundations / pad footings")
- **Product**: full taxonomy with parameter sets

### 14. Conversion path is single-user

Perrie (intermediate engineer persona) is both the user and the buyer of Pro tier. Two financial vehicles exist from Day 1: pay personally with a credit card, or email a purchase request to their manager. KR2 (Key Result 2) must test which path Perrie actually takes.

### 15. Taxonomy maintenance via automated ceremony

Linda (Knowledge Infrastructure Operator) scans standards body feeds weekly for new or revised publications. Graeme validates quarterly for paid standard editions that require manual review. Estimated cost: a few dollars per week for automated scanning plus 15 minutes per quarter for Graeme's validation.

## New Principles Committed

The following principles were agreed during the session and are documented in `docs/product/strategy/principles.md`:

1. **Teach for free, check for pay** — The Skeleton Generator teaches engineers what parameters to include; Pre-Review checks whether they actually did.
2. **Gate on depth, not visibility** — The free tier shows what is missing; the paid tier shows where, why, and how to fix it.
3. **Within each product tier, gate by consumption** — Skeleton is freemium with a quota limit; Pre-Review is fully paid.
4. **Dual purchase path** — Personal credit card and firm expense, both available from Day 1.
5. **Redline does not author engineering opinions** — The tool identifies gaps and flags them. It never states what the correct parameter value should be. Switzerland-neutral.
6. **The senior reviewer is always right** — The tool is subordinate to human engineering judgement. If the reviewer disagrees with a flag, the reviewer wins.

## Pricing (deferred to KR2 discovery)

The following pricing questions remain open and are explicitly deferred to KR2 discovery testing:

- Per-firm vs per-seat pricing model: not a principle yet
- Infrastructure pricing vs SaaS pricing: not a principle yet
- Six purchase-path questions have been added to `docs/product/strategy/discovery-guide.md` Part 5b
- Price points of $20-30/month (Pro) and $40-60/month (Business) are hypotheses, not decisions

## 4-Stream Parallelisation Plan

The implementation is structured as four parallel streams:

1. **Skeleton + Infra** (Sprint 1, current) — Skeleton Generator MVP and platform infrastructure
2. **Rule Engine + taxonomy-free rules** (Sprint 2-3) — Rule engine architecture with rules that do not depend on the taxonomy
3. **Taxonomy discovery** (starts now, parallel) — Graeme-led knowledge work to define the full design-type taxonomy and parameter sets
4. **Parameter completeness rules** (Sprint 3-4) — Plugs into the rule engine once taxonomy is available

## Marketing Insights

John identified the following actions for his next sprint:

- **Big 5 content briefs**: five articles identified covering Pricing, Problems (x2), Versus, and Best in Class categories
- **Product-Led SEO**: parameter quick-scan approved as a modified free tool; interactive checklist rejected
- **LinkedIn post**: practitioner-facing pitch on the parameter gap problem drafted
- **Publish strategy**: two design types published openly to demonstrate domain credibility; remaining types gated behind the product
- **Domain sign-off**: all domain claims in marketing content require Graeme's sign-off before publishing

## Knowledge Documents Created/Updated

Graeme created or updated the following knowledge documents during and after the session:

- Design-type taxonomy expanded (11 categories, approximately 30 sub-types)
- Regional parameter overlays (Canterbury, Auckland, Wellington)
- Input vs output parameter classification
- Parameter completeness scope statement (canonical requirement definition)
- Standard of care context (case law, Eurocode 7, QA checklists)

These are filed under `docs/knowledge/geotechnical/report-writing/`.

## Parked Decisions

Two new parked decisions were added to `docs/product/strategy/decisions/parked-decisions.md`:

- **P-034**: Anti-scraping triple approach (ToS + detection + anomalous pattern monitoring)
- **P-035**: Taxonomy Query Channel ("Benton" internal sales enablement tool)

## Open Risks

1. **Taxonomy maintenance for paid standards** — Mitigated by Standards NZ/AU notification feeds, but requires ongoing Graeme validation for paid editions.
2. **Auckland and Wellington regional requirements are knowledge gaps** — Needs Linda to research council-specific geotechnical requirements.
3. **False precision risk** — If the taxonomy boundary between sub-types is fuzzy, showing quantitative completeness scores may mislead. Mitigation: show qualitative assessment (e.g., "key parameters missing") rather than counts.
4. **Conversion path assumption** — KR2 must test whether Perrie pays personally or expenses through the firm. The dual-path design hedges this, but marketing messaging differs depending on the dominant path.

## Cross-References

- [principles.md](../product/strategy/principles.md)
- [pricing-methodology.md](../product/strategy/pricing-methodology.md)
- [discovery-guide.md](../product/strategy/discovery-guide.md)
- [parked-decisions.md](../product/strategy/decisions/parked-decisions.md) (P-034, P-035)
- [strategic-bets.md](../product/strategy/strategic-bets.md) (Bet 2, Bet 3)
- `docs/knowledge/geotechnical/report-writing/` (5 knowledge documents)
