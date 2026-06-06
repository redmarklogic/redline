# Spec Kit — Detailed Reference

### Inputs
- Feature description (conversation context or external `.md` file)
- `.specify/` project configuration (`architecture.yml`, `extensions.yml`)
- Concept docs or research docs from `docs/`

### Outputs
- `specs/NNN-feature/spec.md` -- feature specification with RICE-scored scenarios
- `specs/NNN-feature/plan.md` -- implementation plan with MoSCoW and domain impact
- `specs/NNN-feature/tasks.md` -- dependency-ordered vertical-slice tasks
- `specs/NNN-feature/pipeline-diagram.md` -- function pipeline (Phase 1, produced during plan)
- `specs/NNN-feature/class-diagram.md` -- value object class diagram (Phase 2, produced during plan after pipeline approval)
- `.specify/` project infrastructure (on first use)

### Out of Scope
- Design exploration and requirements elicitation (`brainstorming`)
- Research queries against NotebookLM knowledge bases (`redline-research`)
- Code implementation patterns (`python-*` skills)

## Setup (automated on first use)

The agent runs these steps silently when any spec-kit command is invoked.

### 1. CLI check

```powershell
specify version
```

If `specify` is not found:

```powershell
rtk uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

### 2. Project init

If `.specify/` does not exist:

```powershell
specify init --here --ai copilot --script ps --force --no-git
```

This installs agent mode files in `.github/agents/speckit.*.agent.md` and prompt
files in `.github/prompts/speckit.*.prompt.md` (usable as slash commands in Copilot Chat).

### 3. Preset install

If the project preset is not already installed (`specify preset list` does not show it):

```powershell
specify preset add --dev .agents/skills/spec-kit/presets/
```

### 4. Architecture decision (greenfield only)

On first-time setup (no existing `src/` directory or only one package exists and declared in pyproject.toml), ask the
developer:

> **Will this project use a monorepo layout with multiple independent packages under
> `src/`, or a single package?**
>
> - **Monorepo (sibling packages)**: Each bounded context is a top-level package under
>   `src/`. One package acts as the integration hub, others are independent tools that
>   may graduate to standalone PyPI packages. New features trigger a modularity
>   assessment (new package vs. subpackage).
> - **Single package**: All code lives under one top-level package (e.g., `src/rl/`).
>   New features add subpackages within the existing layer hierarchy.

Record the answer in `.specify/architecture.yml`:

```yaml
### Upgrade

When the user asks to upgrade spec-kit:

```powershell
rtk uv tool install specify-cli --force --from git+https://github.com/github/spec-kit.git
specify init --here --ai copilot --script ps --force --no-git
```

Then re-check the project preset is still installed.

### Spec input modes

The `specify` command accepts feature descriptions from two sources:

- **Conversation context**: The user describes the feature in Copilot chat. The agent
  extracts requirements from the conversation.
- **External .md file**: The user references a markdown file (e.g., a research doc or
  concept doc in `docs/`). The agent reads it and uses it as the specification input.

### Conditional clarification

After `specify`, check the generated `spec.md` for `[NEEDS CLARIFICATION]` markers.
If any exist, trigger `clarify` automatically. If the spec is clean, proceed to `plan`.

### RICE Scoring (spec-template)

Each scenario in the specification gets a RICE score:

$$Score = \frac{Reach \times Impact \times Confidence}{Effort}$$

- **Reach**: How many users/workflows does this affect?
- **Impact**: How much improvement? (scale 0.5 to 3)
- **Confidence**: How sure are the estimates? (percentage)
- **Effort**: How much time/resources? (person-days for this single-dev repo)

Scenarios are ordered by RICE score (highest first) to drive prioritisation.

### MoSCoW (plan-template)

The plan includes a MoSCoW section recording scope decisions:

