---
name: ai-acceptable-use-policy
description: Use when defining AI tool governance rules, enforcing small-batch discipline on AI-generated code, designing an acceptable-use policy for a small engineering team, or operationalising DORA AI capabilities.
---

# AI Acceptable-Use Policy

## Overview

AI is an amplifier of existing organisational strengths and weaknesses. The greatest returns come not from the tools themselves, but from a strategic focus on the underlying organisational system. (DORA 2025)

## Boundary Contract

### Applies To
- AI acceptable-use policy structure: permitted tools, review requirements, human verification thresholds
- DORA AI capabilities model: seven capabilities mapped to Redline's team
- Small-batch enforcement: max PR size thresholds, automated warnings for oversized AI PRs
- Author-side AI feedback configuration (flagging at authoring time, not PR review time)
- Deliberate practice design for architecturally complex components
- AI output verification mentoring
- Domain-specific AI governance rules: Graeme's blocking gate operationalised as a policy clause

### Produces
- AI acceptable-use policy document (co-authored with Ron) in `docs/architecture/`
- PR size threshold configuration

### Does Not Cover
- Geotechnical domain accuracy rules — Graeme owns those
- AI adoption strategy — Ron sets strategic direction
- Code implementation of enforcement tooling — SpecKit and developers implement

## Quick Reference: DORA Seven AI Capabilities

| Capability | Redline Application |
|---|---|
| Use AI in small batches | Configure max PR size; warn on oversized AI PRs |
| AI-accessible data | Version-controlled codebase and well-structured docs |
| Clear AI acceptable-use stance | This policy document (co-authored Peter + Ron) |
| Quality platform | SonarQube + Designite configured and monitored by Peter |
| Healthy data ecosystem | Pins-versioned datasets; documented schemas |
| Version control discipline | All AI output committed; no shadow editing |
| User-centric focus | User outcomes drive AI adoption decisions |

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

All AI-generated geotechnical content requires Graeme's explicit approval before use. This is a hard gate — AI does not bypass the domain expert review requirement.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Treating AI adoption as a velocity lever | DORA: adoption increase correlates with decreased stability. Measure delivery outcomes. |
| Reviewing AI PRs the same way as human PRs | AI PRs need smaller review scope and author-side flagging; reviewer-side AI review does not work. |
| Skipping deliberate practice for complex architecture tasks | Manual alongside AI prevents skill degradation for architecturally complex work. |
| Letting domain content flow through AI without Graeme's gate | Graeme's blocking gate applies to AI-generated geotechnical content. |
| Adopting AI tools faster than verification capacity allows | System health over tool adoption; resist the adoption pressure. |
| Measuring AI impact by lines of code produced | Use SPACE/SEQ/HEART frameworks, not output metrics. |

## Grounding Sources

### DORA Research
- DORA "Impact of Generative AI in Software Development" (April 2026)
- DORA "Balancing AI Tensions" (March 2026)
- DORA 2025 Report

### Notebook Sources (queried via `redline-research`)
- *Software Engineering at Google* — small changes, review discipline
- *Accelerate* (Forsgren, Humble & Kim) — batch size as stability predictor
- *Co-Intelligence* (Mollick) — AI as equaliser; expertise paradox
