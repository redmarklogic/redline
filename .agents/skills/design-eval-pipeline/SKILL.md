---
name: design-eval-pipeline
description: Use when architecting an evaluation pipeline — designing the FTI (Feature/Training/Inference) architecture, structuring HITL (Human-in-the-Loop) review, planning production monitoring, or managing ground truth collection for AI-generated outputs.
---

# Design Eval Pipeline

## Overview

The evaluation pipeline operationalises rubrics at scale — from offline batch evaluation through to continuous production monitoring. The architect designs the pipeline structure; individual rubric definitions come from `design-eval-rubric`.

## Boundary Contract

### Applies To

- Evaluation pipeline architecture (FTI — Feature/Training/Inference pattern)
- HITL (Human-in-the-Loop) review design: sampling strategies, reviewer calibration
- Production monitoring: drift detection, quality alerts, continuous training triggers
- Ground truth collection infrastructure (not the domain content itself)

### Produces

- Evaluation harness design documents in `docs/evaluation/`
- Production monitoring design documents

### Does Not Cover

- Rubric structure and scoring systems — use `design-eval-rubric`
- LLM-as-judge prompt design — use `design-eval-rubric`
- Geotechnical domain content — domain expert owns this (blocking gate)
- Python implementation — use SpecKit
- Strategic DDD decisions — use `ddd-strategic`
- Shaping work for SpecKit — use `shaping`

## Pipeline Architecture

| Stage | Purpose | Key decision |
|---|---|---|
| Feature | Data preparation, feature extraction | What inputs does the evaluator see? |
| Training | Ground truth collection, judge calibration | Who labels? How many labels? |
| Inference | Automated evaluation at scale | Batch vs. online; latency vs. coverage |

## Workflow Procedure

Who does what (architect designs harness, domain expert validates content, calibration
steps, deployment gates) is defined in the `/evaluation-workflow` prompt.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Running HITL on every output at production scale | Sample strategically — label the hardest cases, not all cases |
| Treating drift detection as optional | Production monitoring is mandatory — models degrade silently without it |

## Grounding Sources

Queried via `redline-research`:

- *LLM Engineer's Handbook* (Iusztin & Labonne) — FTI architecture, testing pipeline
- *Building Applications with AI Agents* (Albada) — HITL review, executor/reviewer/governor pattern, feedback pipelines
