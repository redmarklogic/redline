---
name: redline-research
description: Structured research workflow for the Redline project. Queries multiple NotebookLM knowledge bases with iterative cross-referencing, then writes a cited research document to docs/research/. Never uses online search.
---
# Redline Research

This skill governs how to conduct knowledge-base research for the **Redline** project.
It orchestrates multiple NotebookLM notebooks with iterative back-and-forth investigation,
grounds all queries in project context, and produces a structured Markdown research document
in `docs/research/<YYYYMMDD>-<snakecase title of research>.md`.

## Knowledge Bases

| Notebook | Purpose | URL |
|---|---|---|
| **Engineering Standards** | NZ infrastructure design standards (IDS), earthworks and compaction requirements (NZS 4431), geotechnical QA procedures, and subdivision consent documentation for practitioners working in the Canterbury / NZ regulatory context | `https://notebooklm.google.com/notebook/0f6cd98a-9dfa-46f8-9a73-4671d2164949` |
| **Ground Engineering Magazine** | Issues of Ground Engineering magazine (2014–2026) covering geotechnical industry news, technical papers, and key standards development (Eurocode 7, BS 5930, SPERWall, CIRIA) across piling, foundations, tunnelling, earthworks, and slope stability | `https://notebooklm.google.com/notebook/d29c2cef-9f34-442f-ae6d-715251dea9aa` |
| **Geotechnical Baseline Reports (GBR)** | Industry guidance on preparing and contractually applying GBRs to allocate subsurface construction risk. Covers Differing Site Conditions claims, ASCE guidelines, CIRIA C807, the NZTS guide, and the FIDIC Emerald Book | `https://notebooklm.google.com/notebook/8eab0bf9-090d-4b1e-975f-00dbd96342af` |
| **Geotechnical Engineering Report Workflows and Standard Procedures** | Professional practice guides, templates, QA checklists, and training materials for geotechnical report structuring, factual/interpretive delineation, and client-centric writing — compiled from a leading NZ geotechnical consultancy's internal knowledge base | `https://notebooklm.google.com/notebook/ee83806c-ff73-436d-ad0b-ca319818e553` |
| **Risk Assessment in Engineering** | Risk management, professional liability, and probabilistic risk assessment in geotechnical engineering. Sources span ASCE, CIRIA, and NZGS guidelines, field manuals, and legal notes covering contracts, non-disclosure agreements, and professional indemnity insurance | `https://notebooklm.google.com/notebook/0b726429-82bc-43f7-9225-ba06f71046c3` |
| **AI System Engineering** | Generative AI application design and deployment: foundation models, prompt engineering, retrieval-augmented generation (RAG), multiagent orchestration, and FastAPI/Docker serving. Covers MCP, OAuth2, the NIST AI Risk Management Framework, the EU AI Act, and GDPR | `https://notebooklm.google.com/notebook/a9dda38b-1a68-4287-826d-378965f57be6` |
| **Software Architecture & Domain-Driven Design** | Ten canonical books (Evans, Vernon, Khononov, Ford, Ousterhout, GoF, and others) covering DDD strategic/tactical patterns (Bounded Contexts, Ubiquitous Language, Aggregates, Repositories, Domain Events), architecture styles (Hexagonal, CQRS, Microservices, Event-Driven), SOLID principles, GoF design patterns, functional domain modeling, EventStorming, Context Mapping, Event Sourcing, saga patterns, and Data Mesh | `https://notebooklm.google.com/notebook/c04e18d3-e1e6-47f0-879a-d0e4a65adcb0` |
| **Business Process Management** | BPM methodologies and continuous process improvement tools including Lean, Six Sigma, BPMN, 7FE, PDCA, and DMAIC frameworks. Drawn from expert-authored management books and the BPM Common Body of Knowledge (BPM CBOK) | `https://notebooklm.google.com/notebook/625aacce-d0b2-42bd-b83c-7f9e3e15f4c7` |
| **Product Roadmapping** | Strategic product roadmapping for product leaders: defining vision, prioritising customer opportunities, and achieving stakeholder buy-in. Covers Kano model, MoSCoW prioritisation, ROI scorecards, user journey maps, and opportunity-solution trees | `https://notebooklm.google.com/notebook/dfb04e76-20c3-44c3-872f-eef2f6c04bb7` |
| **Writing Painless Product and Functional Specifications** | Software product management frameworks and specification writing: PRDs, functional specifications, OKRs, the Shape Up framework, product discovery vs delivery, and alternatives to traditional roadmaps | `https://notebooklm.google.com/notebook/fb7cbc5c-1ff2-44cc-a61f-bfcdee4519fb` |
| **Engineers' Guide to Technical Communication and Writing** | Technical writing and editing best practices for engineering and scientific audiences: document design, audience analysis, ethics, citation standards (Chicago Manual of Style), and structure for reports, proposals, laboratory studies, specifications, and business correspondence | `https://notebooklm.google.com/notebook/c611ced9-393d-45ef-bc66-f2be77fbbf0c` |

