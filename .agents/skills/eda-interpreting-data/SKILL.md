---
name: eda-interpreting-data
description: Use when screening data quality before building an EDA plot, or writing insights after observing results -- outlier detection, axis compression, or decimal-shift correction
---

## Boundary Contract

### Applies To
- Pre-flight data quality screening before any distribution, scatter, or time-series plot

### Produces
- Cleaned data with outlier, axis-compression, and sentinel-zero corrections; post-plot narrative insights

### Does Not Cover
- Chart type selection and visual design (`eda-visual-design`)
- Codebook generation (`eda-codebook`)
- Data quality assurance against codebooks (`eda-qa`)


See `procedures/eda-interpreting-data.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Plotting without a pre-flight data quality check | Run outlier detection and range checks before any visualisation; a single sentinel value can compress the entire axis |
| Writing "the data shows X" without quantifying X | Every insight must cite a specific value, range, or percentage � vague observations are not insights |
| Treating all outliers as errors | Investigate before removing; some outliers are legitimate domain extremes, not noise |