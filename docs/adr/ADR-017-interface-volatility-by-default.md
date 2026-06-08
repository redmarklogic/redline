# ADR-017 — Interface Volatility by Default

## Summary

All interfaces in this codebase are volatile unless explicitly declared stable. A volatile
interface may be changed or removed without notice, without a deprecation period, and without
a migration path. Stability is opt-in: a consumer that needs a guarantee must negotiate it
and record it. This is the binding contract for all cross-module boundaries, internal agent
protocols, and agent briefs in the repository.

## Decision

Interface stability is opt-in. The default is volatile. Breaking changes on volatile
interfaces are permitted in any commit and require no deprecation period. An interface
becomes stable only when explicitly declared so in a recorded decision (ADR or equivalent
artifact). Until that declaration exists, any consumer depending on the interface accepts
the risk of breakage.

## Status

Accepted — 2026-06-08

## Context

Redline is a greenfield project in Phase 1. The team is a solo founder working with AI
agents. The primary concern at this stage is learning velocity: discovering the right
boundaries, contracts, and domain model faster than building a durable system. Premature
interface stability is a threat to that goal — it introduces drag (deprecation cycles,
migration paths, backwards-compatibility constraints) before the system's shape is known.

Without a stated policy, contributors (human and AI) apply inconsistent assumptions. An AI
agent, by default, tends to treat any interface it has seen used as implicitly stable, adding
unnecessary backwards-compatibility scaffolding or avoiding refactors out of caution. A human
contributor may assume that touching an internal boundary requires a deprecation cycle by
analogy to public SDK practice.

Both assumptions are wrong for this codebase at this stage.

The decision codifies the actual working assumption: everything is changeable, refactoring
is cheap, and the cost of a broken interface is low because all consumers are internal and
the monorepo structure means all breakages are visible in the same PR.

### Scope

This ADR governs:

- Python package APIs across module and package boundaries (including `rl`, `marker`, and
  any future sibling packages)
- Internal agent protocols (agent briefs in `.claude/agents/*.md`, skill files in
  `.agents/skills/`)
- Structured data schemas used only internally (Pydantic models, dataclasses, TypedDicts)
- File format conventions used across internal tooling

This ADR does not govern:

- External-facing HTTP APIs (separate ADR required when introduced)
- Data migration discipline (separate concern)

## Options Considered

- **Volatile by default (selected):** No interface is stable unless explicitly declared.
  Breaking changes require no ceremony. Stability is added only when a consumer negotiates
  and records a guarantee.
- **Stable by default:** All interfaces are treated as stable once released. Breaking changes
  require a deprecation period and migration path. Rejected — imposes deprecation overhead
  before the system's shape is known; optimises for consumer convenience over shaping
  velocity in a phase where shaping is the primary activity.
- **Module-boundary stability:** Interfaces crossing package boundaries are stable;
  within-package interfaces are volatile. Rejected — the boundary between "crosses a package
  boundary" and "doesn't" is not consistently applied by AI agents, and the project has no
  internal consumers with different deployment cycles that would justify the distinction.
- **No policy:** Leave stability assumptions implicit. Rejected — produces exactly the
  inconsistency this ADR resolves; AI agents default to overcautious backwards-compatibility
  behaviour without an explicit rule.

## Decision Rationale

Three facts justify volatile-by-default:

1. **Monorepo.** All consumers of any interface are in the same repository. A breaking change
   is visible in the same PR as the interface change. GitHub Actions CI can detect and update
   impacted modules automatically. The cost of a breaking change is low.

2. **Greenfield phase.** No interface has an established track record. Declaring anything
   stable before its shape is proven locks in a design before the problem is fully understood.
   Phase 1 architecture is explicitly disposable (see constitution constraint).

3. **No implicitly stable interfaces exist.** The founder has confirmed there are no
   interfaces already being treated as stable. This ADR therefore has no retroactive
   breakage — it records the policy that has been operating informally.

Opt-in stability is the mechanism that preserves future flexibility. When a consumer
genuinely needs a stability guarantee — for example, a future external integration or a
component that has proven its design — that guarantee is negotiated and recorded. The absence
of a declaration is itself a signal: this interface is not ready for that commitment.

## Testable Rules

These rules are enforceable via pre-commit hooks or CI checks (per ADR-011):

1. An interface annotated `# stable: <ADR-number>` may not be changed without updating the
   referenced ADR.
2. An interface with no stability annotation may be changed in any PR without ceremony.
3. A PR that adds a stability annotation must include or reference the ADR that records the
   negotiated guarantee.

Rule 1 is the enforcement gate. Rules 2 and 3 are the expected workflow on either side of
a declaration.

## Consequences

**Positive:**

- AI agents have an unambiguous instruction: refactor freely unless a `# stable:` annotation
  exists. This eliminates overcautious backwards-compatibility scaffolding.
- Contributors (human and AI) do not need to negotiate every refactor. The default answer to
  "can I change this?" is yes.
- Stability declarations are explicit, searchable, and grounded in a recorded decision.
  There is no ambiguity about what is protected.
- Same-PR updates are the standard when a change breaks consumers in the same monorepo. No
  separate migration PR required.

**Negative:**

- Consumers outside the monorepo (if introduced in future) have no protection unless they
  negotiated an explicit stability declaration. Teams integrating externally must check for
  the annotation before depending on an interface.
- The opt-in mechanism (the `# stable:` annotation) is only as reliable as the enforcement
  hook. Until a hook enforces Rule 1, the protection is advisory (per ADR-011, P1).

## References

- ADR-011 — Hook-first Enforcement (P1: enforcement must be a hook, not just an instruction)
- ADR-014 — Function Error Handling Policy (companion convention governing function
  contracts; stable/volatile classification applies to these interfaces too)
- Shape Up (*Singer*): appetite and disposability as first-class design inputs
- Redline constitution — "Phase 1 architecture is explicitly disposable — optimise for
  learning velocity, not durability"
