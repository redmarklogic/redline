# Python Testing Api — Detailed Reference

## Procedure

1. Add or update endpoint tests under `tests/` mirroring router/server module structure.
2. Use `TestClient` with dependency overrides for component-level API behavior checks.
3. Mock non-DI external boundaries with `mocker.patch` (and `pytest-httpx` for outbound HTTP).
4. Assert status codes, response contracts, and key orchestration/error paths.
5. Add contract checks for DTO validation/OpenAPI where interface shape is critical.

### Directory structure

Mirror the source layout under `tests/`:

```text
tests/<package>/app/
    conftest.py                          # app fixture, shared mocks
    api/v1/
        conftest.py                      # api_v1_client fixture
        routers/
            test_health.py               # maps to src/.../routers/health.py
            test_items.py                # maps to src/.../routers/items.py
    mcp/v1/
        test_server.py                   # maps to src/.../mcp/v1/server.py
```

No `__init__.py` files are needed when pytest is configured with
`--import-mode=importlib`.

### Rules

- One test module per router/server module.
- Apply `pytestmark = pytest.mark.api_v1` in every API v1 test module (or <!-- hook: allow -->
  `pytest.mark.mcp_v1` for MCP v1 tests). These markers allow selective test execution. <!-- hook: allow -->
- **Group tests into classes per router** (e.g., `TestHealth`, `TestCreateItem`,
  `TestGetItem`). Classes group related tests, collapse nicely in the test runner,
  and allow class-scoped fixture overrides when needed.
- Place fixture layers strategically:
  - `tests/<package>/app/conftest.py` -- app-level fixtures (`app`, shared mocks).
  - `tests/<package>/app/api/v1/conftest.py` -- v1-specific fixtures (`api_v1_client`).

### App fixture

```python
from collections.abc import Generator

import pytest
from fastapi import FastAPI
from myapp.main import create_app


@pytest.fixture
def app() -> Generator[FastAPI, None, None]:
    """Provide the FastAPI application instance.

    Function scope is mandatory — dependency_overrides.clear() in teardown
    ensures overrides set by one test cannot leak into the next test.
    """
    application = create_app()
    yield application
    application.dependency_overrides.clear()
```

The teardown call to `dependency_overrides.clear()` ensures test isolation when overrides
are applied.

### Client fixture

Use `TestClient` from `fastapi.testclient` (sync, built on `requests`) for component
tests. Reserve `httpx.AsyncClient` with `ASGITransport` for async in-process tests:

```python
from httpx import ASGITransport, AsyncClient

async def test_async_endpoint(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
```

`ASGITransport` runs against the ASGI app in-process — no live server required.
Do not point `AsyncClient` at a real running server for component tests.

**Bypass authentication via `dependency_overrides`** -- do not read the real API key from
config files. This decouples tests from deployment configuration and is the idiomatic
FastAPI approach.

```python
from fastapi.testclient import TestClient
from myapp.core.security import get_api_key


@pytest.fixture
def api_v1_client(app):
    """Provide a TestClient with API key auth bypassed via dependency override."""
    app.dependency_overrides[get_api_key] = lambda: "test-key"
    return TestClient(app)
```

Tests should include the versioned prefix in request paths
(e.g., `/api/v1/health`), since `TestClient` does not prepend a path component
automatically.

### Shared mock fixtures

When the same patches are needed across multiple test classes, define them as **explicit
fixtures in conftest** (not `autouse`). Request them by name in each test so dependencies
are visible.

```python
from pathlib import Path


@pytest.fixture
def mock_storage_setup(mocker):
    """Patch storage path resolution and config loading for isolation."""
    mocker.patch(
        "myapp.api.v1.routers.items._resolve_storage_path",
        return_value=Path("dummy/storage"),
    )
    mocker.patch(
        "myapp.api.v1.routers.items._load_config",
        return_value={"bucket": "test"},
    )
```

Place shared fixtures at `tests/<package>/app/conftest.py` so all test modules can use
them.

**`autouse=True` — when it is legitimate:** Use `autouse=True` only for
*environmental* setup that must run before every test regardless of what is being
tested — for example, creating test database tables or seeding a filesystem. For
*behavioural* dependencies (mocks, patches, return-value overrides), always request
fixtures by name so the dependency graph is visible at the call site.

## Mocking Strategy (Hybrid)

This repo uses a hybrid mocking approach:

| What to mock                                  | Technique                  |
| --------------------------------------------- | -------------------------- |
| `Depends()` callables (auth, DB sessions)     | `app.dependency_overrides` |
| Module-level functions in endpoint call chain | `mocker.patch()`           |
| Outbound HTTP calls made by application code  | `pytest-httpx`             |

