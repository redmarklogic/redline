# Eda Visual Design — Detailed Reference

## Procedure

Apply these rules whenever creating or reviewing a statistical or EDA plot. Rules are language- and library-agnostic.

> **Prerequisite**: Before applying any rule below, complete the pre-flight data
> quality check in `.agents/skills/eda-interpreting-data/SKILL.md`. A single
> axis-compressing outlier makes all design rules irrelevant. Clean the data first.

# EDA Visual Design

## 1. Match Chart Type to the Data Relationship

Select the chart geometry that matches the mathematical relationship being shown.
A wrong chart type forces a false conceptual model onto the reader.

| Relationship                      | Use                               | Avoid                                   |
| --------------------------------- | --------------------------------- | --------------------------------------- |
| Continuous trend over time        | Line chart                        | Bar chart (implies discrete buckets)    |
| Correlation between two variables | Scatter plot                      | Line connecting unrelated points        |
| Categorical magnitude             | Bar chart (y starts at 0)         | Pie or bubble chart                     |
| Distribution (continuous)         | Histogram, KDE, violin            | Bar chart of binned counts              |
| Distribution (small n, <30/group) | Violin + strip overlay            | Boxplot (hides individual observations) |
| Single-variable ranking           | Sorted horizontal bar or dot plot | Single-column heatmap                   |
| Two-variable matrix               | Heatmap                           | Sorted bar (loses matrix structure)     |
| Cumulative concentration          | Lorenz curve                      | Ranked bar chart                        |
| Part-of-whole (few categories)    | Stacked bar                       | Pie chart                               |

A heatmap requires at least two categorical dimensions. Do not use it for a
single column of ranked values — that is a sorted bar or dot plot.

For small-n groups (<30 observations), use violin + strip instead of a boxplot.
The box collapses real variation into five statistics and hides skew and gaps.

## 2. Maximise Data-Ink Ratio

Every visual element must encode new information. Remove anything a reader
can remove without losing understanding.

**Always remove:**

- Heavy background grids, 3D effects, drop shadows, gradient fills
- Colour encoding when annotated numbers already carry the value
- Redundant legends when the axis already names the category
- Decorative cell borders that add no grouping information

**Keep only:** data marks, axis labels with units, a descriptive title,
and annotations that name specific values the reader must compare.

When two visualisations in the same section show the same pattern, keep
the more precise one and remove the other.

## 3. Use Position Before Colour

Cleveland's perceptual hierarchy (most to least accurate for magnitude comparison):
position → length → angle → area → colour saturation/hue.

- Use position (bar, dot plot) for the primary comparison.
- Use colour only for a secondary categorical grouping.
- Never use colour as the sole carrier of the primary variable.
- Avoid pie charts (angle is 4th) and bubble charts (area is 5th) for precise
  comparisons.

## 4. Maintain Graphical Integrity

- Bar charts must start at zero. Truncating distorts length encoding (Tufte's "Lie Factor").
- Set colour scale limits to match the actual data range, not a theoretical maximum.
- Time always flows left to right on the x-axis.
- Place the independent variable on x and the dependent variable on y.
- When observations carry timestamps, use datetime on the x-axis. An arbitrary index
  is a last resort only when no temporal information exists.

## 5. Sort Categories by the Variable of Interest

When a plot ranks or compares categories by a quantitative variable, sort the
rows or bars by that variable — not by insertion order, code list, or alphabet.
Unsorted categorical axes force the reader to mentally re-rank every item.

Exception: when a natural universally-understood order exists (e.g., months of
the year, chronological survey rounds), use that order instead.

## 6. Show Uncertainty and Context

- For correlations: annotate with the coefficient, p-value (or significance stars),
  and sample size n.
- For distributions: show spread via violin, density bands, or error bars — not
  only a central tendency marker.
- When domain thresholds exist, overlay them as reference lines or bands so
  values are self-interpreting without prose.
- Annotate contextual reference marks (vertical lines, bands, threshold markers)
  directly on the plot with a short label. Do not rely solely on a title string
  or figure caption to explain what a reference mark represents. A reader who <!-- hook: allow -->
  sees only the rendered image must understand the mark without reading surrounding <!-- hook: allow -->
  text.

## 7. Label Completely and Unambiguously

Every plot must have:

- A descriptive title stating what is shown.
- Axis labels with units of measurement.
- A data-subset qualifier in the title, axis label, and caption independently
  when multiple strata exist. A reader who sees only the image must know
  which subset is plotted.
- Full expansion of every code, abbreviation, or single-letter identifier used
  in legends, tick labels, or annotations. Never show raw database codes (e.g. `E`,
  `N`) when a human-readable label (e.g. `East pond`, `North pond`) is available.

Define acronyms on first narrative use: `Full Name (ACRONYM)`.

## 8. One Plot, One Message

Each plot answers one analytical question. If a figure needs a paragraph to
decode, it is either the wrong chart type or asking too many questions at once.

- Use facet grids (small multiples) when a grouping variable has more than
  ~4 levels.
- Avoid overlaying more than ~4 series on a single panel.

## 9. Remove Redundancy Across the Section

Before adding a new visualisation, verify no adjacent element already
communicates the same pattern. If the answer is the same, keep the more
precise representation and remove the other.

## 10. Write the Post-Plot Narrative After Reading the Plot

- Frame hypotheses and questions before the plot.
- After the plot, state what it actually shows: observed values, direction,
  which hypothesis the result supports or contradicts, and what remains ambiguous.
- Use dynamic values computed in the same cell. Never hard-code numbers in prose.
- Do not write conditional narratives ("if X then A, if Y then B") after the
  result is already visible.

## 11. Position Legends to Minimise Data Obstruction

Default placement is **top-left, horizontal orientation**. English-language
readers scan left-to-right, top-to-bottom, so a top-left legend is seen first
and requires no extra eye movement.

**Adjustment rule:** move the legend to whichever corner overlaps the least
data. The default assumes a clear top-left region; override it when the data
shape says otherwise:

| Data pattern                              | Preferred legend position              |
| ----------------------------------------- | -------------------------------------- |
| Values rise with x (low-left, high-right) | Top-left (default)                     |
| Values fall with x (high-left, low-right) | Top-right or bottom-right              |
| High density at both ends of x            | Bottom-centre or outside the plot area |
| Flat / no clear trend                     | Top-left (default)                     |

- Prefer horizontal layout when the legend has few items (up to ~4); switch to
  vertical when items would overflow the plot width.
- If no in-canvas position avoids obstruction, move the legend outside the plot
  area entirely.
- Never let a legend box hide data points, lines, or distribution shapes that
  the reader needs to interpret.

## Quick Checklist

- [ ] **Pre-flight data quality check complete** (see `eda-interpreting-data`)
- [ ] Chart type matches the data relationship (Rule 1)
- [ ] No decorative ink — every element encodes information (Rule 2)
- [ ] Primary comparison uses position, not colour alone (Rule 3)
- [ ] Axes start at zero for magnitude comparisons; colour scale matches data range (Rule 4)
- [ ] Categories sorted by the variable of interest (Rule 5)
- [ ] Uncertainty shown; reference marks labelled directly on the plot (Rule 6)
- [ ] Title, axis labels, units, subset qualifier, and full label expansions present (Rule 7)
- [ ] One clear message per plot (Rule 8)
- [ ] No redundancy with adjacent tables or plots (Rule 9)
- [ ] Post-plot narrative reports the actual result with dynamic values (Rule 10)
- [ ] Legend placed where it least obstructs data; top-left horizontal by default (Rule 11)
