# Marketing Product Led Seo — Detailed Reference

### Inputs
- SEO opportunity or keyword cluster, product feature set

### Outputs
- Product-Led SEO marketing brief for handoff to the Product Manager (`pm-prd-builder`)

### Out of Scope
- PRD writing (`pm-prd-builder`)
- Blog content planning (`marketing-content-big-5`)
- Code implementation (`spec-kit`)

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
