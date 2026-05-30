# Framework Analysis: Superpowers vs. Spec-Kit

**Date:** 2026-05-30  
**Scope:** obra/superpowers and github/spec-kit only. Custom Redline skills are out of scope.  
**Purpose:** Diagnose redundancy and contradiction, identify contract boundaries, and propose reconciliation strategies.

---

## 1. Skill Area Map

| Skill Area | Superpowers | Spec-Kit |
|---|---|---|
| **Ideation & Requirements Discovery** | `brainstorming` — Socratic, agent-led dialogue to refine rough ideas through questions; explores alternatives; produces a saved design document | `speckit.specify` — Template-driven conversion of a user prompt into a structured PRD (user stories, acceptance criteria, `[NEEDS CLARIFICATION]` markers)<br>`speckit.clarify` — Follow-up pass to resolve ambiguities in an existing spec before planning begins |
| **Project Governance & Principles** | _(none — philosophy is implicit in skill frontmatter, not a separate artifact)_ | `speckit.constitution` — Creates an explicit, versioned governance document encoding project principles, architectural articles, and amendment process |
| **Architecture & Implementation Planning** | `writing-plans` — Decomposes approved design into bite-sized tasks (2–5 min each); each task carries exact file paths, complete code snippets, and verification steps | `speckit.plan` — Produces a high-level architectural plan: tech stack, constitutional compliance checks (Articles VII, VIII, IX), data models, API contracts, research notes<br>`speckit.tasks` — Derives an executable `tasks.md` from `plan.md`; marks parallelisable tasks `[P]` |
| **Agentic Execution** | `subagent-driven-development` — Dispatches a fresh subagent per task; two-stage review (spec compliance → code quality) after each task<br>`executing-plans` — Batch execution with human checkpoints at configurable intervals<br>`dispatching-parallel-agents` — Concurrent subagent workflows for independent tasks | `speckit.implement` — Executes all tasks in `tasks.md` sequentially; single-agent, no built-in two-stage review<br>`speckit.taskstoissues` — Converts `tasks.md` into GitHub Issues for team-tracked execution outside the agent |
| **Test-Driven Development** | `test-driven-development` — Standalone skill; enforces strict RED→GREEN→REFACTOR cycle; deletes code written before tests; includes anti-patterns reference | _(no standalone TDD skill — TDD is Constitution Article III: "All implementation MUST follow strict Test-Driven Development"; enforced at plan-generation time via Phase -1 gates and file-creation ordering in templates)_ |
| **Quality Assurance & Specification Review** | `requesting-code-review` — Pre-review checklist; reviews against plan; critical issues block progress<br>`receiving-code-review` — Structured process for responding to reviewer feedback; includes GitHub thread reply guidance<br>`verification-before-completion` — Requires running verification commands and confirming output before claiming anything "done" | `speckit.analyze` — Cross-artifact consistency and coverage analysis across `spec.md`, `plan.md`, and `tasks.md`; runs after tasks, before implement<br>`speckit.checklist` — Generates custom quality checklists for requirements completeness, clarity, and consistency ("unit tests for English") |
| **Debugging** | `systematic-debugging` — 4-phase root-cause process; includes root-cause-tracing, defense-in-depth, and condition-based-waiting techniques | _(none)_ |
| **Version Control & Branch Management** | `using-git-worktrees` — Creates isolated workspace on a new branch after design approval; runs project setup; verifies clean test baseline<br>`finishing-a-development-branch` — End-of-task verification; presents merge/PR/keep/discard options; cleans up worktree | _(branch creation is a side-effect of `speckit.specify`, which auto-generates a semantic branch name from the feature description and creates `specs/<NNN-branch-name>/`; no explicit branch lifecycle skill)_ |
| **Framework Extensibility & Meta** | `writing-skills` — Skill for creating new SKILL.md files following Superpowers conventions; includes testing methodology<br>`using-superpowers` — Introduction to the skills system; entry-point for the agent | Extensions — New commands and templates added via `extension.yml` manifest; installed via `specify extension add`<br>Presets — Template/terminology overrides for core and extensions; stacked with priority ordering<br>Project-local overrides — One-off adjustments in `.specify/templates/overrides/` |

---

