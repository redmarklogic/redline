# AI Acceptable-Use Policy

## Purpose

AI tool governance, DORA AI capabilities model, and small-batch enforcement for Redline's AI-assisted development workflow.

## Key Principle

"AI's primary role is as an amplifier, magnifying an organization's existing strengths and weaknesses. The greatest returns on AI investment come not from the tools themselves, but from a strategic focus on the underlying organizational system." (DORA 2025)

## What This Skill Covers

- AI acceptable-use policy structure: which AI tools are permitted, how AI-generated code is reviewed, what outputs require human verification
- DORA AI capabilities model: seven capabilities mapped to Redline's team (small batches, AI-accessible data, clear AI stance, quality platform, healthy data ecosystem, version control, user-centric focus)
- Small-batch enforcement: max PR size thresholds, automated warnings for oversized AI-generated PRs, review-scope discipline for machine-generated changes
- Author-side AI feedback: configuring AI tools to flag issues at authoring time, not at PR review time
- Deliberate practice for complex tasks: requiring manual implementation alongside AI for architecturally complex components as a learning exercise
- AI output verification mentoring: explicit pairing practices to build the verification skill
- Workflow gap planning: accounting for prototype-to-production gap in timelines
- System health over tool adoption: resisting AI tooling that outpaces verification capacity
- Domain-specific rules for geotechnical content: Graeme's blocking gate operationalised as a policy clause

## Grounding Sources

### External research (DORA)

- DORA "Impact of Generative AI in Software Development" (April 2026)
- DORA "Balancing AI Tensions" (March 2026)
- DORA 2025 Report

### Notebook sources (to be queried via `redline-research`)

- *Software Engineering at Google* — small changes, review discipline
- *Accelerate* — batch size as stability predictor
- *Co-Intelligence* (Mollick) — AI as equaliser, expertise paradox

## DORA Key Findings (2024-2026)

These findings ground the policy:

1. **AI currently hurts delivery performance:** 25% AI adoption increase = 1.5% throughput decrease + 7.2% stability decrease.
2. **Root cause:** larger batch sizes from faster code generation.
3. **Verification tax:** time saved writing code is re-spent auditing AI output.
4. **Expertise paradox:** AI lowers barriers but risks skill degradation.
5. **AI is an amplifier** of existing organisational strengths and weaknesses.
6. **Seven AI capabilities model** defines what organisations need to benefit from AI.
7. **Clear AI acceptable-use policy** correlates with 451% higher AI adoption.
8. **Only 24% of developers trust AI-generated code highly.**

## Status

**Pending notebook grounding.** This skill requires queries to the Software Development Methodology & Engineering Organisation notebook plus integration of external DORA 2024-2026 research before the content can be fully elaborated.

## Who Uses This Skill

Peter (primary — operationalises policy in tooling), Ron (co-author — sets strategic direction).
