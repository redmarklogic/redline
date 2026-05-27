# ADR-012: `.agents/` as Primary Agent Customisation Home

## Summary

The `.agents/` directory at the repository root is the single authoritative location for
all agent customisations in this project: skills, tools, and evaluations. Two AI agents are
supported — Claude Code (primary) and GitHub Copilot in VS Code (secondary). `AGENTS.md` at
the repo root is the canonical always-on instruction file; `CLAUDE.md` at the repo root
bridges Claude Code to `AGENTS.md` via import. `.github/copilot-instructions.md` MUST NOT
exist — it would duplicate `AGENTS.md` and violate ADR-001. The `.claude/rules/` directory
is allowed for path-scoped rules that both tools recognise (accepted 2026-05-26).

**Status**: Accepted
**Date**: 2026-05-26
**Deciders**: Peter (architecture), Kabilan (engineering)

---

## Decision

The `.agents/` directory is the single authoritative location for all agent customisations.
`AGENTS.md` at the repository root is the canonical always-on instruction file. `CLAUDE.md`
at the repository root imports `AGENTS.md` so that Claude Code reads the same instructions
without duplication.

---

## Context

This project uses two AI agents:

- **Claude Code** (primary): Anthropic's agentic coding tool. Its primary instruction file
  is `CLAUDE.md` at the project root. It does not read `AGENTS.md` natively, but supports
  `@path/to/file` imports within `CLAUDE.md`, allowing it to consume `AGENTS.md` without
  duplication.

- **GitHub Copilot in VS Code** (secondary): Microsoft/GitHub's IDE agent. It reads
  `AGENTS.md` at the project root as always-on instructions. It also reads `CLAUDE.md` and
  `.claude/rules/*.md`, so shared locations work for both tools.

Skills were already organised under `.agents/skills/`, which is an officially supported
project-level location per the [agentskills.io](https://agentskills.io/) open standard.

**Terminology — two entirely separate "hooks" systems in this repo**

| Name | Location | When it runs | Run by |
|---|---|---|---|
| Pre-commit checks | `hooks/*.py` | At `git commit` | pre-commit framework |
| Agent lifecycle hooks | `.agents/hooks/` | During AI agent sessions | VS Code / GitHub Copilot |

"Hooks" without qualification in this codebase refers to pre-commit checks. "Agent lifecycle
hooks" always refers to `.agents/hooks/`. See ADR-011.

**Customisation file locations for each tool**

| File / Directory | Claude Code | GitHub Copilot (VS Code) | Notes |
|---|---|---|---|
| `AGENTS.md` (root) | Via `@AGENTS.md` import in `CLAUDE.md` | Always-on instructions | Canonical instruction file |
| `CLAUDE.md` (root) | Always-on instructions | Always-on instructions | Bridge file; must import `@AGENTS.md` |
| `.agents/skills/` | Via skill invocation | Via skill invocation | Authoritative skill location |
| `.agents/tools/` | Tool definitions | Tool definitions | Authoritative tool location |
| `.agents/evals/` | Evaluation harnesses | Evaluation harnesses | Authoritative eval location |
| `.agents/hooks/` | Not loaded | Agent lifecycle hooks (VS Code) | Lifecycle hooks only |
| `.claude/rules/*.md` | Path-scoped rules | Path-scoped rules | Shared rule location |
| `.github/instructions/*.instructions.md` | Not loaded | Path-scoped instructions | Copilot-only; use `.claude/rules/` for shared rules |
| `.github/copilot-instructions.md` | **FORBIDDEN** | **FORBIDDEN** | Would duplicate `AGENTS.md` — SSOT violation |

**Forbidden paths**

Two artefacts MUST NOT be created:

- `.github/copilot-instructions.md` — duplicates `AGENTS.md`. This project uses `AGENTS.md`
  as the canonical instruction file. Creating a separate `copilot-instructions.md` splits the
  source of truth and violates ADR-001.

- `.claude/settings.json` for agent lifecycle hook configuration — agent lifecycle hooks are
  configured via `.agents/hooks/hooks.json` loaded by VS Code. Claude Code's
  `.claude/settings.json` format serves a different purpose (permissions, tool restrictions)
  and must not be used for hook configuration.

---

## Options Considered

- **Option A — `CLAUDE.md` as primary instruction file, `AGENTS.md` removed.** Rejected:
  `AGENTS.md` is the cross-agent standard recognised by the broadest set of tools (GitHub
  Copilot, GitHub cloud agent, Gemini, and others). Replacing it with `CLAUDE.md` would
  reduce portability and would be a step backwards for GitHub Copilot support.

- **Option B — `.claude/` as the primary customisation home.** Rejected: `.agents/` is
  already established as the skill and tool home, and it is the authoritative location per
  the agentskills.io open standard. Moving to `.claude/` would require migrating all existing
  skills and tools and would create a location inconsistency between skills and hooks.

- **Option C — `AGENTS.md` as canonical instruction file; `CLAUDE.md` imports it; `.agents/`
  for skills/tools/evals (chosen).** Accepted: SSOT is maintained in `AGENTS.md`; Claude
  Code reads the same content via import; VS Code Copilot reads `AGENTS.md` natively; no
  duplication. The `.claude/rules/` directory is available as a shared zone for path-scoped
  rules when needed.

---

## Decision Rationale

`AGENTS.md` already contains the authoritative, detailed project instructions for all agents.
It is read natively by GitHub Copilot and recognised by the widest set of AI coding tools.
Claude Code's import mechanism (`@AGENTS.md` in `CLAUDE.md`) allows it to consume the same
content without duplication — satisfying ADR-001. The `.agents/` directory is the established
home for skills and tools; extending it to evaluations is consistent with that convention.

---

## Consequences

- `CLAUDE.md` at the repository root must exist and must begin with `@AGENTS.md` so that
  Claude Code reads all project instructions. Additional Claude-specific guidance may follow
  the import.

- `.github/copilot-instructions.md` MUST NOT be created. Any write to this path is a SSOT
  violation (ADR-001). If an enforcement hook is added in the future, it should reference this
  ADR (ADR-012) in its error output per ADR-011 P6.

- `.claude/settings.json` must not be used for agent lifecycle hook configuration. Lifecycle
  hooks belong in `.agents/hooks/hooks.json`.

- Path-scoped rules that should apply to both Claude Code and GitHub Copilot go in
  `.claude/rules/`. Rules that apply only to GitHub Copilot may go in
  `.github/instructions/`. Do not duplicate rules across both locations.

- `.agents/skills/` remains the authoritative skill location. The agentskills.io naming
  convention applies.

---

## References

- [ADR-001](adr-001-single-source-of-truth.md) — Single Source of Truth (grounds the
  prohibition on `copilot-instructions.md` as a duplicate of `AGENTS.md`)
- [ADR-010](adr-010-dependency-inversion-principle-for-skills-agents-boundary.md) — Dependency
  Inversion for Skills/Agents Boundary (skills must not reference agent names)
- [ADR-011](adr-011-hook-first-enforcement.md) — Hook-first Enforcement (hooks terminology;
  P6 requirement that enforcement hooks reference their governing ADR)
- [Claude Code memory docs](https://code.claude.com/docs/en/memory) — `CLAUDE.md` file
  locations, `@import` syntax, and `.claude/rules/` path-scoped rules
- [VS Code Copilot customisation docs](https://code.visualstudio.com/docs/copilot/customization/custom-instructions) — `AGENTS.md`, `CLAUDE.md`, and `.claude/rules/` support in VS Code
