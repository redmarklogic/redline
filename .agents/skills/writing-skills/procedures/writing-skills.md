# Writing Skills

## Description Field Rules

1. Start with `"Use when..."` — triggering conditions only.
2. **Never summarize the workflow** — Claude will follow the description as a shortcut and skip the skill body.
3. Write in third person. Keep under 500 characters.

### Keyword Coverage

Use words Claude would search for: error messages, symptoms (`flaky`, `hanging`), synonyms (`timeout/hang/freeze`), and tool names.

### Naming

Use active-voice gerunds: `condition-based-waiting` over `async-test-helpers`. Never name after agents.

### Token Efficiency

| Target | Limit |
|---|---|
| Getting-started workflows | < 150 words each |
| Frequently-loaded skills | < 200 words total |
| Other skills | < 500 words |

- Move step-by-step workflows to `procedures/`.
- Move heavy reference (100+ lines) to a separate `.md` file.
- Cross-reference other skills rather than repeating content.
- One excellent example beats multiple mediocre ones.

### Cross-Referencing

Use skill name with explicit markers — never `@file` syntax (force-loads context):
- `**REQUIRED:** Use \`test-driven-development\`` — good
- `@skills/test-driven-development/SKILL.md` — bad (force-loads 200k+ context)

## Overview

Writing skills IS TDD applied to process documentation. You write test cases (pressure scenarios with subagents), watch them fail (baseline), write the skill, watch tests pass, and refactor (close loopholes).

**Core principle:** If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing.

**Required background:** `test-driven-development`. Official Anthropic guidance: `anthropic-best-practices.md`.

## TDD Mapping

| TDD Concept | Skill Creation |
|---|---|
| Test case | Pressure scenario with subagent |
| Production code | Skill document (SKILL.md) |
| RED | Agent violates rule without skill (baseline) |
| GREEN | Agent complies with skill present |
| REFACTOR | Close loopholes while maintaining compliance |

**Full workflow:** `procedures/create-skill.md`

## When to Create a Skill

**Create when:** technique wasn't intuitively obvious; you'd reference it across projects; others would benefit.

**Don't create for:** one-off solutions; practices documented elsewhere; project-specific conventions; mechanically enforceable rules (automate instead).

**Never name a skill after an agent.** Skills are agent-agnostic. Use domain/function prefixes: `hiring-`, `python-`, `pm-`. Agents know which skills to load — skills must not reference which agent uses them.

## Skill Types

| Type | Description | Examples |
|---|---|---|
| Technique | Concrete method with steps | condition-based-waiting, root-cause-tracing |
| Pattern | Mental model for problems | flatten-with-flags, test-invariants |
| Reference | API docs, syntax guides | graphviz-conventions, office-docs |

## SKILL.md Structure

```markdown
---
name: Skill-Name-With-Hyphens
description: Use when [specific triggering conditions and symptoms]
---

# Skill Name

## Overview
Core principle in 1–2 sentences.

## Core Pattern / Quick Reference
Table or code for scanning.

## CSO (Claude Search Optimization)
```

### CSO (Claude Search Optimization)

```yaml
# BAD — summarizes workflow
description: Use when executing plans - dispatches subagent per task with code review

# GOOD — triggering conditions only
description: Use when executing implementation plans with independent tasks in the current session
```

## No Hardcoded User Paths

Never embed machine-specific paths (`C:\Users\<USER>\...`). Use: <!-- hook: allow -->

| Context | Use |
|---|---|
| Python venv | `.venv\Scripts\python.exe` (project-relative) |
| Repo root | `pathlib.Path(__file__).resolve().parents[N]` |
| Temp files | `pathlib.Path(tempfile.gettempdir())` or `$env:TEMP` |

Use placeholders `<repo-root>`, `<venv>` in examples.

## Directory Structure

```
.agents/skills/
  skill-name/
    SKILL.md              # Lean reference (required)
    procedures/           # Step-by-step workflows
    supporting-file.*     # Heavy reference or reusable tools
```

## Flowchart Usage

Use **only** for non-obvious decision points or process loops. Never for:
- Reference material → tables
- Code examples → code blocks
- Linear instructions → numbered lists
- Labels without semantic meaning (step1, helper2)

See `graphviz-conventions.dot` for style rules.

