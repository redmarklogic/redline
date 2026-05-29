# ADR-013: spec-kit Lifecycle Hook Enforcement

**Status**: Accepted
**Date**: 2026-05-29
**Deciders**: Peter (architecture)

---

## Context

ADR-011 established hook-first enforcement for deterministic, pattern-checkable rules and
explicitly deferred agent lifecycle hooks to a future ADR. This is that ADR.

spec-kit supports lifecycle extensions: YAML-declared hooks that fire at named pipeline
points and inject a structured prompt into LLM context. Extensions are probabilistic (the
LLM can misinterpret or skip the instruction), unlike git hooks which are deterministic
gates.

Four Tier 1 rule candidates exist. Two (`static-checks`, `verification-gate`) apply in any
implementation context, not only after `specify implement`. Two (`shaping-gate`,
`source-reconciliation`) are scoped exclusively to the spec-kit pipeline.

---

## Decision

For rules with scope beyond the spec-kit pipeline, the extension dispatches to the governing
skill (Option C); the skill remains SSOT. For rules native to the spec-kit pipeline, the
extension is the sole SSOT (Option A). Extensions, git hooks, and `AGENTS.md` instructions
coexist as defence-in-depth; no layer substitutes for another.

---

## Options Considered

**A — Migrate (extension as sole SSOT):** Correct for pipeline-native rules. Incorrect for
rules that also apply outside spec-kit, as retiring the skill removes enforcement for
non-pipeline invocations.

**B — Augment (duplicated content in both):** Rejected. Drift between two SOTs is
structurally guaranteed.

**C — Dispatcher (extension invokes skill):** Correct for general rules. Extension contains
only a pointer; skill remains authoritative.

**D — Reject extensions:** Rejected. Phase-level semantics (`before_specify`) cannot be
expressed as git hooks.

---

## Rationale

SSOT strategy cannot be uniform across all four candidates because they differ in scope.
Option A for pipeline-native rules, Option C for general rules. Option B rejected without
exception.

---

## Consequences

- Phase-level enforcement semantics are captured that git hooks cannot express.
- Each rule has exactly one authoritative source.
- Extensions are probabilistic; git hooks remain the deterministic backstop.
- `specify extension add` writes to three locations; manual deletion leaves residue. Always
  use `specify extension remove`.

---

## References

- [ADR-001](adr-001-single-source-of-truth.md) — SSOT principle
- [ADR-011](adr-011-hook-first-enforcement.md) — Hook-first enforcement (deferred lifecycle
  hooks to this ADR)
- [ADR-012](adr-012-agents-folder-as-primary-customisation-home.md) — `.agents/` as primary
  customisation home
