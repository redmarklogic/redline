# Deep Research Prompt — Word Task Pane & OOXML Learning Resources

**Status**: Ready to paste. **Prepared by**: Linda (Knowledge Infrastructure). **Date**: 2026-06-12.
**Purpose**: Paste into Google Deep Research (Gemini) to produce a ranked shortlist of
learning resources for (A) building a Microsoft Word task pane add-in and (B) understanding
OOXML (Office Open XML), the file format behind `.docx`.
**Grounding sources**: `docs/deferred/P-024-word-task-pane-integration-for-pre-revie.md`
(task pane is a parked-but-live product surface), `docs/product/strategy/strategic-bets.md`,
`docs/architecture/api/http-api-standard.md` (violations payload designed for a future
Word task pane), market research on Word-native competitors
(`docs/research/market/microsoft-legal-agent.md` — "LLMs cannot be trusted to produce
correct OOXML"; deterministic DOCX handling is a product principle).

---

## Paste-ready prompt

```text
TASK
Find the best learning resources for two related topics, for the specific team and
product described below. The output is a ranked study/reference shortlist. I will
download, buy, or clone directly from your list, so verify that every title, author,
maintainer, edition year, and link actually exists and points where you say it does.

TOPIC A — Building a Microsoft Word TASK PANE add-in (modern web add-in model)
TOPIC B — OOXML / WordprocessingML: understanding, parsing, and troubleshooting .docx
files under the hood

OUTPUT FORMAT — STRICT, NON-NEGOTIABLE
- Your answer must be THREE TABLES plus at most 150 words of prose in total (a 2-3
  sentence intro and any table footnotes). No executive summary, no narrative sections,
  no per-resource paragraphs, no methodology discussion. If an explanation does not fit
  in a table cell, cut it.
- TABLE 1 — "TASK PANE RESOURCES": exactly 8 to 12 resources, ranked by usefulness
  (rank 1 = start here). Mix of types is expected: official docs worth treating as
  canonical, downloadable PDFs/ebooks, and mature GitHub repos (official sample add-ins,
  scaffolds/generators, REAL open-source Word add-ins shipped to users). Include both
  technical how-to resources and design-oriented resources (task pane UX patterns,
  Fluent UI) — at least 1 and at most 3 design-oriented entries.
- TABLE 2 — "OOXML RESOURCES": exactly 6 to 10 resources, ranked by usefulness. Must
  include the free official spec PDFs (ECMA-376; note its relationship to ISO/IEC 29500),
  at least one explanatory book or long-form PDF that teaches WordprocessingML rather
  than just reprinting the schema, and the documentation for the main Python tooling
  (python-docx and ecosystem) plus any deep-dive references on docx internals
  (relationships, parts, content types, tracked changes / comments markup).
- Columns for BOTH Table 1 and Table 2, in this order:
  1. Rank
  2. Title — Author or Maintainer (for repos: org/repo name)
  3. Type — exactly one of: BOOK, FREE PDF, OFFICIAL DOCS, GITHUB REPO, COURSE
  4. First published (year) AND last updated (year) — two values, always both; for
     repos and docs the last-updated year is the critical one (use last substantive
     commit or doc revision, not a trivial typo fix)
  5. Format & cost — e.g., "free PDF download", "paid ebook ~USD 40", "free, online
     docs", "free, MIT-licensed repo"
  6. Language relevance — exactly one of: PYTHON, JAVASCRIPT/TYPESCRIPT, or
     LANGUAGE-AGNOSTIC
  7. Why useful for OUR context — maximum 2 sentences, written FOR THE UNINITIATED:
     plain language a non-expert can follow, no unexplained jargon. For Table 1, say
     concretely why it helps build a Word task pane for a document-checking product.
     For Table 2, say concretely why it helps parse or troubleshoot .docx files.
  8. Link — a working URL to the resource itself (not a review or aggregator page)
- TABLE 3 — "AVOID / LEGACY": 3 to 6 famous or frequently recommended resources that
  LOOK relevant but teach the WRONG technology or are dangerously outdated (e.g.,
  well-known VSTO / .NET task pane books, tutorials built on deprecated APIs or the
  legacy COM add-in model). Columns: Title — Author | Year | Why avoid (1 sentence,
  name the wrong/legacy technology explicitly) | Use instead (a Table 1 or Table 2
  entry, or "nothing").

OUR CONTEXT — filter every recommendation against this
- Who we are: a solo technical founder building a B2B SaaS "quality layer" that checks
  geotechnical engineering reports (Word documents) for routine compliance problems
  before a senior engineer reviews them. The product's document analysis backend is
  written in Python and treats deterministic, correct handling of .docx files as a core
  product principle.
- The surface we are studying for: a Word task pane that shows checking results inside
  Word and lets an engineer act on them in the document. It must work in BOTH Word on
  the web AND desktop Word (Microsoft 365 subscription versions).
- Therefore the ONLY acceptable add-in technology is the modern web add-in model:
  Office JavaScript API (Office.js) task panes built with web technologies, declared
  via an add-in manifest. VSTO, COM add-ins, .NET-based custom task panes, and
  anything that runs only on Windows desktop Word are the WRONG technology for us —
  they belong in Table 3 only.
- Language reality check — be honest about this in your selections: the founder
  strongly prefers Python, but the task pane platform itself is JavaScript/TypeScript.
  So: (a) JS/TS resources are acceptable and expected as the platform reference;
  (b) resources covering Python-backed architectures are ESPECIALLY valuable — a
  Python backend (API server) doing the document analysis while a thin JS/TS task pane
  calls it, hybrid approaches, or tooling that lets Python do more of the work;
  (c) do NOT invent or oversell "Python for Office add-ins" resources — if Python
  genuinely cannot be used for some layer, prefer resources that make that boundary
  clear, and use the Language relevance column accurately.
- For OOXML (Topic B), Python relevance is real and direct: we parse and generate
  .docx server-side in Python (python-docx ecosystem and raw XML when needed), so
  spec-level and internals-level resources are in scope even when language-agnostic.

RECENCY RULES — apply strictly; the Office add-in platform moves fast
- Prefer resources published or substantively updated in 2021 or later. Anything older
  must justify its place in the "Why useful" cell (e.g., the ECMA-376 spec is old but
  is the normative source) or move to Table 3.
- Flag in the "Why useful" cell any resource that predates, or is silent on, the
  unified manifest for Microsoft 365 / current manifest guidance, if that affects how
  much of it can be followed verbatim.
- For GitHub repos: require active-maintenance signals (commits within roughly the
  last 18 months, issues triaged). A famous but stale repo either carries an explicit
  "STALE" note in the "Why useful" cell or goes to Table 3.
- For official docs: link the current live version, not archived or versioned snapshots.

QUALITY BAR
- Rank by usefulness to THIS team (Python-leaning solo founder, document-checking
  product, web + desktop Word), not by fame or general acclaim.
- Verify every link resolves to the stated resource and edition. If a book exists only
  in print or behind a paywall, say so in the Format & cost cell.
- Do not pad: if only 8 task pane resources and 6 OOXML resources genuinely fit, list
  exactly that many.
```

---

## Usage notes

1. No placeholders to fill — the context block is grounded in P-024 (Word task pane,
   parked but under re-evaluation), the architecture docs that already anticipate a task
   pane consumer of the violations API, and the product principle of deterministic DOCX
   (Word file format) handling, all as of 2026-06-12. If P-024's status or the surface
   strategy changes materially, regenerate the context block before reuse.
2. To re-run with narrower scope, drop one topic: delete Table 1 or Table 2 (and its
   topic block) and keep all format, recency, and Table 3 rules unchanged; bounds for the
   remaining table stay as written.
3. Whatever the research returns: free PDFs and ebooks should come to me (Linda) for the
   standard four-step library ingestion (file, rename, index, NotebookLM upload) before
   anyone studies from them. Judging whether a given architecture resource fits our stack
   is Peter's domain — a pre-adoption sanity pass by Peter is recommended for Table 1's
   top picks.
