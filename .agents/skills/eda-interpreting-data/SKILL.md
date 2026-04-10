---
name: eda-interpreting-data
description: Pre-flight data quality screening and post-plot insight writing for EDA. Apply before building any distribution, scatter, or time-series plot: outlier detection, axis-compression diagnosis, decimal-shift and sentinel-zero correction patterns, and rules for writing insights from observed results.
---

# EDA — Interpreting Data

## Procedure

Apply Rules 1–7 sequentially _before_ building any plot. After the plot is rendered, apply Rules 8–10 to write the narrative interpretation.

For visual design decisions (chart type, axes, colours, labels), see `.agents/skills/eda-visual-design/SKILL.md`.

Apply this skill in sequence: rules 1–7 run _before_ any plot is built; rules 8–10
govern the narrative written after the plot is rendered.

For _how to build the plot_ (chart type, axes, colour, labels), see
`.agents/skills/eda-visual-design/SKILL.md`.

## 1. Screen Every Numeric Column Before Plotting

Compute summary statistics (min, max, percentiles, count of nulls) for every column
that will appear on an axis. Do this at first use of the dataset, not after a plot
looks wrong.

A value outside the physically plausible domain for its variable is evidence of an
anomaly. Do not plot before investigating.

## 2. Apply Domain Plausibility Bounds

Every physical measurement has bounds beyond which values are implausible regardless
of context. Use these as the initial screening gate.

| Variable class                    | Implausibly low                    | Implausibly high                           | Notes                                                                                            |
| --------------------------------- | ---------------------------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| Temperature (ambient water / air) | Below freezing for the environment | > 60 °C for liquid water                   | Field instruments and manual entry commonly produce 10× errors                                   |
| pH                                | < 0                                | > 14                                       | Physically impossible outside this range                                                         |
| Dissolved oxygen                  | < 0                                | > 50 mg/L                                  | Hypereutrophic ponds can genuinely exceed 20 mg/L via algal supersaturation — do not auto-reject |
| Electrical conductivity           | near 0 for any aqueous sample      | domain-dependent (seawater ≈ 55 000 µS/cm) | Order of magnitude above neighbours warrants investigation                                       |
| Relative humidity                 | < 0 %                              | > 100 %                                    |                                                                                                  |
| Atmospheric pressure              | < 870 hPa                          | > 1 084 hPa                                | Record extremes; most sites are much narrower                                                    |
| Percentages and saturations       | < 0 %                              | > theoretical maximum for variable         | Some saturations (DO %) can exceed 100% — check the variable definition                          |

Maintain a project-specific override table where the environment constrains the range
further (e.g., an ice-free inland pond narrows the water temperature window). Store
those bounds alongside the dataset codebook, not scattered in analysis scripts.

## 3. Diagnose With Corroborating Evidence Before Acting

For every out-of-range value, examine at least two independent lines of evidence
before deciding what it is:

- **Paired or redundant sensor**: same variable, same sample, different depth layer,
  instrument, or replicate.
- **Correlated variable**: a variable that co-varies with the suspect one (e.g.,
  conductivity and TDS should scale together; if one is ×10 high and the other is
  not, the error is isolated).
- **Spatial neighbours**: other sites in the same sampling round.
- **Temporal neighbours**: earlier and later measurements at the same site.

Do not conclude "transcription error" from a single suspicious value alone.

## 4. Classify Every Anomaly Before Correcting It

| Class                                  | Criterion                                                                                                                                           | Action                                                                                                 |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **A — Confirmed error, recoverable**   | True value can be inferred with high confidence from corroborating evidence; recovered value is consistent with neighbours and within domain bounds | Correct in analysis code with an auditable guard; document in source codebook                          |
| **B — Suspected error, unrecoverable** | Value is implausible but no reliable corroboration exists to infer the true value                                                                   | Exclude (null); document in codebook; note in figure caption                                           |
| **C — Genuine extreme**                | Value appears implausible by the reference table but is physically explicable given the specific context                                            | Retain; verify with domain knowledge; annotate the figure; update the reference table bounds if needed |

Never skip classification. "Looks like an outlier" is not a class.

## 5. Correct Class A Errors Auditably

When applying a correction in analysis code:

- Filter to the exact row using all identifying keys (site, date, layer, raw value).
- Assert the filter matches exactly one row. Raise an error if it does not.
- Overwrite the cell. Never modify the source file.
- Include a comment naming the error class, the evidence, and the codebook reference.

