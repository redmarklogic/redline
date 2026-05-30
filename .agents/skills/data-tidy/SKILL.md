---
name: data-tidy
description: Use when designing DataFrame schemas or value-object models that must adhere to tidy data principles
---
## Boundary Contract

### Applies To
- DataFrame schema design and value-object modeling decisions

### Produces
- Tidy data structures (one variable per column, one observation per row, one table per observational unit)

### Does Not Cover
- Data ingestion implementation (`python-data-ingestion`)
- Domain modeling specifics (`python-domain-modeling`)
- Dataset versioning (`python-pins-data-version-control`)


See `procedures/data-tidy.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Storing multiple variables in a single column (e.g. depth_0.5m_kPa) | One column per variable; encode depth and unit as separate columns |
| Using wide format when observations are repeated measures | Use long (tidy) format: one row per observation, one column per variable |
| Mixing units in the same column | Normalise to one unit per column; store the unit in the column name or metadata |