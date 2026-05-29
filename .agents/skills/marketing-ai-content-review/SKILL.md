---
name: marketing-ai-content-review
description: Use when drafting marketing content with generative AI for a technical domain (geotechnical, civil engineering), or before publishing any AI-assisted content that makes domain claims requiring expert verification.
---

# Marketing — AI Content Review (EEAT + Hallucination Defense)

Source: `Digital Marketing & Social Selling` notebook.

## Boundary Contract

### Inputs
- AI-generated marketing content draft with technical domain claims

### Outputs
- Reviewed content with EEAT compliance and hallucination flags
- SME sign-off requirements routed to the Domain Expert for domain verification

### Out of Scope
- Content topic selection (`marketing-content-big-5`)
- SEO strategy (`marketing-product-led-seo`)
- Domain expertise itself (route to the Domain Expert)

## Core Principle

Generative AI scales content production but **fabricates facts** ("hallucinates").
In a technical field like geotechnical engineering, a single wrong claim — a wrong
formula, a misattributed standard clause, a fabricated case study — destroys
brand trust and creates engineering liability.

Google ranks content on **EEAT** — Experience, Expertise, Authoritativeness,
Trustworthiness. AI alone cannot supply any of these. A human Subject Matter Expert
(SME) must.

**Hard rule:** No AI-assisted content with a domain claim ships without the Domain Expert's
sign-off.

## When to Use

- Drafting blog posts, whitepapers, social posts, or landing pages with ChatGPT,
  Claude, Gemini, or any LLM
- Reviewing content from a freelance writer who used AI assistance (assume yes)
- Auditing already-published content for AI-introduced errors

## Hallucination Risk Triage

Not every AI-assisted piece needs the Domain Expert. Triage by claim type:

| Claim type | Example | Review required |
|------------|---------|-----------------|
| **Domain-technical** | "BS 5930 clause 6.4 requires…" / "The bearing capacity formula is…" | **the Domain Expert — mandatory, blocking** |
| **Product-factual** | "Redline supports DOCX export" / "Redline integrates with X" | **the Product Manager — mandatory, blocking** |
| **Strategic-positional** | "Redline competes with X by…" / "The market for AI in civil engineering is…" | **the Strategy Advisor — mandatory, blocking** |
| **General-marketing** | "Engineers value clarity" / "Trust is built over time" | the Marketing Lead self-review |
| **Pure-stylistic** | Headlines, transitions, meta descriptions | the Marketing Lead self-review |

If a single piece of content spans multiple claim types, route to the highest
applicable reviewer.

## Procedure

1. **Tag the draft.** For every paragraph, mark which claim type it contains. If <!-- hook: allow -->
   uncertain, escalate to mandatory review.
2. **Trace every domain claim.** For each technical claim, identify the source.
   AI cannot be the source — only a citable standard, paper, or the Domain Expert-verified
   fact in `docs/knowledge/geotechnical/` qualifies.
3. **Strip uncited domain claims.** If a claim has no traceable source, delete it
   or replace it with a the Domain Expert-verified equivalent. Do not publish unsourced
   technical claims.
4. **Run the EEAT check.** Does the piece demonstrate:
   - **Experience** — first-person Redline voice, real customer stories?
   - **Expertise** — author byline of a real SME, not "Redline Team"?
   - **Authoritativeness** — links to standards, peer-reviewed sources?
   - **Trustworthiness** — honest about limitations, no overclaiming?
   If any pillar is missing, rewrite.
5. **Send for sign-off.** Route to the Domain Expert/the Product Manager/the Strategy Advisor per the triage table above.
   Reviewers reply with one of: APPROVE, APPROVE WITH EDITS, REJECT.
6. **Apply edits, get final APPROVE, publish.**
7. **Log the review.** Append to `docs/product/marketing/ai-content-review-log.md`:
   date, content URL, reviewer, decision, edits made.

## What Gets Stripped Automatically

- Specific clause numbers from standards unless verified against the actual standard
- Numerical values (capacities, factors of safety, percentages) without a citation
- Named case studies / project references that AI invented
- Quotes attributed to people unless verified
- "Studies show…" / "Research indicates…" without a real study
- Competitor product features that may not exist

## Anti-Patterns

- **Trusting the AI's own citations.** LLMs invent plausible-looking citations
  (real journal names + fake DOIs, real authors + fake papers). Always verify.
- **Reviewer fatigue shortcuts.** "Looks fine, ship it" without claim-tracing.
  Make the Domain Expert actually open the standard.
- **Publishing during reviewer absence.** If the Domain Expert is on leave, technical posts
  wait. There is no fallback reviewer for domain claims.
- **Reviewing in the publishing tool.** Review in Markdown, not in the CMS — once
  it's in the CMS the temptation to ship is too high.
- **Treating social posts as exempt.** A LinkedIn post with a wrong technical
  claim is just as damaging as a blog post. Same review rules apply.

## Output Location

- Review log: `docs/product/marketing/ai-content-review-log.md`
- Drafts under review: `docs/product/marketing/drafts/<slug>.md` with a frontmatter
  `review_status` field (`drafting | in-review | approved | published`).

## Cross-References

- Domain reviewer: the Domain Expert — see `.github/agents/rl.graeme.agent.md` and <!-- hook: allow -->
  `docs/knowledge/geotechnical/`.
- Product reviewer: the Product Manager.
- Strategy reviewer: the Strategy Advisor.
- Use `marketing-content-big-5` for content topic selection before drafting.