**Anti-pattern — over-mocking with `mocker.patch`:** Tests that rely heavily on
`mocker.patch` couple themselves to internal implementation structure, become brittle
when internals change, and can mask integration failures. Prefer `dependency_overrides`
whenever the dependency is declared via `Depends()`. Fall back to `mocker.patch` only
when DI is not available at that call site.

### `app.dependency_overrides` -- for FastAPI DI callables

Use for anything declared as a `Depends()` parameter in a router signature.

```python
from myapp.core.security import get_api_key


def test_endpoint_rejects_bad_key(app):
    """Endpoint returns 403 when the API key dependency rejects the request."""
    # Do NOT override the dependency -- let the real auth check run
    client = TestClient(app)

    response = client.get("/api/v1/health")

    assert response.status_code == 403
```

Always clear overrides in fixture teardown (the `app` fixture above handles this).

### `mocker.patch()` -- for non-DI functions

Use for patching business-logic generators, helper functions, and third-party SDK calls
that are not injected via `Depends()`.

```python
def test_create_item_calls_service(api_v1_client, mocker):
    """POST /items delegates to the item service and returns 201."""
    mocker.patch(
        "myapp.api.v1.routers.items.item_service.create",
        return_value={"id": 1, "name": "Widget"},
    )

    response = api_v1_client.post(
        "/api/v1/items", json={"name": "Widget"},
    )

    assert response.status_code == 201
```

Follows `mocker` from `pytest-mock` (never `unittest.mock`), consistent with the unit
testing skill.

### `pytest-httpx` -- for outbound HTTP

Use when application code makes HTTP calls (e.g., downloading a file from a URL). The
`pytest-httpx` library (add to the `test` dependency group — not present by default)
intercepts `httpx` calls without hitting the network.

```python
def test_fetch_remote_resource(httpx_mock):
    """Endpoint fetches the remote file when given a URL."""
    httpx_mock.add_response(
        url="https://example.com/data.csv",
        content=b"col1,col2\n1,2",
        headers={"content-type": "text/csv"},
    )
    # ... call the endpoint or helper that uses httpx internally
```

### What to test

- **Status codes**: correct codes for success, auth failure, validation failure.
- **Response body shape**: JSON structure matches expectations.
- **Header behavior**: content-type, custom headers.
- **Router orchestration**: the router calls the right downstream functions and handles
  errors correctly (verified via mocks and response assertions).
- **Auth rejection**: one test per router module confirming 403 without API key.

### What NOT to test here

- **Business logic** inside service/logic layers -- that belongs in unit tests.
- **Private helper functions** directly -- test them through the endpoint.
- **Framework internals** (FastAPI routing mechanics, Pydantic validation internals).
- **Database access** -- use `dependency_overrides` for session injection and test the
  query logic in dedicated repository tests.

### Testing pure helper functions

If a router module contains **pure functions with no I/O** (e.g., a serialiser or
formatter), test them as standard unit tests in the same test module. No `TestClient`
needed.

```python
from myapp.api.v1.routers.items import format_sse_event


class TestFormatSseEvent:
    """Unit tests for the SSE frame serializer."""

    def test_serializes_event_to_sse_frame(self):
        """format_sse_event produces a valid SSE frame."""
        event = {"type": "progress", "data": {"status": "Processing"}}

        result = format_sse_event(event)

        assert result == 'event: progress\ndata: {"status": "Processing"}\n\n'
```

### Examples

#### Simple GET endpoint

```python
import pytest
from fastapi.testclient import TestClient

API_V1_PREFIX = "/api/v1"

pytestmark = pytest.mark.api_v1 <!-- hook: allow -->


class TestHealth:
    """Component tests for GET /api/v1/health."""

    def test_returns_200(self, api_v1_client):
        """Health endpoint returns 200."""
        response = api_v1_client.get(f"{API_V1_PREFIX}/health")

        assert response.status_code == 200

    def test_returns_status_and_timestamp(self, api_v1_client, mocker):
        """Health response contains status and timestamp."""
        mock_dt = mocker.patch("myapp.api.v1.routers.health.datetime")
        mock_dt.now.return_value.isoformat.return_value = "2025-01-01T00:00:00+00:00"

        response = api_v1_client.get(f"{API_V1_PREFIX}/health")

        assert response.json() == {
            "status": "healthy",
            "timestamp": "2025-01-01T00:00:00+00:00",
        }

    def test_rejects_without_api_key(self, app):
        """Requests without a valid API key receive 403."""
        client = TestClient(app)

        response = client.get(f"{API_V1_PREFIX}/health")

        assert response.status_code == 403
```

