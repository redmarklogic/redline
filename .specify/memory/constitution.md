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

### XV. Infrastructure as Code for GCP Resources

All GCP infrastructure is declared in Terraform HCL under `deploy/infra/terraform/`.
Two resources are exempt: the GCP project and the Terraform state bucket, which are
created by a one-off bootstrap script (`deploy/infra/bootstrap/bootstrap.sh`) because
Terraform requires them to exist before it can initialise. After the bootstrap runs,
no human or CI job modifies GCP infrastructure except through a reviewed
`terraform apply`. The `gcloud` CLI is permitted for read-only operations and
operational commands (deployments, image pushes) that are not infrastructure
definitions. Direct GCP Console changes to Terraform-managed resources are
prohibited — they will be reverted on the next apply.
`deploy/infra/terraform/terraform.tfvars` is the single source of truth for
canonical GCP project identifiers.

*Grounded in ADR-020.*

### XIV. Platform Obligation Follows Deployment Context

Development happens on Windows; CI and production run on Linux. A platform
compatibility obligation is set by where an artifact *executes*, not where it is
authored. Application code (`src/`) deploys to Linux and must be Linux-compatible:
`pathlib.Path` for all file-system operations, no Windows-only environment variables
without a POSIX fallback, LF line endings. Enforcement hooks (`hooks/`) run on both
platforms and must be cross-platform Python. Claude Code hooks (`.claude/hooks/`) run
only on a Windows developer's machine — they are Windows PowerShell by design and carry
no portability obligation. Hook tests for Windows-only dev tooling skip on non-Windows
via `sys.platform != "win32"`; this is accurate scope declaration, not a coverage loss.

*Grounded in ADR-019.*

### XVI. Process Environment as Sole Config Source

The application process assumes its environment is correctly configured by the
caller (shell, orchestrator, or container runtime). No Python source file in
`src/` or `scripts/` may call `load_dotenv()`, import `python-dotenv`, or
supply a default value to `os.getenv()` / `os.environ.get()`. Use
`os.environ["VAR"]` (fails loudly on misconfiguration) or `pydantic-settings`
with `env_file=None`. `.env` files are a local developer ergonomic tool only;
they are excluded from the Docker build context and never present at runtime.
This prevents silent local/CI divergence: a missing var raises `KeyError` at
startup, not a silent wrong value surfacing at runtime. Runtime business state
(e.g. per-user quota caps) is platform data, edited through the application and
stored in the platform datastore — it is not deployment configuration and does
not enter the process environment.

*Grounded in ADR-021, ADR-024.*

### XVII. All-Python Toolchain Boundary

The team runs one language toolchain: Python. No technology may be adopted that
requires a second compiler, package/version manager, or skillset needing a new
owner. Vendored JavaScript (single static file, no build step), CSS, and Python
packages that emit JavaScript are acceptable; a Node/npm toolchain is not. The
test is toolchain and ownership complexity, not file extension.

*Grounded in ADR-024.*

### XVIII. Stateless Core, Stateful Shell — Framework Confined to the Web Shell

The generator core (`domain` and `functions` packages) is stateless, pure Python:
no web-framework import may appear there, and no geotechnical concept may be
modelled as a framework ORM model. ORM models hold platform state only (users,
sessions, quota counters, audit-log rows). The web shell calls the core through
its facade with typed inputs and receives bytes — it never touches
document-engine types.

*Grounded in ADR-024; boundary per ADR-002.*

### XIX. Office.js API Floor Is a Commercial Commitment

The Word taskpane declares **WordApi 1.3** as its minimum. This floor is set by
`ContentControl.getRange()` (Replace primitive). It may only increase by ADR
amendment — never by implementation drift. Any new Office.js call must be
pre-checked against the current floor before it ships.

*Grounded in ADR-028.*

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

**Version**: 1.9.0 | **Ratified**: 2026-05-31 | **Last Amended**: 2026-06-14
