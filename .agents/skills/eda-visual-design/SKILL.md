---
name: eda-visual-design
description: Use when choosing chart types, encoding data, reducing cognitive load, or annotating EDA and statistical visualisations
---

## Boundary Contract

### Applies To
- Statistical and EDA plot creation or review, any plotting library

### Produces
- Accessible, cognitively efficient visualisations following Tufte, Cleveland, and Norman

### Does Not Cover
- Pre-flight data quality screening (`eda-interpreting-data`)
- Color selection specifics (`python-plot-colors`)
- Codebook generation (`eda-codebook`)


See `procedures/eda-visual-design.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Using a bar chart for continuous data | Use a histogram or KDE for distributions; bar charts are for discrete/categorical comparisons |
| Omitting axis labels and units | Every axis must have a label including units; unlabelled axes force readers to guess |
| Using 3D charts for 2D data | Never use 3D effects for 2D data — they distort perception and add no information |