---
name: marketing-product-led-seo
description: Use when planning SEO strategy beyond blog content, considering free programmatic tools or calculators to capture organic search traffic, or when handing an SEO idea off to product and engineering.
---

# Marketing — Product-Led SEO

Source: `Digital Marketing & Social Selling` notebook (Product-Led SEO by Eli Schwartz).

## Boundary Contract

### Inputs
- SEO opportunity or keyword cluster, product feature set

### Outputs
- Product-Led SEO marketing brief for handoff to the Product Manager (`pm-prd-builder`)

### Out of Scope
- PRD writing (`pm-prd-builder`)
- Blog content planning (`marketing-content-big-5`)
- Code implementation (`spec-kit`)

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

## Procedure

1. **Identify the query cluster.** Use keyword research to find a category of related
   queries (e.g. all variations of "soil classification", "bearing capacity",
   "settlement calculation") with collective high volume.
2. **Validate the gap.** Search the top 5 queries. If the SERP is filled with poor
   tools, dated PDFs, or pure ad pages, there is a gap. If a single dominant tool
   already rules, do not compete head-on — find an adjacent angle.
3. **Sketch the tool.** One-page sketch: input fields, output, why a search visitor
   would use it, the natural funnel into Redline.
4. **Write the marketing brief.** Hand to the Product Manager. The brief contains:
   - Target query cluster + estimated combined monthly search volume
   - User story ("As a graduate geotechnical engineer searching for X, I want Y...")
   - Required inputs, expected outputs, accuracy expectations
   - Funnel hypothesis — how does this convert to a Redline trial?
   - SEO requirements (URL structure, schema markup, indexability)
5. **the Product Manager converts to PRD.** the Marketing Lead does not write the PRD. the Product Manager owns scoping,
   acceptance criteria, and engineering handoff via `pm-prd-builder`.
6. **the Product Manager hands to the Domain Expert for technical accuracy.** Any geotechnical calculation
   tool must be vetted by the Domain Expert — a wrong answer at scale destroys the brand.
7. **Instrument the funnel.** Before launch, agree the conversion metric with the Product Manager
   (e.g. % of tool users who start a Redline trial within 30 days).

## Co-Ownership Boundaries

| Role | Owns |
|------|------|
| the Marketing Lead | Query cluster identification, marketing brief, SEO requirements, content around the tool, distribution |
| the Product Manager | PRD, scope, acceptance criteria, engineering handoff, funnel instrumentation |
| the Domain Expert | Technical accuracy of any domain calculation |
| Engineering | Build, deploy, maintain |

If the Marketing Lead writes the PRD, the boundary is broken. If the Product Manager sets the SEO strategy, the
boundary is broken. Escalate disagreements via `/challenge`.

## Anti-Patterns

- **Tool with no funnel.** A free tool that doesn't route users into Redline is a
  charity, not a marketing asset. Always design the funnel first.
- **Tool that's worse than the alternatives.** If Redline's free calculator gives
  worse answers than the dominant competitor's tool, it damages brand trust.
  Either be best-in-class or don't ship.
- **Treating Product-Led SEO as marketing's deliverable.** It's a product. Engineering
  builds, the Product Manager scopes, the Domain Expert verifies. the Marketing Lead briefs and distributes.
- **Skipping the validation step.** Building a tool for a query cluster nobody actually
  searches wastes engineering time. Prove demand before briefing.

## Output Location

Marketing briefs at `docs/product/marketing/seo/product-led-seo-briefs/<tool-slug>.md`.
Linked from `docs/product/marketing/seo/README.md`.

## Cross-References

- Hand the brief to `pm-prd-builder` (via the Product Manager) to convert to a PRD.
- Use `pm-personas` to identify which persona the tool serves.
- Route any geotechnical claim through the Domain Expert before launch.
