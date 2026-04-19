---
name: pm-prd-builder
description: Use when an initiative has at least one validated or in-testing hypothesis and engineering or design needs a formal brief to begin work.
---

# PRD Builder

## Overview

Convert a structured initiative and its linked hypotheses into a stakeholder-ready PRD. The PRD is an ending point of validated initiative work, not a starting point.

## When to Use

- Initiative has at least one Validated or Testing hypothesis
- Engineering or design needs a formal brief
- Before a build decision when scope must be committed
- Stakeholders need a written artifact to align on

## Quick Reference

| PRD Section | Source |
|---|---|
| Strategic Context | `docs/product/strategy/strategic-bets.md` |
| Problem Statement | `pm-problem-framer` output or initiative description |
| Success Definition | Initiative outcome metric + hypothesis thresholds |
| Scope (In/Out) | Derived from initiative + hypothesis boundaries |
| Hypothesis Summary | `docs/product/hypotheses/` linked files |
| Constraints | `docs/product/strategy/constraints.md` |
| Open Questions | At least one — a PRD with none has not been stress-tested |

## Behaviour Rules

- Refuse if initiative has no measurable outcome — flag and halt
- Refuse if initiative has no linked hypothesis — flag and halt
- Problem statement must come from `pm-problem-framer`, not invented
- Scope must be explicit: what is IN and what is OUT
- Success metrics must match the initiative's outcome metric exactly
- Open questions must be listed — add at least one
- Do not generate solutions or UI recommendations
- Adapt depth to stakeholder: Engineering needs constraints and edge cases, Exec needs outcome and risk

## Input

**Required:** Initiative file from `docs/product/initiatives/`, linked hypothesis file(s) from `docs/product/hypotheses/`, target stakeholder (Engineering / Exec / Design / Cross-functional).

**Recommended:** Personas, problem-framer output, strategic bets.

## Output Structure

**Header:** Initiative name, version, status (Draft), owner, date, target reader.

**Sections:** Strategic Context (bet + why now), Problem Statement (who, workaround, cost), Success Definition (metric, target, failure), Scope (in/out), Hypothesis Summary (table: name, status, confidence), Constraints, Open Questions, Risks.

**Structural Flags:** Missing outcome, no hypothesis, invalidated hypothesis. Omit if none.

## Common Mistakes

- **Building a PRD without a hypothesis** — proceeds on unvalidated assumptions.
- **Inventing the problem statement** — must come from `pm-problem-framer` to stay grounded.
- **No "out of scope"** — scope creep enters through undefined boundaries.
- **Zero open questions** — signals overconfidence, not completeness.
