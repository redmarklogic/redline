---
name: marketing-content-big-5
description: Use when planning content marketing topics, deciding what blog posts, videos, or pages to publish next, or when prospects keep asking the same sales questions — applies the They Ask You Answer / Big 5 framework.
---

# Marketing — The Big 5 Content Framework

Source: `Digital Marketing & Social Selling` notebook (They Ask, You Answer by Marcus
Sheridan).

## Core Principle

B2B buyers do most of their research online before talking to sales. Whoever answers
their questions most transparently wins their trust. Refusing to answer (especially on
price, problems, or competitors) sends them to a competitor who will.

**Rule:** If a prospect has asked the question more than twice in sales calls, it must
have a public answer on the website.

## The Big 5 Topics

These five categories drive the majority of B2B buyer-research traffic. Every content
calendar must show coverage across all five.

| # | Topic | What it answers | Redline example |
|---|-------|-----------------|-----------------|
| 1 | **Pricing & Costs** | What does it cost? What drives the price up or down? | "How much does Redline cost vs the billable hours of manual report drafting?" |
| 2 | **Problems** | What are the downsides, risks, fears? | "Will AI hallucinate soil data?" / "Who carries engineering liability for an AI-drafted report?" |
| 3 | **Versus & Comparisons** | How does X compare to Y? | "Redline vs manual Word/CAD workflow" / "Redline vs Bentley OpenGround" |
| 4 | **Reviews** | What do users actually think? | "Honest review of Redline after 6 months at a 30-engineer consultancy" |
| 5 | **Best in Class** | What are the top tools/methods/firms in the space? | "The 7 best geotechnical reporting workflows in 2026" (Redline included on merit, not first) |

## When to Use

- Drafting or refreshing the editorial calendar
- A sales rep reports the same prospect question for the third time
- A competitor publishes content you don't have an answer to
- Audience metrics show traffic but no conversion — usually a Big 5 gap

## Procedure

1. **List unanswered questions.** Pull the last 30 days of sales-call notes, support
   tickets, and LinkedIn DMs. Extract every question a prospect asked.
2. **Bucket each question into one of the Big 5.** Questions that don't fit a bucket
   are usually not Big 5 content — park them.
3. **Score by frequency.** A question asked 5+ times = priority. Asked once = nice-to-have.
4. **Check current coverage.** For each bucket, list what Redline has already published.
   Identify the gap.
5. **Draft the content brief.** Each Big 5 piece needs: target persona, the exact
   buyer question (verbatim if possible), the honest answer, the call to action.
6. **Apply transparency check.** If the draft dodges the question or buries the answer,
   rewrite. The whole point is transparency.
7. **Route AI-assisted drafts through `marketing-ai-content-review`** before publishing.

## The Hardest Two Topics (and how to handle them)

### Pricing
Founders resist publishing prices because "every deal is custom." Push back: at minimum
publish the pricing model, the variables that move the price, and a typical range.
Anchor against the cost of the alternative (e.g. billable hours of manual drafting).

### Problems
Founders resist naming weaknesses. The opposite is true — naming the elephant in the
room (AI hallucination, liability, integration friction) and explaining how Redline
mitigates it converts skeptics. Silence reads as evasion.

## Anti-Patterns

- **Bucket imbalance.** Publishing 20 "Best in Class" listicles and zero Pricing pages
  means you're avoiding the hard conversations. Re-balance.
- **Marketing-speak answers.** "We offer flexible pricing tailored to your needs" is
  not an answer. Give numbers or give a model.
- **Comparison cowardice.** A Versus piece that refuses to name the competitor or
  honestly admit where they win is worse than no piece at all.
- **Treating Big 5 as one-time work.** Big 5 content needs refreshing every 6-12
  months as the product, market, and competitors evolve.

## Output Location

Big 5 content briefs and drafts live at `docs/product/marketing/the-big-5/<topic-slug>.md`.
Index them in `docs/product/marketing/the-big-5/README.md` with bucket, persona, and
publish status.

## Cross-References

- Use `marketing-ai-content-review` before publishing any AI-assisted draft.
- Use `pm-personas` to confirm which persona each piece targets.
- Use `qmd-narrative-design` for long-form structure (Hook-Problem-Insight-Proof-Action).
