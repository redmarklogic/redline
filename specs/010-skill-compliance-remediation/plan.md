# Implementation Plan: Skill Compliance Remediation

**Feature**: 010-skill-compliance-remediation  
**Created**: 2026-05-30  
**Scope**: 82 editable SKILL.md files (86 total − 4 vendor-managed speckit-* symlinks)

## Baseline Audit Results

| Principle | Failing Skills | Count |
|---|---|---|
| Description starts with "Use when" | See T-010 batch | 39 |
| Common Mistakes section present | See T-020 batch | 56 |
| Token efficiency (≤500w / ≤200w frequently-loaded) | See T-030 batch | ~50 |
| Boundary Contract present | mental-models | 1 |
| No hardcoded paths | library-management, notebooklm-index, notebooklm-mcp | 3 |
| Vendor exclusion documented | speckit-* (4 skills) | 4 |

**Frequently-loaded skills (200-word limit):** `using-superpowers` (769w), `cce-mcp` (811w), `dev-environment` (641w)

## Skills with Existing `procedures/` Directories
ceremony-agent-topology-sync, ddd-strategic, hiring-agent-management, library-management, mermaid-diagrams, resolving-pr-issues, writing-skills

## Work Batching Strategy

Work is batched by principle rather than per-skill sequential TDD, per the Assumptions in spec.md. Each batch applies one fix pattern across a cohort of skills. Pressure-scenario testing is per-principle.

### Phases

| Phase | Description | Tasks |
|---|---|---|
| 0 | Setup & vendor exclusion documentation | T-001 |
| 1 | Quick wins: boundary contract + hardcoded paths | T-002–T-005 |
| 2 | Description rewrites (39 skills) | T-010–T-014 |
| 3 | Common Mistakes sections (56 skills) | T-020–T-026 |
| 4 | Token efficiency extraction (50 skills) | T-030–T-040 |
| 5 | Final compliance audit | T-050 |

## Architecture Notes

- All changes are SKILL.md edits + optional new `procedures/<name>.md` files
- No Python code changes; no test files required (pressure scenarios are subagent runs, not automated tests)
- Token efficiency extraction: move step-by-step procedures to `procedures/<name>.md`, add cross-reference in SKILL.md
- Description rewrites: preserve meaning, rewrite as "Use when [triggering conditions]" under 500 chars, no workflow summary
- Common Mistakes: minimum one mistake→fix pair per skill; derive from existing inline examples or domain knowledge

## File Structure

```
.agents/skills/<name>/
  SKILL.md              # Edited in-place (every phase)
  procedures/           # New files for token extraction (Phase 4)
```

## Task Naming Convention

`T-NNN`: Three-digit task ID  
`[P]`: Tasks within a phase that can execute in parallel (different skills)
