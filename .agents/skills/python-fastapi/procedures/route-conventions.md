# Route Conventions — Per-Endpoint Rules

Rules applied for every new external (north-south) FastAPI route.

**Live standard:** `docs/architecture/api/http-api-standard.md` §1, §2, §4–§6, §9, §12, §14–§15

---

## 1. URI shape (ADR-018 §1)

Plural nouns. HTTP method carries the verb. No version prefix yet (§15).

```
POST /skeletons          ✓
GET  /skeletons/{id}     ✓
POST /generateSkeleton   [x]  (verb in path)
POST /skeleton           [x]  (singular)
GET  /api/v1/skeletons   [x]  (version prefix — deferred)
```

---

## 2. Status codes (ADR-018 §2, §5)

| Route behaviour | Status | Notes |
|---|---|---|
| Synchronous artifact returned as body | `200` | The skeleton case — no `Location` header |
| Addressable resource created | `201` | Must include `Location` header |
| Long-running work accepted | `202` | Returns `job_id`; not for #51 |
| Parsed body fails validation | `422` | FastAPI+Pydantic default — keep it |
| Body malformed/unparsable | `400` | Custom handler (see `app-wiring.md`) |
| No/invalid credentials | `401` | Must set `WWW-Authenticate: Bearer` |
| Authenticated, not authorised | `403` | |
| Unhandled server fault | `500` | Envelope via global handler |

Declare status code on the route decorator:

```python
@router.post("/skeletons", status_code=200)
```

---

## 3. Request model (ADR-018 §4)

Use a Pydantic model for every POST/PUT/PATCH body. Never accept raw `dict` or
`Any` at the route boundary.

```python
from pydantic import BaseModel, Field


class CreateSkeletonRequest(BaseModel):
    model_config = {"extra": "forbid"}

    project_name: str = Field(..., min_length=1)
```

`extra="forbid"` causes FastAPI to return 422 for unexpected fields, which is the
correct behaviour — unknown fields are a validation error, not a parse error.

---

## 4. Binary artifact response (ADR-018 §6)

For a synchronous `.docx` return use `StreamingResponse`. Never wrap bytes in JSON.

```python
from io import BytesIO

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from rl.app.api.dependencies.auth import require_bearer
from rl.app.api.schemas.skeletons import CreateSkeletonRequest
from rl.skeleton_generator import build_skeleton

DOCX_MEDIA_TYPE = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)

router = APIRouter()


@router.post("/skeletons", status_code=200)
async def create_skeleton(
    body: CreateSkeletonRequest,
    _token: str = Depends(require_bearer),
) -> StreamingResponse:
    docx_bytes: bytes = build_skeleton(project_name=body.project_name)
    return StreamingResponse(
        content=BytesIO(docx_bytes),
        media_type=DOCX_MEDIA_TYPE,
        headers={
            "Content-Disposition": f'attachment; filename="{body.project_name}.docx"',
        },
        status_code=200,
    )
```

**Why `StreamingResponse` over `Response`:** `StreamingResponse` accepts a file-like
object and streams chunks, which avoids loading the full bytes into memory twice.
For the docx sizes at Phase 1 this is not critical, but it is the correct pattern
for binary artifacts.

**Why not `FileResponse`:** `FileResponse` requires a path on disk. `build_skeleton`
returns bytes in memory; there is no intermediate file.

---

## 5. Content negotiation (ADR-018 §10 — future)

One resource, multiple representations via `Accept`. Not implemented in #51 (only
`.docx` is served). When the JSON violations representation lands, the route reads
the `Accept` header and branches:

```python
from fastapi import Request

@router.post("/skeletons", status_code=200)
async def create_skeleton(request: Request, ...) -> StreamingResponse | dict:
    accept = request.headers.get("Accept", DOCX_MEDIA_TYPE)
    if "application/json" in accept:
        ...  # violations JSON — deferred to domain expert schema
    return StreamingResponse(...)
```

Do not implement this until the violations schema is defined.

---

## 6. No SSE on synchronous routes (ADR-018 §9)

The honesty constraint (standard §9) binds: a synchronous endpoint MUST NOT emit
client-facing SSE. Do not add an SSE generator or a `text/event-stream` response
to the skeleton route.

Internal lifecycle events (logging) are allowed and encouraged, but they go to the
logger, not to the HTTP response.

---

## 7. OpenAPI — let FastAPI generate it (ADR-018 §12)

FastAPI auto-generates `/openapi.json` from route decorators and Pydantic models.
Do not hand-author it. If the generated schema is wrong, fix the Pydantic model or
route decorator — never edit the schema directly.

The `openapi-spec-validator` contract test (see `contract-testing.md`) catches
schema regressions automatically.

---

## Checklist before PR

- [ ] URI uses plural noun, no verb, no `/v1/` prefix
- [ ] `status_code` declared on the decorator (not defaulted)
- [ ] Request body is a Pydantic model with `extra="forbid"`
- [ ] Binary return uses `StreamingResponse` with `media_type` and `Content-Disposition`
- [ ] Auth dependency injected via `Depends(require_bearer)`
- [ ] No SSE response on this route
- [ ] No hand-authored OpenAPI changes
