# Redline Research — Procedure

Full reference for the `redline-research` skill. Load this file when actively running a research session.

**REQUIRED:** Before writing any query, review the prompting principles in
[`notebooklm-mcp/prompting-guide.md`](.agents/skills/notebooklm-mcp/prompting-guide.md).
The procedure below encodes those principles; the guide is the authoritative reference
if a situation is not covered here.

## Knowledge Bases

The canonical notebook register lives at `.agents/skills/notebooklm-mcp/register.json`.
Read that file to get the full list of notebooks, their URLs, topic areas, access controls,
and use cases.

**Access rules:**
- Entries with `"access": "open"` may be queried by any agent.
- Entries with `"access": "advisory-board-only"` must be skipped unless the session context
  explicitly identifies the user as an advisory board member (Ron, Mark, or Graeme).
  Do not mention skipped notebooks.

## Project Context Files

Always load the following files for context before formulating queries. They must inform
the framing and relevance filter for every research session:

| File | Purpose |
| ---- | ------- |
| `docs/architecture/*.md` | System architecture and domain model — primary grounding for understanding what Redline builds and why. |
| `docs/concepts/**/*.md` | Feature-level concepts and process descriptions. Load any file whose title suggests relevance. |
| `docs/adr/*.md` | Architecture Decision Records — authoritative records of design choices and their rationale. |

## Procedure

### Step 1 — Read project context

1. Read all files in `docs/architecture/` in full.
2. Scan `docs/concepts/**/*.md` and `docs/adr/*.md` for titles/headings relevant to the research topic.
3. Load any relevant additional files before writing a single query.

### Step 2 — Frame the research question

Before querying any notebook, write out internally:

