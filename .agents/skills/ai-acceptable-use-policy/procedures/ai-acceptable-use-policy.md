# Ai Acceptable Use Policy — Detailed Reference

### DORA Research
- DORA "Impact of Generative AI in Software Development" (April 2026)
- DORA "Balancing AI Tensions" (March 2026)
- DORA 2025 Report

### Notebook Sources (queried via `redline-research`)
- *Software Engineering at Google* — small changes, review discipline
- *Accelerate* (Forsgren, Humble & Kim) — batch size as stability predictor
- *Co-Intelligence* (Mollick) — AI as equaliser; expertise paradox

# AI Acceptable-Use Policy

## Overview

AI is an amplifier of existing organisational strengths and weaknesses. The greatest returns come not from the tools themselves, but from a strategic focus on the underlying organisational system. (DORA 2025)

## DORA Key Findings (2024–2026)

| Finding | Implication for Redline |
|---|---|
| 25% AI adoption increase → 1.5% throughput decrease + 7.2% stability decrease | Measure outcomes, not adoption |
| Root cause: larger batch sizes from faster code generation | Enforce small-batch discipline actively |
| Verification tax: time saved writing code re-spent auditing output | Account for audit time in estimates |
| Expertise paradox: AI lowers barriers but risks skill degradation | Deliberate practice for complex tasks |
| AI is an amplifier | Fix the system first; AI magnifies what is already there |
| Clear AI acceptable-use policy correlates with 451% higher AI adoption | Publish and enforce this policy |
| Only 24% of developers highly trust AI-generated code | Build verification discipline into the workflow |

## Small-Batch Enforcement Rules

1. Configure maximum PR size threshold — AI-generated PRs above the threshold trigger an automated warning.
2. Require author-side AI feedback: flag issues at authoring time, not PR review time.
3. For architecturally complex components: require manual implementation alongside AI as deliberate practice.
4. Pair with the founder to review AI-generated architectural decisions.
5. Account for prototype-to-production gap in every timeline estimate.
6. Resist AI tooling adoption that outpaces verification capacity.

## Domain-Specific Clause

All AI-generated geotechnical content requires the Domain Expert's explicit approval before use. This is a hard gate — AI does not bypass the domain expert review requirement.

## Grounding Sources
