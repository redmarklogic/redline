# Data Model: Skeleton Conditional Section Logic

**Feature**: `specs/002-skeleton-conditional-logic/`
**Date**: 2026-06-09

---

## HTTP Transport Layer (`marker.api.schemas`)

### `HazardCategory` (enum)

Maps practitioner vocabulary to guideline section numbers. 18 values:

| Enum value | Activates | Guideline ref |
| --- | --- | --- |
| `LIQUEFACTION` | 7.1 | CL-G1 |
| `LATERAL_SPREADING` | 7.2 | CL-G1 |
| `EXPANSIVE_SOILS` | 7.3 | CL-G1 |
| `COMPRESSIBLE_SOILS` | 7.4 | CL-G1 (soil characterisation; not settlement outcome) |
| `SLOPE_INSTABILITY` | 7.5, 7.7, 7.13 | CL-G1 (only one-to-many mapping) |
| `UNCONTROLLED_FILL` | 7.6 | CL-G1 (cannot be derived from combo) |
| `EROSION_AND_DRAINAGE` | 7.8 | CL-G1 (covers inland + coastal; coastal is a qualifier) |
| `SENSITIVE_AND_COLLAPSIBLE_SOILS` | 7.9 | CL-G1 (quick clays, loess, metastable) |
| `CONTAMINATION` | 7.10 | CL-G1 |
| `FALLING_DEBRIS` | 7.11 | CL-G1 (kinematically distinct from SLOPE_INSTABILITY) |
| `SUBSIDENCE` | 7.12 | CL-G1 |
| `FLOODING` | 7.14 | CL-G1 (orthogonal to flooding_info_uncertain flag) |
| `OTHER` | 7.15 | CL-G1 (practitioner-flagged only; not auto-included) |
| `FAULT_RUPTURE` | 7.NZ-1 | NZ extension (Hikurangi context) |
| `VOLCANIC` | 7.NZ-2 | NZ extension |
| `TSUNAMI` | 7.NZ-3 | NZ extension |

### `SectionFlags` (Pydantic `BaseModel`, frozen, `extra="forbid"`)

All fields optional; absent → default value.

| Field | Type | Default | Activates | Rule |
| --- | --- | --- | --- | --- |
| `detailed_analysis_performed` | `bool` | `False` | Section 7 full analysis detail | CL-G2 |
| `retaining_walls_present` | `bool` | `False` | Section 8.4 (Retaining Walls) | CL-G5 |
| `flooding_info_uncertain` | `bool` | `False` | Section 4.3 modifier | CL-G6 |
| `site_plan_footprint_available` | `bool` | `False` | Appendix: site plan footprint | CL-G7a |
| `professional_opinion_required` | `bool` | `False` | Appendix: professional opinion | CL-G7b |
| `hazards` | `list[HazardCategory]` | `[]` | Section 7 sub-sections (per lookup table) | CL-G1 |
| `foundation_recommendations_required` | `bool` | `False` | Section 8.2 + sub-sections 8.2.1–8.2.9 | CL-G3 |
| `earthworks_proposed` | `bool` | `False` | Section 8.3 (Filling and Earthworks) | CL-G4 |

### `ReportContext` (Pydantic `BaseModel`, frozen, `extra="forbid"`)

| Field | Type | Required | Validation |
| --- | --- | --- | --- |
| `jurisdiction` | `Literal["NZ"]` | Yes | Only "NZ" accepted; absent → 422 |
| `report_type` | `Literal["GAR"]` | Yes | Only "GAR" accepted; absent or other → 422 |

### `SkeletonRequest` (Pydantic `BaseModel`, frozen, `extra="forbid"`)

Replaces `CreateSkeletonRequest` from 001.

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `project_metadata` | `ProjectMetadataDTO` | No | All sub-fields optional; absent → blank placeholders |
| `report_context` | `ReportContext` | Yes | Both sub-fields required |
| `section_flags` | `SectionFlags` | No | Absent/null → all defaults; produces mandatory sections only |

