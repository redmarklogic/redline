---
name: eda-qa
description: Use when auditing an existing codebook and raw dataset for data quality problems -- requires a codebook to already exist
---

## Boundary Contract

### Applies To
- Raw datasets with an existing codebook for data quality investigation

### Produces
- Updated codebook Findings section with validated data quality problems

### Does Not Cover
- Codebook creation (`eda-codebook`)
- Visual design (`eda-visual-design`)
- Pre-flight data screening (`eda-interpreting-data`)


See `procedures/eda-qa.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Running EDA QA without an existing codebook | This skill requires a codebook; run eda-codebook first if none exists |
| Reporting a data quality issue without a concrete hypothesis | Every nominated problem must include a falsifiable hypothesis about its cause |
| Marking a column as clean without checking its full distribution | A column can have clean min/max but still contain sentinel zeros or mid-range nulls |