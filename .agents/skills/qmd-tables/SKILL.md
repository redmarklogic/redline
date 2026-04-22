---
name: qmd-tables
description: Conventions for rendering tabular output in Quarto (.qmd) documents using great_tables GT — cross-format (HTML/PDF) helpers, percentage formatting, row labels, missing values, and when to prefer a chart over a table.
---

# QMD Tables

## Boundary Contract

### Applies To
- Tables in Quarto `.qmd` documents using `great_tables.GT`

### Produces
- Cross-format (HTML/PDF) tables with proper formatting and accessibility

### Does Not Cover
- Narrative design and structure (`qmd-narrative-design`)
- Plot construction (`eda-visual-design`)
- Data quality screening (`eda-interpreting-data`)

## BLOCKING RULE — Read Before Any Table Output

> **NEVER use `print(df.to_markdown(...))`, `print(df.to_string())`, or bare variable display for any runtime-computed DataFrame in a `.qmd` file.** This rule applies unconditionally: during initial authoring, during edits, and during review. Violation of this rule has occurred in production code when this skill was loaded but this constraint was not front of mind. Use `great_tables.GT` exclusively. There are no exceptions for "quick diagnostics", "merge summaries", or "metric tables".

## Procedure

Apply this skill whenever adding or reviewing a table in a Quarto `.qmd` document — whether in an EDA notebook, results report, or client-facing deck. Use `great_tables.GT` for computed DataFrames, implement cross-format helpers for multi-output documents, and always decide whether a table or chart better serves your audience.

## 1. Always Use `great_tables.GT` for Computed DataFrames

Never display a runtime-computed DataFrame with `print(df.to_string())` or by bare
variable display. In HTML output this produces monospaced text; in PDF/typst it renders
as raw terminal output without borders or formatting.

| Data origin                                               | Rendering approach    |
| --------------------------------------------------------- | --------------------- |
| Computed at runtime (any data derived from analysis code) | `great_tables.GT`     |
| Static reference data (does not change between runs)      | Markdown table syntax |

## 2. Use the Cross-Format `_gt()` Helper in Multi-Output Documents

Quarto documents targeting both HTML and PDF/typst require a format-aware output
function. Define it once in the notebook setup cell:

```python
import os
from great_tables import GT as _GT

def _gt(gt_tbl) -> None:
    _qfmt = os.environ.get("QUARTO_DOCUMENT_FORMAT", "html")
    if _qfmt in ("pdf", "typst", "latex", "beamer"):
        print(gt_tbl.as_latex())
    else:
        print(gt_tbl.as_raw_html())
```

Every cell that calls `_gt()` must declare `#| output: asis` so Quarto passes the
raw HTML or LaTeX through without escaping it.

If the document targets HTML only, calling `gt_tbl.as_raw_html()` directly with
`#| output: asis` is sufficient — the full helper is only needed for multi-format builds.

## 3. Control Row Labels via `rowname_col`, Not `set_index`

Pass the DataFrame without `.set_index()`. Use the `rowname_col=` parameter in
`GT(df, rowname_col="col_name")` instead. This gives GT full control over how the
row-label column is rendered and styled.

```python
# Good
GT(df, rowname_col="parameter")

# Bad — removes GT's ability to style the row-label column
GT(df.set_index("parameter"))
```

## 4. Handle Missing Values with `sub_missing`

Always call `.sub_missing(missing_text="—")` to render `None` or `NaN` cells as an
em-dash rather than an empty cell or the literal string `nan`.

## 5. Format Percentage Columns with `fmt_percent`

Never use `.fmt_number()` for a column whose values represent percentages.
Use `.fmt_percent()` instead.

| Parameter             | Rule                                                                                                                                |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `scale_values`        | Set to `False` when values are in the 0–100 range. The default `True` multiplies by 100, which is correct only for 0–1 source data. |
| `drop_trailing_zeros` | Set to `True` so `100.0%` renders as `100%` and `0.0%` as `0%`.                                                                     |
| `decimals`            | Infer from the data spread; do not pre-round values in Python before passing to GT — let GT own the rounding.                       |