## Anti-Patterns

| Anti-pattern | Why it fails |
| --- | --- |
| Narrative examples ("In session 2025-10-03...") | Too specific, not reusable |
| Multi-language examples (js + py + go) | Mediocre quality, maintenance burden |
| Code in flowcharts | Can't copy-paste, hard to read |
| Generic labels (step1, helper2) | No semantic meaning |
| Skill named after an agent | Agent-specific, not reusable |

## The Iron Law

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

Write skill before testing? Delete it. Start over. Edit without testing? Same violation. See `procedures/create-skill.md`.

## SRP Rule

Every skill must do **one thing**. This rule is enforceable from this document alone — no
cross-reference to another document is required to reach a verdict (SC-006).

### Naming Constraint

- Skill name must be a single **verb-noun** pair: `resolve-conflict`, `design-eval-rubric`.
- The word "and" is **prohibited** in a skill name when it joins two distinct concerns
  (structural conjunction). Example violations: `hire-and-manage`, `find-and-fix`,
  `hiring-and-assessment`.
- Exception: domain compound nouns where "and" is part of a recognised domain term are
  not structural conjunctions. Add the skill to the Known Exception Skip-List in
  `.agents/skills/sync-agent-topology/procedures/srp-scan-procedure.md`.

### Responsibility-Statement Constraint

- The `description:` field must describe **one triggering concern** only.
- The word "and" in a description is a violation signal when it joins independent concerns.
  Example violation: `"Use when hiring agents, running agent audits, or maintaining the org chart"` —
  three independent concerns joined.
- A description that lists sequential steps of a single concern is not a violation.
  Example pass: `"Use when resolving a failing PR from reproduction through to merge-ready state"` —
  one concern, multiple steps.

### Pass / Fail Test Format

Apply this test to any candidate skill name and description before creating or approving the skill:

| Question | Pass | Fail |
| --- | --- | --- |
| Does the name contain structural "and"? | No "and", or "and" is a domain compound noun | "and" joins two independent verbs/nouns |
| Does the description reference more than one independent triggering concern? | Single concern stated | Multiple independent concerns listed |
| Could the skill be split into two skills that each have distinct, non-overlapping use-when conditions? | No — splitting would destroy coherence | Yes — split is the right action |

### Exception Path

When a skill has multiple sub-concerns but splitting would destroy end-to-end coherence
(justified orchestrator, justified pipeline, or coherent interface pattern), add it to
the Known Exception Skip-List in
`.agents/skills/sync-agent-topology/procedures/srp-scan-procedure.md`.

Required fields: `exception-category`, `rationale`.

Exception categories:

- `justified-orchestrator` — skill wraps a lifecycle of sub-skills serving one concern
- `justified-pipeline` — skill coordinates sequential steps with a single trigger and single output concern
- `justified-coherent-interface` — skill is a thin adapter to a single external service with multiple operations
- `domain-compound-noun` — skill name contains "and" as part of a recognised domain term, not a structural conjunction

### SRP Compliance Pass

Every Agent Topology Sync run must include an SRP Compliance Pass that scans all
`SKILL.md` frontmatter `name` and `description` fields. See `sync-agent-topology`
`procedures/srp-scan-procedure.md` for the scan algorithm and false-positive rules.

---

## Procedures

| Procedure | Purpose |
|---|---|
| `procedures/create-skill.md` | Full RED-GREEN-REFACTOR cycle + creation checklist |
| `procedures/test-skill.md` | Testing methodology by skill type + bulletproofing |

## Supporting Files

| File | Purpose |
|---|---|
| `anthropic-best-practices.md` | Official Anthropic skill-authoring guidance |
| `testing-skills-with-subagents.md` | Full pressure-scenario testing methodology |
| `persuasion-principles.md` | Research foundation for bulletproofing discipline skills |
| `graphviz-conventions.dot` | Flowchart style rules |
| `skill-advanced-techniques.md` | Advanced frontmatter options, decision table, and audit checklist — load when creating, editing, or auditing any skill for `paths:`, `!` injection, `arguments`, `context: fork`, or `disable-model-invocation` |

Same benefits: Better quality, fewer surprises, bulletproof results.

If you follow TDD for code, follow it for skills. It's the same discipline applied to documentation.
