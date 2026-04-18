# Prioritisation Framework — Redline

**Status**: Adopted (founder-authored). **Owner**: Mark (per-feature application).
**Methodology custodian**: Ron.

> This is the founder's framework, recorded verbatim. Every feature, candidate
> initiative, or build-or-defer call inside Redline is scored against it. Mark owns
> per-feature application from this point forward — see `feature-backlog.md` for the
> first scored pass and the Mark handoff at the bottom of this file.

## Vectors

Each vector scored 1–5 (higher is better). All vectors carry equal weight.
Total possible score: 25.

### 1. Client Impact (Value)

How much pain does this solve?

- **5**: Eliminates hours of manual work, removes a critical bottleneck, saves
  the client measurable money.
- **4**: Removes a recurring friction; clearly noticeable in weekly workflow.
- **3**: Useful, but not pain-killing. Saves minutes per use.
- **2**: Mild convenience. Saves a click or two.
- **1**: Cosmetic; saves seconds.

### 2. Ease of Building (Effort)

How fast and simple to build, test, and deploy?

- **5**: Days. Existing architecture supports it. Low maintenance.
- **4**: One sprint. Some new patterns, no architectural risk.
- **3**: 2–3 sprints. New module, but no architectural overhaul.
- **2**: Weeks of research, novel architecture decisions.
- **1**: Months of foundational R&D, technical debt risk, unsolved problem.

### 3. Localisation Penalty (Scalability)

How easily does this transfer to a new geography (NZ → AU → next market)?

- **5**: Universal logic. Parameter tweaks only.
- **4**: Mostly portable. Localisation isolated to a config file or two.
- **3**: Partial portability. Standards corpus changes; engine survives.
- **2**: Heavily jurisdictional. Significant rebuild per market.
- **1**: Hardcoded to one country's compliance regime. Full rebuild per market.

### 4. Confidence (Risk)

How certain are we that we are building the right thing, with enough domain
knowledge to do it well?

- **5**: Rich curated reference material (memos, prior research, textbooks,
  documented examples). Founder + advisors confident.
- **4**: Solid grounding from one or two memo sources. Minor open questions.
- **3**: Partial grounding. Pattern is plausible but unvalidated end-to-end.
- **2**: Hunch with one anecdote. Significant primary research needed.
- **1**: Speculative. Built on assumption, not evidence. High risk of building
  the wrong thing.

### 5. GTM Alignment (Strategic Fit)

Does this serve the immediate commercial goal (close NZ/AU beta clients in H1 2026)?

- **5**: Exactly the missing piece to close the next 3 local beta clients.
- **4**: Strong contributor; visible in the funnel within H1.
- **3**: Useful, but not on the critical path for H1.
- **2**: Long-tail value; serves a Phase-2 segment.
- **1**: Built for the wrong segment, wrong geography, or wrong time horizon.

## Method

1. Score each vector independently. Do not let totals leak between vectors.
2. Tally the total. Highest wins.
3. **Sense check**: if the math feels wrong — if the framework is recommending
   something the gut rejects — you are overvaluing on personal preference.
   Re-score, do not override the math.
4. Re-score quarterly or whenever a Strategic Bet is added, killed, or rewritten.

## Operating Notes (Ron)

Three things the framework does well, two it doesn't:

**Strengths.**
- It forces Confidence and Localisation Penalty into the scoring conversation.
  Both are routinely under-weighted by founders chasing client impact.
- The "if math feels wrong, re-score" rule prevents the most common abuse
  pattern (justifying the favourite by tweaking weights).
- Equal weighting forces honest scoring rather than weight-tuning.

**Weaknesses to manage.**
- Equal weighting can hide that two vectors are *correlated* in this domain
  (Confidence and Ease of Building tend to move together when memo material is
  rich). Mark should flag when scoring two vectors feels redundant.
- The framework scores features, not sequences. Two high-scoring features may
  share a dependency that the framework does not surface. Mark must run a
  dependency map alongside the score table when proposing a sprint slate.

## Mark Handoff

Per-feature prioritisation is now Mark's territory:

1. Load the `pm-prioritization` skill before the next ranking pass.
2. Use this framework as the *portfolio* scoring rubric (distinct from the
   scenario-level RICE inside `spec-kit`).
3. Re-score the `feature-backlog.md` table at the start of every sprint
   planning session, not at the start of every conversation.
4. When Mark disagrees with the founder on a score, the disagreement is logged
   in `decisions/` with both scores, both rationales, and the decision-maker.
   Do not silently overwrite founder scores.

## Provenance

Rubric authored verbatim by the founder this pass. Operating notes are Ron's
synthesis. The framework distinction (portfolio rubric here vs. scenario-level
RICE in `spec-kit`) follows `docs/architecture/skills-architecture.md`.
