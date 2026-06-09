# Redline Constitution

## Core Principles

### I. Single Source of Truth

For every well-defined concern, exactly one authoritative location exists. All other
locations import, derive, or query from it. Duplication of an authoritative artifact
-- by copy-paste, static snapshot, or parallel definition -- is a defect, not a
shortcut.

*Grounded in ADR-001.*

### II. Hook-First Enforcement

For every project rule that can be expressed as a deterministic pattern check, a
pre-commit hook is the required enforcement mechanism. An instruction in `AGENTS.md`
or a skill document alone is insufficient for architectural invariants. If it cannot
be expressed as an automated check, it is guidance, not a constraint.

*Grounded in ADR-011.*

### III. Defence-in-Depth (No Layer Substitutes for Another)

Git hooks (deterministic), agent instructions in `AGENTS.md` (probabilistic), and
spec-kit lifecycle extensions (probabilistic) coexist as independent enforcement
layers. Each layer catches failures the others miss. None substitutes for the others
-- adding a hook does not remove the obligation to document the rule in the governing
skill.

*Grounded in ADR-013.*

### IV. Dependency Direction: Skills Inward, Agents Outward

Skills are the stable inner core. Agent manifests are the volatile outer
orchestration layer. All dependencies point inward: agents may reference skills,
but skills must never reference agents by name. Violating this direction couples
stable abstractions to volatile personalities.

*Grounded in ADR-010.*

### V. Facade Boundaries -- Primitives Only Across Layers

Components communicate through stable protocol interfaces (Facades). Only primitive
types (`str`, `int`, `list[str]`) cross component boundaries. Domain objects,
Pydantic models, and enums are translated by the caller before they cross a boundary.
This preserves the ability to swap implementations without propagating changes inward.

*Grounded in ADR-002, ADR-004.*

### VI. Data-Driven Configuration Over Hard-Coded Logic

Variant behavior (jurisdiction, report type, company convention) is captured in
explicit data objects, not in conditional branches or hard-coded constants. Each
variation produces a distinct configuration instance. This makes behavior inspectable
and testable independently of the code that consumes it.

*Grounded in ADR-003.*

### VII. Shared Taxonomy, Multiple Consumers

One canonical taxonomy serves multiple feature components. Each component attaches
its own logic (templates, rules, checks) to shared nodes. There is never a
per-component fork of the taxonomy -- forks drift and create consistency defects.

*Grounded in ADR-007.*

### VIII. Determinism Over LLM Inference for Factual Lookups

Factual lookups (applicable standards, registry entries, known identifiers) must be
sourced from human-curated registries. LLM inference of factual values is prohibited.
LLMs reason; registries remember.

*Grounded in ADR-008.*

### IX. Citation-Only Knowledge Storage

The Standards Knowledge Store holds clause references and applicability mappings only.
Proprietary standard text is never stored, reproduced, or served. The system cites;
it does not republish.

*Grounded in ADR-006.*

### X. Raise on Failure — No Sentinel Returns

Functions signal failure by raising typed exceptions. Sentinel return values (`None`,
`False`, `-1`, empty collections) are never used to communicate failure. On success, a
function returns its meaningful output or `None` when there is nothing to return. Standard
Python exceptions are used for standard failure modes (`ValueError`, `TypeError`,
`OSError`, `pydantic.ValidationError`). A thin `RedlineError` base class covers
domain-specific failures with no standard equivalent. Subclasses are introduced only when
callers need to catch a failure mode distinctly — never speculatively.

*Grounded in ADR-014.*

### XI. Function Argument Ordering for Infrastructure Types

Public functions accepting connection, data, or file_path arguments must order them as:
connection → data → file_path, followed by keyword-only parameters introduced with `*`.
This canonical order ensures predictable signatures across the codebase. Exemptions
apply to callbacks, factory functions, protocols, and pure statistical functions.

*Grounded in ADR-015.*

### XII. CLI-First Tool Selection

When an external operation can be accomplished via a CLI tool (`gh`, `gws`, `gcloud`),
an MCP server, or a direct API call, the CLI is the required first choice. MCP servers
are a secondary option when no CLI covers the operation. Direct API calls are a last
resort. The narrowest-scope CLI applies: `gh` for GitHub, `gws` for Google Workspace,
`gcloud` for GCP infrastructure. Routing rules live in `.agents/skills/tool-selection/SKILL.md`
as SSOT.

*Grounded in ADR-016.*

### XIII. Interface Volatility by Default

All interfaces are volatile unless explicitly declared stable. Breaking changes to
volatile interfaces are permitted without deprecation, migration paths, or ceremony.
An interface becomes stable only by explicit declaration using a `# stable: <ADR-number>`
annotation backed by a recorded ADR. Stability is negotiated and earned — never assumed.

*Grounded in ADR-017.*

### XIV. Dev-Session Tools Do Not Cross the CI Boundary

Tooling that gates or assists a developer's local session (Claude Code hooks, CCE,
local index engines) is Windows-only and development-scoped. It is not installed in CI
or production and must not be expected to run there. Hook tests that depend on
Windows-only infrastructure skip on non-Windows platforms — this is correct scope
declaration, not a coverage loss. Hook scripts must guard Windows-only environment
variables with a `$HOME` fallback and must not re-throw from catch blocks under
`$ErrorActionPreference = 'Stop'`.

*Grounded in ADR-019.*

## Architectural Constraints

All new features must be assessed against the following before entering SpecKit:

- Does the feature introduce a new SSOT concern? Document it in ADR-001's authority
  table.
- Does the feature add a component boundary? Apply Principles V and VI.
- Does the feature depend on standards data? Apply Principles VIII and IX.
- Does the feature introduce a new agent rule? Apply Principle II (write a hook first).

## Development Workflow

- **ADR before code**: Every new system-level decision is recorded in `docs/adr/`
  before implementation begins.
- **Shaped Pitch before SpecKit**: No feature enters `speckit.specify` without a
  shaped Pitch with scope boundaries set and rabbit holes removed.
- **Constitution updated on ADR acceptance**: When an ADR with cross-cutting
  implications is accepted or amended, the principal engineer updates this document
  in the same commit. Enforced by the `check-adr-constitution-sync` pre-commit hook.

## Governance

This constitution supersedes all other practices where they conflict. Amendments
require:

1. A new or amended ADR grounding the change.
2. The principal engineer's review for cross-cutting implications.
3. This document updated in the same commit as the ADR.

The principal engineer is the sole custodian of this constitution. The sync procedure
is defined in `.agents/skills/adr-constitution-sync/SKILL.md`.

**Version**: 1.5.0 | **Ratified**: 2026-05-31 | **Last Amended**: 2026-06-09
