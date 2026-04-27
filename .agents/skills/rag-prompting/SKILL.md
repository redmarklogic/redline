---
name: rag-prompting
description: Use when writing queries for a NotebookLM notebook — covers prompt anatomy, RAG retrieval rules, structured extraction schemas, and hallucination scoping.
---

# RAG Prompting

Principles and templates for writing effective queries against NotebookLM, a
retrieval-augmented generation (RAG) system that retrieves passages from uploaded
documents and generates citation-backed responses. The retrieval and generation
steps are **separate** — this has concrete consequences for prompt design.

## Boundary Contract

### Inputs
- Research question or data extraction request
- Domain context (optional)

### Outputs
- Well-formed query string ready to send to NotebookLM

### Out of Scope
- MCP tool configuration or authentication (`notebooklm-mcp`)
- Research workflow orchestration (`redline-research`)
- Notebook management (creating, deleting, sharing)

## When to Use

- Before sending any query to a NotebookLM notebook.
- When an agent or skill needs to formulate a question for NotebookLM.
- When extracting structured data (CSV, JSON) from notebook sources.

## When NOT to Use

- Setting up the MCP server or authenticating (`notebooklm-mcp`).
- Orchestrating a multi-notebook research session (`redline-research`).

## Prompt Anatomy

Build every query in this order. Not all elements are required every time.

```
[Audience prefix]      <- always first (Rule 1)
[Role / Persona]       <- optional; when domain frame matters
[Context block]        <- delimited with """ or <context> tags
[Instruction]          <- one task, one question (Rule 3)
[Constraints]          <- framed positively (Rule 4)
[Output Format]        <- explicit: prose, JSON, CSV, bullet list
[One-Shot Example]     <- optional; anchors format for structured output
[Refocus + Transition] <- required for long prompts >150 words (Rule 5)
```

## Rules

### Rule 1 — Always prepend the audience prefix

Every query **MUST** begin with:

```
Explain for the uninitiated. Define any specialist term or acronym the first time
it appears. Keep citations. Avoid ambiguity.
```

Unless the caller has already specified a different audience.

### Rule 2 — Self-contained, pronoun-free queries

The retrieval engine sees the question in isolation. Pronouns break retrieval.

| Bad | Good |
|-----|------|
| `How does it handle this?` | `How does NZS 4431 handle differential settlement?` |
| `What did they recommend?` | `What does CIRIA C807 recommend for GBR risk allocation?` |
| `When was that introduced?` | `When was the FIDIC Emerald Book first introduced?` |

Replace every pronoun and demonstrative with the explicit noun phrase it refers to.

### Rule 3 — One question per prompt

Multi-part questions cause the model to skip or conflate parts. Decompose into
sequential single-topic queries and synthesise results yourself.

```
# Bad -- one overloaded query
"What is GBR risk allocation, how is it applied in NZ, and how does it differ from FIDIC?"

# Good -- three sequential queries
Q1: What is GBR risk allocation and what purpose does it serve?
Q2: How is GBR risk allocation applied in New Zealand contracts?
Q3: How does GBR risk allocation in the FIDIC Emerald Book differ from NZ practice?
```

### Rule 4 — Scope to prevent hallucination

Always include one of:

- `Answer only using information found in the notebook sources.`
- `If the notebook does not contain a direct answer, say "Not covered in sources."`

### Rule 5 — Sandwich long prompts

For queries with substantial context (>150 words), restate the core question at
the end:

```
[Audience prefix]
<context>...</context>
[Instruction]
...
Restate question in one sentence. Answer based only on the sources:
```

## Response Handling

After receiving a response from NotebookLM:

- **MUST** scan for unexplained jargon or ambiguity. If any remains,
  append a short glossary at the end of the answer.
- **NEVER** rewrite the body of a NotebookLM response to simplify it.
- **NEVER** remove or paraphrase citations returned by NotebookLM.

## Templates

### Factual lookup

```
Explain for the uninitiated. Define any specialist term the first time it appears.
Keep citations. Avoid ambiguity.

What is the Standard Penetration Test (SPT), how is it performed in the field, and
what physical property of the soil does the SPT blow count (N-value) measure?
Answer only using information found in the notebook sources. If not covered, say so.
```

### Contextualised analysis

```
Explain for the uninitiated. Define any specialist term the first time it appears.
Keep citations. Avoid ambiguity.

<context>
A geotechnical investigation found SPT N-values between 4 and 8 at 3 m depth in a
sandy silt deposit beneath a proposed residential foundation.
</context>

What bearing capacity concerns should a geotechnical engineer flag for a residential
foundation on a sandy silt deposit with SPT N-values between 4 and 8 at 3 m depth?
List the key failure modes and any relevant NZ standard references.
Answer only using information found in the notebook sources. If not covered, say so.
```

## Common Mistakes

| Mistake | Why it fails | Fix |
|---------|-------------|-----|
| Vague instruction ("tell me about X") | Model guesses scope | Specific, bounded question |
| Pronouns ("it", "that value") | Retrieval loses context | Explicit noun phrases |
| Multi-question blob | Model skips or conflates parts | One question per prompt |
| No output format | Unpredictable shape | Always name the format |
| Negative constraints ("don't hallucinate") | Less reliable than positive | `"Answer only from sources"` |
| No audience prefix | Jargon unexplained, citations omitted | Prepend standard prefix |
| Leading/biased phrasing | Model validates premise instead of analysing | Neutral language: "What are the advantages and challenges?" |

## Quick Checklist

- [ ] Audience prefix present
- [ ] Single, concrete instruction
- [ ] Pronouns replaced with explicit noun phrases
- [ ] Context and instructions separated by delimiters
- [ ] Output format stated
- [ ] Scope constraint + escape hatch
- [ ] Long prompts (>150 words): refocus at end
- [ ] Multi-part: decomposed into sequential queries
- [ ] Structured data (CSV/JSON): see [`structured-extraction.md`](structured-extraction.md)

## Structured Extraction

For extracting data into CSV, JSON, or any tabular format, read
[`structured-extraction.md`](structured-extraction.md) — covers Rule 6
(Schema Contract), the three extraction templates (flat CSV, flat JSON,
nested JSON two-step), and structured-specific common mistakes.
