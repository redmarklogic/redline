---
name: python-data-ingestion
description: Use when implementing data ingestion or validation -- import/process/read patterns, Pandera contracts, multi-worksheet handling, or schema reuse
paths: "src/**/*.py,tests/**/*.py"
---

## Boundary Contract

### Applies To
- Data reader modules under `functions/readers/` and Pandera schema definitions

### Produces
- Validated DataFrames via the import/process/read pattern with Pandera contracts

### Does Not Cover
- Domain value objects and constants (`python-domain-modeling`)
- General function design (`python-function-design`)
- Data versioning (`python-pins-data-version-control`)


See `procedures/python-data-ingestion.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Reading a file directly in a reader function instead of following import/process/read | Split into three functions: import_ (raw load), process_ (transform), 
ead_ (return typed output) |
| Defining the Pandera schema inline per caller | Define one DataFrameModel in domain/ and reuse it across all readers for the same source |
| Silently dropping rows with dropna during ingestion | Raise a validation error via Pandera; callers should decide how to handle missing data |