Use this helper to infer decimal places automatically:

```python
def _pct_decimals(values) -> int:
    """Infer decimal places for a 0-100 percentage column."""
    arr = np.asarray([v for v in np.asarray(values).flatten() if not np.isnan(v)], dtype=float)
    if len(arr) == 0:
        return 1
    interior = arr[(arr > 0.5) & (arr < 99.5)]
    if len(interior) < 2:
        return 0
    return 2 if float(interior.max() - interior.min()) < 1.0 else 1
```

Full pattern:

```python
_decimals = _pct_decimals(df["coverage_pct"].values)

GT(df).fmt_percent(
    columns="coverage_pct",
    scale_values=False,        # values already in 0–100
    decimals=_decimals,
    drop_trailing_zeros=True,  # 100.0% → 100%, 0.0% → 0%
)
```

## 6. Drop a Table When a Labelled Chart Already Shows the Same Information

Before rendering a table, check whether any adjacent visualisation (bar chart, dot plot)
with value labels already communicates the same pattern. If it does, remove the table.
A labelled bar chart is more scannable and carries lower cognitive load than a companion
table with identical values.

Keep the underlying DataFrame construction if it feeds a downstream cell or an evidence
table — only suppress the visible rendered output.

## 7. Set Explicit Column Widths on Static Markdown Tables

Browser layout engines size Markdown table columns proportionally to the longest token
in each column's header or cells. This makes any column whose **header is long relative
to its content** (e.g. `Priority`, `Status`, `Type`) consume far more width than it
deserves, squeezing the content-heavy columns (e.g. `Why`, `Description`, `Notes`) that
should be getting the space.

Whenever a table has at least one short-identifier column alongside one or more
prose-heavy columns, add `tbl-colwidths` to redistribute width explicitly.

**How to compute the widths:**

1. For each column, collect the character lengths of the header and every cell value.
2. Take the **75th-percentile** length per column — not max (one outlier cell should not
   dominate) and not median (columns with occasional long cells still need headroom).
3. Express each column's p75 as a percentage of the total p75 across all columns. Round
   to integers; adjust the largest column by ±1 so values sum to 100.
4. **Hard cap:** any short-identifier column (`Priority`, `#`, `Status`, `Type`, `Rank`)
   must be capped at **10%**; redistribute freed percentage proportionally to the rest.

```markdown
| Priority | Action                                        | Why                                           |
| -------- | --------------------------------------------- | --------------------------------------------- |
| 1        | Install conductivity and sludge depth sensors | Enables Regression Kriging on continuous data |

: {tbl-colwidths="[8,35,57]"}
```

Quick calculation (illustrative):

```
col p75 chars:  Priority=8,  Action=42,  Why=72   → total=122
raw %:          6.6%         34.4%       59.0%
cap Priority:   8% (cap; +1.4% freed)  → Action=35%, Why=57%
final:          [8, 35, 57]
```

Always add the attribute — browser defaults are unreliable across viewport widths.

## Quick Checklist

- [ ] Computed DataFrame uses `great_tables.GT` — not `print(df.to_string())` or bare display (Rule 1)
- [ ] Cross-format `_gt()` helper defined in setup cell; calling cells declare `#| output: asis` (Rule 2)
- [ ] `rowname_col=` used instead of `.set_index()` for row labels (Rule 3)
- [ ] `.sub_missing(missing_text="—")` applied (Rule 4)
- [ ] Percentage columns use `.fmt_percent()` with `scale_values`, `drop_trailing_zeros`, and inferred `decimals` (Rule 5)
- [ ] No adjacent labelled chart already communicates the same data (Rule 6)
- [ ] Static Markdown tables with any short identifier column (Priority / Status / #) carry `tbl-colwidths` (Rule 7)
