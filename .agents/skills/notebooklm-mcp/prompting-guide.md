# NotebookLM Prompting Guide

A definitive reference for any agent writing prompts to query NotebookLM (or any
knowledge-base RAG system). Follow these principles to get accurate, citation-backed,
on-target answers.

---

## Prompt Anatomy — the 7 Elements

Every effective prompt is composed of these structural layers. Not every query needs all
seven, but omitting a layer without a deliberate reason degrades output quality.

| # | Element | Purpose | Required? |
|---|---------|---------|-----------|
| 1 | **Role / Persona** | Sets the knowledge frame and tone the LLM adopts | Situational |
| 2 | **Instruction** | The concrete task — one specific action | Always |
| 3 | **Context** | What the agent already knows; separates static rules from dynamic data | Always |
| 4 | **Constraints** | Explicit boundaries (length, scope, forbidden paths) | As needed |
| 5 | **Output Format** | Exact shape of the response (Markdown, JSON, bullet list, etc.) | Always |
| 6 | **Examples** | One or more input→output pairs that demonstrate the desired style | Situational |
| 7 | **Refocus / Transition** | Restates the core question at the end; cues the model to begin answering | When prompt is long |

### Element notes

**Role / Persona** — Relevant when the knowledge frame matters.
Example: `You are a geotechnical engineer reviewing NZ regulatory documents.`

**Instruction** — One task per prompt. If you need multiple results, decompose into
multiple sequential queries (see Rule 3 below).

**Context** — Use delimiters (`"""` or XML tags like `<context>`) to separate
instructions from input data so the model does not confuse the two.

**Constraints** — Prefer positive framing: `Use only information found in the notebook`
rather than `Do not hallucinate`. Negative commands are processed less reliably.

**Output Format** — Always specify. For NotebookLM queries the default is:
cited Markdown prose. Override explicitly when you need structured data or a summary list.

**Examples (Few-Shot)** — Include when format adherence is critical. Randomise the order
of positive and negative examples to avoid spurious pattern continuation by the model.

**Refocus / Transition** — For queries longer than ~150 words, repeat the core question
at the very end. End the prompt with a transition cue:
`Based only on the sources above, answer:` or simply append a colon and a line break.

---

## NotebookLM-Specific Rules

NotebookLM is a Retrieval-Augmented Generation (RAG) system. RAG retrieves passages from
a fixed set of uploaded documents before generating a response. The retrieval step is
separate from the generation step. This has concrete consequences for how you write a prompt.

### Rule 1 — Always prepend the audience prefix

Every `ask_question` call **MUST** begin with:

```
Explain for the uninitiated. Define any specialist term or acronym the first time it
appears. Keep citations. Avoid ambiguity.
```

This ensures the response is grounded, jargon-aware, and citation-rich.

### Rule 2 — Self-contained, pronoun-free queries

The retrieval engine sees your question text in isolation. Pronouns and back-references
break retrieval.

| Bad (breaks retrieval) | Good (self-contained) |
|---|---|
| `How does it handle this?` | `How does the NZS 4431 earthworks standard handle differential settlement?` |
| `What did they recommend?` | `What does CIRIA C807 recommend for geotechnical baseline risk allocation?` |
| `When was that introduced?` | `When was the FIDIC Emerald Book first introduced for underground projects?` |

**Rule:** Replace every pronoun and demonstrative with the explicit noun phrase it refers to.

### Rule 3 — Query Decomposition for multi-part questions

Loading a single prompt with multiple questions causes the model to skip some of them.

**Instead:** Decompose into sequential single-topic queries. Synthesise results yourself.

```
# Bad — one overloaded query
"What is GBR risk allocation, how is it applied in NZ contracts,
 and what are the differences from FIDIC?"

# Good — three sequential queries
Q1: "What is geotechnical baseline report (GBR) risk allocation and what
    purpose does it serve in subsurface construction contracts?"

Q2: "How is GBR risk allocation applied in New Zealand construction contracts?
    Cite any NZ-specific guidance found in the notebook."

Q3: "How does GBR risk allocation in the FIDIC Emerald Book differ from
    standard NZ subsurface contract practice?"
```

### Rule 4 — Scope to prevent hallucination

Explicitly tell NotebookLM to stay within its sources. Always include one of these phrases:

- `Answer only using information found in the notebook sources.`
- `If the notebook does not contain a direct answer, say "Not covered in sources."`

This activates an escape hatch — the model signals absence of evidence rather than
fabricating an answer.

### Rule 5 — Sandwich long prompts

For queries that include substantial context (>150 words), restate the core question at
the end immediately before asking for the answer:

```
[Audience prefix]
[Context block wrapped in <context>...</context>]
[Instruction]
...
[Refocus: restate the core question in one sentence]
Answer based only on the sources:
```

---

## Before / After Templates

### Short factual lookup

```
# Bad
What is SPT?

# Good
Explain for the uninitiated. Define any specialist term the first time it appears.
Keep citations. Avoid ambiguity.

What is the Standard Penetration Test (SPT), how is it performed in the field, and
what physical property of the soil does the SPT blow count (N-value) measure?
Answer only using information found in the notebook sources. If not covered, say so.
```

### Contextualised analysis query

```
Explain for the uninitiated. Define any specialist term the first time it appears.
Keep citations. Avoid ambiguity.

Context: A geotechnical investigation has found SPT N-values between 4 and 8 at 3 m
depth in a sandy silt deposit beneath a proposed residential foundation.

Question: Based on the sources in this notebook, what bearing capacity concerns should
a geotechnical engineer flag for a residential foundation on a sandy silt deposit with
SPT N-values between 4 and 8 at 3 m depth? List the key failure modes and any
relevant NZ standard references.

Answer only using information found in the notebook sources. If not covered, say so.
```

---

## Common Mistakes and Fixes

| Mistake | Why it fails | Fix |
|---------|-------------|-----|
| Vague instruction ("tell me about X") | Forces the model to guess scope | Use a specific, bounded question |
| Pronoun references ("it", "that value") | Retrieval engine loses context | Replace with explicit noun phrases |
| Multi-question blob | Model skips or conflates questions | Decompose; one query per topic |
| No output format specified | Response shape is unpredictable | Always name the format: cited prose, JSON, bullet list |
| Negative constraints ("don't hallucinate") | Less reliable than positive framing | Use `"Answer only from sources. If absent, say so."` |
| No audience prefix | Jargon goes unexplained; citations may be omitted | Always prepend the standard audience prefix |
| Leading/biased phrasing | Model validates your premise instead of analyzing | Use neutral language: "What are the advantages and challenges?" |

---

## Quick Checklist

Before sending any query to NotebookLM, verify:

- [ ] Audience prefix present (`Explain for the uninitiated...`)
- [ ] Instruction is a single, concrete task
- [ ] All pronouns replaced with explicit noun phrases
- [ ] Context and instructions separated by delimiters if mixing both
- [ ] Output format stated
- [ ] Scope constraint present (`Answer only from sources...` + escape hatch)
- [ ] If the query is long (>150 words): refocus statement at the end
- [ ] Multi-part question decomposed into sequential queries

---

## Prompt Anatomy Quick Reference

```
[Audience prefix]           ← always first
[Role / Persona]            ← optional; use when domain frame matters
[Context block]             ← what you already know; delimited
[Instruction]               ← one task, one question
[Constraints]               ← framed positively
[Output Format]             ← explicit
[Examples]                  ← optional; use for format-critical queries
[Refocus + Transition]      ← required for long prompts
```
