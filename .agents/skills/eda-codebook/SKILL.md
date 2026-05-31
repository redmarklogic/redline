---
name: eda-codebook
description: Use when generating or updating a Markdown codebook (data dictionary + statistical profile) for a CSV or Excel dataset
---

## Boundary Contract

### Applies To
- CSV and Excel datasets requiring documentation or profiling

### Produces
- Markdown codebook (data dictionary + statistical profile) with layperson glossary

### Does Not Cover
- Data quality investigation (`eda-qa`)
- Plot construction (`eda-visual-design`)
- Data ingestion pipelines (`python-data-ingestion`)


See `procedures/eda-codebook.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Overwriting an existing codebook instead of updating it | Check for an existing file at the output path; update in place, never overwrite without diffing |
| Omitting the layperson glossary section | Every codebook must include a plain-language glossary — domain jargon must be decoded for non-specialist readers |
| Computing statistics on non-numeric columns | Restrict statistical profiling to numeric columns; apply categorical frequency counts to string columns |