---
name: evaluation-architecture
description: Use when designing an LLM evaluation lifecycle, structuring evaluation rubrics, implementing LLM-as-judge patterns, or architecting an evaluation pipeline for AI-generated geotechnical outputs.
---

# Evaluation Architecture

## Overview

Evaluation criteria are defined **before** implementation begins â€” Evaluation-Driven Development (Huyen). The architect designs the harness structure; the domain expert fills it with domain truth content. No rubric ships without the domain expert's explicit sign-off.

## Boundary Contract

### Applies To
- LLM evaluation lifecycle design: per-task, per-turn, end-to-end, production monitoring
- Evaluation rubric structure: scoring systems, test formats, automation approaches
- LLM-as-judge prompt design and calibration against human evaluation
- Ground truth management: structuring the collection process for domain expert review
- Evaluation pipeline architecture (FTI â€” Feature/Training/Inference pattern)
- HITL (Human-in-the-Loop) review design: sampling strategies, reviewer calibration
- Production monitoring: drift detection, quality alerts, continuous training triggers

### Produces
- Evaluation rubric structures in `docs/evaluation/`
- Evaluation harness design documents in `docs/evaluation/`
- LLM-as-judge prompt templates (domain-expert-validated)
- Ground truth collection process documents

### Does Not Cover
- Geotechnical domain content for rubrics â€” domain expert owns this (blocking gate)
- Python implementation of evaluation pipelines â€” use SpecKit
- Strategic DDD decisions â€” use `ddd-strategic`
- Shaping work for SpecKit â€” use `shaping`

## Evaluation Levels

Four levels. Every rubric must be classified before design begins.

| Level | What is measured | Automation |
|---|---|---|
| Per-task | Single atomic task output (e.g., one extracted clause) | High â€” unit-test style |
| Per-turn | One conversation turn or agent action | Moderate |
| End-to-end | Full report generation pipeline | Lower â€” integration-test style |
| Production monitoring | Live output quality over time | Continuous â€” drift detection |

## Workflow Procedure

Who does what (architect designs harness, domain expert validates content, calibration
steps, deployment gates) is defined in the `/evaluation-workflow` prompt.

## Grounding Sources

Queried via `redline-research`:

- *AI Engineering* (Huyen) â€” Evaluation-Driven Development, rubric design, domain expert role
- *LLM Engineer's Handbook* (Iusztin & Labonne) â€” FTI architecture, testing pipeline
- *Building Applications with AI Agents* (Albada) â€” HITL review, executor/reviewer/governor pattern, feedback pipelines

## Common Mistakes

| Mistake | Fix |
|---|---|
| Defining a rubric without anchoring scores to observable output examples | Every rubric level needs a concrete example of output that achieves that score |
| Using a single judge model without a second-pass reviewer | Apply maker-checker: one model generates, a different (or same) model judges — never self-evaluation |
| Skipping the calibration phase before deploying an LLM judge | Run the judge on a labelled hold-out set first; uncalibrated judges have unknown reliability |