#### POST with file upload

```python
class TestUploadFile:
    """Component tests for POST /api/v1/items/upload."""

    @pytest.mark.usefixtures("mock_storage_setup", "mock_item_service") <!-- hook: allow -->
    def test_returns_200_on_success(self, api_v1_client):
        """File upload returns 200."""
        files = {
            "file": (
                "report.docx",
                b"dummy content",
                "application/vnd.openxmlformats-officedocument"
                ".wordprocessingml.document",
            )
        }

        response = api_v1_client.post(
            f"{API_V1_PREFIX}/items/upload",
            files=files,
        )

        assert response.status_code == 200

    def test_rejects_without_api_key(self, app):
        """Requests without API key receive 403."""
        client = TestClient(app)
        files = {"file": ("test.docx", b"dummy", "application/octet-stream")}

        response = client.post(
            f"{API_V1_PREFIX}/items/upload",
            files=files,
        )

        assert response.status_code == 403
```

#### POST with JSON body

```python
class TestCreateItem:
    """Component tests for POST /api/v1/items."""

    def test_returns_201_on_success(self, api_v1_client, mocker):
        """Valid payload returns 201 with created item."""
        mocker.patch(
            "myapp.api.v1.routers.items.item_service.create",
            return_value={"id": 1, "name": "Widget"},
        )

        response = api_v1_client.post(
            f"{API_V1_PREFIX}/items",
            json={"name": "Widget"},
        )

        assert response.status_code == 201

    def test_rejects_without_api_key(self, app):
        """Requests without API key receive 403."""
        client = TestClient(app)

        response = client.post(
            f"{API_V1_PREFIX}/items",
            json={"name": "Widget"},
        )

        assert response.status_code == 403
```

#### Validation rejection (invalid Pydantic payload)

```python
    def test_rejects_missing_required_field(self, api_v1_client):
        """Endpoint returns 422 when a required field is missing."""
        response = api_v1_client.post(
            f"{API_V1_PREFIX}/items",
            json={},
        )

        assert response.status_code == 422
```

#### Validation rejection (extra fields with `extra="forbid"`)

```python
    def test_rejects_extra_fields(self, api_v1_client):
        """Endpoint returns 422 when unexpected fields are sent."""
        payload = {
            "name": "Widget",
            "unexpected_field": "value",
        }

        response = api_v1_client.post(
            f"{API_V1_PREFIX}/items",
            json=payload,
        )

        assert response.status_code == 422
```

#### Using `@pytest.mark.usefixtures` for side-effect fixtures <!-- hook: allow -->

When a fixture is needed only for its patch side effect (not return value), use
`@pytest.mark.usefixtures()` instead of adding unused parameters. This avoids <!-- hook: allow -->
lint warnings (`ARG002`) and makes the test signature cleaner.

```python
    @pytest.mark.usefixtures("mock_storage_setup", "mock_item_service") <!-- hook: allow -->
    def test_returns_200_on_success(self, api_v1_client):
        """Endpoint succeeds when all dependencies are mocked."""
        response = api_v1_client.post(
            f"{API_V1_PREFIX}/items",
            json={"name": "Widget"},
        )

        assert response.status_code == 200
```

### Pattern: module-level `parse_sse_events` helper

`TestClient` buffers the full response by default. Access the streamed content via
`response.text`, then parse SSE frames with a **module-level helper** defined at the top
of each test module that needs it (or in `conftest.py` for wider reuse).

```python
import json


def parse_sse_events(raw: str) -> list[dict]:
    """Parse raw SSE text into a list of event dicts.

    Each SSE frame is separated by a blank line. Lines starting with
    ``event:`` and ``data:`` are extracted.
    """
    events = []
    for frame in raw.strip().split("\n\n"):
        event = {}
        for line in frame.strip().split("\n"):
            if line.startswith("event: "):
                event["type"] = line[len("event: "):]
            elif line.startswith("data: "):
                event["data"] = json.loads(line[len("data: "):])
        if event:
            events.append(event)
    return events
```

### Example: assert on streamed events

