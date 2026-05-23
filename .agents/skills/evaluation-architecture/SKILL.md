---
name: evaluation-architecture
description: Use when designing an LLM evaluation lifecycle, structuring evaluation rubrics, implementing LLM-as-judge patterns, or architecting an evaluation pipeline for AI-generated geotechnical outputs.
---

# Evaluation Architecture

## Overview

Evaluation criteria are defined **before** implementation begins — Evaluation-Driven Development (Huyen). The architect designs the harness structure; the domain expert fills it with domain truth content. No rubric ships without the domain expert's explicit sign-off.

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
- LLM-as-judge prompt templates (domain-expert-validated)
- Ground truth collection process documents

### Does Not Cover
- Geotechnical domain content for rubrics — domain expert owns this (blocking gate)
- Python implementation of evaluation pipelines — use SpecKit
- Strategic DDD decisions — use `ddd-strategic`
- Shaping work for SpecKit — use `shaping`

## Evaluation Levels

Four levels. Every rubric must be classified before design begins.

| Level | What is measured | Automation |
|---|---|---|
| Per-task | Single atomic task output (e.g., one extracted clause) | High — unit-test style |
| Per-turn | One conversation turn or agent action | Moderate |
| End-to-end | Full report generation pipeline | Lower — integration-test style |
| Production monitoring | Live output quality over time | Continuous — drift detection |

## Workflow Procedure

Who does what (architect designs harness, domain expert validates content, calibration
steps, deployment gates) is defined in the `/evaluation-workflow` prompt.

## Grounding Sources

Queried via `redline-research`:

- *AI Engineering* (Huyen) — Evaluation-Driven Development, rubric design, domain expert role
- *LLM Engineer's Handbook* (Iusztin & Labonne) — FTI architecture, testing pipeline
- *Building Applications with AI Agents* (Albada) — HITL review, executor/reviewer/governor pattern, feedback pipelines