## Context & Guidelines

- **Scope**: Apply this skill whenever the user asks to "research", "investigate",
  "look up", or "find out" something in the Redline knowledge base.
- **Constraints**:
  - **NEVER** use online search (web, Bing, DuckDuckGo, etc.) unless the user explicitly
    requests it with words such as "search online" or "look it up on the web".
  All knowledge must come from the NotebookLM notebooks above and/or the
    project context files described below.
  - Always read project context before formulating notebook queries (see Step 1).
- **Output**: Write the research document to `docs/research/<slug>.md` where `<slug>` is a
  short kebab-case name derived from the topic (e.g. `docs/research/lateral-earth-pressure.md`).
  Confirm the path with the user if the topic is ambiguous. Never overwrite an existing file
  without asking.
- **MCP prerequisite**: Follow the `notebooklm-mcp` skill to confirm authentication before
  querying. If the session is not authenticated, resolve it before proceeding.

## Project Context Files

Always load the following files for context before formulating queries. They must inform
the framing and relevance filter for every research session:

| File                               | Purpose                                                                                                                                  |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `docs/project/goals.md`          | Authoritative project goals, wall-type coverage, key inputs/outputs, limitations, and open questions — the primary grounding document.  |
| `docs/project/*.md` (all others) | Additional project context: architecture, data model, decisions, etc. Load any file whose name suggests relevance to the research topic. |

## Procedure

### Step 1 — Read project context

1. Read `docs/project/goals.md` in full.
2. Scan all other `docs/project/*.md` files for titles/headings relevant to the research topic.
3. Load any relevant additional files before writing a single query.

### Step 2 — Frame the research question

Before querying any notebook, write out internally:

- **Actor**: Who will use this information, and how? (e.g. "an intermediate civil engineer
  implementing an embedment depth estimation module for a retaining wall AI tool"). Every
  query sent to NotebookLM must include the Actor in its preamble so the notebook returns
  answers pitched at the right technical level.
- **Research question**: A precise, self-contained question.
- **Relevance filter**: Which Redline domains / goals / limitations does this touch?

### Step 3 — Select applicable notebooks

Before querying, decide which notebooks are relevant by topic area:

- **Engineering theory and standards** → Engineering Standards, Ground Engineering Magazine
- **Geotechnical domain** → Geotechnical Baseline Reports (GBR), Geotechnical Engineering Report Workflows and Standard Procedures, Risk Assessment in Engineering
- **AI and software architecture** → AI System Engineering, Software Architecture & Domain-Driven Design
- **Process and product** → Business Process Management, Product Roadmapping, Writing Painless Product and Functional Specifications
- **Communication and documentation** → Engineers' Guide to Technical Communication and Writing

Query all notebooks that apply; skip one only when it is clearly out of scope.

### Step 4 — Query the most relevant engineering notebook first

Open a session on the most relevant engineering notebook (typically **Engineering Standards**
or **Ground Engineering Magazine**) and ask your first question using the following mandatory
preamble template:

```
Actor: <role and context from Step 2, e.g. "an intermediate civil engineer building
an embedment depth calculation module for a retaining wall AI concept-design tool">

Explain for the uninitiated. Define any specialist term or acronym the first time it
appears. Keep all citations. Avoid ambiguity.

<Your precise, self-contained research question here.>
```

Rules for engineering notebook queries:

- Use explicit noun phrases, never pronouns ("the Rankine active pressure coefficient Kₐ",
  not "it").
- One concept per query — break compound questions into sequential calls.
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

Query Business Process Management, Product Roadmapping, Writing Painless Product and Functional Specifications, Software Architecture & Domain-Driven Design, or communication notebooks when
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

Write the output to `docs/research/<slug>.md`. Use the structure below exactly.

````markdown
# <Research Topic Title>

**Date**: YYYY-MM-DD
**Research question**: <single sentence>
**Actor**: <role and context>
**Redline domains**: <list relevant domains from goals.md>

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
limitation in goals.md does this address or exacerbate? Reference goals.md section numbers
where applicable.>

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
- **MUST** include the Implications section — connecting findings to Redline goals is
  the primary value of the research.
- Keep each Findings sub-section self-contained and readable without the preceding section.

## Naming Convention for Output Files

| Topic type         | Example slug                              |
| ------------------ | ----------------------------------------- |
| Engineering theory | `lateral-earth-pressure.md`             |
| Wall type specific | `concrete-pile-embedment.md`            |
| Data / ML          | `interpolation-methods-ml.md`           |
| Sustainability     | `embodied-carbon-retaining-walls.md`    |
| Standards          | `nzs-3101-concrete-requirements.md`     |
| Project decisions  | `team-discussion-anchor-constraints.md` |

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
- Do not ask a compound question in a single `ask_question` call — split it.
