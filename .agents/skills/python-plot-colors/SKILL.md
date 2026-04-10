---
name: python-plot-colors
description: Color selection, colormap choice, color-blindness safety, and cross-figure consistency for all plotting libraries used in this repo.
---

# Plot Colors

This skill governs how colors are chosen and applied in any plot produced in this
repo — whether with matplotlib, seaborn, plotly, altair, or another library.

Good color use is a learned discipline. The overarching rule is: **color must
encode information. Never use it as decoration.**

## Context & Guidelines

### Scope

Apply whenever you create, review, or refactor a plot in `src/scripts/`, `src/notebooks/`,
`src/<package>/`, or notebooks files (.qmd and .ipynb) anywhere in the repo.

### The `cmap` library (optional cross-library bridge)

[`cmap`](https://github.com/pyapp-kit/cmap) is a numpy-only library that exposes
colormaps from matplotlib, cmocean, colorbrewer, crameri, seaborn, and others, and
can export them to matplotlib, plotly, bokeh, altair, vispy, and more.

Use it when:

- You need a colormap that is not built into your plotting library.
- You want a single source of truth for a colormap that is shared across different
  visualization backends.

Install via `uv add cmap`. Basic usage:

```python
import cmap
cm = cmap.Colormap("okabe_ito")          # colorblind-friendly qualitative
mpl_cm = cm.to_matplotlib()              # hand to matplotlib
plotly_cs = cm.to_plotly()               # hand to plotly
```

If matplotlib is already in the environment, prefer `matplotlib.colormaps` directly
to avoid an extra dependency.

---

## 1. Choose the right colormap _type_

Select the colormap category that matches the structure of your data. Using the wrong
type misleads the viewer.

| Data structure                                            | Category        | Recommended colormaps                     |
| --------------------------------------------------------- | --------------- | ----------------------------------------- |
| Ordered / continuous, no midpoint                         | **Sequential**  | `viridis`, `plasma`, `cividis`            |
| Deviates from a critical midpoint (e.g. flux around zero) | **Diverging**   | `BrBG`, `RdBu`                            |
| Wraps at endpoints (angle, time-of-day, wind direction)   | **Cyclic**      | `twilight`, `twilight_shifted`            |
| Unordered categories                                      | **Qualitative** | Okabe-Ito (preferred), `tab10` (fallback) |

**Sequential colormaps** must increase monotonically in lightness ($L^*$). This
ensures they degrade gracefully when printed in grayscale and are interpretable
without color vision.

**Diverging colormaps** should have equal lightness at both extremes and peak
near $L^* = 100$ in the center. `BrBG` and `RdBu` satisfy this; `coolwarm` does
not span a wide $L^*$ range and should be used cautiously.

---

## 2. Always use perceptually uniform colormaps for continuous data

Perceptually uniform colormaps map equal steps in data to equal perceived steps in
color. This is what allows the viewer to accurately read magnitudes without
distortion.

**Preferred sequential/continuous colormaps** (`viridis`, `plasma`, `inferno`,
`magma`, `cividis`) are perceptually uniform and therefore first-choice options.
`cividis` is additionally optimized for color-vision-deficient viewers and is the
recommended default when the audience is unknown or broad.

### Banned colormaps

Never use the following — they are not monotone in lightness, cause perceptual
banding, and print as indecipherable noise in grayscale:

- `jet`
- `rainbow`
- `hsv`
- `gist_rainbow`
- `nipy_spectral`
- `spectral`
- `turbo` (visually attractive but not perceptually uniform; use only if the goal
  is pure display aesthetics with no quantitative reading expected)

---

## 3. Color-blindness safety

Approximately 8% of men and 0.5% of women have a color-vision deficiency (CVD).
The most common form is red-green deficiency (deuteranopia / protanopia).

**Rules:**

- Never use red and green as the _only_ distinguishing feature between two series.
- For sequential/continuous data, prefer `cividis` over `viridis` when accessibility
  is a concern.
- For qualitative/categorical data, use the **Okabe-Ito** palette as the default.
  It is designed to be distinguishable under all common CVD types:

  ```python
  # Okabe-Ito 8-color palette (safe under deuteranopia, protanopia, tritanopia)
  OKABE_ITO: list[str] = [
      "#E69F00",  # orange
      "#56B4E9",  # sky blue
      "#009E73",  # bluish green
      "#F0E442",  # yellow
      "#0072B2",  # blue
      "#D55E00",  # vermilion
      "#CC79A7",  # reddish purple
      "#000000",  # black
  ]
  ```

  `tab10` (matplotlib's default qualitative palette) is an acceptable fallback for
  internal/exploratory plots, but Okabe-Ito is preferred for any plot shown to an
  external audience.

- **Always pair color with a second encoding channel** — linestyle, marker shape,
  hatch pattern, or direct data labels. Never let color be the _sole_ distinguishing
  feature.

  ```python
  # Good: color + linestyle + marker
  ax.plot(x, y1, color="#0072B2", linestyle="-",  marker="o", label="Pond A")
  ax.plot(x, y2, color="#D55E00", linestyle="--", marker="s", label="Pond B")

  # Bad: color only
  ax.plot(x, y1, label="Pond A")
  ax.plot(x, y2, label="Pond B")
  ```

- **Recommended CVD simulation tools**: [Coblis](https://www.color-blindness.com/coblis-color-blindness-simulator/),
  [Colour Oracle](https://colororacle.org/), or the built-in CVD simulation in the
  `cmap` documentation.

---

## 4. Greyscale / print safety

If a plot may be printed or exported as black-and-white PDF:

- Sequential perceptually uniform colormaps (`viridis`, `cividis`, `plasma`,
  `inferno`, `magma`) degrade gracefully — they remain readable.
- Qualitative palettes and the banned colormap family print as nearly uniform grey
  smears, making the data unreadable.
- For qualitative series on black-and-white output, use hatching or linestyles as
  the primary distinguishing channel and drop color entirely.

---

## 5. Cross-figure color consistency

When a categorical variable (e.g. a pond name, treatment type, sensor zone) appears
in more than one plot, it **must** map to the same color in every plot. Do not allow
the library to auto-assign colors per-figure.

**Pattern: define a module-level color lookup dict.**

```python
# Define in a shared constants module within the package
# (e.g., src/<package>/domain/constants.py or a dedicated colors.py submodule).
# If this module does not exist, create it as a module-level constants file.
from typing import Final

POND_COLORS: Final[dict[str, str]] = {
    "Pond 1": "#0072B2",   # blue (Okabe-Ito)
    "Pond 2": "#E69F00",   # orange
    "Pond 3": "#009E73",   # bluish green
    "Pond 4": "#D55E00",   # vermilion
    "Wetland": "#56B4E9",  # sky blue
}
```

Then pass it explicitly at every call site:

```python
# Good: explicit, consistent
for pond, df_pond in df.groupby("pond"):
    ax.plot(df_pond["datetime"], df_pond["flux_ch4"], color=POND_COLORS[pond], label=pond)

# Bad: implicit — color assignment depends on iteration order and figure history
for pond, df_pond in df.groupby("pond"):
    ax.plot(df_pond["datetime"], df_pond["flux_ch4"], label=pond)
```

Keep the dict in a shared constants module when the lookup is used across multiple
scripts or notebook cells. For a lookup used only within a single script, define it
at the top of that file.

---

## 6. Cosmetic principles

These are brief reminders drawn from Tufte's data-to-ink principle and the five
principles of good graphs. They are adjacent to color but directly affect how color
choices land.

**Encode, don't decorate.**
Use a single neutral color (e.g. `"#6b6b6b"` or `"darkgrey"`) for non-focal series.
Apply a single accent color to draw the viewer's eye to the data point you are
communicating about. Avoid multi-color designs where each bar gets a different color
for no informational reason.

```python
# Good: grey baseline + one accent
colors = ["#6b6b6b"] * len(categories)
colors[focal_index] = "#0072B2"
ax.bar(categories, values, color=colors)
```

**Maximise the data-to-ink ratio.**
Remove spines, tick marks, and grid lines that add no information:

```python
ax.spines[["right", "top", "bottom"]].set_visible(False)
ax.tick_params(bottom=False)
ax.yaxis.grid(True, color="white", linewidth=0.8)  # white grid on grey background
ax.set_facecolor("#f0f0f0")
```

**Never use 3D.**
3D plots distort perceived volume and length, making accurate reading impossible.
Always find a 2D equivalent (facets, small multiples, heatmaps).

**Label everything.**
Both axes must have labels with units. Legends must use human-readable text, not
raw variable names. Color alone is never a sufficient legend — pair with a
descriptive label.

**Use a linear scale unless there is a domain-specific reason not to.**
Avoid pie charts, doughnut charts, and stacked bar charts; they rely on angle
and area judgments that humans perform poorly relative to position-along-a-scale
judgments.

---

## Procedure

When producing or reviewing a plot, apply these checks in order:

1. Identify the data structure (ordered continuous / diverging / cyclic / unordered
   categorical) and confirm the correct colormap category is used (Section 1).
2. For continuous colormaps, confirm one of the perceptually uniform maps is used
   and that no banned colormap (`jet`, `rainbow`, `hsv`, etc.) is present.
3. For qualitative/categorical series, confirm colors come from the Okabe-Ito palette
   or a project `dict[str, str]` constant — never from implicit matplotlib cycling.
4. Verify that color is paired with at least one other encoding channel (linestyle,
   marker shape, direct label, or position on a common scale).
5. Check that all lookup dicts are defined at module level (not inline). If a color
   lookup is shared across multiple scripts or notebooks, place it in a dedicated
   constants module within the package (e.g., `src/<package>/domain/constants.py`
   or a `colors.py` submodule — create this module if it does not exist). Pass dicts
   explicitly at every call site.
6. Confirm axes have labels with units and the legend uses human-readable text.
7. Remove decorative color, 3D elements, and unnecessary spines.

---

## Examples

### Good: consistent colors + Okabe-Ito + second encoding channel

```python
POND_COLORS: dict[str, str] = {
    "Pond 1": "#0072B2",
    "Pond 2": "#E69F00",
    "Pond 3": "#009E73",
}
POND_MARKERS: dict[str, str] = {
    "Pond 1": "o",
    "Pond 2": "s",
    "Pond 3": "^",
}

fig, ax = plt.subplots()
for pond, df_pond in df.groupby("pond"):
    ax.plot(
        df_pond["datetime"],
        df_pond["flux_ch4"],
        color=POND_COLORS[pond],
        marker=POND_MARKERS[pond],
        label=pond,
    )
ax.set_xlabel("Date")
ax.set_ylabel("CH4 flux (mg m⁻² d⁻¹)")
ax.spines[["right", "top"]].set_visible(False)
ax.legend(title="Pond")
```

### Bad: implicit cycling, banned colormap, no second channel

```python
# matplotlib picks colors arbitrarily — changes if a pond is missing from one figure
for pond, df_pond in df.groupby("pond"):
    ax.plot(df_pond["datetime"], df_pond["flux_ch4"], label=pond)

# jet on a heatmap — not perceptually uniform, fails in grayscale, not CBF
ax.imshow(grid, cmap="jet")
```

---

## References

- [Choosing Colormaps in Matplotlib](https://matplotlib.org/stable/users/explain/colors/colormaps.html)
- [cmap library](https://github.com/pyapp-kit/cmap) — cross-library colormap bridge
- Okabe M. & Ito K. (2008). Color Universal Design. [jfly.uni-koeln.de](https://jfly.uni-koeln.de/color/)
- Gordon I. & Finch S. (2015). Statistician heal thyself: have we lost the plot? _Journal of Computational and Graphical Statistics_, 24(4), 1210–1229.
- Rougier N.P. et al. (2014). Ten Simple Rules for Better Figures. _PLOS Computational Biology_.
- Cleveland W.S. & McGill R. (1985). Graphical Perception and Graphical Methods for Analyzing Scientific Data. _Science_.