The assertion is not optional. It ensures the correction breaks loudly — rather than
silently doing nothing or corrupting more rows — if the upstream data ever changes.

## 6. Document Every Anomaly in the Source Codebook

Regardless of class, add a prominent note to the codebook for the originating
dataset. This is the authoritative record for any future consumer of that data.

The note must state: the variable and location (site, date, layer), the raw value
and units, the anomaly class, the evidence, the corrected or excluded value, and the
discovery date.

## 7. Rescue Axis-Compressed Plots Explicitly

If a genuine extreme (Class C) or an unresolvable suspected error (Class B) remains
in the data after classification, the plot axis will compress all other observations.
Do not accept a compressed plot silently.

Options in order of preference:

| Situation                                                      | Preferred action                                                                                                   |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Class A error confirmed                                        | Correct the value (Rule 5); re-plot on a linear axis                                                               |
| Class B or C — value is extreme but real                       | Clip the display axis to a meaningful range; annotate with "N values outside display range" directly on the figure |
| Distribution is genuinely right-skewed across all observations | Use a log-scale axis; label it explicitly                                                                          |

Never clip or log-scale without annotating the figure. A reader who sees only the
image must know the axis has been modified and why.

---

## Common Anomaly Patterns

| Pattern                                   | Signature                                                                                                               | Detection heuristic                                                                                   | Recovery                                                                                     |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **Decimal-point shift**                   | One value is exactly 10× or 100× higher (or lower) than all neighbours                                                  | Value exceeds 5× the 99th percentile of the same column                                               | Divide by 10; accept if result falls within domain bounds and matches corroborating readings |
| **Sentinel zero**                         | All measurement columns for a row are simultaneously 0, while a structural column (ID, timestamp, metadata) is non-null | Flag rows where every measurement column is exactly 0 simultaneously                                  | Replace all zeros on that row with null; do not attempt to recover individual values         |
| **Sentinel null coded as a valid number** | A specific non-zero number (e.g., −9999, 999, −1) appears repeatedly at positions where values are absent               | Check the dataset documentation; sort by the suspect column and inspect the highest and lowest values | Replace sentinel with null; document the sentinel value in the codebook                      |
| **Unit mismatch**                         | Values are consistently scaled by a fixed factor relative to a known reference (e.g., all in mg where µg expected)      | Compare to a trusted reference measurement or published typical range                                 | Apply a scale factor; document the source unit and the conversion                            |

---

## 8. State the Actual Result — Not the Hypothesis

After a plot is rendered, the accompanying narrative must report what the plot shows.
Do not restate the hypothesis as if it were the finding, and do not describe what
_would_ follow _if_ a pattern were present.

- Report direction, magnitude, and any notable feature (bimodality, cluster,
  seasonal split, outlier group).
- Do not restate the plot title.
- If the plot contradicts the hypothesis, say so directly.

## 9. Use Computed Values — Never Hard-code Numbers in Narrative

Every statistic cited in prose (median, range, correlation coefficient, sample size)
must be read from a computed variable in the same analysis unit, not typed manually.

Hard-coded numbers become stale silently when data changes. A computed value that
references the actual result is always correct.

## 10. Name the Hypothesis; Flag Remaining Ambiguity

Every narrative block must close two questions:

1. Does the observed pattern support, contradict, or remain inconclusive regarding
   the hypothesis stated before the plot?
2. What limits confidence in the finding? Name it explicitly — small n, a pattern
   driven by a single cohort or time period, confounding with another variable.

Do not leave either question unanswered with vague language ("further analysis may
be needed").

---

## Quick Checklist

- [ ] Summary statistics computed for every numeric column to be plotted (Rule 1)
- [ ] Min/max checked against domain plausibility bounds (Rule 2)
- [ ] Every out-of-range value diagnosed with at least two corroborating lines of evidence (Rule 3)
- [ ] Every anomaly classified as A, B, or C before any correction is applied (Rule 4)
- [ ] Class A corrections applied with an exact-row filter and a count assertion (Rule 5)
- [ ] Every anomaly documented in the source codebook regardless of class (Rule 6)
- [ ] No axis-compressed plots accepted silently; clipped/log axes annotated on the figure (Rule 7)
- [ ] Post-plot narrative states the observed result, not the hypothesis (Rule 8)
- [ ] All cited statistics are computed values, not hard-coded numbers (Rule 9)
- [ ] Narrative names the hypothesis outcome and any remaining ambiguity (Rule 10)
