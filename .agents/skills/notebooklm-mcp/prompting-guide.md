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

### Rule 6 — Schema Contract for Structured Output

When you ask NotebookLM to extract data into a table, CSV, or JSON object, the
retrieval step finds relevant passages but the generation step has no schema to
constrain its output. Without an explicit contract, the model improvises column
names, invents enum synonyms ("Critical" instead of "High"), wraps output in
markdown code fences, and injects conversational filler — all of which break
downstream parsing.

NotebookLM has no API-level parameter to enforce a JSON schema (unlike OpenAI's
structured outputs). Emulate how Pydantic AI instructs LLMs: define a strict
**Schema Contract** directly in the prompt that dictates fields, data types,
constraints, and the exact output format.

The contract has five parts:

1. **Explicit Types** — label each field with `[String]`, `[Integer]`,
   `[Float]`, `[Boolean]`, `[Enum]`, etc. This forces the model to think
   programmatically about the value it writes.
2. **Enum Constraints** — list the exact allowed values
   (e.g. `"High", "Medium", "Low"`). Prevents synonyms that break parsing.
3. **Missing-Value Sentinel** — define what to output when the sources lack a
   value (e.g. `"N/A"` for strings, `null` for numbers). Without this the model
   guesses or omits the field entirely. For booleans, prefer a three-value enum
   (`"TRUE"`, `"FALSE"`, `"UNKNOWN"`) so "not stated" is distinguishable from
   a confirmed negative.
4. **Explicit Delimiter & Row Separator** — state the column delimiter
   (`comma`) and that each record must be on its own line. Without this the
   model may use spaces or collapse all rows onto one line.
5. **One-Shot Example Row** — after the schema, include a single example row
   that anchors the exact format (delimiter, quoting, line breaks). This
   eliminates residual ambiguity that the schema text alone cannot.

Always pair the schema with a formatting instruction: *"Provide raw CSV/JSON
only. No markdown code fences, no commentary, no explanations."*

**Boundary anchoring (JSON):** Add `"Start your response with [ and end
with ]. Nothing else."` Without this, the model often wraps valid JSON in
conversational prose.

**Citation markers in values:** NotebookLM may inject citation markers
(e.g. `\n1\n`) directly inside string values, breaking JSON/CSV parsing.
Add `"Do not embed citation numbers or markers inside field values."` to the
output format block. If citations still leak through, post-process with a
regex strip (`\n\d+\n`).

**Complex / nested schemas:** On a cold-start (first message in a session),
complex nested schemas often fail — the model defaults to narrative mode.
For nested extractions, warm up the session with a simpler flat query first,
then request the nested version as a follow-up in the same session.

See the Before / After templates below for CSV and JSON examples.

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

### Tabular extraction (CSV)

```
# Bad — no schema, ambiguous formatting
Extract the design requirements from Section 4 and put them in a table.
Include the clause, a summary, the risk level, and whether we need to act.

# Typical messy result without a schema:
#   Clause 4.1 – Requires adequate bearing capacity → HIGH risk, action needed
#   "4.2: Settlement must be < 25 mm" (medium)
#   ...
# Problems: inconsistent delimiters, invented risk labels, mixed formats.
```

```
# Good — Schema Contract
Explain for the uninitiated. Define any specialist term the first time it appears.
Keep citations. Avoid ambiguity.

Extract all design requirements from Section 4 of the guidelines.

OUTPUT FORMAT:
Provide raw CSV only. No markdown code fences, no commentary, no explanations.
Use comma (,) as the column delimiter. Place each row on its own line.

SCHEMA (each row = one requirement):
- "Clause":      [String]  Exact clause reference, e.g. "4.1.2".
- "Requirement": [String]  One-sentence summary. Maximum 15 words.
- "Risk_Level":  [Enum]    Exactly one of: "High", "Medium", "Low".
- "Actionable":  [Enum]    Exactly one of: "TRUE", "FALSE", "UNKNOWN".

MISSING VALUES: Use "N/A" for strings. Use "UNKNOWN" for Actionable when
the source does not state whether the requirement needs action.

EXAMPLE (first two rows, for format reference):
Clause,Requirement,Risk_Level,Actionable
4.1.2,Foundation must resist lateral loads,High,TRUE

Answer only using information found in the notebook sources. If not covered,
say so.
```

### Structured extraction (JSON)

