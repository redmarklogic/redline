---
name: rag-prompting
description: Use when writing queries for a NotebookLM notebook — covers prompt anatomy, RAG retrieval rules, structured extraction schemas, and hallucination scoping.
---

## Boundary Contract

## When to Use

- Before sending any query to a NotebookLM notebook.
- When an agent or skill needs to formulate a question for NotebookLM.
- When extracting structured data (CSV, JSON) from notebook sources.


See `procedures/rag-prompting.md` for detailed rules, examples, and extended reference.

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
