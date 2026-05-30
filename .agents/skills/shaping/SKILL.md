---
name: shaping
description: Use when translating a product intent or PRD into a buildable scoped brief (Pitch) before work enters SpecKit, or when deciding what to cut to fit the declared appetite.
---

# Shaping

## Overview

Shaping inserts a Layer 1.5 between Discovery (PRDs) and Execution (SpecKit). The Pitch communicates constraints and scope — solutions live within the team's creative freedom. If a constraint can only be satisfied by one specific design, it has been over-constrained.

## Boundary Contract

### Applies To
- Translating a PRD into a buildable scoped brief
- Writing a Pitch: problem statement, appetite, solution sketch (breadboard level), rabbit holes, no-gos
- Breadboarding: components and connections only — no visual design, no wireframes
- Rabbit hole identification and resolution before work reaches SpecKit
- Appetite setting: the Product Manager sets business appetite; the Principal Engineer sets technical appetite
- Scope hammering: what to cut when shaped work exceeds appetite
- Touch 1 constraints memo to the UI/UX Designer

### Produces
- Shaped Pitch in `specs/shaped/`
- Touch 1 constraints memo (embedded in or alongside the Pitch; delivered to the UI/UX Designer)

### Does Not Cover
- Detailed specifications — SpecKit's `specify` agent writes the spec from the Pitch
- UX design or wireframes — the UI/UX Designer designs freely after Touch 1
- PRD writing — the Product Manager writes PRDs upstream of shaping
- Code or implementation — SpecKit and the development team

## Quick Reference

| Shape Up Concept | Redline Equivalent | Owner | Output |
|---|---|---|---|
| Pitch | Shaped brief (post-PRD, pre-spec) | the Principal Engineer writes, the Product Manager approves | `specs/shaped/` |
| Breadboard | Components + connections sketch | the Principal Engineer | Embedded in Pitch |
| Rabbit holes | Technical risks resolved before SpecKit | the Principal Engineer | In Pitch |
| Business appetite | How much time the business invests | the Product Manager sets | In Pitch |
| Technical appetite | What is feasible within the appetite | the Principal Engineer sets | In Pitch |
| Touch 1 | Constraints memo to the UI/UX Designer | the Principal Engineer | In Pitch or alongside |
| Touch 2 | Architectural compliance review of SpecKit output | the Principal Engineer | Inline verdict |

## The Two-Touch Model

```
the Principal Engineer shapes (Touch 1: constraints memo / Pitch)
    --> the UI/UX Designer designs (full creative freedom — the Principal Engineer is ABSENT)
    --> SpecKit specifies
    --> the Principal Engineer reviews (Touch 2: SpecKit output compliance, NOT design specs)
```

the Principal Engineer does NOT touch: the UI/UX Designer's wireframes, interaction patterns, component specs, or any design artifact between Touch 1 and Touch 2.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Adding wireframes to the Pitch | Breadboard only — components and connections; no visual design. |
| Prescribing solutions in the Pitch | Pitch communicates constraints; solutions belong to the UI/UX Designer and SpecKit. |
| Shaping before a PRD exists | Shaping is post-PRD; verify the Product Manager's PRD exists before shaping. |
| Handing the Pitch to SpecKit without the Product Manager's approval | the Product Manager must approve appetite before work enters SpecKit. |
| Skipping rabbit hole identification | Unresolved rabbit holes cause mid-sprint scope explosions. |
| Touching the UI/UX Designer's work between Touch 1 and Touch 2 | the Principal Engineer is absent during the design phase. |
| Reviewing design specs at Touch 2 | Touch 2 reviews only SpecKit output for architectural compliance — not the UI/UX Designer's design artifacts. |

## Grounding Sources

Queried via `redline-research`:

- *Shape Up* (Singer) — shaping, Pitch, breadboarding, appetite, rabbit holes
- *Empowered* (Cagan) — trio collaboration, feasibility role, designer creative freedom
- *Inspired* (Cagan) — "plan to throw one away"; premature feasibility veto warning
