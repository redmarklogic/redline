---
name: strategy-pre-mortem
description: Use when asked to stress-test, pre-mortem, or risk-assess an un-implemented plan, launch, initiative, or strategic bet before execution begins.
---

# Pre-Mortem Analysis

## Boundary Contract

## Overview

See [pre-mortem](../mental-models/strategic_decisions/pre-mortem.md) for the full definition and methodology.

**Core principle:** A pre-mortem is a stress-testing tool, not a verdict tool. The output is reinforced risks and mitigations, never a go/no-go recommendation.

## When to Use

- User asks to "pre-mortem", "stress-test", or "risk-assess" a plan
- Before committing build resources to a new initiative
- Before presenting a plan to stakeholders
- When a plan feels solid but has not been challenged

**When NOT to use:**
- Post-launch retrospectives (use a post-mortem instead)
- Auditing an existing artifact's structure (use `pm-structural-integrity-auditor`)
- Evaluating strategic alignment (use `pm-product-strategist`)

## The Four-Step Procedure

Follow these four steps in strict order. Do not skip steps or merge them.

## Behaviour Rules

- **Stress-test, do not verdict.** Never conclude with "Do not build this" or "I recommend proceeding." The pre-mortem surfaces risks and mitigations. The user decides.
- **Follow the four steps in order.** Do not jump from Step 1 to detailed analysis. Do not skip the brainstorm to go straight to deep-dives.
- **Brainstorm broadly, then filter.** Step 2 is a broad sweep. Step 3 filters. Step 4 goes deep on filtered risks only. Do not write detailed analysis for every risk.
- **Stay within the plan as written.** Analyze the plan that was presented, not a hypothetical better plan. Mitigations amend the plan --- they do not replace it.
- **Cite grounding when available.** If notebooks, strategy docs, or domain knowledge support a risk, cite the source. Do not fabricate citations.
- **Use the three categories.** Every risk belongs in Internal/Execution, External/Market, or Technical/Operational. No custom categories, no uncategorized risks.

## Output Structure

```markdown
## Pre-Mortem Analysis: [Plan Name]

**Date:** [today]
**Plan analyzed:** [one-line summary]


See `procedures/strategy-pre-mortem.md` for detailed rules, examples, and extended reference.

## Common Mistakes

- **Issuing a verdict** --- "Do not build this" is a decision, not a pre-mortem finding. Surface the risks; the user decides.
- **Skipping the brainstorm** --- jumping straight to detailed analysis for every risk produces an essay, not a prioritized risk register.
- **Custom categories** --- inventing categories like "Strategic Alignment" or "Conversion Risk" breaks the standardized taxonomy. Map every risk to Internal, External, or Technical.
- **Vague mitigations** --- "Validate demand" is not actionable. "Run a landing page test with 200 visits over 5 days, measuring signup conversion rate" is actionable.
- **Analyzing more than 5 risks in depth** --- the brainstorm can be broad, but Step 4 covers only the prioritized risks from Step 3.