```
# Bad — shape left to the model
List all the soil layers found in Borehole BH-01 with their depths and
classification. Return as JSON.

# Typical messy result without a schema:
#   {"layers": ["Fill (0-1.5m)", "Alluvial Sandy SILT, 1.5 to 4.0m, ..."]}
# Problems: depths embedded in free text, no consistent keys, flat strings
# instead of typed fields.
```

```
# Good — Schema Contract
Explain for the uninitiated. Define any specialist term the first time it appears.
Keep citations. Avoid ambiguity.

Extract all soil layers logged in Borehole BH-01.

OUTPUT FORMAT:
Provide raw JSON only. No markdown code fences, no commentary, no explanations.
Do not embed citation numbers or markers inside field values.
Return a JSON array of objects, one per layer.
Start your response with [ and end with ]. Nothing else.

SCHEMA (each object):
- "top_m":       [Float]   Top depth in metres.
- "base_m":      [Float]   Base depth in metres.
- "description": [String]  Soil description as logged. Maximum 20 words.
- "uscs_class":  [String]  USCS classification symbol, e.g. "SM", "CL".
- "origin":      [Enum]    Exactly one of: "Fill", "Natural", "Unknown".

MISSING VALUES: Use null for numbers, "N/A" for strings, "Unknown" for origin.

EXAMPLE (single object, for format reference):
[{"top_m": 0.0, "base_m": 1.5, "description": "Compacted hardfill", "uscs_class": "GP", "origin": "Fill"}]

Answer only using information found in the notebook sources. If not covered,
say so.
```

### Nested extraction (JSON with arrays)

For complex, nested structures (e.g. a parent object containing an array of
child objects), warm up the session with a flat extraction first, then request
the nested version in a follow-up message using the same `session_id`.

```
# Step 1 — Warm-up (flat extraction, first message)
Explain for the uninitiated. Define any specialist term the first time it appears.
Keep citations. Avoid ambiguity.

List all contract frameworks mentioned in the sources that describe subsurface
construction risk allocation. For each framework, state who bears the default
risk and the primary allocation mechanism.

OUTPUT FORMAT:
Raw JSON array only. No markdown code fences, no explanations.
Do not embed citation numbers or markers inside field values.
Start your response with [ and end with ]. Nothing else.

SCHEMA (each object = one framework):
- "framework":          [String] Name of the framework. Maximum 6 words.
- "allocated_to_default":[Enum]   Exactly one of: "Owner", "Contractor", "Shared", "Unspecified".
- "mechanism":          [String] How risk allocation works. Maximum 15 words.

EXAMPLE:
[{"framework":"FIDIC Emerald Book","allocated_to_default":"Shared","mechanism":"GBR baseline exceedance triggers owner liability"}]

Answer only using information found in the notebook sources. If not covered, say so.
```

```
# Step 2 — Nested follow-up (same session_id)
Now expand each framework with its specific risk categories.

OUTPUT FORMAT:
Raw JSON array only. No markdown code fences, no explanations.
Do not embed citation numbers or markers inside field values.
Start your response with [ and end with ]. Nothing else.

SCHEMA (top-level = one framework):
- "framework":        [String] Name. Maximum 6 words.
- "risk_allocations": [Array]  Array of risk allocation objects.

SCHEMA (each object inside "risk_allocations"):
- "risk_category": [String] Type of risk. Maximum 8 words.
- "allocated_to":  [Enum]   Exactly one of: "Owner", "Contractor", "Shared", "Unspecified".
- "mechanism":     [String] How allocation works. Maximum 15 words.

MISSING VALUES: Use "N/A" for strings, "Unspecified" for allocated_to.

EXAMPLE:
[{"framework":"FIDIC Emerald Book","risk_allocations":[{"risk_category":"Unforeseen ground conditions","allocated_to":"Shared","mechanism":"GBR baseline exceedance triggers owner liability"}]}]

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
| No schema contract for structured output | Model improvises column names, enum synonyms, and formatting | Define fields with types, enum values, missing-value sentinels, and a raw-output instruction (Rule 6) |
| Complex nested schema on cold start | Model defaults to narrative prose, ignores JSON schema entirely | Warm up the session with a flat extraction first, then request nested version in follow-up |
| No boundary anchoring for JSON | Model wraps valid JSON in conversational prose | Add `"Start your response with [ and end with ]. Nothing else."` |
| Citation markers in structured values | NotebookLM injects `\n1\n` markers into field values, breaking parsing | Add `"Do not embed citation numbers inside field values"`; post-process with regex if needed |

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
- [ ] If requesting structured data: schema contract with types, enums, and missing-value sentinels (Rule 6)

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
