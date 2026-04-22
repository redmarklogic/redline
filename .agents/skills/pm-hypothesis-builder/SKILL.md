---
name: pm-hypothesis-builder
description: Use when an assumption needs formalizing into a testable hypothesis, a hypothesis draft is non-falsifiable or vague, or before designing any experiment.
---

# Hypothesis Builder

## Overview

Convert assumptions into falsifiable hypotheses ready to file in `docs/product/hypotheses/`. Every hypothesis must have a metric, threshold, and time boundary — the three non-negotiables.

## Boundary Contract

### Inputs
- Assumption or belief to be tested from an initiative or problem statement
- Problem framing output from `pm-problem-framer`

### Outputs
- Falsifiable hypothesis document at `docs/product/hypotheses/`

### Out of Scope
- Problem framing (`pm-problem-framer`)
- Experiment execution and result tracking
- PRD writing (`pm-prd-builder`)

## When to Use

- After extracting assumptions from an initiative
- When a hypothesis draft is vague or non-falsifiable
- Before designing any experiment

## Quick Reference

| Element | Good | Bad |
|---|---|---|
| Metric | "30-day retention rate" | "engagement" |
| Success threshold | ">15% within 90 days" | "improves" |
| Failure threshold | "<5% after 90 days" | Not defined |
| Time bound | "within 90 days" | "eventually" |

## Behaviour Rules

- Reject any hypothesis that cannot be proven wrong
- Require a specific metric — "engagement improves" is not a metric
- Require both success and failure thresholds — not just a target
- Require a time boundary — open-ended hypotheses are untestable
- Flag language like "users will like", "it will be better", "should improve"

## Input

Provide a raw assumption, a draft hypothesis to sharpen, or an initiative description to extract and formalize its core hypothesis.

## Output Structure

**Hypothesis Statement:** "We believe that [segment] experiences [problem]. If we [intervention], then [outcome] will change by [amount] within [period]."

**Hypothesis File** (paste-ready for `docs/product/hypotheses/`):

```
# HYP — [Short statement]

## Related Initiative
- [[Initiative: ...]]

## Risk Level / Why This Might Fail / Test Plan / Metric + Threshold / Status / Last Updated
```

**Validation Flags:** Falsifiable, Metric defined, Thresholds defined, Time-bound — each Yes/No.

## Common Mistakes

- **Vague metrics** — "user satisfaction" is a concept, not a metric. Name the instrument.
- **Success-only thresholds** — without a failure threshold, you cannot invalidate.
- **No time boundary** — "eventually" is not testable. Pick a date.
- **Hypothesis as wish** — "users will love it" is a hope, not a hypothesis.
