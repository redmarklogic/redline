# Evaluation Architecture

## Purpose

LLM evaluation lifecycle design, rubric structures, LLM-as-judge patterns, and evaluation pipeline architecture for Redline's AI-assisted geotechnical document quality platform.

## What This Skill Covers

- Evaluation-Driven Development (Huyen): define evaluation criteria before building
- Four-level evaluation taxonomy: per-task, per-turn, end-to-end, production monitoring
- LLM-as-judge patterns: designing judge prompts, calibrating against human evaluation, Graeme's domain validation of judge prompts
- Evaluation rubric structure design: scoring systems, test formats, automation approaches
- Ground truth management: structuring the process for Graeme to provide domain content
- Evaluation pipeline design: FTI (Feature/Training/Inference) architecture (language-, framework-, platform-agnostic per LLM Engineer's Handbook)
- HITL (Human-in-the-Loop) review design: which outputs require human review, sampling strategies, reviewer calibration
- Production monitoring: drift detection, quality alerts, continuous training triggers

## Key Boundary

Peter designs the evaluation architecture. Graeme fills it with domain truth. No rubric ships without Graeme's sign-off. This boundary is absolute.

## Grounding Sources (to be queried via `redline-research`)

- *AI Engineering* (Huyen) — Evaluation-Driven Development, rubric design, domain expert role
- *LLM Engineer's Handbook* (Iusztin & Labonne) — FTI architecture, testing pipeline
- *Building Applications with AI Agents* (Albada) — HITL review, executor/reviewer/governor pattern, feedback pipelines

## Status

**Pending notebook grounding.** This skill requires queries to the Software Development Methodology & Engineering Organisation notebook and the AI System Engineering notebook before the content can be fully elaborated. The structure above defines what the skill must cover; the notebook grounding will provide the specific patterns and anti-patterns.

## Who Uses This Skill

Peter (primary). Graeme consults for domain content within the rubric structure.
