# App Wiring — FastAPI Application Startup

Covers the structural guarantees wired once at application startup:
global exception handler, 422/400 split, HTTP auth dependency, and 401 header.
These are not per-route concerns — they are framework-level bindings.

**Live standard:** `docs/architecture/api/http-api-standard.md` §3, §4, §7

---

## 1. Application factory

Always use a factory function (`create_app`) so tests can instantiate a fresh app
with dependency overrides.

```python
# src/rl/app/main.py
from fastapi import FastAPI

from rl.app.api.exception_handlers import register_exception_handlers
from rl.app.api.routers import skeletons


def create_app() -> FastAPI:
    app = FastAPI(docs_url=None, redoc_url=None)  # disable docs in prod
    register_exception_handlers(app)
    app.include_router(skeletons.router)
    return app
```

---

## 2. Global exception handler (ADR-018 §3)

**Rule:** One handler module, registered at app startup. Never per-route `try/except`
for envelope production.

```python
# src/rl/app/api/exception_handlers.py
import logging
import uuid

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


def _envelope(
    *,
    code: str,
    message: str,
    details: object = None,
) -> dict:
    return {
        "code": code,
        "message": message,
        "trace_id": str(uuid.uuid4()),
        "details": details,
    }


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_envelope(
                code=f"HTTP_{exc.status_code}",
                message=exc.detail if isinstance(exc.detail, str) else "Request error.",
            ),
            headers=dict(exc.headers) if exc.headers else None,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        errors = exc.errors()
        # exc.body (raw bytes) is available for logging — never include in the response (may contain PII)
        # NOTE: "json_invalid" is a Pydantic v2 internal error type, not a documented stable API.
        # It is the correct detector for a completely unparsable body as of Pydantic v2.x.
        # If a future Pydantic upgrade renames this type, the 400/422 split will silently revert
        # to always returning 422. Add a test for this path (see contract-testing.md).
        is_parse_error = any(e.get("type") == "json_invalid" for e in errors)
        if is_parse_error:
            return JSONResponse(
                status_code=400,
                content=_envelope(
                    code="BAD_REQUEST",
                    message="Malformed request body.",
                ),
            )
        return JSONResponse(
            status_code=422,
            content=_envelope(
                code="VALIDATION_ERROR",
                message="Request validation failed.",
                details=errors,
            ),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.exception("Unhandled exception on %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=500,
            content=_envelope(
                code="INTERNAL_ERROR",
                message="An unexpected error occurred.",
            ),
        )
```

**Why `StarletteHTTPException` (not `fastapi.HTTPException`):** FastAPI's
`HTTPException` inherits from Starlette's. Registering on the Starlette base
catches both and routes every HTTP error through the envelope, including 401s raised
by the auth dependency so their `headers` dict flows through.

**Why `uuid.uuid4()` per call, not a request-scoped var:** At Phase 1 with a single
handler per error, a fresh UUID per response is sufficient for log correlation.
A request-ID middleware is the next step when multiple handlers need the same ID.

---

## 3. Auth dependency — bearer token (ADR-018 §7)

**Rule:** Bearer token in `Authorization` header. 401 MUST set
`WWW-Authenticate: Bearer`. Format-agnostic — do not validate JWT internals here
(SSO decision deferred to #73/#48b).

```python
# src/rl/app/api/dependencies/auth.py
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

_bearer = HTTPBearer(auto_error=False)


def require_bearer(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> str:
    """Return the raw bearer token string, or raise 401."""
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials
```

Usage in a router:

```python
from fastapi import APIRouter, Depends
from rl.app.api.dependencies.auth import require_bearer

router = APIRouter()

@router.post("/skeletons", status_code=200)
async def create_skeleton(
    _token: str = Depends(require_bearer),
    ...
) -> ...:
    ...
```

**Why `auto_error=False`:** Lets our dependency raise with the correct envelope
(`WWW-Authenticate` header included) rather than FastAPI's built-in 403.

**Simpler alternative — `auto_error=True` (default):** `HTTPBearer` has a built-in
`make_not_authenticated_error()` that raises `HTTPException(status_code=401,
headers={"WWW-Authenticate": "Bearer"})` automatically when no token is present.
With `auto_error=True`, our `StarletteHTTPException` handler catches it and passes
`exc.headers` through — so the envelope and `WWW-Authenticate` both land correctly
with less code. Use `auto_error=False` only when you need a custom 401 detail message.

**Placeholder note (Option B — #78 pending):** Token validation (signature check,
audience, expiry) is a placeholder until the SSO decision (#73/#48b) resolves the
provider and token format. The bearer-pattern wiring above is final; the
verification logic inside `require_bearer` will be updated when #73/#48b closes.

---

## 4. `trace_id` and observability

Each error response gets a fresh `trace_id` (UUID). At Phase 1 this is sufficient.
When structured logging lands, emit the same UUID as a log field on every
`logger.exception(...)` call inside the unhandled exception handler so logs and
responses are correlated.

Do not pass `trace_id` to domain functions — it is an API-layer concern.

---

## Checklist before PR

- [ ] `register_exception_handlers` called inside `create_app`, not at module level
- [ ] No per-route `try/except` producing error responses
- [ ] `StarletteHTTPException` handler passes `headers` from the exception (needed for `WWW-Authenticate`)
- [ ] `RequestValidationError` handler emits 400 for `json_invalid`, 422 otherwise
- [ ] `require_bearer` raises with `headers={"WWW-Authenticate": "Bearer"}`
- [ ] Unhandled exception handler logs with `logger.exception` (includes traceback in logs, not in response)
- [ ] `message` field in every envelope contains no class names, file paths, or stack fragments