```python
class TestProcessItems:
    @pytest.mark.usefixtures("mock_storage_setup") <!-- hook: allow -->
    def test_streams_progress_and_result(
        self, api_v1_client, mocker,
    ):
        """Processing endpoint streams progress then result events."""
        async def mock_generator(*_args, **_kwargs):
            yield {"type": "progress", "data": {"status": "Processing"}}
            yield {"type": "result", "data": {"message": "Done"}}

        mocker.patch(
            "myapp.api.v1.routers.items.process_items",
            new=mocker.MagicMock(side_effect=mock_generator),
        )

        response = api_v1_client.post(
            "/api/v1/items/process", json={"ids": [1, 2]},
        )

        assert response.status_code == 200
        events = parse_sse_events(response.text)
        assert events[0]["type"] == "progress"
        assert events[0]["data"]["status"] == "Processing"
        assert events[1]["type"] == "result"
        assert events[1]["data"]["message"] == "Done"
```

### Testing error paths through SSE

When a downstream call raises, the endpoint should stream an error event rather than
returning a non-200 status. Test this by patching the failing dependency:

```python
    def test_streams_error_on_service_failure(
        self, api_v1_client, mock_storage_setup, mocker,
    ):
        """Endpoint streams an error event when the service raises."""
        mocker.patch(
            "myapp.api.v1.routers.items._fetch_remote_data",
            new=mocker.AsyncMock(side_effect=ValueError("Connection refused")),
        )

        response = api_v1_client.post(
            "/api/v1/items/process", json={"ids": [1]},
        )

        events = parse_sse_events(response.text)
        assert events[0]["type"] == "error"
```

Place `parse_sse_events` at module level in the test file that needs it, or in
conftest for wider reuse across multiple test modules.

### Testing Auth Guards

Every endpoint that requires authentication must have tests that verify the guard
rejects correctly — not just that the happy path accepts a valid token.

**Pattern 1 — Component-level rejection (one test per router):**

```python
def test_rejects_unauthenticated(self, app):
    """Endpoint returns 401 when no bearer token is provided."""
    client = TestClient(app)  # raw client, no auth override

    response = client.post("/skeletons", json={"project_name": "Acme"})

    assert response.status_code == 401
    assert response.headers.get("www-authenticate") == "Bearer"
```

Use a raw `TestClient(app)` — not the `api_v1_client` fixture — so the real
auth dependency runs. This test confirms the dependency is wired to the router,
not just that it exists.

**Pattern 2 — Adversarial tests (at least one per security scheme):**

Write at least one test per auth scheme that exercises an invalid credential scenario:

```python
def test_rejects_malformed_token(self, app):
    """Endpoint returns 401 when the Authorization header value is not a bearer token."""
    client = TestClient(app, headers={"Authorization": "NotBearer xyz"})

    response = client.post("/skeletons", json={"project_name": "Acme"})

    # FastAPI's HTTPBearer rejects non-Bearer schemes
    assert response.status_code in (401, 403)
```

**Pattern 3 — Property-based auth testing with Schemathesis (gate-pending):**

Schemathesis reads the auto-generated `openapi.json` and generates large volumes of
test data automatically, including adversarial inputs for authenticated endpoints.

```python
import schemathesis

schema = schemathesis.from_pytest_fixture("api_v1_client")

@schema.parametrize()
def test_api_schema_conformance(case):
    case.call_and_validate()
```

> **Gate:** Schemathesis (`schemathesis>=3.0`) must be present in the `test` dependency
> group in `pyproject.toml` before this pattern is used — confirm the declaration exists
> before implementing (assumption, not yet verified). It also requires **the principal engineer's explicit
> approval** before being used in active test suites — it touches the OpenAPI contract
> surface and generates requests that may hit real downstream services if dependency
> overrides are not set. Add the `@schema.parametrize()` tests only after both the
> dependency and the gate are confirmed.

---

### Testing Binary File Download Responses

For endpoints returning binary artifacts (e.g., `POST /skeletons` returning a `.docx`),
status code alone is insufficient. Assert the full download contract.

```python
def test_returns_docx_binary_with_correct_headers(self, api_v1_client, mocker):
    """POST /skeletons returns 200 with raw DOCX bytes and correct download headers."""
    fake_docx = b"PK\x03\x04" + b"\x00" * 100  # ZIP/DOCX magic header
    mocker.patch(
        "marker.api.routers.skeletons.build_skeleton",
        return_value=fake_docx,
    )

    response = api_v1_client.post("/skeletons", json={"project_name": "Acme"})

    assert response.status_code == 200
    assert response.headers["content-type"] == (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    assert "attachment" in response.headers["content-disposition"]
    assert ".docx" in response.headers["content-disposition"]
    assert len(response.content) > 0
    # DOCX is a ZIP — PK\x03\x04 is the local file header magic number
    assert response.content[:4] == b"PK\x03\x04"
```

**What to assert:**

