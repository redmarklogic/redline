# ADR-007: Standards Registry as Deterministic Anchor for Skeleton Generator

**Status**: Accepted
**Date**: 2026-05-14
**Deciders**: Ron (strategy), Graeme (domain), Mark (PM)

---

## Context

The Skeleton Generator (Bet 1) must nominate applicable standards when producing a report
template for a given project type and jurisdiction. Two approaches are possible:

1. **LLM inference** — the language model infers which standards apply based on project
   type, jurisdiction, and scope described in the prompt.
2. **Registry lookup** — applicable standards are retrieved from the human-curated
   Standards Registry, which maps project types and jurisdictions to a deterministic
   list of mandatory and advisory standards.

The choice is not primarily a performance question. It is a correctness and trust question
that determines whether the adversarial loop is genuinely broken.

---

## Decision

**Standards nomination in the Skeleton Generator must be deterministic, sourced from the
human-curated Standards Registry. LLM inference of applicable standards is prohibited.**

---

## Options Considered

- **Option A — LLM inference**: The model infers applicable standards at generation time.
  Fast to implement; requires no pre-populated registry.
- **Option B — Registry lookup (selected)**: Applicable standards are fetched from the
  Standards Registry before generation. Deterministic; human-curated; auditable.
- **Option C — Hybrid**: Registry is preferred; LLM inference fills gaps for unregistered
  project types. Rejected because the hybrid creates a silent fallback that undermines the
  correctness guarantee without surfacing it to the user.

---

## Decision Rationale

If the model infers which standards apply when generating a skeleton, the adversarial loop
is not broken — the model nominates, the model writes, the model confirms. Consistent
errors become invisible to the checker because both the generation and the verification
share the same failure mode.

The Standards Registry is the deterministic anchor that severs this loop. It represents
a human commitment: a qualified engineer has verified that these standards apply to this
project type in this jurisdiction. That commitment cannot be delegated to inference.

Option C was rejected because a silent LLM fallback recreates the same loop for any
project type not yet in the registry, without alerting the user that the nomination was
inferred rather than curated.

---

## Consequences

**Positive:**

- The adversarial loop is genuinely broken for all registered project types.
- Standards nominations are auditable — every skeleton can cite its registry entry.
- The quality guarantee is honest: it holds exactly where the registry holds and no
  further.

**Negative / Constraints:**

- The Standards Registry must be populated before the Skeleton Generator ships.
- Any new project type requires a human-curated entry in the Standards Registry before
  the Skeleton Generator can serve it. There is no graceful degradation — the generator
  must decline to produce a skeleton for unregistered types rather than fall back to
  inference.
- This is a correctness and trust constraint, not a performance constraint. Speed-of-
  delivery pressure must not be used to justify a temporary inference fallback.

---

## References

- ADR-005: Standards Knowledge Store — Citation-Only Internal Architecture
- ADR-006: Shared Taxonomy — Skeleton Generator, Checklist Engine, Pre-Review Engine
