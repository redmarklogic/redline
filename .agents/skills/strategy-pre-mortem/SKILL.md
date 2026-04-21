---
name: strategy-pre-mortem
description: Use when asked to stress-test, pre-mortem, or risk-assess an un-implemented plan, launch, initiative, or strategic bet before execution begins.
---

# Pre-Mortem Analysis

## Boundary Contract

### Inputs
- Un-implemented plan, launch, initiative, or strategic bet to stress-test

### Outputs
- Pre-mortem analysis with failure modes, mitigations, and risk assessment

### Out of Scope
- Strategy creation (`pm-product-strategist`)
- Problem framing (`pm-problem-framer`)
- Code implementation

## Overview

Assume the plan has already failed. Work backward to find why. A pre-mortem removes optimism bias by making failure concrete before execution begins.

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

### Step 1: The Failure Premise

Set a concrete failure scene 6-12 months in the future. The plan was executed exactly as written and has failed catastrophically. Write 2-4 sentences that make the failure vivid and specific.

**Purpose:** Remove optimism bias. The team must inhabit failure before analyzing it.

**Rules:**
- Name a specific future date
- State the plan was executed faithfully (this is not about bad execution)
- Describe the observable symptoms of failure (empty pipeline, zero conversions, budget burned, team demoralized)
- Do not analyze causes yet --- just set the scene

### Step 2: Root Cause Brainstorming (Categorized)

Generate a comprehensive list of plausible reasons the plan failed. Organize every reason into exactly three categories:

| Category | What it covers | Examples |
|---|---|---|
| **Internal / Execution** | Resource bottlenecks, team misalignment, process breakdown, skill gaps, competing priorities, cultural resistance | Key person leaves; team lacks domain expertise; scope creep consumes budget |
| **External / Market** | Competitor response, economic shifts, customer rejection, regulatory change, market timing, audience mismatch | Incumbent launches free version; target users do not want this; SEO competition too strong |
| **Technical / Operational** | Software failures, integration issues, data quality, infrastructure limits, scaling problems, tooling gaps | API dependency breaks; data pipeline unreliable; performance too slow for production |

**Rules:**
- Every risk must appear in exactly one category
- Aim for 3-5 risks per category (breadth over depth at this stage)
- Use one-line descriptions --- do not elaborate yet
- Do not filter or prioritize yet --- this is a brainstorm

### Step 3: Risk Prioritization

Select the **top 3-5 most critical risks** from the full brainstorm. Rank them using both dimensions:

| Dimension | High | Medium | Low |
|---|---|---|---|
| **Likelihood** | Will probably happen given current conditions | Could happen under plausible scenarios | Unlikely without unusual circumstances |
| **Impact** | Plan fails entirely or loses strategic coherence | Plan succeeds partially but misses key targets | Plan is inconvenienced but recovers |

**Rules:**
- Select only risks that are **High Likelihood + High Impact** or **High on one + Medium on the other**
- Present as a numbered ranked list with explicit Likelihood and Impact ratings
- Include which category (Internal/External/Technical) each risk came from
- Do not exceed 5 prioritized risks --- fewer is better if the plan is simple

**Output format:**

```
1. [Risk name] (Category: External/Market)
   - Likelihood: High — [one-sentence justification]
   - Impact: High — [one-sentence justification]

2. [Risk name] (Category: Internal/Execution)
   - Likelihood: High — [one-sentence justification]
   - Impact: Medium — [one-sentence justification]
```

### Step 4: Reinforcement and Mitigation

For each prioritized risk (and only for prioritized risks), provide **1-2 specific, actionable steps** that can be taken *right now* to amend the original plan and prevent the failure.

**Rules:**
- Mitigations must be concrete actions, not general advice ("Run a one-week smoke test with 200 LinkedIn-driven visits" not "Validate demand first")
- Mitigations must be executable before the plan launches --- not contingency plans for after failure
- Each mitigation must name who should do it and roughly when
- Do not repeat the risk description --- reference by number

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

### Step 1: The Failure Premise

[2-4 sentences setting the failure scene]

### Step 2: Root Cause Brainstorm

**Internal / Execution Risks**
- [risk 1]
- [risk 2]
- ...

**External / Market Risks**
- [risk 1]
- [risk 2]
- ...

**Technical / Operational Risks**
- [risk 1]
- [risk 2]
- ...

### Step 3: Prioritized Risks

1. [Risk] (Category)
   - Likelihood: [H/M/L] -- [justification]
   - Impact: [H/M/L] -- [justification]

2. ...

### Step 4: Reinforcement and Mitigation

**Risk 1: [name]**
- Action A: [specific step, who, when]
- Action B: [specific step, who, when]

**Risk 2: [name]**
- ...
```

## Common Mistakes

- **Issuing a verdict** --- "Do not build this" is a decision, not a pre-mortem finding. Surface the risks; the user decides.
- **Skipping the brainstorm** --- jumping straight to detailed analysis for every risk produces an essay, not a prioritized risk register.
- **Custom categories** --- inventing categories like "Strategic Alignment" or "Conversion Risk" breaks the standardized taxonomy. Map every risk to Internal, External, or Technical.
- **Vague mitigations** --- "Validate demand" is not actionable. "Run a landing page test with 200 visits over 5 days, measuring signup conversion rate" is actionable.
- **Analyzing more than 5 risks in depth** --- the brainstorm can be broad, but Step 4 covers only the prioritized risks from Step 3.
