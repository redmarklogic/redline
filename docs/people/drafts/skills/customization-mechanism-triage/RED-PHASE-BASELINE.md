# RED-Phase Baseline — customization-mechanism-triage

**Date**: 2026-05-24
**Test type**: Baseline failure analysis (no triage skill loaded)
**Skill under test**: `customization-mechanism-triage`
**Subagent config**: Harriet persona with hard constraints active; no triage skill loaded

---

## Failure Mode 1 — VS Code hooks conflated with git pre-commit hooks

**Scenario**: "Add a skill to auto-run `ruff format` on every file after the agent edits it."

**Observed behaviour**: The subagent correctly rejected creating a skill. However, it
identified the right category as "pre-commit hook" (a *git* hook) rather than a
VS Code `PostToolUse` lifecycle hook (`.github/hooks/*.json`). These are different
mechanisms with different scopes:

- A **git pre-commit hook** runs before a git commit. It does not run after every
  file edit during an agent session.
- A **VS Code `PostToolUse` hook** runs after every tool invocation (including file
  edits) during an agent session, regardless of whether anything is committed.

**Without the triage skill**, agents know "automation → hook" but cannot distinguish
which hook system applies. The wrong implementation path is chosen even when the
correct category is identified.

**Correct behaviour**: Identify the VS Code `PostToolUse` hook as the mechanism and
direct to `.github/hooks/*.json`.

---

## Failure Mode 2 — Rule-only standard attributed to an existing skill rather than
                    identified as an instruction

**Scenario**: "Add a skill for enforcing that all Python files use Google-style docstrings."

**Observed behaviour**: The subagent avoided the failure by pointing to the existing
`python-documentation` skill rather than creating a duplicate. It did not identify the
underlying design issue: a rule-only coding standard with no procedure or scripts
belongs in a `.instructions.md` file (always-on, passively applied), not a skill
(loaded on-demand, procedure-oriented).

**The subagent dodged the failure but did not apply the correct triage.** The right
answer is: "This is a passive rule, not a procedure — use an `.instructions.md` file
with `applyTo: '**/*.py'`. The existing `python-documentation` skill may already cover
it; if not, the new rule goes in an instruction file, not a new skill."

**Without the triage skill**, agents either create duplicate skills or note the duplicate
without re-routing to the correct mechanism.

---

## Failure Mode 3 — Agent vs skill boundary is correctly identified ONLY when persona
                    constraints are active

**Scenario**: "Add a skill for a code reviewer persona that only reads files."

**Observed behaviour**: The subagent correctly identified this as a custom agent (`.agent.md`).
This test passed.

**Risk**: This correct identification depended on Harriet's hard constraints being
active. A neutral agent (no persona constraints) presented with the same request would
likely create a `SKILL.md` with "acting as a code reviewer" instructions, because
skills can contain persona-like instructions and there is no automatic signal directing
to the custom agent path. The triage skill is needed to provide that signal to neutral agents.

---

## Rationalization patterns observed

| Pressure | Observed rationalization | Triage skill must counter |
|---|---|---|
| Authority ("everyone uses skills") | "This should be a pre-commit hook" (right concept, wrong system) | Name VS Code hooks explicitly and distinguish from git hooks |
| Sunk cost (30 min research) | "The existing skill already covers it" (sidestep, not correct triage) | Drive to instruction files for rule-only content |
| Momentum (user said "yes") | Not observed — hard constraints blocked premature creation | Keep hard constraints binding; no "yes" overrides RED phase |
