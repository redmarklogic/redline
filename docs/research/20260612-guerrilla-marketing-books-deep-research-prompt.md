# Deep Research Prompt — Guerrilla Marketing Books (Buy List)

**Status**: Ready to paste. **Prepared by**: Linda (Knowledge Infrastructure). **Date**: 2026-06-12.
**Purpose**: Paste into Google Deep Research (Gemini) to produce a purchase shortlist of
guerrilla-marketing books relevant to Redline's specific situation.
**Grounding sources**: `docs/product/strategy/positioning.md`, `docs/product/strategy/personas.md`,
`docs/product/strategy/launch-perimeter-constraints.md`, `docs/product/strategy/gtm/2026-launch-plan.md`,
`docs/product/strategy/gtm/content-engine.md` (referenced titles).

---

## Paste-ready prompt

```text
TASK
Find books on guerrilla marketing and low-budget marketing that fit the specific business
described below. The output is a purchase shortlist. I will buy directly from your list,
so verify titles, authors, edition years, and purchase links actually exist.

OUTPUT FORMAT — STRICT, NON-NEGOTIABLE
- Your answer must be TWO TABLES plus at most 120 words of prose in total (a 2-3 sentence
  intro and any table footnotes). No executive summary, no narrative sections, no per-book
  paragraphs, no methodology discussion. If an explanation does not fit in a table cell, cut it.
- TABLE 1 — "BUY LIST": exactly 8 to 12 books, ranked by relevance (rank 1 = buy first).
  Columns, in this order:
  1. Rank
  2. Title — Author(s)
  3. First published (year)
  4. Latest edition (year) — if same as first published, repeat the year
  5. Type — exactly one of: PRINCIPLES (timeless, channel-independent) or PLAYBOOK
     (tactical, channel-specific)
  6. Why relevant to THIS business — maximum 2 sentences, must reference a specific
     element of the business context below (not generic praise)
  7. Currency — exactly one of: CURRENT, or PARTLY DATED + a parenthetical naming what
     to skip (e.g., "PARTLY DATED (skip the Facebook organic-reach chapters)")
  8. Where to buy — a working link (Amazon, publisher, or Book Depository equivalent)
- TABLE 2 — "DO NOT BUY": 3 to 6 famous or frequently recommended guerrilla-marketing
  titles that LOOK relevant but fail the rules below. Columns: Title — Author | First
  published | Why not (1 sentence) | Read instead (a Table 1 entry, or "nothing").

BUSINESS CONTEXT — filter every recommendation against this, reject anything that does not fit
- Who we are: a solo technical founder, bootstrapped, no marketing budget, no paid
  advertising, no marketing team. The product is B2B SaaS: a "quality layer" that checks
  geotechnical engineering reports for routine compliance problems (wrong standards cited,
  missing mandatory clauses, copy-paste errors) before a senior engineer reviews them.
- Market: New Zealand and Australia geotechnical consulting firms — a niche professional
  market of only a few hundred relevant practitioners, who largely know each other.
  Extremely reputation-sensitive: one spammy, gimmicky, or hype-flavoured move travels
  through the entire professional network and is not recoverable.
- Buyers: conservative, pragmatist professional engineers — Technical Directors who
  co-own 5-50 person consultancies and can approve small subscriptions without board
  sign-off. They are not early adopters and are hostile to "AI-powered" hype framing.
- Motion: product-led growth — a free tool acquires individual engineers; the founder
  personally converts the best-fit users through direct outreach. Primary channels:
  the founder's LinkedIn presence, niche industry forums and professional associations,
  and word-of-mouth referral. Explicitly excluded channels: paid ads of any kind,
  Reddit, consumer mass-market channels, high-volume cold outreach.
- Therefore RELEVANT book topics: zero/low-budget B2B marketing, founder-led marketing
  and sales, marketing to skeptical expert/professional audiences, niche and community
  marketing in small markets, LinkedIn-centric social selling, word-of-mouth and referral
  mechanics in tight professional networks, positioning for conservative buyers.
- Therefore NOT RELEVANT: B2C/retail guerrilla stunts, street/ambient marketing,
  paid-ad optimisation, e-commerce growth, viral consumer growth hacking, enterprise
  sales playbooks, personal-brand influencer playbooks.

ALREADY OWNED / APPLIED — exclude from Table 1 (may appear in Table 2 "Read instead" only):
- "They Ask, You Answer" — Marcus Sheridan
- "Content-Based Networking" — James Carbary
- "Product-Led SEO" — Eli Schwartz
- "Crossing the Chasm" — Geoffrey Moore

RECENCY RULES — apply strictly; marketing channel tactics date quickly
- Exclude any book whose tactical advice assumes a pre-social-media or early-social-media
  channel landscape (fax blasts, classified ads, early-SEO tricks, organic Facebook reach
  plays) UNLESS its enduring value is channel-independent principles — in which case label
  it PRINCIPLES and use the Currency column to name exactly which parts are dated.
- Always cite and link the most recent edition; record both first-publication year and
  latest-edition year so I can judge age myself.
- Any book first published before 2015 whose latest edition is also before 2015 must
  justify its place explicitly in the "Why relevant" cell or be moved to Table 2.
- The Guerrilla Marketing franchise itself (Levinson et al.) is in scope ONLY if a
  specific volume survives these rules; otherwise list it in Table 2 and name the modern
  replacement.

QUALITY BAR
- Rank by fit to THIS business, not by fame, sales figures, or general acclaim.
- Verify every purchase link resolves to the stated edition. If a book is out of print,
  say so in the "Where to buy" cell and link a used-copy source.
- Do not pad: if only 8 books genuinely fit, list 8.
```

---

## Usage notes

1. No placeholders to fill — the business context block is grounded in the current
   positioning, personas, and GTM (go-to-market) plan as of 2026-06-12. If positioning
   changes materially, regenerate the context block before reuse.
2. To re-run with narrower scope, replace the "Therefore RELEVANT" list with a single
   topic (e.g., only "word-of-mouth mechanics in small professional networks") and lower
   the bound to "5 to 7 books"; keep all format and recency rules unchanged.
3. Before purchasing, the buy list can be cross-checked against `library-index.xlsx` in
   the digital library (`G:\My Drive\Library`) to avoid duplicate purchases — ask Linda.
   Relevance of individual titles to marketing strategy is John's domain; a pre-purchase
   sanity pass by John is recommended.
