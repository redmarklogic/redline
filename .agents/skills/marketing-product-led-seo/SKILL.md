---
name: marketing-product-led-seo
description: Use when planning SEO strategy beyond blog content, considering free programmatic tools or calculators to capture organic search traffic, or when handing an SEO idea off to product and engineering.
---

# Marketing — Product-Led SEO

Source: `Digital Marketing & Social Selling` notebook (Product-Led SEO by Eli Schwartz).

## Boundary Contract

## Core Principle

Traditional SEO writes blog posts targeting keywords. **Product-Led SEO builds the
product itself to be the SEO asset** — a free calculator, classifier, lookup tool, or
database that ranks for thousands of long-tail queries simultaneously and introduces
search visitors to the paid product.

A blog post is a leaf. A Product-Led SEO tool is a tree.

**Redline example.** Instead of writing "How to classify soil per BS 5930", build a
free interactive Soil Classification Calculator at `redline.app/tools/soil-classifier`.
It ranks for hundreds of variations of soil-type queries, demonstrates Redline's
domain accuracy live, and routes engaged users into the paid product.

## When to Use

- Setting the annual SEO strategy (always evaluate Product-Led options first)
- A traditional content campaign is producing diminishing returns
- A competitor has launched a free tool that's eating your search share
- You spot a category of queries with high volume and low quality results

## When NOT to Use Product-Led SEO

- The query has low search volume (< 500/month combined long-tail). Blog post is fine.
- The tool would require paid data feeds Redline doesn't own. Cost > benefit.
- The tool would expose proprietary IP. Build something adjacent instead.

## Co-Ownership Boundaries

| Role | Owns |
|------|------|
| the Marketing Lead | Query cluster identification, marketing brief, SEO requirements, content around the tool, distribution |
| the Product Manager | PRD, scope, acceptance criteria, engineering handoff, funnel instrumentation |
| the Domain Expert | Technical accuracy of any domain calculation |
| Engineering | Build, deploy, maintain |

If the Marketing Lead writes the PRD, the boundary is broken. If the Product Manager sets the SEO strategy, the
boundary is broken. Escalate disagreements via `/challenge`.

## Output Location

Marketing briefs at `docs/product/marketing/seo/product-led-seo-briefs/<tool-slug>.md`.
Linked from `docs/product/marketing/seo/README.md`.

## Cross-References

- Hand the brief to `pm-prd-builder` (via the Product Manager) to convert to a PRD.
- Use `pm-personas` to identify which persona the tool serves.
- Route any geotechnical claim through the Domain Expert before launch.


See `procedures/marketing-product-led-seo.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Building an SEO tool without linking it to the product | Product-led SEO tools should require or showcase the core product; orphaned tools don't convert |
| Targeting head keywords with a new tool | Target long-tail, job-to-be-done keywords with calculators and tools; head terms are too competitive |
| Launching a tool without a clear content handoff path | Each tool page needs a narrative article explaining the result and an obvious CTA to the product |