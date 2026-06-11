# Spec-Kit Implement

Entry point for the implement phase of a completed Spec-Kit feature.
Handles branch setup then delegates implementation to Kabilan.

**Prerequisite: `/spec-kit` must have reached `complete` state first.**

---

## Phase 0 — Identify the Target Feature

1. If a feature name or `specs/NNN-feature/` path was given → use it.
2. Otherwise scan `specs/` for dirs where `tasks.md` exists and `analyze` has been completed (state: `complete`):
   - **None**: stop — "No completed spec found. Run `/spec-kit` first."
   - **Exactly one**: confirm the name, continue.
   - **Two or more**: list them, ask "Which one?"

Do not guess. If uncertain, ask.

---

## Phase 1 — Prerequisite Gate

Verify all three artifacts exist and are clean:

```powershell
Test-Path specs/NNN-feature/spec.md
Test-Path specs/NNN-feature/plan.md
Test-Path specs/NNN-feature/tasks.md
```

If any are missing: stop. Tell the user which doc is absent and offer to run `/spec-kit`.

Check `tasks.md` for any unchecked tasks — confirm this is a fresh implementation run, not a resume of partial work. If partial work exists, ask: "Tasks are partially complete. Resume from where you left off? (yes/no)"

Also check for existing commits on the branch:

```powershell
git log --oneline master..HEAD
```

If commits exist and the founder chose to resume, note this explicitly: "Resuming — branch has existing commits." If commits exist but the founder said no (fresh start), stop and warn: "Branch has existing commits. A fresh start would discard them. Confirm or switch to a clean branch."

---

## Phase 2 — Branch Setup

Load and run the `speckit.branching-strategy.run` command from the branching-strategy extension.

This fires the `before_implement` hook and creates the feature branch before any code is written.

---

## Phase 3 — Delegate to Kabilan

Hand off to Kabilan with:

- Path to `specs/NNN-feature/tasks.md`
- Feature name
- Current branch name (set in Phase 2)

> "Kabilan, implement `specs/NNN-feature/tasks.md`. Branch: `feature/NNN-feature-slug`."

Do not prescribe which skill Kabilan loads — his routing table governs that.

Do not write any code. Do not load the spec-kit implement phase directly.

---

## Terminal State

After Kabilan signals completion, output:

```text
Implementation complete.

Next steps:
  1. Run /make-pr
  2. Founder review before any push
```

Stop. Do not push. Do not merge.
