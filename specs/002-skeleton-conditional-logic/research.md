# Research: Skeleton Conditional Section Logic

**Feature**: `specs/002-skeleton-conditional-logic/`
**Branch**: `feature/51-platform-p-skeleton-endpoint-post-skeleton-returns-docx-behind-auth`
**Date**: 2026-06-09

---

## D1 — Layer placement conflict: pitch vs import-linter contracts

**Question**: The pitch places `SkeletonRequest` and `SectionFlags` in `src/rl/schemas/` and the
activation function in `src/rl/domain/`. The existing `marker independence` import-linter contract
(`pyproject.toml` lines 207–210) forbids `marker → rl` and `rl → marker` imports. The FastAPI
route (001 decision D1) lives in `marker.api`. A route in `marker.api` cannot import from
`rl.schemas`.

**Decision**: Place `SkeletonRequest`, `SectionFlags`, and `HazardCategory` in `marker.api.schemas`
alongside the existing transport DTO from 001. Place `activate_sections` and `SectionID` in a new
`marker.domain.section_activation` module.

**Rationale**: The independence contract is enforced by import-linter and is a structural
guarantee. Overriding it for this feature without a new ADR is not permitted. The pitch's stated
layer placement was inconsistent with the existing contracts — an oversight, not a decision.
Keeping everything in `marker` is the only option that does not require an ADR, a contract change,
or a third shared package. The `rl.schemas/` and `rl.domain/` stubs remain empty for Sprint 1.

**Deviation from pitch**: The pitch's "What Kabilan builds" layer placement (`src/rl/schemas/skeleton_request.py`,
`src/rl/domain/section_activation.py`) is not implementable under the current contracts. Correct paths:
- `src/marker/api/schemas.py` — `SkeletonRequest`, `SectionFlags`, `HazardCategory`
- `src/marker/domain/section_activation.py` — `SectionID`, `activate_sections`, `SECTION_HEADINGS`, `SECTION_ORDER`

**Alternatives rejected**:
- *Relax independence contract*: Requires a new ADR; out of scope for Sprint 1.
- *Third shared package (`src/schemas/`)*: Requires pyproject.toml changes and a new contract; architectural scope exceeds Sprint 1.
- *Move FastAPI app to `rl.functions`*: Would need `rl.functions → marker.functions` for the builder call — also blocked by independence.

---

## D2 — Section ordering: activation produces a set, builder needs an ordered list

**Question**: `activate_sections` returns a `frozenset[SectionID]`. The existing `build_skeleton`
accepts a `ReportStructure` (an ordered tuple of `SectionHeading`). A canonical ordering function
is needed to bridge them.

**Decision**: Define `SECTION_ORDER: tuple[SectionID, ...]` — a hardcoded sequence listing every
possible section ID in the guideline's document order. To build the `ReportStructure`, filter
`SECTION_ORDER` to the activated section IDs (preserving order), then map each to a heading string
via `SECTION_HEADINGS`.

**Rationale**: The guideline defines a fixed document structure. Ordering is not dynamic —
it is identical for every skeleton. Encoding it as a data constant makes it inspectable and
testable independently of the activation logic (Constitution Principle VI).

---

## D3 — Heading text: Standards Knowledge Store is out of scope

**Question**: The pitch says heading text "comes from the Standards Knowledge Store" (Feature N,
out of scope). Where does heading text come from for Sprint 1?

**Decision**: Define `SECTION_HEADINGS: dict[SectionID, str]` — a hardcoded mapping from section
ID to heading text, co-located with `SECTION_ORDER` in `marker.domain.section_activation`.
Sections 7.NZ-1, 7.NZ-2, 7.NZ-3 use placeholder strings pending Graeme's canonical heading text.

**Rationale**: Data-driven (Principle VI). When Feature N ships, `SECTION_HEADINGS` is replaced by
a lookup into the Standards Knowledge Store without changing `activate_sections` or the route.

---

## D4 — Audit trail: no existing infrastructure

**Question**: AC2d (per PRD) requires a record of section flags + activated sections per generation
event. No audit infrastructure exists yet.

**Decision**: Write a structured `INFO`-level log entry via Python `logging` at generation time,
containing `section_flags` (serialised as dict) and `activated_sections` (sorted list of str).
Testable via pytest `caplog` fixture.

**Rationale**: Simplest audit mechanism that is inspectable, testable, and replaceable. A durable
store (database, append-only file) is a separate infrastructure decision deferred to a later sprint.

---

## D5 — `report_type` required or optional?

**Question**: The pitch says "Do not silently default to GAR — return an explicit error." This implies
`report_type` is required, but the pitch does not state this explicitly.

**Decision**: `report_type` is required. Absent `report_type` → 422.

**Rationale**: The pitch prohibits silent defaulting. If `report_type` is absent, returning 422
is the only honest response. The spec (User Story 3, Scenario 3) encodes this.

---

## D6 — `SectionFlags` cross-layer use within `marker`

**Question**: `SectionFlags` is an HTTP input schema containing a Pydantic enum. Does passing it
from `marker.api` to `marker.domain.activate_sections` violate Constitution Principle V (primitives
only across component boundaries)?

**Decision**: No violation. Principle V governs inter-package facades, not intra-package layer calls.
`marker.api` and `marker.domain` are layers of the same package; no facade boundary is crossed.

---

## D7 — `SkeletonRequest` supersedes `CreateSkeletonRequest` from 001

**Question**: 001's plan defines `CreateSkeletonRequest` in `marker.api.schemas`. This feature
defines `SkeletonRequest` as a richer model. Should it replace or extend `CreateSkeletonRequest`?

**Decision**: `SkeletonRequest` replaces `CreateSkeletonRequest`. Both features are on the same
branch; there is no external consumer yet. The route handler is updated to accept `SkeletonRequest`
directly. `CreateSkeletonRequest` is deleted.

**Rationale**: No backwards-compatibility obligation. One DTO, one truth.