## 2. Overlap, Redundancy, and Contradiction Analysis

### 2.1 Ideation / Discovery

**Overlap:** Both frameworks have a structured pre-code design phase.

| Dimension | Superpowers `brainstorming` | Spec-Kit `speckit.specify` + `speckit.clarify` |
|---|---|---|
| Trigger | Automatic (agent detects "building something") | Explicit slash command |
| Method | Socratic conversation; agent asks questions iteratively | Template fills a PRD with forced `[NEEDS CLARIFICATION]` markers |
| Output artifact | Free-form design document (location agent-decided) | `specs/NNN-branch-name/spec.md` with structured sections |
| Branch creation | Handled separately by `using-git-worktrees` | Automatic inside `speckit.specify` |

**Contradiction:** If both are active, the agent may run `brainstorming` first (automatic), produce a conversational design doc, then a user invokes `/speckit.specify` producing a parallel `spec.md`. There is now **no declared source of truth**. The two artifacts may diverge silently.

**Redundancy severity:** High — both solve the same problem (structured pre-code thinking) for the same actor.

---

### 2.2 Architecture & Implementation Planning

**Overlap:** Both decompose approved requirements into tasks.

| Dimension | Superpowers `writing-plans` | Spec-Kit `speckit.plan` + `speckit.tasks` |
|---|---|---|
| Level of abstraction | Concrete micro-tasks (2–5 min, file paths + code) | Macro plan first (architecture, constitutional gates), then task list |
| Output location | Agent-chosen file in project root or memory | `specs/NNN/plan.md` and `specs/NNN/tasks.md` |
| Parallelism marking | Not standard | `[P]` markers in `tasks.md` |
| Constitutional compliance | None | Embedded Phase -1 gates (Simplicity, Anti-Abstraction, Integration-First) |

**Contradiction:** Two competing task files in different locations with different formats. `subagent-driven-development` reads the Superpowers plan; `speckit.implement` reads `tasks.md`. An agent asked to "execute the plan" has ambiguous input.

**Redundancy severity:** High — both solve task decomposition, with different depth and artifact contract.

---

### 2.3 Agentic Execution

**Overlap:** Both provide a mechanism to execute tasks with an AI agent.

| Dimension | Superpowers `subagent-driven-development` | Spec-Kit `speckit.implement` |
|---|---|---|
| Review per task | Two-stage (spec compliance → code quality) | None built in |
| Subagent isolation | Yes — fresh subagent per task | No — single-agent sequential |
| Input | Superpowers plan file | `specs/NNN/tasks.md` |
| Human checkpoints | Yes (`executing-plans`) | No |

**Contradiction:** These are mutually incompatible execution models consuming different inputs. Using both would require maintaining two task files in sync.

**Redundancy severity:** High — direct execution conflict.

---

### 2.4 Test-Driven Development

**Overlap:** Both require TDD.

| Dimension | Superpowers `test-driven-development` | Spec-Kit Constitution Article III |
|---|---|---|
| Enforcement mechanism | Standalone active skill; deletes pre-test code | Template gates and file-creation ordering inside `speckit.plan` and `speckit.tasks` |
| Scope | Runtime (during implementation) | Design-time (baked into plan and task templates) |
| RED phase verification | Explicit — agent must watch tests fail | Implied — not enforced at runtime |

**Assessment:** These are **complementary**, not contradictory. Spec-Kit bakes TDD into artifact design; Superpowers enforces it at runtime. Using both strengthens the guarantee. No conflict, but there is semantic duplication in documentation that could confuse new team members.

---

### 2.5 Quality Assurance & Review

| Dimension | Superpowers | Spec-Kit |
|---|---|---|
| Scope | **Code** quality (post-implementation review against plan) | **Artifact** quality (spec ↔ plan ↔ tasks consistency) |
| Timing | Between implementation tasks | After `speckit.tasks`, before `speckit.implement` |

**Assessment:** These operate on different objects at different lifecycle stages. **No redundancy, no contradiction.** Natural handoff: Spec-Kit `speckit.analyze` before execution; Superpowers `requesting-code-review` after each task.

---

### 2.6 Version Control & Branch Management

**Overlap:** Both manage branches, with different scope.

