# Spec-Kit Command — Acceptance Scenarios

Acceptance criteria for `/spec-kit`. Each scenario is a test case.
The command passes if, given the stated state and input, it produces the stated behaviour.

## Filesystem State Definitions

| State label | Condition |
|---|---|
| `bare` | `.specify/` does not exist |
| `ready` | `.specify/` exists, no in-progress spec dirs in `specs/` |
| `specifying` | `specs/NNN-feature/spec.md` exists AND contains `[NEEDS CLARIFICATION]` |
| `specified` | `specs/NNN-feature/spec.md` exists, clean (no `[NEEDS CLARIFICATION]`) |
| `planned` | spec.md + plan.md exist, tasks.md absent |
| `tasked` | spec.md + plan.md + tasks.md exist, analyze not yet run this session |
| `complete` | All three docs exist, analyze done |

"In-progress" means any spec dir where tasks.md is absent or analyze has not been run.

---

## Scenarios

### S01 — Cold start, no args
- **State**: bare
- **Input**: `/spec-kit`
- **Expected**: Run setup silently. Ask: "What feature are you working on? Describe it or paste a rough idea." If the description is vague → offer brainstorm mode. If clear → run specify.

### S02 — Named feature, bare state
- **State**: bare
- **Input**: `/spec-kit my-feature`
- **Expected**: Run setup silently. Ask: "Describe my-feature — what problem does it solve and what does success look like?" Run specify with answer as input.

### S03 — Brainstorm entry point, bare state
- **State**: bare or ready
- **Input**: `/spec-kit brainstorm`
- **Expected**: Run setup if needed. Load brainstorming skill. On completion ask: "Ready to create the spec from this? (yes/no)." If yes → run specify using brainstorm output. If no → stop.

### S04 — Doc as input
- **State**: bare or ready
- **Input**: `/spec-kit specs/2026-04-11-spec-kit-skill-design.md`
- **Expected**: Detect arg is a .md path. Run setup if needed. Read doc. Run specify using doc content as input.

### S05 — Auto-detect, needs clarification
- **State**: specifying
- **Input**: `/spec-kit`
- **Expected**: Identify in-progress spec. Surface each `[NEEDS CLARIFICATION]` as a direct question to the user. Wait for answers. Run clarify. Re-check spec. Repeat until clean.

### S06 — Auto-detect, clean spec, no plan
- **State**: specified
- **Input**: `/spec-kit`
- **Expected**: Identify in-progress spec. Run incremental analysis (spec vs source). Fix CRITICAL/HIGH findings. Run plan.

### S07 — Auto-detect, has plan, no tasks
- **State**: planned
- **Input**: `/spec-kit`
- **Expected**: Identify in-progress spec. Run incremental analysis (plan vs spec). Fix CRITICAL/HIGH. Run tasks.

### S08 — Auto-detect, has tasks, no analyze
- **State**: tasked
- **Input**: `/spec-kit`
- **Expected**: Identify in-progress spec. Run 6-pass analyze. Report findings. Ask: "Want fixes for the top N issues?" STOP. Do not implement.

### S09 — All complete
- **State**: complete
- **Input**: `/spec-kit`
- **Expected**: Report "Spec complete." List output docs. Print handoff line. STOP.

### S10 — Jump to plan, spec missing
- **State**: ready (no spec.md)
- **Input**: `/spec-kit plan`
- **Expected**: Error — "No spec.md found for this feature. Run `/spec-kit` to create one first." Offer to start.

### S11 — Jump to plan, spec clean
- **State**: specified
- **Input**: `/spec-kit plan`
- **Expected**: Validate spec.md exists and is clean. Skip to plan step. Run plan.

### S12 — Multiple in-progress specs
- **State**: two or more spec dirs with incomplete docs
- **Input**: `/spec-kit`
- **Expected**: List in-progress specs with their state label. Ask: "Which one?" Do not proceed until user selects one.

### S13 — Named feature + brainstorm
- **State**: bare or ready
- **Input**: `/spec-kit brainstorm my-feature`
- **Expected**: Load brainstorming skill with "my-feature" as the topic. On completion, confirm before proceeding to specify.

### S14 — Named feature, already complete
- **State**: complete
- **Input**: `/spec-kit my-feature`
- **Expected**: Report state is complete. List docs. Ask: "Do you want to re-run a step or start a new feature?"

---

## Terminal State Contract

The command MUST stop after `analyze` completes. It MUST NOT:
- Invoke `speckit.implement`
- Invoke Kabilan
- Write any source code files
- Modify files outside `specs/NNN-feature/` and `.specify/`

Required output at terminal state:

```
Spec complete. Docs:
  specs/NNN-feature/spec.md
  specs/NNN-feature/plan.md
  specs/NNN-feature/tasks.md

Next: "Kabilan, implement specs/NNN-feature/tasks.md"
```

---

## Invariants (hold across all scenarios)

1. Never proceed past an ambiguous state without asking the user.
2. Never run `speckit.implement`. No exceptions.
3. Incremental analysis runs after specify AND after plan — not only at the end.
4. Clarification questions are batched per step (one ask, not one per marker).
5. Setup (`.specify/` init, preset install) runs silently without user confirmation.
6. Architecture question (monorepo vs single-package) is asked exactly once, on first setup only.
