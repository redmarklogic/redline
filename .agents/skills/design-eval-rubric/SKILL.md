---
name: design-eval-rubric
description: Use when designing an evaluation rubric — structuring scoring systems, selecting test formats, designing LLM-as-judge patterns, or calibrating an automated judge against human evaluation for AI-generated outputs.
---

# Design Eval Rubric

## Overview

Evaluation criteria are defined **before** implementation begins — Evaluation-Driven Development (Huyen). The architect designs the rubric structure; the domain expert fills it with domain truth content. No rubric ships without the domain expert's explicit sign-off.

## Boundary Contract

### Applies To

- Evaluation rubric structure: scoring systems, test formats, automation approaches
- LLM-as-judge prompt design and calibration against human evaluation
- Ground truth management: structuring the collection process for domain expert review
- Per-task, per-turn, end-to-end, and production monitoring rubric classification

### Produces

- Evaluation rubric structures in `docs/evaluation/`
- LLM-as-judge prompt templates (domain-expert-validated)
- Ground truth collection process documents

### Does Not Cover

- Geotechnical domain content for rubrics — domain expert owns this (blocking gate)
- Evaluation pipeline architecture (FTI pattern) — use `design-eval-pipeline`
- HITL review design — use `design-eval-pipeline`
- Production monitoring architecture — use `design-eval-pipeline`
- Python implementation — use SpecKit

## Evaluation Levels

Four levels. Every rubric must be classified before design begins.

| Level | What is measured | Automation |
|---|---|---|
| Per-task | Single atomic task output (e.g., one extracted clause) | High — unit-test style |
| Per-turn | One conversation turn or agent action | Moderate |
| End-to-end | Full report generation pipeline | Lower — integration-test style |
| Production monitoring | Live output quality over time | Continuous — drift detection |

## Common Mistakes

| Mistake | Fix |
|---|---|
| Defining a rubric without anchoring scores to observable output examples | Every rubric level needs a concrete example of output that achieves that score |
| Using a single judge model without a second-pass reviewer | Apply maker-checker: one model generates, a different (or same) model judges — never self-evaluation |
| Skipping the calibration phase before deploying an LLM judge | Run the judge on a labelled hold-out set first; uncalibrated judges have unknown reliability |

## Grounding Sources

Queried via `redline-research`:

- *AI Engineering* (Huyen) — Evaluation-Driven Development, rubric design, domain expert role