| Dimension | Superpowers | Spec-Kit |
|---|---|---|
| Branch creation | `using-git-worktrees` (isolated worktree, after design approval) | Auto-created inside `speckit.specify` (semantic name from feature description) |
| Branch naming | Agent-decided or user-specified | `NNN-kebab-feature-name` |
| Branch close | `finishing-a-development-branch` (explicit merge/PR/discard) | No equivalent |

**Contradiction:** `speckit.specify` creates a branch with Spec-Kit's naming convention. `using-git-worktrees` creates a separate worktree for execution. Running both creates **two branches/worktrees** for the same feature with different names. The Superpowers worktree diverges from the Spec-Kit branch.

**Redundancy severity:** Medium — partial overlap; Superpowers handles full lifecycle, Spec-Kit only handles creation.

---

### 2.7 Framework Extensibility

| Dimension | Superpowers `writing-skills` | Spec-Kit Extensions / Presets |
|---|---|---|
| Extension format | `SKILL.md` with YAML frontmatter | `extension.yml` manifest + `commands/*.md` templates |
| Discovery | File-system scan by the agent | `specify extension search` / catalog |
| Scope | Agent behaviour | CLI commands + prompt templates |
| Composability | Skills compose via frontmatter `triggers` | Extensions stack via priority ordering |

**Assessment:** Structurally incompatible but non-overlapping in scope. Superpowers skills modify agent reasoning; Spec-Kit extensions add new CLI commands. A Redline custom skill and a Spec-Kit extension are different things and can coexist, but there is no bridge between the two extension models — a capability added as a Superpowers skill is invisible to `specify extension search`, and vice versa.

---

## 3. Summary Diagnostic Table

| Skill Area | Conflict Type | Severity |
|---|---|---|
| Ideation & Discovery | Source-of-truth ambiguity (two artifact formats) | High |
| Planning / Task Decomposition | Competing task files and task formats | High |
| Agentic Execution | Mutually incompatible execution models | High |
| TDD Enforcement | Semantic duplication, complementary in practice | Low |
| Quality / Review | No overlap, complementary | None |
| Version Control | Dual branch creation, lifecycle gap in Spec-Kit | Medium |
| Debugging | Superpowers-only, no Spec-Kit equivalent | Gap (not conflict) |
| Governance / Constitution | Spec-Kit-only, no Superpowers equivalent | Gap (not conflict) |
| Extensibility | Structurally incompatible, non-overlapping scope | Low |

---

## 4. Reconciliation Strategies

The core problem is that both frameworks assume they own the **design → plan → execute** pipeline. The reconciliation goal is to assign each framework a non-overlapping zone of authority.

### 4.1 Recommended Partition: Spec-Kit as Artifact Layer, Superpowers as Execution Layer

Assign phases to frameworks based on their comparative strengths:

| Phase | Owner | Rationale |
|---|---|---|
| Discovery → Spec | **Spec-Kit** (`speckit.specify`, `speckit.clarify`) | Template-driven quality, structured PRD, branch auto-creation, `[NEEDS CLARIFICATION]` enforcement |
| Spec → Architecture Plan | **Spec-Kit** (`speckit.plan`) | Constitutional gates, data models, API contracts, research docs |
| Plan → Task List | **Spec-Kit** (`speckit.tasks`) | `[P]` parallelism, constitutional compliance trace |
| Pre-execution QA | **Spec-Kit** (`speckit.analyze`, `speckit.checklist`) | Artifact consistency before code is written |
| Task Execution | **Superpowers** (`subagent-driven-development`) | Two-stage review per task, subagent isolation, human checkpoints — reading from `specs/NNN/tasks.md` |
| TDD Enforcement | **Superpowers** (`test-driven-development`) | Runtime RED-GREEN-REFACTOR enforcement during execution |
| Post-task Code Review | **Superpowers** (`requesting-code-review`, `receiving-code-review`) | Code quality against the plan |
| Debugging | **Superpowers** (`systematic-debugging`, `verification-before-completion`) | No Spec-Kit equivalent |
| Branch Lifecycle | **Spec-Kit** creates (via `speckit.specify`) + **Superpowers** closes (via `finishing-a-development-branch`) | Eliminates dual-branch problem; Superpowers `using-git-worktrees` is **suppressed** in favour of Spec-Kit branch |
| Governance | **Spec-Kit** (`speckit.constitution`) | No Superpowers equivalent |

