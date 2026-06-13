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
| `<github-issue-url>` | GitHub issue URL — derive branch name, use issue body as spec input |
| `<feature-name>` | Start or resume a named feature |
| `<path/to/doc.md>` | Use existing doc as spec input (arg contains `/` or ends in `.md`) |
| `plan` / `tasks` / `analyze` | Jump to a specific step (validates prerequisites first) |

When intent is ambiguous, **ask the user** before acting.

---

## Phase 0 — Identify the Target Feature

Determine which feature you are working on before any other action.

1. If the arg matches a GitHub issue URL (contains `github.com` and `/issues/`):

   ```powershell
   # Extract org/repo and issue number from the URL
   $issue = gh issue view <number> --repo <org/repo> --json number,title,body | ConvertFrom-Json
   $slug  = $issue.title.ToLower() -replace '[^a-z0-9]+', '-' -replace '^-|-$', ''
   $branch = "feature/$($issue.number)-$slug"
   $specDir = "specs/$($issue.number)-$slug"

   # Create and switch to the branch (from current HEAD if it doesn't exist yet)
   git checkout -b $branch 2>$null; if ($LASTEXITCODE -ne 0) { git checkout $branch }
   ```

   Store `$issue.body` as the spec input for Phase 3. Announce the branch name and spec directory (`$specDir`) to the user.

2. If a feature name, doc path, or `brainstorm` arg was given → use it.
3. Otherwise scan `specs/` for in-progress dirs (dirs where tasks.md is absent
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
| `no-spec` | spec.md does not exist in the target feature directory (`specs/<issue-number>-<slug>/` for GitHub issue URL flow; `specs/NNN-feature/` otherwise) |
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
2. GitHub issue body was captured in Phase 0 → use that.
3. Brainstorm produced output → use that.
4. User described the feature in conversation → extract requirements.
5. None of the above → ask: "Describe the feature. What problem does it solve and what does success look like?"

**Spec directory naming:**

- If `$specDir` was set in Phase 0 (GitHub issue URL flow): pass `SPECIFY_FEATURE_DIRECTORY=$specDir`
  in the speckit.specify invocation arguments. The agent will use this path as-is instead of
  auto-generating a sequence-numbered directory.
- Otherwise (feature name, doc path, or brainstorm flow): omit `SPECIFY_FEATURE_DIRECTORY` and
  let spec-kit auto-number the directory (`NNN-<short-name>`).

**Writing style (applies to spec.md):** Write spec.md in plain English for an
uninitiated reader — someone who has not seen the source issue or sat in the
discussion. Use flowing narrative prose, not terse fragments or note form, so the
document reads as a self-contained explanation of the problem, the users, and what
success looks like. The first time any acronym or abbreviation appears, write the
full term followed by the acronym in parentheses (for example, "Architecture
Decision Record (ADR)"), then use the short form thereafter. Define project- and
domain-specific terms on first use. See **Writing Style for Generated Documents** below.

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
  <feature-dir>/spec.md
  <feature-dir>/plan.md
  <feature-dir>/tasks.md

Next: "Kabilan, implement <feature-dir>/tasks.md"
```

Where `<feature-dir>` is the resolved feature directory (e.g., `specs/63-infra-adr-cloud-run` for a GitHub issue flow, or `specs/007-user-auth` for an auto-numbered flow).

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

## Writing Style for Generated Documents

These rules govern the prose in every document this command produces (spec.md,
plan.md, tasks.md). They override the compressed working style used elsewhere — the
generated documents are read by people who were not in the room.

- **Plain English, for the uninitiated.** Assume the reader has not seen the source
  issue, brainstorm, or conversation. Explain the problem and the solution from
  first principles. Avoid insider shorthand.
- **Expand acronyms on first use.** The first time an acronym or abbreviation appears
  in a document, write the full term with the acronym in parentheses — for example,
  "Test-Driven Development (TDD)" — then use the short form for the rest of that
  document. Define domain-specific jargon on first use.
- **Narrative in spec.md.** Write spec.md as flowing narrative prose. The problem
  statement, user context, and success criteria should read as connected paragraphs
  that tell a coherent story, not as disconnected bullet fragments. (plan.md and
  tasks.md may stay structured, but still expand acronyms and read clearly.)
- **Self-contained.** A reader should understand each document without needing the
  source issue or any prior context open beside it.

---

## Constraints

- Output location: `specs/<issue-number>-<slug>/` when started from a GitHub issue URL (derived from issue number and title); `specs/NNN-feature/` (auto-numbered by spec-kit CLI) for all other flows.
- Vendor-generated files in `.github/agents/` and `.github/prompts/` must not be edited manually.
- Extensions go in `.specify/extensions.yml`, not in vendor files.
- Never use emoji in any output or document.