### `ProjectMetadataDTO` (Pydantic `BaseModel`, frozen, `extra="forbid"`)

HTTP transport DTO (distinct from `marker.domain.models.ProjectMetadata`).

| Field | Type | Default |
| --- | --- | --- |
| `project_number` | `str \| None` | `None` |
| `client_name` | `str \| None` | `None` |
| `site_address` | `str \| None` | `None` |
| `report_date` | `datetime.date \| None` | `None` (defaults to today in builder) |

---

## Domain Layer (`marker.domain.section_activation`)

### `SectionID` (type alias)

```python
type SectionID = str
```

String identifiers for document sections. Examples: `"7.1"`, `"7.NZ-1"`, `"8.2"`, `"8.4"`.

### `SECTION_HEADINGS: dict[SectionID, str]`

Canonical heading text per section. Authoritative SSOT. Populated from the ENZ/NZGS 2023
guideline. Sections 7.NZ-1, 7.NZ-2, 7.NZ-3 use placeholder text pending Graeme's confirmation.

### `SECTION_ORDER: tuple[SectionID, ...]`

Canonical document ordering of all possible section IDs. Used to produce an ordered list from
the `frozenset[SectionID]` returned by `activate_sections`. No section appears more than once.
Order follows the ENZ/NZGS 2023 guideline document structure.

### `activate_sections(flags: SectionFlags) -> frozenset[SectionID]`

**Signature**: `(SectionFlags) -> frozenset[SectionID]`

Pure function. No I/O. No external calls. Same input → same output (verified by tests).

**Invariants**:
- Section 7 heading (`"7"`) always included in the output (mandatory structural element).
- `SLOPE_INSTABILITY` in `flags.hazards` → `{"7.5", "7.7", "7.13"}` added.
- `OTHER` in `flags.hazards` → `"7.15"` added only if explicitly present in the list.
- `FAULT_RUPTURE`, `VOLCANIC`, `TSUNAMI` → `"7.NZ-1"`, `"7.NZ-2"`, `"7.NZ-3"` respectively.
- All remaining hazard values → one-to-one mapping per the `HazardCategory` table above.
- Each `True` Tier A flag adds its corresponding section ID.
- `foundation_recommendations_required: True` → `"8.2"` plus `"8.2.1"` through `"8.2.9"`.
- `earthworks_proposed: True` → `"8.3"`.
- `section_flags=None` or absent → equivalent to `SectionFlags()` (all defaults).

**Always-included sections** (independent of flags):

| Section ID | Heading | Reason |
| --- | --- | --- |
| `"7"` | Section 7 — Geotechnical Hazards | Mandatory template structure |
| `"8.5"` | Section 8.5 — Slope Design | Sprint 1 default: always-present pending Graeme confirmation |
| `"8.6"` | Section 8.6 — Other Engineering Considerations | Sprint 1 default: always-present pending Graeme confirmation |

---

## Audit Record (log entry, not persisted)

Written via `logging.info()` at generation time.

| Key | Value |
| --- | --- |
| `section_flags` | `dict` — serialised from `SectionFlags` (Pydantic `.model_dump()`) |
| `activated_sections` | `list[str]` — sorted `SectionID` values from `activate_sections()` output |

---

## Entity Relationships

```text
HTTP Request
  └── SkeletonRequest
        ├── ProjectMetadataDTO   (optional; → ProjectMetadata domain model)
        ├── ReportContext        (required; report_type validated)
        └── SectionFlags         (optional; → activate_sections())
                                             |
                                             ↓
                              frozenset[SectionID]
                                             |
                              filter SECTION_ORDER → ordered SectionIDs
                              map via SECTION_HEADINGS → list[str]
                                             |
                                             ↓
                              ReportStructure (domain model)
                                             |
                                             ↓
                              build_skeleton_bytes() → bytes (.docx)
```