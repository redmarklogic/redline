---
name: python-plot-colors
description: Use when selecting colors for plots -- colormap choice, color-blindness safety, or maintaining cross-figure consistency across plotting libraries
---

## Boundary Contract

### Applies To
- Color selection in plots produced with matplotlib, seaborn, plotly, altair, or similar

### Produces
- Accessible, information-encoding color schemes with cross-figure consistency

### Does Not Cover
- Chart type selection and layout (`eda-visual-design`)
- Data quality screening (`eda-interpreting-data`)
- General style (`python-style`)


See `procedures/python-plot-colors.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Using a rainbow (jet) colormap for continuous data | Use a perceptually uniform sequential colormap (iridis, plasma) instead |
| Relying on color alone to distinguish categories | Add shape, pattern, or label annotations — required for color-blind accessibility |
| Redefining the color palette per figure | Define a shared palette constant once and import it in every plot module |