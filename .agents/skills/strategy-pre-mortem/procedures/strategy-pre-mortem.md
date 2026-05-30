# Strategy Pre Mortem — Detailed Reference

### Inputs
- Un-implemented plan, launch, initiative, or strategic bet to stress-test

### Outputs
- Pre-mortem analysis with failure modes, mitigations, and risk assessment

### Out of Scope
- Strategy creation (`pm-product-strategist`)
- Problem framing (`pm-problem-framer`)
- Code implementation

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
