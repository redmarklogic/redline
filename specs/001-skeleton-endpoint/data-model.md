# Phase 1 Data Model: Skeleton Endpoint

Entities crossing the `POST /skeletons` boundary. Transport DTOs live in `marker.api.schemas`; domain models are reused unchanged from `marker.domain.models`. Per Principle V (ADR-004) and `python-testing-api`, transport DTOs and domain models are **separate classes** — the route translates DTO → domain before calling the builder.

---

## 1. `CreateSkeletonRequest` (transport DTO — NEW, `marker/api/schemas.py`)

The request body. Pydantic `BaseModel` with `model_config = {"extra": "forbid"}` (unknown fields → 422).

| Field | Type | Constraint | Maps to |
|-------|------|-----------|---------|
| `sections` | `list[str]` | ≥1 item; each non-blank; no duplicates — **enforced on the DTO** | `ReportStructure.sections` (`Sections` → `SectionHeading.heading`) |
| `project_number` | `str` | `min_length=1` (non-blank) — **enforced on the DTO** | `ProjectMetadata.project_number` (`Project Number`) |
| `client_name` | `str` | `min_length=1` (non-blank) — **enforced on the DTO** | `ProjectMetadata.client_name` (`Client Name`) |
| `site_address` | `str` | `min_length=1` (non-blank) — **enforced on the DTO** | `ProjectMetadata.site_address` (`Site Address`) |
| `date` | `datetime.date` | ISO-8601 date | `ProjectMetadata.date` (`Date`) |

**Validation responsibility (CRITICAL — get this right or 422s become 500s).** The DTO MUST carry **all** the semantic constraints (≥1 / unique / non-blank sections via a `@field_validator`; `min_length=1` on each metadata string), because only validation of the *declared request model* is converted by FastAPI into a `RequestValidationError` → `422`. A `pydantic.ValidationError` raised **inside the route** during the DTO→domain translation (e.g. if `ReportStructure.model_validate(...)` rejects something the DTO let through) is an *unhandled exception* → the catch-all handler → **500**, not 422. Two defences, both required:
  1. **Primary** — mirror every constraint on `CreateSkeletonRequest` so the failure is caught at the request-model boundary as `422` with field-level `details`.
  2. **Defense-in-depth** — register a handler for `pydantic.ValidationError` mapping to `422` (same envelope), so any domain rule the DTO does not mirror still returns `422`, never `500`.

The domain models (`ProjectMetadata`) do **not** currently enforce non-blank on their string fields — so the non-blank guarantee lives on the DTO, not the domain layer. Do not rely on the domain model to produce the `422`.

**Why a separate DTO (not the domain model directly as the body)**: keeps HTTP-only concerns (future auth context, content-negotiation hints) out of the domain layer; lets the transport shape evolve (volatile, ADR-017) without touching the frozen domain models.

**Example body**:

```json
{
  "sections": ["Introduction", "Site Description", "Conclusions"],
  "project_number": "GIR-001",
  "client_name": "Acme Corp",
  "site_address": "123 Example Street",
  "date": "2026-06-09"
}
```

---

## 2. `ReportStructure` (domain — REUSED, `marker/domain/models.py`)

Frozen Pydantic model. Ordered, non-empty, duplicate-free section headings.

- `sections: tuple[SectionHeading, ...]` (alias `Sections`) — `@model_validator`: non-empty; no duplicate headings.
- `SectionHeading.heading: str` (alias `Heading`) — `@field_validator`: rejects blank/whitespace-only.

Constructed in the route via `ReportStructure.model_validate({"Sections": [{"Heading": s} for s in body.sections]})`.

## 3. `ProjectMetadata` (domain — REUSED, `marker/domain/models.py`)

Frozen Pydantic model: `project_number`, `client_name`, `site_address` (`str`), `date` (`datetime.date`), each with a human-readable alias. Constructed via `ProjectMetadata.model_validate({"Project Number": ..., ...})`.

---

## 4. `DocumentFacade` (protocol — CHANGED, `marker/domain/protocols.py`)

Add one method to the existing structural protocol:

| Method | Signature | Notes |
|--------|-----------|-------|
| `to_bytes` | `to_bytes(self) -> bytes` | NEW. Returns the rendered `.docx` as bytes (no disk I/O). `bytes` is primitive → ADR-004-compliant. |

Existing methods unchanged: `add_heading`, `add_table`, `write_table_cell`, `save`.

`PythonDocxFacade.to_bytes()` (`marker/functions/engines.py`): save the underlying `docx.Document` to an `io.BytesIO`, return `.getvalue()`.

---

## 5. Error envelope (transport — produced by the global handler)

Not a Pydantic request/response model the route returns; produced uniformly by `register_exception_handlers`. Shape per Standard §3:

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `code` | `str` | yes | Stable machine-readable code (e.g. `VALIDATION_ERROR`, `BAD_REQUEST`, `HTTP_401`, `INTERNAL_ERROR`). |
| `message` | `str` | yes | Human-readable, display-safe. **No** stack/class/path/SQL. |
| `trace_id` | `str` | yes | UUID per response for log correlation. |
| `details` | any | optional | Machine-actionable specifics (e.g. validation error list on 422). Omitted/`null` when empty. |

Status → code mapping:

| Status | When | `code` |
|--------|------|--------|
| 400 | unparsable body (`json_invalid`) | `BAD_REQUEST` |
| 401 | no/invalid bearer | `HTTP_401` |
| 422 | parsed-but-invalid body | `VALIDATION_ERROR` |
| 500 | unhandled fault | `INTERNAL_ERROR` |

---

## 6. Skeleton document (response artifact)

Not a model — the raw `.docx` bytes streamed as the `200` body via `StreamingResponse`:

- `media_type`: `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
- header `Content-Disposition: attachment; filename="<safe-name>.docx"` where `<safe-name>` is `project_number` **sanitized** to a header-safe filename — strip/replace anything outside `[A-Za-z0-9._-]` (a raw `"`, newline, `/`, or `;` in `project_number` would otherwise break or inject the header). Fall back to `"skeleton"` if sanitization yields an empty string.
- body: ZIP/OOXML bytes (first 4 bytes `PK\x03\x04`). Never base64, never JSON-wrapped.
