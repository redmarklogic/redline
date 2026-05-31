---
name: adr-constitution-sync
description: Use when an ADR is added or amended -- determines whether .specify/memory/constitution.md needs updating and executes the sync procedure
---

# ADR -> Constitution Sync

## Boundary Contract

### Applies To
- Any newly accepted or amended ADR in `docs/adr/`

### Produces
- Updated `.specify/memory/constitution.md` (when the ADR carries cross-cutting
  implications)
- No change (when the ADR is implementation-specific, with explicit reasoning noted
  in the commit message)

### Does Not Cover
- Writing or amending ADRs (use `arch-engineering`)
- Deciding whether a new ADR is needed (architectural judgment, not this skill)

## When to Use

Load this skill when:
- A new ADR file is accepted in `docs/adr/`
- An existing ADR's status changes (Proposed -> Accepted, Accepted -> Deprecated)
- The `check-adr-constitution-sync` pre-commit hook blocks a commit with an ADR
  change

Do NOT load when:
- The ADR is implementation-specific (e.g. library selection for a single component)
  and establishes no cross-cutting principle
- The constitution already reflects the principle introduced by the ADR

## Cross-Cutting vs. Implementation-Only

An ADR warrants a constitution update if it establishes a rule that applies across
all features, not just the feature being built:

| ADR type | Constitution update? |
|---|---|
| Establishes a new SSOT boundary for a system-wide concern | Yes |
| Defines a new enforcement mechanism (hook, gate, lifecycle extension) | Yes |
| Changes the dependency direction rule for a layer | Yes |
| Selects a library for a single component with no architectural pattern | No |
| Adjusts a threshold or configuration value | No |
| Corrects a mistake in a prior ADR with no new rule introduced | No |

## Procedure

1. **Read the ADR** -- identify the Decision section and stated consequences.
2. **Apply the classification table above** -- cross-cutting or implementation-only?
3. **If implementation-only** -- record reasoning in the commit message and exit.
   Do not update the constitution.
4. **If cross-cutting** -- identify whether it amends an existing principle or
   warrants a new one:
   - **Amends existing**: patch the relevant principle section; update the
     *Grounded in* reference line.
   - **New principle**: add a numbered section under Core Principles following the
     pattern: title, 2-3 sentence statement, `*Grounded in ADR-NNN.*`
5. **Update the version metadata** -- bump the patch number and set *Last Amended*
   to today's date (the last line of constitution.md).
6. **Stage both files** -- constitution and ADR must be in the same commit.
   The `check-adr-constitution-sync` hook enforces this direction.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Updating the constitution for every ADR regardless of scope | Apply the classification table first; implementation-only ADRs belong in `docs/adr/`, not in the constitution |
| Writing a paragraph instead of 2-3 sentences | Principles are invariants, not explanations. Explanations live in the ADR body. |
| Forgetting to bump the version metadata | Check the last line of constitution.md before staging |
| Staging constitution without the ADR (or vice versa) | Both files must be in the same commit |

## Git Hook Enforcement

The `check-adr-constitution-sync` pre-commit hook (registered in `prek.toml`) blocks
commits that modify `docs/adr/adr-*.md` without also staging
`.specify/memory/constitution.md`. This is the deterministic enforcement layer
per ADR-011.