**Key contracts this partition requires:**

1. `subagent-driven-development` MUST read from `specs/NNN/tasks.md`, not a Superpowers plan file. This requires overriding the skill's input reference via a Redline custom skill or Superpowers `writing-skills`.
2. `brainstorming` MUST be disabled or explicitly positioned as a *pre-specify* warm-up only (not a substitute for `speckit.specify`). Add a trigger guard that routes to `speckit.specify` at the end.
3. `using-git-worktrees` MUST be suppressed when Spec-Kit is active. Override with a stub that reads the branch name from `specs/` instead of creating a new worktree.

---

### 4.2 Spec-Kit Extension: Superpowers Execution Bridge

Create a Spec-Kit extension (`redline-superpowers-bridge`) that overrides `speckit.implement` to delegate to Superpowers `subagent-driven-development`:

```
.specify/
  extensions/
    redline-superpowers-bridge/
      extension.yml
      commands/
        speckit.implement.md   # Override: calls subagent-driven-development
                               #            reading specs/NNN/tasks.md
```

This wires Superpowers' superior execution model (two-stage review, subagent isolation) into Spec-Kit's structured lifecycle, without forking either framework.

---

### 4.3 Superpowers Skill Overrides

Use Superpowers' `writing-skills` mechanism to create Redline-local overrides:

| Superpowers Skill | Override Behaviour |
|---|---|
| `brainstorming` | Append: "Output feeds into `/speckit.specify`; do not produce a standalone design doc." |
| `writing-plans` | Replace with stub: "Plans are produced by `speckit.plan` + `speckit.tasks`; invoke those instead." |
| `executing-plans` | Replace with stub: "Execution is handled by `subagent-driven-development` reading `specs/NNN/tasks.md`." |
| `using-git-worktrees` | Replace with stub: "Branch is created by `speckit.specify`; use that branch rather than a new worktree." |

These overrides live in `.agents/skills/` (Redline's custom skills layer) and take precedence over upstream Superpowers skills via the agent's file resolution order.

---

### 4.4 Explicit Non-Negotiable Boundaries (Contract Summary)

| Boundary | Rule |
|---|---|
| Single source of truth for requirements | `specs/NNN/spec.md` owns requirements. The Superpowers design document is a scratch artefact only. |
| Single source of truth for tasks | `specs/NNN/tasks.md` owns the task list. No parallel Superpowers plan file. |
| Single branch per feature | Created by `speckit.specify`. Superpowers worktrees are not used. |
| TDD enforcement | Superpowers `test-driven-development` skill is active during execution; Spec-Kit constitution sets the policy. |
| Execution model | `subagent-driven-development` only; `speckit.implement` is overridden via the bridge extension. |
| Artifact QA | `speckit.analyze` runs before any execution starts; Superpowers `verification-before-completion` runs after. |

---

## 5. Open Questions for Brainstorm Session

1. **Brainstorming suppression**: Should `brainstorming` be fully disabled, redirected to warm up `speckit.specify`, or kept as an optional pre-step for complex ideation before any specifying begins?

2. **Worktree strategy**: Spec-Kit branches live inside the main working tree. Superpowers worktrees isolate work in separate directories. Do we want that isolation, and if so, how do we reconcile it with Spec-Kit's `specs/NNN/` directory assumption?

3. **Receiving-code-review gap**: Spec-Kit has no equivalent for `receiving-code-review`. Is this acceptable (out of Spec-Kit's scope), or should it be added as an extension?

4. **Constitution vs. AGENTS.md**: Spec-Kit's `speckit.constitution` produces a `memory/constitution.md`; Redline's `AGENTS.md` already encodes many of the same principles. How do we prevent dual governance documents from drifting apart?

5. **Extension vs. skill for the bridge**: Should the Superpowers execution bridge be implemented as a Spec-Kit extension (modifying `speckit.implement`) or as a Superpowers skill override (modifying `subagent-driven-development` input source)? The answer depends on which framework "owns" the execution phase contract.