| Assertion | What it catches |
|---|---|
| `response.content[:4] == b"PK\x03\x04"` | Binary bytes in body, not base64/JSON-wrapped |
| `content-type` exact match | Wrong MIME type (e.g., `application/octet-stream`) |
| `"attachment" in content-disposition` | Browser download prompt triggered (inline rendering suppressed) |
| `".docx" in content-disposition` | Filename extension correct |
| `len(response.content) > 0` | Empty body (generation returned nothing) |

Use `response.content` (bytes) not `response.text` for binary assertions.

---

### 1. Pydantic DTO validation tests

Test request/response models directly to confirm the contract holds:

```python
import pytest
from pydantic import ValidationError

from myapp.core.models.items import CreateItemRequest


class TestCreateItemRequestContract:
    """Contract tests for CreateItemRequest."""

    def test_valid_payload_accepted(self):
        """Model accepts a valid payload."""
        req = CreateItemRequest(name="Widget")

        assert req.name == "Widget"

    def test_missing_required_field_rejected(self):
        """Model rejects payload missing a required field."""
        with pytest.raises(ValidationError):
            CreateItemRequest()  # 'name' is required

    def test_extra_fields_rejected(self):
        """Model rejects extra fields (extra='forbid')."""
        with pytest.raises(ValidationError, match="extra_forbidden"):
            CreateItemRequest(
                name="Widget",
                unexpected="value",
            )
```

This tests the shape of the data contract independent of the HTTP layer. Keep DTO tests
in a dedicated module (e.g., `tests/<package>/app/core/models/test_items.py`) mirroring
the source path.

For the relationship between API DTOs and domain models, use the `python-domain-modeling` skill — they must be separate classes.

### 2. OpenAPI specification validation

Validate that the generated OpenAPI schema is structurally correct:

```python
from openapi_spec_validator import validate


def test_openapi_schema_is_valid(api_v1_client):
    """Generated OpenAPI schema passes structural validation."""
    response = api_v1_client.get("/api/v1/openapi.json")

    assert response.status_code == 200
    validate(response.json())  # raises on invalid schema
```

`openapi-spec-validator` must be added to the `test` dependency group (not present by default — only `schemathesis` ships in `test`). This single test catches
schema regressions (missing response models, invalid refs, broken examples) automatically.

# API Testing

This skill defines conventions for testing FastAPI endpoints. It covers two
complementary test types: **API Component Testing** (endpoint behavior in isolation) and
**Contract Testing** (schema/shape enforcement via Pydantic and OpenAPI).

For general testing philosophy (Arrange/Act/Assert, equivalence classes, parametrize
guidelines, mocking boundaries), use the `python-testing-unit` skill — this skill does **not** duplicate those
rules.

## Scope

Apply these rules when writing or updating tests for FastAPI router modules and
MCP server tools.

API component tests are technically thin integration tests -- they spin up the ASGI app
in-process via `TestClient` -- but they still follow the rigorous assertion standards from
the unit testing skill.

## Test Placement & Organization

## Core Fixtures

## API Component Testing

## Testing SSE / Streaming Responses

The main endpoints return `StreamingResponse` with `media_type="text/event-stream"`.
Testing only the status code is insufficient -- verify the **content** of the stream.

## Contract Testing (Lightweight)

Treat Pydantic as the contract enforcement layer. Dedicated consumer-driven
contract testing tools (e.g., Pact) are out of scope unless external consumers explicitly
require version-locked contracts.

## Design Decisions

| #   | Decision             | Choice                                               | Rationale                                                      |
| --- | -------------------- | ---------------------------------------------------- | -------------------------------------------------------------- |
| 1   | Auth mocking         | `dependency_overrides`                               | Idiomatic FastAPI; decouples from deployment config            |
| 2   | Mocking depth        | Mock everything except the router                    | Tests router orchestration; avoids coupling to internals       |
| 3   | SSE assertions       | Parse and assert frame content                       | Status code alone is insufficient for streaming endpoints      |
| 4   | Pure helpers         | Unit-test directly; private helpers through endpoint | Pure formatters are testable in isolation; I/O helpers are not |
| 5   | Test grouping        | Classes per router                                   | Collapse in runner; class-scoped fixture overrides             |
| 6   | Auth rejection scope | One test per router module                           | Confirms dependency wiring per router                          |
| 7   | Private helpers      | Keep private, test through endpoint                  | Preserves encapsulation                                        |
| 8   | Shared mocks         | Explicit fixtures in conftest                        | Visible dependency graph; no hidden `autouse` side effects     |