| Category                 | Rule                                                        |
| ------------------------ | ----------------------------------------------------------- |
| **Must have**            | Without it, the deliverable is unusable or the system fails |
| **Should have**          | Painful to omit, but the system is functional without it    |
| **Could have**           | Useful but a delighter -- no pain if absent                 |
| **Won't have (this time)** | Explicitly out of scope for this iteration                |

Naming Won't Have items is as important as naming Must Haves. An unnamed deferred
item is scope creep waiting to happen.

### Vertical Slice Task Sizing (tasks-template)

> A well-sized task is a **vertical slice**: front-to-back, one complete new
> behaviour, nothing left dangling. Do not split by technical layer (schema +
> logic + UI as three tasks) -- split by user-visible behaviour.

Each task delivers one observable behaviour end-to-end through the layers, rather
than "create all models, then all services, then all endpoints."

### Pre-filled Technical Context (plan-template)

The plan template pre-fills these values so the agent does not need to ask:

- **Language**: Python 3.14
- **Package manager**: uv
- **Testing**: pytest (TDD workflow per `test-driven-development` skill)
- **Project layout**: Read from `.specify/architecture.yml` (`monorepo` or `single-package`)
- **Architecture**: Monorepo: sibling packages under `src/`, each with optional internal layers. Single-package: layered (domain > schemas > functions). Add project-specific higher layers above `functions` only when the project warrants them.
- **Dev OS**: Windows
- **Deploy OS**: Linux
- **Domain modeling**: Pydantic BaseModel, Pandera DataFrameModel

### When to include

Always. Even if the answer is "no domain impact", state that explicitly.

### What to assess

1. **Modularity -- new package or subpackage?**: Check `.specify/architecture.yml`.
   If the project layout is `monorepo`, apply the decision matrix from the
   `python-domain-modeling` skill to determine whether this feature warrants a new
   top-level sibling package under `src/` (new bounded context) or a subpackage
   within an existing package. If the project layout is `single-package`, skip the
   modularity assessment and add to the existing package's layer hierarchy.

2. **New layers**: Does this feature introduce a new subpackage under an
   `exhaustive = true` import-linter container? If yes, state which contract is
   affected and what the updated `layers` list looks like.

3. **New bounded contexts**: Does this feature introduce a new domain area that should
   be independent from existing ones? If yes, propose an `independence` contract
   between the new top-level package and existing bounded context packages.

4. **Layer splits**: Does an existing layer need sub-layering? If yes, propose a
   nested `[[tool.importlinter.contracts]]` block.

5. **Cross-cutting concerns**: Does this feature add a utility package that multiple
   layers or packages need? If yes, add it to `exhaustive_ignores` or as the lowest
   layer, or create a fine-grained shared kernel package.

6. **Subdomain classification**: Is this Core (competitive advantage, custom code),
   Supporting (necessary but not differentiating), or Generic (commodity, off-the-shelf)?
   This drives the tactical pattern choice:
   - **Core**: Full DDD -- aggregates, domain events, rich domain model
   - **Supporting**: Simpler patterns -- transaction scripts, thin domain layer
   - **Generic**: Off-the-shelf libraries, no custom domain model

7. **Ubiquitous Language**: Does this feature introduce new domain terms? List them
   with definitions. These should be added to `docs/architecture/domain-model.md`.

### Template

```markdown
### Post-Plan Step: Library Best Practices (mandatory)

After the initial plan draft, use Context7 MCP to fetch best practices and latest
documentation for every third-party package listed in Technical Context. Append a
`## Library Best Practices` section to the plan file with one subsection per package.

Skip condition: well-known stdlib modules or packages already reviewed in this plan.

### Task format

```
- [ ] T### [P?] [Phase?] Description with exact file path
```

# Spec Kit

