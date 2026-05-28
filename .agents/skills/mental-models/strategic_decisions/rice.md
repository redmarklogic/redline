# RICE

## What it is

RICE is a scoring framework for product prioritisation developed by Sean McBride at Intercom (2016). It ranks project ideas by calculating a single score from four factors: **Reach**, **Impact**, **Confidence**, and **Effort**. The score represents total impact per unit of time worked, enabling consistent comparison across dissimilar ideas.

Formula: **RICE Score = (Reach × Impact × Confidence) / Effort**

## Core principle

Replace gut-feeling prioritisation with a structured, repeatable signal. By forcing an explicit estimate for each factor, RICE makes hidden trade-offs visible -- in particular, it surfaces projects that feel exciting (high Impact) but have low Reach or require disproportionate Effort.

## When to invoke

- Prioritising 5-20 initiatives or projects with rough quantitative inputs available
- When different stakeholders advocate for different projects and a common scoring basis is needed
- When you want to defend a prioritisation decision with traceable reasoning
- Distinct from spec-kit's scenario-level RICE, which ranks acceptance criteria inside a single spec; keep the two altitudes separate

## How to apply

1. **Reach** -- how many people will this project affect within a given time period? Measure in events or people per quarter. Use real product metrics; avoid estimates without data.
2. **Impact** -- how much will this affect each person? Score on a discrete scale: 3 (massive), 2 (high), 1 (medium), 0.5 (low), 0.25 (minimal).
3. **Confidence** -- how confident are you in your estimates? Score as a percentage: 100% (high), 80% (medium), 50% (low). Anything below 50% is a moonshot; name it as one.
4. **Effort** -- how many person-months of total team time (product + design + engineering) will this require? Use whole numbers; minimum 0.5. Do not count engineering time alone.
5. Calculate: **(Reach × Impact × Confidence) / Effort = RICE Score**
6. Sort descending. Re-examine outliers -- scores that feel too high or too low usually signal a miscalibrated estimate, not a genuine priority signal.

## Anti-patterns

- **Gut-feel numbers** -- inflating Impact or Confidence to justify a preferred project; the formula cannot compensate for dishonest inputs
- **Engineering-only effort** -- ignoring product, design, and QA work understates Effort and inflates the score
- **Hard-and-fast rule** -- a lower-scored project may still ship first (e.g., as a dependency or table-stakes feature); use RICE to make trade-offs visible, not to eliminate judgment
- **Mixing altitudes** -- portfolio-level RICE (comparing initiatives) and spec-level RICE (ranking scenarios inside a spec) use the same formula but operate at different scopes; never cross-compare their scores

## Source

Sean McBride, "RICE: Simple Prioritization for Product Managers" -- Intercom Blog (2018).
https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers/
