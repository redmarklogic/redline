# Patch: python-domain-modeling skill — Layer Architecture (Current Reality)

> DRAFT — pending user approval. Do not promote to production.

**Target file:** `.agents/skills/python-domain-modeling/SKILL.md`
**Session:** 2026-05-23 Topology Sync — Kabilan hire skill gaps
**Grounded by:** Peter (`pyproject.toml` import-linter contracts, `src/rl/` directory listing)
**Drafted by:** Harriet
**Gap addressed:** Layer architecture explanation — the current skill table lists layers that
do not yet exist (`adapters/`, `api/`), omits `schemas/` which does exist, and does not
mention that layer boundaries are machine-enforced by `import-linter`, not just convention.

---

## Changes

### 1. Replace the "Layer Architecture" section

Replace the current "Layer Architecture" section (table + notes) with the corrected version
below.

---

**Current content:**

```markdown
## Layer Architecture

This repo follows a layered architecture. Dependencies point inward --- outer layers depend on inner layers, never the reverse.

| Layer | Location | Responsibility |
|---|---|---|
| Domain | `src/rl/domain/` | Core business logic: entities, value objects, aggregates, domain events |
| Functions | `src/rl/functions/` | Stateless business operations and data transformations |
| Adapters | `src/rl/adapters/` | I/O boundaries: file readers, API clients, database access |
| Interface | `src/rl/api/` or `src/rl/web/` | FastAPI endpoints, CLI entrypoints, MCP tools |
| Scripts | `scripts/` | Thin orchestration that wires layers together |

Do not create new top-level packages under `src/rl/` or move code between layers without Peter's approval. Adding a new layer (e.g. a `services/` package) is an architectural decision.
```

**Replace with:**

```markdown
## Layer Architecture

This repo follows a strict layered architecture enforced by `import-linter`. Dependencies
point inward — outer layers depend on inner layers, never the reverse. Violations are
caught at pre-commit time and in CI.

### Current live layers (as of 2026-05-23)

| Layer | Location | Responsibility | Can import from |
|---|---|---|---|
| `functions` | `src/rl/functions/` | Stateless business operations, data transformations, file readers | `schemas`, `domain` |
| `schemas` | `src/rl/schemas/` | Shared data contracts — Pandera/Pydantic schemas used across layers | `domain` only |
| `domain` | `src/rl/domain/` | Core business logic: entities, value objects, aggregates, domain events | Nothing within `src/rl/` |

Layers not listed here (`adapters/`, `api/`, `web/`) **do not exist yet**. They are
described in architecture docs as future intent. Do not create them without Peter's approval.

### Machine enforcement

`import-linter` enforces the layer order via contracts in `pyproject.toml`:

```toml
[[tool.importlinter.contracts]]
name = "rl layers"
type = "layers"
layers = [ "functions", "schemas", "domain" ]
containers = [ "rl" ]
exhaustive = true   # <-- no other top-level packages are permitted
```

`exhaustive = true` means the linter will **fail** if any package other than `functions`,
`schemas`, or `domain` appears directly under `src/rl/`. Adding a new top-level package
is an architectural decision — escalate to Peter, who will update both the architecture
docs and the linter config.

### Prohibited imports (enforced)

| This layer... | MUST NOT import from... |
|---|---|
| `domain` | `schemas`, `functions`, anything outside `src/rl/domain/` |
| `schemas` | `functions` |

Violations will fail the `lint-imports` pre-commit hook. Do not suppress this hook.

### Scripts

`scripts/` sits outside `src/rl/` and is the thin orchestration layer. Scripts wire
layers together — they may import from any layer. Scripts must not contain business logic.

### When to escalate

Escalate to Peter before:
- Adding any new top-level package under `src/rl/` (e.g., `services/`, `adapters/`)
- Moving code between layers
- Updating the `import-linter` contracts in `pyproject.toml`
- Importing across a boundary that the linter currently prohibits (even temporarily)
```
