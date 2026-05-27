---
description: Structured workflow for designing and running an LLM evaluation cycle. Orchestrates the architect (Peter) and domain expert (Graeme) through rubric design, judge prompt validation, calibration, and deployment.
name: evaluation-workflow
---

# Evaluation Workflow

Step-by-step procedure for designing and shipping an LLM evaluation cycle. This prompt
defines who does what. The architectural principles and pattern concepts are in the
`evaluation-architecture` skill.

## Pre-flight

Before starting any evaluation design work, classify the evaluation level:

| Level | What is measured | Automation |
|---|---|---|
| Per-task | Single atomic task output (e.g., one extracted clause) | High — unit-test style |
| Per-turn | One conversation turn or agent action | Moderate |
| End-to-end | Full report generation pipeline | Lower — integration-test style |
| Production monitoring | Live output quality over time | Continuous — drift detection |

**Classify before designing.** A rubric cannot be written without knowing its level.

## Responsibility Boundary

| Responsibility | Peter | Graeme |
|---|---|---|
| Evaluation architecture (what gets evaluated, how, at what level) | Owns | Consulted |
| Rubric structure (scoring system, test format, automation) | Designs | Reviews |
| Rubric content (what "correct" geotechnical output looks like) | — | Owns (blocking gate) |
| Ground truth creation | Structures the process | Provides the content |
| LLM-as-judge prompt | Designs the prompt | Validates domain accuracy |
| Production monitoring | Owns the system | Triages domain-specific alerts |

## Quick Reference

| Activity | Output | Stored at | Gate |
|---|---|---|---|
| Design evaluation harness | Rubric structure doc | `docs/evaluation/` | Peter decides |
| Write LLM-as-judge prompt | Judge prompt template | `docs/evaluation/` | Graeme validates |
| Provide rubric content | Ground truth answers | `docs/evaluation/` | Graeme owns (blocking) |
| Configure production alerts | Alert threshold config | `docs/evaluation/` | Peter configures |
| Design HITL review | Sampling strategy + calibration plan | `docs/evaluation/` | Peter designs |

## LLM-as-Judge Procedure

Use when human evaluation does not scale. Complete all steps in order — no shortcuts.

### Step 1 — Define the rubric (Peter)

Peter writes the scoring dimensions. Each dimension must:
- Be named clearly (e.g., "geotechnical accuracy", "citation completeness")
- Have a defined scale (e.g., 1–5, pass/fail)
- Have explicit criteria for each score level

Output: rubric structure document in `docs/evaluation/`.

### Step 2 — Write the judge prompt (Peter)

Peter authors the judge prompt. Requirements:
- Must be explicit about what "correct" means for each dimension
- Must not assume geotechnical knowledge the LLM judge may not have
- Must include worked examples of correct and incorrect outputs

Output: judge prompt template in `docs/evaluation/`.

### Step 3 — Domain validation (Graeme) — Blocking gate

Graeme reviews the judge prompt against geotechnical domain accuracy. This is a
**hard gate** — no proceeding without explicit sign-off.

**Invoke:** "Graeme, validate this judge prompt for geotechnical accuracy."

Graeme checks:
- Does the prompt correctly define what "accurate" means in NZ/AU geotech practice?
- Are the worked examples technically correct?
- Is there any framing that would reward a plausible-but-wrong geotechnical answer?

If Graeme flags issues, Peter revises and resubmits. This loop repeats until sign-off.

### Step 4 — Calibrate

Compare judge scores against Graeme's manual scores on a sample of 20–50 outputs.
Target: ≥80% agreement between judge and Graeme.

If calibration fails:
1. Identify which dimension is causing disagreement.
2. Peter revises the scoring criteria or judge prompt for that dimension.
3. Return to Step 3 (Graeme re-validates the revised prompt).
4. Re-calibrate.

### Step 5 — Deploy

Only after calibration passes. Peter deploys the evaluation harness.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Treating Graeme's sign-off as advisory | Sign-off is a hard gate. The rubric does not activate without it. |
| Designing rubrics without classifying evaluation level first | Classify per-task / per-turn / end-to-end / production before writing any rubric. |
| Writing judge prompts without domain validation | Every judge prompt requires Graeme to verify it captures domain accuracy. |
| Conflating evaluation structure with evaluation content | Peter structures; Graeme fills. Never merge these roles. |
| Shipping a rubric before golden datasets exist | Ground truth must exist before automation. Never validate with the model being evaluated. |
| Starting evaluation post-build | Evaluation-Driven Development: define criteria before implementation begins. |
| Skipping calibration because Graeme signed off on the prompt | Prompt quality and calibration are separate checks. Both are required. |
