---
name: shaping
description: Use when translating a product intent or PRD into a buildable scoped brief (Pitch) before work enters SpecKit, or when deciding what to cut to fit the declared appetite.
---

# Shaping

Shaping inserts a Layer 1.5 between Discovery (PRDs) and Execution (SpecKit). The Pitch communicates constraints and scope -- solutions live within the team creative freedom.

## Boundary Contract

**Applies To:** Translating a PRD into a scoped Pitch; appetite setting; scope hammering; Touch 1 constraints memo to the UI/UX Designer | **Produces:** Shaped Pitch in \specs/shaped/\; Touch 1 memo | **Does Not Cover:** Detailed specs (SpecKit \specify\), UX design (UI/UX Designer), PRD writing (Product Manager), implementation

## Quick Reference

| Shape Up Concept | Redline Equivalent | Owner | Output |
|---|---|---|---|
| Pitch | Shaped brief (post-PRD, pre-spec) | Principal Engineer writes, PM approves | \specs/shaped/\ |
| Breadboard | Components + connections sketch | Principal Engineer | Embedded in Pitch |
| Rabbit holes | Technical risks resolved before SpecKit | Principal Engineer | In Pitch |
| Touch 1 | Constraints memo to UI/UX Designer | Principal Engineer | In Pitch or alongside |
| Touch 2 | Architectural compliance review of SpecKit output | Principal Engineer | Inline verdict |

Two-touch model: Principal Engineer shapes (Touch 1) --> UI/UX Designer designs (Principal Engineer ABSENT) --> SpecKit specifies --> Principal Engineer reviews (Touch 2: architectural compliance only, NOT design artifacts).

## Common Mistakes

| Mistake | Fix |
|---|---|
| Adding wireframes to the Pitch | Breadboard only -- components and connections; no visual design |
| Prescribing solutions in the Pitch | Pitch communicates constraints; solutions belong to the UI/UX Designer and SpecKit |
| Shaping before a PRD exists | Shaping is post-PRD; verify the PM PRD exists before shaping |
| Handing the Pitch to SpecKit without PM approval | PM must approve appetite before work enters SpecKit |
| Touching the UI/UX Designer work between Touch 1 and Touch 2 | Principal Engineer is absent during the design phase |
