# Implementation Plan: Mental Models Skill

**Date**: 2026-05-27 | **Spec**: [spec.md](spec.md)
**Status**: Delivered

## Summary

Pure Markdown skill — no Python code. Delivered as 36 model files across 6 category subfolders under `.agents/skills/mental-models/`, a `SKILL.md` catalog, inline links in seven agent JDs, and refactored references in six skills that previously defined models inline.

## Design Decisions

| #  | Decision | Choice | Rationale |
| -- | -------- | ------ | --------- |
| D1 | Agent JD integration pattern | Inline links at point-of-use rather than a dedicated `## Mental Models` section | Links are co-located with the behaviour they govern; a separate section would drift and require agents to cross-reference |
| D2 | Model file granularity | One file per model | Keeps files self-contained; agents load only what they need |
| D3 | Refactoring scope | All skills with inline model definitions (not just resolving-pr-issues) | Consistency; partial refactoring leaves divergent sources of truth |

## Delivered Artifacts

| Artifact | Description |
| -------- | ----------- |
| `.agents/skills/mental-models/SKILL.md` | Quick-reference catalog, 36 models | <!-- mental-model-link: allow -->
| `.agents/skills/mental-models/general_thinking/` | 13 model files |
| `.agents/skills/mental-models/strategic_decisions/` | 12 model files |
| `.agents/skills/mental-models/self_awareness/` | 4 model files |
| `.agents/skills/mental-models/root_cause_analysis/` | 2 model files |
| `.agents/skills/mental-models/risk_analysis/` | 3 model files |
| `.agents/skills/mental-models/communication/` | 2 model files |
| Agent JDs (Ron, Mark, Peter, Matt, John, Kabilan) | Inline links to mental-model files |
| `resolving-pr-issues`, `test-driven-development`, `notebooklm-deep-research`, `strategy-pre-mortem`, `strategy-psf-domain`, `pm-prioritization` | Refactored to reference mental-model files |

## Risk Register

| Risk | Mitigation |
| ---- | ---------- |
| New models added without updating `SKILL.md` | `SKILL.md` is the authoritative catalog; PR reviewers must verify any new model file is listed |
| Agent JD links break if files are moved | Model files are stable by convention; renames require a grep across agent JDs |