- **Actor**: Who will use this information, and how? (e.g. "an intermediate civil engineer
  implementing an embedment depth estimation module for a retaining wall AI tool"). Every
  query sent to NotebookLM must include the Actor in its preamble so the notebook returns
  answers pitched at the right technical level.
- **Research question**: A precise, self-contained question.
- **Relevance filter**: Which Redline domains / architecture decisions does this touch?

### Step 3 — Select applicable notebooks

Refer to the Quick Reference table in SKILL.md to select which notebooks to query for the
topic area. Query all that apply; skip one only when it is clearly out of scope — or when it
is marked Advisory Board only and the access condition is not met.

### Step 4 — Query the most relevant engineering notebook first

Open a session on the most relevant notebook for the task at hand, and ask your first question using the following mandatory preamble template:

```
Actor: <role and context from Step 2, e.g. "an intermediate civil engineer building
an embedment depth calculation module for a retaining wall AI concept-design tool">

Explain for the uninitiated. Define any specialist term or acronym the first time it
appears. Keep all citations. Avoid ambiguity.

<Your precise, self-contained research question here.>

Return cited Markdown prose. Answer only using information found in the notebook sources.
If the notebook does not contain a direct answer, say "Not covered in sources."
```

Before sending any query, run through the Quick Checklist in
[`notebooklm-mcp/prompting-guide.md`](.agents/skills/notebooklm-mcp/prompting-guide.md).
One additional rule specific to research sessions:

- Retain the full NotebookLM response verbatim, including citations. Do not paraphrase.

### Step 5 — Cross-reference with complementary notebooks

Open sessions on the other applicable notebooks (from Step 3) and ask complementary
questions to understand how the technical concept applies from different angles — domain
practice, risk, process, or communication. Use the same preamble template (Actor +
plain-language prefix).

Example cross-reference questions:

- "How is [concept from Step 4] applied in geotechnical engineering practice?"
- "What risk considerations apply to [technical concept] in an engineering context?"
- "What communication or documentation conventions apply to [topic]?"

### Step 6 — Cross-reference with process, product, and software design notebooks (when applicable)

Query Business Process Management, Product Roadmapping, Writing Painless Product and Functional
Specifications, Software Architecture & Domain-Driven Design, or communication notebooks when
the topic touches process design, product decisions, or documentation standards. Use the
same preamble template. Example questions:

- "What process mapping approaches apply to [workflow or procedure] in an engineering context?"
- "How should [feature or requirement] be specified using product specification best practices?"
- "What writing conventions apply to [report type or document] in technical engineering communication?"

### Step 7 — Iterate back and forth

Repeat Steps 4–6 as needed. A typical pattern:

1. Engineering Standards / Ground Engineering Magazine → establishes foundational theory.
2. Geotechnical notebooks → grounds theory in domain practice and risk considerations.
3. AI System Engineering / process and product notebooks → applies findings to the Redline tool context.
4. Communication notebooks → validates how findings should be documented or specified.
5. Return to earlier notebooks to resolve any remaining gaps.

Continue until the research question is answered with sufficient depth or until all
notebooks return "no further information" for the outstanding questions.

### Step 8 — Write the research document

Write the output to `docs/research/YYYYMMDD-<topic>.md`. Use the structure below exactly.

````markdown
# <Research Topic Title>

**Date**: YYYY-MM-DD
**Research question**: <single sentence>
**Actor**: <role and context>
**Redline domains**: <list relevant Redline domains, e.g. report skeleton, risk flagging, wall type coverage>

---

## Summary

<2–4 sentences distilling the key finding. Written for the Actor.>

## Findings

### <Sub-topic 1>

<Findings text. Preserve all NotebookLM citations inline in square brackets, e.g. [Source: BS 8002-2015, §3.2].>

### <Sub-topic 2>

...

## Implications for Redline

<Concrete, specific implications: which module, which calculation, which data field, which
limitation does this address or exacerbate? Reference `docs/architecture/` or `docs/adr/`
files where applicable.>

## Open Questions

<Questions this research could not answer — to be pursued in a follow-up session or flagged
as product risk.>

## Glossary

| Term | Definition |
|---|---|
| <term> | <plain-English definition> |
| ... | ... |

## Sources Consulted

| Notebook | Queries asked | Citations returned |
|---|---|---|
| <notebook name> | <number> | <list key citations> |
| ... | ... | ... |
````

Rules for the output document:

- **NEVER** remove or paraphrase citations returned by NotebookLM.
- **MUST** include a Glossary section even if only two terms are defined.
- **MUST** include the Implications section — connecting findings to Redline architecture is
  the primary value of the research.
- Keep each Findings sub-section self-contained and readable without the preceding section.

## Naming Convention for Output Files

| Topic type         | Example slug                                        |
| ------------------ | --------------------------------------------------- |
| Engineering theory | `YYYYMMDD-lateral-earth-pressure.md`              |
| Wall type specific | `YYYYMMDD-concrete-pile-embedment.md`             |
| Data / ML          | `YYYYMMDD-interpolation-methods-ml.md`            |
| Sustainability     | `YYYYMMDD-embodied-carbon-retaining-walls.md`     |
| Standards          | `YYYYMMDD-nzs-3101-concrete-requirements.md`      |
| Project decisions  | `YYYYMMDD-team-discussion-anchor-constraints.md`  |

## Anti-patterns (NEVER do these)

- Do not search the internet. If a fact cannot be found in either notebook or project
  context files, state "Not found in knowledge base" and log it under **Open Questions**.
- Do not name or reference specific civil engineering companies, consultancies, or firms
  operating in New Zealand (e.g. Tonkin + Taylor, Beca, WSP, Stantec, GHD, etc.) in any
  research output. Refer to them generically as "the project engineers", "the geotechnical
  consultant", or "the design team" instead.
- Do not merge answers from different notebooks without clearly labelling which
  notebook each piece of information came from.
- Do not skip the Glossary — domain experts who read the document later will need it.
- Do not write findings as lists of bullet points stripped of context — each finding must
  be a coherent prose paragraph with embedded citations.
- Do not ask compound questions or use biased phrasing — see the prompting guide's
  Common Mistakes table and Quick Checklist.
