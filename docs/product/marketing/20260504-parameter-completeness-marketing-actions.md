# Parameter Completeness — Marketing Action Plan

| Field | Value |
|---|---|
| Owner | John (Head of Marketing) |
| Date | 2026-05-04 |
| Source | Parameter completeness advisory session |
| Status | Planned (next sprint) |
| Personas | Anna, Perrie, Prisca |

## Messaging Hierarchy

- Headline: "Redline knows what 'complete' means for your specific design type. ChatGPT does not."
- Never say "Redline catches what your senior reviewer catches" — this threatens Prisca's identity.
- Always frame as "handles the checklist so your reviewer can focus on engineering judgment."

## Key Constraint

Robin AI / Legora analogy is internal-only. Never reference in any external content.

## Action 1: Big 5 Content Briefs (5 articles)

| Field | Value |
|---|---|
| Location | `docs/product/marketing/the-big-5/` |
| Status | Planned (next sprint) |
| Dependency | Graeme sign-off on all domain claims (marketing-ai-content-review, non-negotiable) |
| Dependency | Persona validation (P-029) — briefs flagged as "pending persona validation" until KR2 confirms personas |

Articles identified in session:

1. **"What Does a Missing Parameter Cost Your Firm?"**
   Bucket: Pricing. Target: Anna.

2. **"Why ChatGPT Cannot Review Your Retaining Wall Design Report"**
   Bucket: Problems. Target: Perrie, Prisca.

3. **"The 5 Parameters Intermediate Engineers Forget Most Often in NZ Residential GIR Reports"**
   Bucket: Problems. Target: Perrie, Prisca.

4. **"Redline vs ChatGPT for Geotechnical Report Review: What Gets Missed"**
   Bucket: Versus. Target: Anna, Prisca.
   **Status: Deferred** — parked per P-031 (do not publish until all three P-031 unfreeze conditions are met: working product live, real reproducible side-by-side test, founder review).

5. **"What a Complete Timber Pole Wall Report Looks Like: The Parameter Checklist"**
   Bucket: Best in Class. Target: all.

## Action 2: Product-Led SEO — Quick-Scan Documentation

| Field | Value |
|---|---|
| Location | `docs/product/marketing/seo/` |
| Status | Planned (next sprint) |

Document the approved quick-scan approach:

- Interactive parameter checklist tool (Tool A): REJECTED — exposes taxonomy to scraping.
- Parameter quick-scan (Tool B): APPROVED with modifications — gate on depth, not visibility.
- Launches AFTER Skeleton Generator proves acquisition model (not H2 priority).
- Requires keyword research validation before briefing Mark.

## Action 3: Founder LinkedIn Post Draft

| Field | Value |
|---|---|
| Location | `docs/product/marketing/messaging/` |
| Status | Planned (backlog) |
| Dependency | Graeme sign-off on domain claims |

Draft the practitioner pitch post:

> "Every senior reviewer has a list of things they check first. For a timber pole wall in Canterbury, it includes embedment depth. For a cantilever abutment in Auckland, that parameter does not even appear..."

Requirements:

- Text-only, under 150 words.
- Soft signal, not a pitch.
- Follows 10:1 LCS (Like, Comment, Share) rule.

## Action 4: Open Taxonomy Publish Strategy

| Field | Value |
|---|---|
| Location | `docs/product/marketing/seo/` |
| Status | Planned (next sprint) |

Strategy for publishing 2 design types openly:

- **Timber pole retaining wall** — residential, highest volume, most relatable to Perrie.
- **RC cantilever wall** — infrastructure, contrast demonstrates domain depth.
- Full parameter lists for these 2 published openly (not gated).
- Remaining ~28 types gated behind product.
- Conditional logic and full taxonomy structure always proprietary.
