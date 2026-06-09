# Implementation Plan: Skeleton Conditional Section Logic — Input Model

**Date**: 2026-06-09 | **Spec**: [spec.md](./spec.md) | **Branch**: `feature/51-platform-p-skeleton-endpoint-post-skeleton-returns-docx-behind-auth`
**Status**: Draft

## Summary

This feature adds a structured input model to `POST /skeletons` that enables conditional section
inclusion in generated skeletons. The request body gains `report_context` (required) and
`section_flags` (optional) alongside existing project metadata. A pure domain function
(`activate_sections`) maps section flags to a set of section identifiers using a deterministic
lookup table. The route wires activation output into the existing builder. All decisions are
audited in the application log. This feature and 001 (skeleton endpoint) are implemented together
on the same branch; 001 provides the FastAPI app shell, auth, and error envelope — this feature
extends the request schema and adds the activation layer.

## Technical Context

**Language/Version**: Python 3.14
**Package manager**: uv
**Testing**: pytest with `TestClient` (in-process ASGI); `caplog` for audit log assertions
**Project layout**: monorepo (`hub_package: rl`); `marker` and `rl` packages are import-independent
**HTTP framework**: FastAPI (added by 001)
**Schema validation**: Pydantic v2 (frozen models; `extra="forbid"`)
**Linting / layer enforcement**: ruff + import-linter (`marker independence` contract enforced)
**Layer ordering**: `marker.api` (outermost) → `marker.functions` → `marker.domain` (innermost)
**Domain modelling**: Pydantic `BaseModel` frozen; existing models: `ReportStructure`, `ProjectMetadata`, `SectionHeading`
**Builder entrypoint**: `marker.functions.builders.build_skeleton_bytes(structure, metadata) -> bytes` (added by 001)
**Key constraint**: `marker` and `rl` packages are import-independent (research D1). All new code lives in `marker`.

## Constitution Check

*Gate passed. Re-check after Phase 1 design.*

| Principle | Assessment |
| --- | --- |
| I (Single SSOT) | `SECTION_HEADINGS` and `SECTION_ORDER` are the SSOT for section mapping. No duplication. |
| V (Primitives across facades) | `SectionFlags` passes from `marker.api` to `marker.domain` — intra-package call; no facade crossed. No violation. |
| VI (Data-driven config) | `SECTION_HEADINGS: dict[SectionID, str]` and `SECTION_ORDER: tuple[SectionID, ...]` are explicit data constants. |
| VIII (Determinism) | `activate_sections` is a pure function over a lookup table. No LLM inference. |
| X (Raise on failure) | Pydantic validation raises `ValidationError` on bad input (translated to 422 by FastAPI). No sentinel returns. |
| ADR before code | No new system-level decision requires a new ADR. D1 resolves within existing contracts; D4 is an implementation choice within existing logging. |

## Project Structure

### Documentation (this feature)

```text
specs/002-skeleton-conditional-logic/
├── plan.md
├── research.md
├── data-model.md
├── checklists/
│   └── requirements.md
└── tasks.md             (Phase 2 output — not yet created)
```

### Source Code (additions and changes for this feature)

```text
src/marker/
├── api/
│   └── schemas.py                    # CHANGED: CreateSkeletonRequest → SkeletonRequest
│                                     #   + HazardCategory (enum, 18 values)
│                                     #   + SectionFlags (frozen Pydantic model, 8 fields)
│                                     #   + ReportContext (frozen Pydantic model)
├── domain/
│   └── section_activation.py         # NEW: SectionID, SECTION_HEADINGS, SECTION_ORDER,
│                                     #       activate_sections(flags) -> frozenset[SectionID]

tests/marker/
├── api/
│   ├── test_schemas.py               # CHANGED: extend for new request model
│   └── test_routes.py                # CHANGED: integration tests for conditional logic
└── domain/
    └── test_section_activation.py    # NEW: unit tests for activate_sections
```

**Structure decision**: All new code stays within `marker` (import-linter independence constraint).
The `rl.schemas/` and `rl.domain/` stubs remain empty for Sprint 1.

## Design Decisions

| # | Decision | Choice | Rationale |
| --- | --- | --- | --- |
| D1 | Layer placement | `marker.api.schemas` + `marker.domain.section_activation` | Import-linter independence forbids `rl ↔ marker`; pitch's `rl.schemas/` placement is not implementable without a new ADR. See research D1. |
| D2 | Section ordering | `SECTION_ORDER: tuple[SectionID, ...]` constant; filter to activated IDs then map via `SECTION_HEADINGS` | Builder needs ordered list; activation produces set. Canonical ordering is fixed guideline structure — encode as data (Principle VI). |
| D3 | Heading text | `SECTION_HEADINGS: dict[SectionID, str]` constant in `marker.domain.section_activation` | Standards Knowledge Store (Feature N) out of scope. NZ extensions use placeholder strings until Graeme provides canonical text. |
| D4 | Audit trail | `logging.info()` with serialised `section_flags` and `activated_sections` at generation time | No audit infrastructure exists. Simplest testable approach (caplog). Replaceable when durable storage is designed. |
| D5 | `report_type` | Required; absent → 422 | Pitch prohibits silent defaulting; spec US3 Scenario 3. |
| D6 | `SectionFlags` intra-package | Not a facade violation | Principle V governs inter-package boundaries; `marker.api → marker.domain` is intra-package. |
| D7 | `CreateSkeletonRequest` replaced | Deleted; `SkeletonRequest` is the sole transport DTO | Same branch; no external consumer. One DTO, one truth. |
| D8 | `SectionID` type | `type SectionID = str` (PEP 695 type alias) | Section IDs are strings ("7.1", "7.NZ-1"). Type alias documents intent without runtime overhead. |

## Domain Impact

**New packages**: None. All additions are within `marker`.

**Layer contract changes**: The `marker layers` import-linter contract gains `api` as the outermost
layer (001's change). No change to `marker independence` or `rl layers` contracts.

**New SSOT**: `SECTION_HEADINGS` and `SECTION_ORDER` in `marker.domain.section_activation` — canonical
source of truth for section-to-heading mapping and document ordering.

**Subdomain classification**: Supporting — deterministic mapping function over a lookup table.

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Graeme has not provided 7.NZ-1/2/3 heading text before merge | Medium | Low | Placeholder strings are explicit; skeleton is structurally correct. No code gate blocks merge. |
| `SECTION_ORDER` ordering is wrong | Low | Medium | Verified manually against pitch activation table before tasks are written; covered by acceptance test (Section 8.4 in correct position). |
| 001's `build_skeleton_bytes` not yet implemented | Low | High | Same branch; task ordering ensures bytes seam (001 D3) is implemented before route wiring task. |
