# Spec-Kit

State-aware orchestrator for the GitHub Spec Kit workflow. Resumes from wherever
the current feature is in the pipeline. Creates spec, plan, and tasks documents.

**Hard stop: never runs speckit.implement, never invokes Kabilan, never writes code.**

Acceptance scenarios: `specs/spec-kit-command/scenarios.md`

---

## Argument Forms

| Arg | Meaning |
| --- | --- |
| (none) | Auto-detect state and resume |
| `brainstorm [topic]` | Start with brainstorming skill before specifying |
| `<feature-name>` | Start or resume a named feature |
| `<path/to/doc.md>` | Use existing doc as spec input (arg contains `/` or ends in `.md`) |
| `plan` / `tasks` / `analyze` | Jump to a specific step (validates prerequisites first) |

When intent is ambiguous, **ask the user** before acting.

---

## Phase 0 — Identify the Target Feature

Determine which feature you are working on before any other action.

1. If a feature name, doc path, or `brainstorm` arg was given → use it.
2. Otherwise scan `specs/` for in-progress dirs (dirs where tasks.md is absent
   OR analyze has not been completed):

   - **No in-progress specs**: ask — "What feature are you working on? Describe it or paste a rough idea." If the answer is vague or exploratory, offer brainstorm mode before proceeding to specify.
   - **Exactly one in-progress spec**: confirm the name, continue.
   - **Two or more in-progress specs**: list each with its state label (see State Table), ask "Which one?"

Do not guess. If uncertain, ask.

---

## State Table

Check conditions in order. First failing check is the current state.

| State | Condition |
| --- | --- |
| `no-setup` | `.specify/` directory does not exist |
| `no-spec` | `specs/NNN-feature/spec.md` does not exist |
| `needs-clarification` | spec.md exists AND contains `[NEEDS CLARIFICATION]` |
| `no-plan` | spec.md clean, `plan.md` absent |
| `no-tasks` | spec.md + plan.md exist, `tasks.md` absent |
| `no-analyze` | All three docs exist, analyze not yet completed this session |
| `complete` | All three docs exist, analyze done |

---

## Phase 1 — Environment Setup (state: no-setup)

Run silently. No user confirmation needed.

```powershell
# 1. Check CLI
specify version
# If not found:
rtk uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# 2. Init project
# If .specify/ does not exist:
specify init --here --ai copilot --script ps --force --no-git

# 3. Install preset
# If not in: specify preset list
specify preset add --dev .agents/skills/spec-kit/presets/
```

First-time only (no `src/` directory exists): ask the architecture question:

> **Will this project use a monorepo layout (multiple packages under `src/`) or a
> single package?**

Record the answer in `.specify/architecture.yml` as `layout: monorepo` or
`layout: single-package`. Skip if the file already exists.

Then advance to the next phase.

---

## Phase 2 — Brainstorm (brainstorm mode only)

Load the `brainstorming` skill. Work through it with the user.

When the brainstorm produces output:

- Summarise the constraints and the selected direction.
- Ask: "Ready to create the spec from this? (yes/no)"
- Yes → proceed to Phase 3 using brainstorm output as spec input.
- No → stop. Do not proceed.

---

## Phase 3 — Specify (state: no-spec)

Run `speckit.specify` using the installed agent template
(`.github/agents/speckit.specify.agent.md`).

Determine spec input — in priority order:

1. A `.md` doc path was given → read the doc, use its content.
2. Brainstorm produced output → use that.
3. User described the feature in conversation → extract requirements.
4. None of the above → ask: "Describe the feature. What problem does it solve and what does success look like?"

After specify completes:

**Incremental analysis — spec vs source:**

- Read the generated spec.md.
- Check the spec against any source document(s). Identify CRITICAL and HIGH findings.
- Report findings to the user and fix them before proceeding.

Then check for `[NEEDS CLARIFICATION]` markers:

- Found → proceed to Phase 4.
- Clean → proceed to Phase 5.

---

## Phase 4 — Clarify (state: needs-clarification)

Collect all `[NEEDS CLARIFICATION]` markers from spec.md. Batch them into a single
set of questions for the user. Wait for answers.

Run `speckit.clarify` (`.github/agents/speckit.clarify.agent.md`) with the answers.

Re-read spec.md. If `[NEEDS CLARIFICATION]` markers remain, repeat. Continue until clean.

Then proceed to Phase 5.

---

## Phase 5 — Plan (state: no-plan)

**Incremental analysis — spec integrity check:**

- Scan spec.md for any unresolved issues before writing the plan.
- Fix CRITICAL/HIGH findings. Do not skip this step.

Run `speckit.plan` (`.github/agents/speckit.plan.agent.md`).

The preset fills technical context automatically (Python 3.14, uv, pytest, layout from
architecture.yml, MoSCoW, Domain Impact). Minimal user input needed.

After plan completes:

**Incremental analysis — plan vs spec:**

- Verify every spec scenario maps to a plan phase.
- Fix CRITICAL/HIGH findings before proceeding.

Then proceed to Phase 6.

---

## Phase 6 — Tasks (state: no-tasks)

Run `speckit.tasks` (`.github/agents/speckit.tasks.agent.md`).

The preset enforces vertical-slice sizing and TDD task ordering automatically.

After tasks completes, proceed to Phase 7.

---

## Phase 7 — Analyze (state: no-analyze)

Run the 6-pass analysis across all three artifacts plus any source document:

1. Duplication
2. Ambiguity
3. Underspecification
4. Skill alignment
5. Coverage gaps
6. Inconsistency

Max 30 findings. Severity levels: CRITICAL, HIGH, MEDIUM, LOW.

Report findings. Ask: "Want me to suggest fixes for the top N issues?"

- Yes → apply fixes, re-run the relevant analysis pass.
- No → stop.

---

## Terminal State (state: complete)

Output this and stop:

```text
Spec complete. Docs:
  specs/NNN-feature/spec.md
  specs/NNN-feature/plan.md
  specs/NNN-feature/tasks.md

Next: "Kabilan, implement specs/NNN-feature/tasks.md"
```

**Do not call speckit.implement. Do not invoke Kabilan. Do not write any code.**

---

## Jump Mode

When the user provides a step name (`plan`, `tasks`, `analyze`):

1. Identify the target feature (Phase 0 rules apply).
2. Validate prerequisites:
   - `plan` → spec.md must exist and be clean.
   - `tasks` → spec.md + plan.md must both exist.
   - `analyze` → all three docs must exist.
3. Prerequisite missing → tell the user which doc is absent. Offer to run the missing step. Do not jump.
4. Prerequisites satisfied → jump to that phase.

---

## Clarification Rules

- Ask before starting if the feature is ambiguous.
- Ask when multiple in-progress specs exist.
- Ask for each `[NEEDS CLARIFICATION]` batch (one ask per clarify cycle, not one per marker).
- Ask the architecture question on first setup only.
- Do NOT ask about things the preset fills automatically (tech context, RICE, MoSCoW).
- Batch multiple questions into one ask per phase. Never ask one question at a time across multiple turns when they can be combined.

---

## Constraints

- Output location: `specs/NNN-feature/` (auto-numbered by spec-kit CLI).
- Vendor-generated files in `.github/agents/` and `.github/prompts/` must not be edited manually.
- Extensions go in `.specify/extensions.yml`, not in vendor files.
- Never use emoji in any output or document.
