---
name: evaluation-architecture
description: Use when designing an LLM evaluation lifecycle, structuring evaluation rubrics, implementing LLM-as-judge patterns, or architecting an evaluation pipeline for AI-generated geotechnical outputs.
---

# Evaluation Architecture

## Overview

Evaluation criteria are defined **before** implementation begins — Evaluation-Driven Development (Huyen). Peter designs the harness structure; Graeme fills it with domain truth content. No rubric ships without Graeme's explicit sign-off.

## Boundary Contract

### Applies To
- LLM evaluation lifecycle design: per-task, per-turn, end-to-end, production monitoring
- Evaluation rubric structure: scoring systems, test formats, automation approaches
- LLM-as-judge prompt design and calibration against human evaluation
- Ground truth management: structuring the collection process for domain expert review
- Evaluation pipeline architecture (FTI — Feature/Training/Inference pattern)
- HITL (Human-in-the-Loop) review design: sampling strategies, reviewer calibration
- Production monitoring: drift detection, quality alerts, continuous training triggers

### Produces
- Evaluation rubric structures in `docs/evaluation/`
- Evaluation harness design documents in `docs/evaluation/`
- LLM-as-judge prompt templates (validated by Graeme)
- Ground truth collection process documents

### Does Not Cover
- Geotechnical domain content for rubrics — Graeme owns this (blocking gate)
- Python implementation of evaluation pipelines — use SpecKit
- Strategic DDD decisions — use `ddd-strategic`
- Shaping work for SpecKit — use `shaping`

## Quick Reference

| Activity | Output | Stored at | Gate |
|---|---|---|---|
| Design evaluation harness | Rubric structure doc | `docs/evaluation/` | Peter decides |
| Write LLM-as-judge prompt | Judge prompt template | `docs/evaluation/` | Graeme validates |
| Provide rubric content | Ground truth answers | `docs/evaluation/` | Graeme owns (blocking) |
| Configure production alerts | Alert threshold config | `docs/evaluation/` | Peter configures |
| Design HITL review | Sampling strategy + calibration plan | `docs/evaluation/` | Peter designs |

## Evaluation Levels

Four levels. Every rubric must be classified before design begins.

| Level | What is measured | Automation |
|---|---|---|
| Per-task | Single atomic task output (e.g., one extracted clause) | High — unit-test style |
| Per-turn | One conversation turn or agent action | Moderate |
| End-to-end | Full report generation pipeline | Lower — integration-test style |
| Production monitoring | Live output quality over time | Continuous — drift detection |

## LLM-as-Judge Pattern

Use when human evaluation does not scale. Required steps in order:

1. **Define the rubric** — Peter writes the scoring dimensions.
2. **Write the judge prompt** — Peter authors; must be explicit about what "correct" means.
3. **Domain validation** — Graeme verifies the judge prompt captures geotechnical accuracy. Blocking gate.
4. **Calibrate** — Compare judge scores against Graeme's manual scores on a sample. Target: ≥80% agreement.
5. **Deploy** — Only after calibration passes.

## The Evaluation Boundary

| Responsibility | Peter | Graeme |
|---|---|---|
| Evaluation architecture (what gets evaluated, how, at what level) | Owns | Consulted |
| Rubric structure (scoring system, test format, automation) | Designs | Reviews |
| Rubric content (what "correct" geotechnical output looks like) | — | Owns (blocking gate) |
| Ground truth creation | Structures the process | Provides the content |
| LLM-as-judge prompt | Designs the prompt | Validates domain accuracy |
| Production monitoring | Owns the system | Triages domain-specific alerts |

## Common Mistakes

| Mistake | Fix |
|---|---|
| Treating Graeme's sign-off as advisory | Sign-off is a hard gate. Rubric does not activate without it. |
| Designing rubrics without classifying evaluation level first | Classify per-task / per-turn / end-to-end / production before writing any rubric. |
| Writing judge prompts without domain validation | Every judge prompt requires Graeme to verify it captures domain accuracy. |
| Conflating evaluation structure with evaluation content | Peter structures; Graeme fills. Never merge these roles. |
| Shipping a rubric before golden datasets exist | Ground truth must exist before automation. Never validate with the model being evaluated. |
| Starting evaluation post-build | Evaluation-Driven Development: define criteria before implementation begins. |

## Grounding Sources

Queried via `redline-research`:

- *AI Engineering* (Huyen) — Evaluation-Driven Development, rubric design, domain expert role
- *LLM Engineer's Handbook* (Iusztin & Labonne) — FTI architecture, testing pipeline
- *Building Applications with AI Agents* (Albada) — HITL review, executor/reviewer/governor pattern, feedback pipelines
