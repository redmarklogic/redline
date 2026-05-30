---
name: mental-models
description: Use when a structured thinking framework is needed for decision-making, root cause analysis, strategic planning, self-awareness, risk evaluation, or communication.
---

# Mental Models

Match the trigger column to the current situation, then load the referenced model file. When updating another skill that needs a mental model, reference a file from this skill rather than embedding the definition inline.

## Boundary Contract

**Applies To:** Any agent or skill that needs a structured thinking framework | **Produces:** A named model and its reference file | **Does Not Cover:** Executing model mechanics (each model file contains the procedure), domain-specific judgments (route to the relevant domain agent after selecting a model), creating new mental models

## Quick Reference (Sample)

| Category | Model | Trigger |
|---|---|---|
| Root Cause Analysis | Five Whys | Postmortem or recurring failure; trace symptoms back to structural root cause |
| Strategic Decisions | Reversible vs Irreversible | Calibrating how much deliberation a decision deserves |
| Strategic Decisions | Pre-mortem | Before committing to a plan; assume it failed and surface hidden risks |
| Risk Analysis | Precautionary Principle | About to perform a destructive/irreversible operation; require safety proof first |
| General Thinking | Inversion | Stuck on a problem; flip it and ask how to guarantee failure |

See \procedures/mental-models.md\ for the full 33-model catalog with triggers and file references.

## Common Mistakes

- Picking a model by name recognition rather than matching the trigger condition.
- Applying two conflicting models to the same decision without resolving the tension first.
- Defining a mental model inline in another skill rather than referencing this one -- creates redundancy and lets definitions drift out of sync.
- Selecting a model before applying the Circle of Competence gate -- operating outside your territory without acknowledging it leads to false precision.