Thin orchestrator around the [GitHub Spec Kit](https://github.com/github/spec-kit) CLI.
Ensures the CLI is installed, initialises project infrastructure, installs the project
preset, and delegates to spec-kit's command templates for specification-driven development.

Replaces the former `spec-planning`, `writing-plans`, and `executing-plans` skills with a
single end-to-end workflow.

# Architecture decision recorded during spec-kit init
layout: monorepo   # or: single-package
hub_package: rl    # the integration hub (monorepo only)
```

If the file already exists, skip this step.

This decision affects:
- The **Architecture** line in the plan template's Technical Context
- Whether the **Domain Impact** section requires a modularity assessment
- How `constitution` pre-fills project principles

## Command Workflow

Seven commands, used in this order. Each maps to a spec-kit command template.
Artifacts are validated incrementally: each artifact is analyzed against its
predecessors before the next one is written (see Incremental Analysis below).

| Step | Command       | Human Input                             | Automated by Preset                                    |
| ---- | ------------- | --------------------------------------- | ------------------------------------------------------ |
| 0    | reconcile     | None (automated)                        | Source document reconciliation (see `speckit.source-reconciliation.run`) |
| 1    | constitution  | Project principles (first time only)    | Pre-fill: Python 3.14, layout from architecture.yml, TDD, single-dev |
| 2    | specify       | Feature description (chat or .md file)  | RICE scoring for scenario prioritisation                |
| 3    | clarify       | Answers to ambiguity questions (if any) | Triggers only if spec has NEEDS CLARIFICATION markers   |
| 4    | plan          | Minimal -- preset fills tech context    | Tech context, MoSCoW, Domain Impact; pipeline-diagram.md (Phase 1, founder approval gate); class-diagram.md (Phase 2) |
| 5    | tasks         | None                                    | Vertical slice sizing, behaviour-based phases           |
| 6    | analyze       | None                                    | Read-only consistency check, max 30 findings            |
| 7    | implement     | None                                    | Execute tasks in order, mark completed                  | <!-- hook: allow -->

## Concept-to-Plan Phase Mapping (plan phase)

When the spec input is a concept doc with numbered steps or phases, the plan MUST
start with an explicit mapping table before the Phased Delivery section:

```markdown
## Concept-to-Plan Phase Mapping

| Concept Step | Concept Name | Plan Phase | Notes |
| ------------ | ------------ | ---------- | ----- |
| Step 0       | [name]       | Phase 0    | [differences, if any] |
| Step 1       | [name]       | Phase 1    | [combined with Step X] |
| Step N       | [name]       | Deferred   | [reason] |
```

This prevents phase-numbering confusion and makes scope exclusions visible at a glance.

## Preset Conventions

The project preset lives in `.agents/skills/spec-kit/presets/` and overrides spec-kit
defaults with project-specific conventions.

## Domain Impact Section (plan phase)

Every plan MUST include a **Domain Impact** section assessing whether the feature
changes the project's architectural structure. This catches drift at design-time.

## Domain Impact

```
**Modularity assessment**: [New top-level package / subpackage of existing -- state
which signals from the decision matrix drove the choice]
**New packages**: [None / list with target import-linter contract]
**Bounded context changes**: [None / describe]
**Import-linter contract updates**: [None / show proposed TOML]
**Subdomain classification**: [Core / Supporting / Generic]
**New domain terms**: [None / term: definition]
```

For import-linter contract details, see the reference at
`.agents/skills/spec-kit/references/import-linter.md`.

## Plan Rules

1. Every phase has: Goal, TDD approach, Deliverables, Verification command, Acceptance Gate.
2. Verification must be a runnable command (`.venv\Scripts\activate; python -m ...`).
3. Acceptance Gates are hard pass/fail stops. The next phase MUST NOT start until both
   acceptance gate items are checked off.
4. Every phase MUST end with working, runnable code. Stubs, pseudocode, or placeholder
   implementations are NOT permitted as phase deliverables.
5. If a phase modifies or introduces any function file, running pytest on the affected
   test modules is a mandatory gate item.
6. All new or modified functions MUST be written test-first (Red -> Green -> Refactor)
   following the `test-driven-development` skill.
7. File Inventory lists every new and deleted file, grouped by phase.
8. Design Decisions table captures choices with rationale (not just the choice).
9. Domain model sketches include module path, class name, and key fields.
10. Write for the uninitiated: every **problem-domain** term or acronym that appears in the
    plan MUST be defined in a `## Glossary` section at the end of the file. Problem-domain
    terms are concepts from the business or analytical domain the project is solving (e.g.
    "skeleton", "GIR", "acceptance criteria"). Technical stack terms (pytest, Pydantic,
    import-linter, uv, etc.) do not belong in the Glossary. The plan body must expand
    domain acronyms on first use and state why a decision matters before stating what it is.

## Task Rules

1. Task IDs are globally sequential (T001 through TXXX) -- no resets per phase.
2. Every task has: checkbox + ID + phase label + file path.
3. TDD is mandatory for function work: write the failing test first, confirm it
   fails, implement to green, then refactor.
4. Every phase that touches function files MUST include an Acceptance Gate with a
   pytest task. The Gate is a hard stop.
5. Use `[P]` only when tasks are truly independent (different files, no data dependency).
6. Commit after each task or logical group.

## Analyze Rules

1. Read-only -- never modify any file.
2. Run 6 detection passes: Duplication, Ambiguity, Underspecification, Skill alignment,
   Coverage gaps, Inconsistency. Max 30 findings.
3. Severity levels: CRITICAL, HIGH, MEDIUM, LOW.
4. After reporting, offer: "Want me to suggest fixes for the top N issues?"

## Incremental Analysis (between artifacts)

Do NOT write all three artifacts (spec, plan, tasks) and then analyze. Instead,
validate each artifact against its predecessors before writing the next:

1. **After spec**: Analyze spec against the source document(s) and reconciliation
   table. Fix CRITICAL and HIGH issues before writing the plan.
2. **After plan**: Analyze plan against the spec. Check that every spec scenario
   maps to a plan phase, design decisions are consistent with requirements, and
   domain models match. Fix issues before writing tasks.
3. **After tasks**: Run the full 6-pass analysis across all three artifacts plus
   the source document. This is the final consistency gate.

This catches drift early: a naming convention error in the spec is fixed before it
proliferates into the plan and tasks, instead of requiring cascading fixes across
all three files.

## Implement Phase

When executing the plan:

1. Use `subagent-driven-development` skill (preferred) or execute tasks directly.
2. Follow each task exactly as specified.
3. Run `python-static-checks` before declaring implementation complete.
4. Use `finishing-a-development-branch` skill to complete the work.

## Relationship to Other Skills

| Skill                        | Relationship                                                    |
| ---------------------------- | --------------------------------------------------------------- |
| `brainstorming`              | Transitions to `spec-kit` as terminal state                     |
| `test-driven-development`    | Tasks enforce test-first order                                  |
| `python-domain-modeling`     | Spec-template references entity/VO conventions (tactical DDD)   |
| `python-class-design`        | Plan-template references architectural decisions                |
| `python-static-checks`       | Run before declaring implement complete                         |
| `subagent-driven-development`| Preferred execution mode for implement phase                    |
| `finishing-a-development-branch` | Terminal step after implement phase                          |
| `verification-before-completion` | Gates completion claims on fresh verification               |
| `mermaid-diagrams`           | pipeline-diagram.md and class-diagram.md (plan phase)           |

## Constraints

- Output location: `specs/<NNN>-<feature-slug>/` (auto-numbered by spec-kit).
  Spec files: `specs/001-feature-name/spec.md`, `plan.md`, `tasks.md`.
  Design docs from brainstorming: `specs/YYYY-MM-DD-<topic>-design.md`.
- All artifacts are plain markdown -- no tooling dependencies beyond spec-kit CLI.
- Do not duplicate project principles already captured in other skills. Reference them.
- Use RFC-2119 language (MUST, SHOULD, MAY) for requirements.
- Never use emoji or unicode that emulates emoji.
- Spec-kit's agent templates in `.github/agents/` and prompt templates in `.github/prompts/`
  are the canonical implementation. The skill file orchestrates setup and workflow order only.
