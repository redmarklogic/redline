# Design: spec-kit Skill

**Created**: 2026-04-11
**Status**: Implemented
**Branch**: feature/map-doc-writing-process

## Summary

Replace three existing skills (`spec-planning`, `writing-plans`, `executing-plans`) with a
single `spec-kit` skill that wraps the [GitHub Spec Kit](https://github.com/github/spec-kit)
CLI and its Specification-Driven Development (SDD) workflow. The skill acts as a thin
orchestrator: it ensures the `specify` CLI is installed, initialises the project's `.specify/`
infrastructure, installs a project-specific preset, and delegates to spec-kit's command
templates for the actual work.

## Motivation

- **Consolidation**: Three overlapping skills (spec-planning, writing-plans, executing-plans)
  become one end-to-end workflow.
- **Upstream leverage**: Spec-kit's templates, scripts, and preset system evolve independently;
  upgrades are free.
- **Minimal friction**: The user says "create a spec for X" in Copilot chat, and the agent
  handles setup, defaults, and execution with minimal questions.

## Architecture

### Overview

```
.agents/skills/spec-kit/
  SKILL.md                          # Orchestrator: setup, workflow, upgrade
  presets/                          # Project-specific spec-kit preset
    preset.yml                      # Manifest (id, version, provides)
    templates/
      spec-template.md              # RICE scoring for scenarios
      plan-template.md              # Pre-filled tech context + MoSCoW section
      tasks-template.md             # Vertical slice sizing
    commands/
      speckit.plan.md               # Injects tech context presets + MoSCoW
      speckit.tasks.md              # Enforces vertical slice task sizing
```

### Setup (first use, automated by the agent)

1. **CLI check**: Run `specify version`. If the command is not found:

   ```powershell
   rtk uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
   ```

2. **Project init**: If `.specify/` does not exist:

   ```powershell
   specify init --here --ai copilot --script ps --force --no-git
   ```

3. **Preset install**: If the project preset is not already installed:

   ```powershell
   specify preset add --dev .agents/skills/spec-kit/presets/
   ```

### Upgrade

When the user asks to upgrade spec-kit:

```powershell
rtk uv tool install specify-cli --force --from git+https://github.com/github/spec-kit.git
specify init --here --ai copilot --script ps --force --no-git
```

Then re-check that the project preset is still installed (`specify preset list`).

## Command Workflow

The skill supports these commands in this order. Each command maps to a spec-kit
command template installed in `.github/copilot/commands/`.

**Integration mode**: `specify init --here --ai copilot --script ps` installs agent
mode files in `.github/agents/speckit.*.agent.md` and prompt files in
`.github/prompts/speckit.*.prompt.md`. These appear as slash commands in Copilot Chat
(e.g., `/speckit.specify`). The `spec-kit` skill orchestrates which command to invoke
and in what order.

| Step | Command        | Human input                              | Automated by preset                                     |
| ---- | -------------- | ---------------------------------------- | ------------------------------------------------------- |
| 1    | constitution   | Project principles (first time only)     | Pre-fill: Python 3.14, layered arch, TDD, single-dev    |
| 2    | specify        | Feature description (chat or .md file)   | RICE scoring for scenario prioritisation                 |
| 3    | clarify        | Answers to ambiguity questions (if any)  | Triggers only if spec has NEEDS CLARIFICATION markers    |
| 4    | plan           | Minimal -- preset fills tech context     | Python 3.14, uv, pytest, layered arch, MoSCoW section   |
| 5    | tasks          | None                                     | Vertical slice sizing, behaviour-based phases            |
| 6    | analyze        | None                                     | Read-only consistency check, max 30 findings             |
| 7    | implement      | None                                     | Execute tasks in order, mark completed                   |

### Spec input modes

The `specify` command accepts feature descriptions from two sources:

- **Conversation context**: The user describes the feature in the Copilot chat thread.
  The agent extracts requirements from the conversation.
- **External .md file**: The user references a markdown file (e.g., a research doc or
  concept doc in `docs/`). The agent reads it and uses it as the specification input.

### Conditional clarification

After `specify`, the agent checks the generated `spec.md` for `[NEEDS CLARIFICATION]`
markers. If any exist, it triggers `clarify` automatically. If the spec is clean, it
proceeds directly to `plan`.

## Project Preset

The preset lives in `.agents/skills/spec-kit/presets/` and is installed into the project
via `specify preset add --dev`. It overrides spec-kit's default templates with
project-specific conventions.

### RICE Scoring (in spec-template)

Each scenario in the specification gets a RICE score:

$$Score = \frac{Reach \times Impact \times Confidence}{Effort}$$

- **Reach**: How many users will this affect?
- **Impact**: How much will it improve the experience? (scale 0.5 to 3)
- **Confidence**: How sure are you about your estimates? (percentage)
- **Effort**: How much time/resources will it take? (person-months)

Scenarios are ordered by RICE score (highest first) to drive prioritisation.

### MoSCoW (in plan-template)

The implementation plan includes a MoSCoW section that records which features go
into the current plan and which are explicitly deferred:

- **Must have**: Non-negotiable for this release
- **Should have**: Important but not critical; can be delivered later
- **Could have**: Desirable if time permits
- **Won't have (this time)**: Explicitly out of scope for this iteration

This section serves as a decision record so scope choices are transparent and
auditable.

### Vertical Slice Task Sizing (in tasks-template)

The tasks template overrides spec-kit's default user-story grouping:

> A well-sized task is a **vertical slice**: front-to-back, one complete new
> behaviour, nothing left dangling. Do not split by technical layer (schema +
> logic + UI as three tasks) -- split by user-visible behaviour.

This aligns with the project's layered architecture: each task delivers one
observable behaviour end-to-end through the layers, rather than "create all
models, then all services, then all endpoints."

### Pre-filled Technical Context (in plan-template)

The plan template pre-fills these values:

- **Language**: Python 3.14
- **Package manager**: uv
- **Testing**: pytest (TDD workflow per `test-driven-development` skill)
- **Architecture**: Layered (domain -> functions -> scripts)
- **Dev OS**: Windows
- **Deploy OS**: Linux
- **Domain modeling**: Pydantic BaseModel, Pandera DataFrameModel

## Skills Removed

| Skill             | Reason                                           |
| ----------------- | ------------------------------------------------ |
| `spec-planning`   | Fully replaced by spec-kit's specify/plan/tasks  |
| `writing-plans`   | Replaced by spec-kit's plan + tasks commands     |
| `executing-plans` | Replaced by spec-kit's implement command         |

## Skills Updated

| Skill          | Change                                                          |
| -------------- | --------------------------------------------------------------- |
| `brainstorming`| Terminal state changes from `writing-plans` to `spec-kit`       |
| `subagent-driven-development` | Decision tree updated: `executing-plans` removed |
| `python-domain-modeling` | Added strategic DDD cross-ref, subdomain classification, bounded contexts, ubiquitous language, multi-package layout, layer enforcement section |
| `python-linting` | Fixed stale `importlinter.ini` reference to `pyproject.toml` |
| `finishing-a-development-branch` | Updated caller from `executing-plans` to `spec-kit` |
| `requesting-code-review` | Updated integration section from `executing-plans` to `spec-kit` |
| AGENTS.md      | Remove 3 deleted skills, add `spec-kit`, update brainstorming   |

## DDD Integration

Strategic DDD decisions (subdomain classification, bounded context identification,
EventStorming, context maps) are captured during the `plan` phase via the Domain Impact
section. Tactical DDD (how to implement entities, VOs, aggregates in Python) stays in
the `python-domain-modeling` skill.

Living domain document: `docs/architecture/domain-model.md` tracks subdomain
classification, bounded contexts, layer architecture, ubiquitous language, and
entity/VO registry across features.

## Import-Linter Integration

Import-linter contracts in `pyproject.toml` are the executable documentation of the
layered architecture. A deep reference file at
`.agents/skills/spec-kit/references/import-linter.md` covers all contract types
(Layers, Forbidden, Independence, Protected, Acyclic Siblings), configuration options,
failure scenarios, and when to update contracts.

The `plan` phase Domain Impact section explicitly asks whether a feature changes the
layer topology, ensuring architectural drift is caught at design-time.

## Relationship to Other Skills

| Skill                     | Relationship                                                      |
| ------------------------- | ----------------------------------------------------------------- |
| `brainstorming`           | Transitions to `spec-kit` as terminal state                       |
| `test-driven-development` | Referenced by the tasks preset -- tasks enforce test-first order   |
| `python-domain-modeling`  | Referenced by spec-template for entity definitions                |
| `python-class-design`     | Referenced by plan-template for architectural decisions            |
| `python-static-checks`    | Run before declaring `implement` complete                         |

## Risks

| Risk                                  | Impact                                              | Mitigation                                    |
| ------------------------------------- | --------------------------------------------------- | --------------------------------------------- |
| Spec-kit upstream breaking changes    | Preset templates may become incompatible             | Pin to a specific release tag on install       |
| .specify/ dir conflicts with existing | Init may overwrite project files                     | --force flag; review diff after init           |
| Two skill systems (.agents + .github) | Confusion about which skills/commands are canonical  | Skill doc clearly states spec-kit is canonical |
