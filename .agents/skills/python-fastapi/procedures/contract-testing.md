# Contract Testing — ADR-018 HTTP Clauses

ADR-018-specific test assertions for external FastAPI endpoints.
**Load alongside `python-testing-api`** — this procedure covers only the gaps not
addressed by that skill (binary responses, error envelope shape, auth headers,
400/422 distinction). Do not duplicate the general mocking strategy, TestClient
setup, or SSE parsing documented there.

**Live standard:** `docs/architecture/api/http-api-standard.md` §3, §4, §6, §7

---

## 1. Auth rejection — 401 with `WWW-Authenticate: Bearer` (§7)

Every external router module MUST have one test asserting 401 (not 403) when no
credentials are provided, and that the response includes the required header.

```python
class TestCreateSkeleton:

    def test_rejects_unauthenticated_with_401_and_www_authenticate(self, app):
        """Unauthenticated POST /skeletons returns 401 with WWW-Authenticate: Bearer."""
        client = TestClient(app)

        response = client.post("/skeletons", json={"project_name": "Acme"})

        assert response.status_code == 401
        assert response.headers.get("www-authenticate") == "Bearer"
```

Do not use `api_v1_client` here — that fixture overrides the auth dependency.
Use a raw `TestClient(app)` so the real dependency runs.

---

## 2. Error envelope shape (§3)

Assert the envelope shape on any error response. One test per status code that
an endpoint can produce.

```python
    def test_422_uses_error_envelope(self, api_v1_client):
        """Missing required field returns 422 with the uniform error envelope."""
        response = api_v1_client.post("/skeletons", json={})

        assert response.status_code == 422
        body = response.json()
        assert {"code", "message", "trace_id"} <= body.keys()
        assert isinstance(body["code"], str) and body["code"]
        assert isinstance(body["message"], str) and body["message"]
        assert isinstance(body["trace_id"], str) and body["trace_id"]

    def test_500_envelope_contains_no_internal_detail(self, api_v1_client, mocker):
        """Unhandled exception returns 500; message must not leak internals."""
        mocker.patch(
            "marker.api.routers.skeletons.build_skeleton",
            side_effect=RuntimeError("internal DB path /data/db crashed"),
        )

        response = api_v1_client.post("/skeletons", json={"project_name": "Acme"})

        assert response.status_code == 500
        body = response.json()
        assert {"code", "message", "trace_id"} <= body.keys()
        # message must not contain stack traces, file paths, or class names
        for forbidden in ("/data", "RuntimeError", "Traceback", 'File "'):
            assert forbidden not in body["message"]
```

---

## 3. 400 vs 422 distinction (§4)

One test confirming a malformed (unparsable) body → 400, not 422.

```python
    def test_400_for_malformed_json_body(self, api_v1_client):
        """Malformed JSON body returns 400 Bad Request (not 422)."""
        response = api_v1_client.post(
            "/skeletons",
            content=b"{not valid json",
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code == 400
        body = response.json()
        assert body["code"] == "BAD_REQUEST"
        assert {"code", "message", "trace_id"} <= body.keys()
```

Note: pass raw `content=` bytes with an explicit `Content-Type` header.
Using `json=` would have `TestClient` encode valid JSON, bypassing the parse error.

---

## 4. Binary DOCX response (§5, §6)

Assert status code, Content-Type, Content-Disposition, and that the body is raw
bytes (not a JSON envelope).

```python
    def test_returns_docx_bytes_with_correct_headers(self, api_v1_client, mocker):
        """POST /skeletons returns 200 with raw DOCX bytes and correct headers."""
        fake_docx = b"PK\x03\x04" + b"\x00" * 100  # minimal ZIP/DOCX magic
        mocker.patch(
            "marker.api.routers.skeletons.build_skeleton",
            return_value=fake_docx,
        )

        response = api_v1_client.post("/skeletons", json={"project_name": "Acme"})

        assert response.status_code == 200
        assert response.headers["content-type"] == (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        disposition = response.headers["content-disposition"]
        assert "attachment" in disposition
        assert ".docx" in disposition
        # body is raw bytes, not a JSON envelope
        assert response.content[:4] == b"PK\x03\x04"
```

`b"PK\x03\x04"` is the ZIP local file header — present in every valid `.docx`.
Using the magic number confirms the response body is a real binary artifact,
not a JSON-wrapped base64 string.

---

## 5. Exception handler coverage (§3)

Three patterns from the notebook for testing custom `@app.exception_handler`
registrations. These complement the envelope-shape test in §2 above.

**Pattern A — `RequestValidationError` override:** Confirm the custom handler
intercepts validation failures and returns the envelope (not FastAPI's default body).

```python
def test_validation_handler_returns_envelope(self, api_v1_client):
    """Pydantic validation failure returns the uniform error envelope, not FastAPI default."""
    response = api_v1_client.post("/skeletons", json={})  # missing required fields

    body = response.json()
    # FastAPI's default 422 body has a "detail" key, not "code"
    assert "detail" not in body
    assert "code" in body and "message" in body and "trace_id" in body
```

**Pattern B — Unhandled exception envelope:** Confirm the catch-all `Exception`
handler returns 500 with the envelope and no internal detail in `message`.

```python
def test_unhandled_exception_returns_safe_500(self, api_v1_client, mocker):
    """RuntimeError in handler produces 500 envelope with no internal detail."""
    mocker.patch(
        "marker.api.routers.skeletons.build_skeleton",
        side_effect=RuntimeError("pg: connection refused at /var/run/pg"),
    )

    response = api_v1_client.post("/skeletons", json={"project_name": "Acme"})

    assert response.status_code == 500
    body = response.json()
    assert {"code", "message", "trace_id"} <= body.keys()
    # Path and class name must not appear in the safe message
    for fragment in ("/var/run", "RuntimeError", "Traceback", 'File "'):
        assert fragment not in body["message"]
```

**Pattern C — `StarletteHTTPException` handler passes headers:** Confirm a raised
`HTTPException` with custom headers (e.g., `WWW-Authenticate`) flows the headers
through to the response.

```python
def test_401_headers_flow_through_envelope_handler(self, app):
    """HTTPException headers (WWW-Authenticate) survive the global exception handler."""
    client = TestClient(app)

    response = client.post("/skeletons", json={"project_name": "Acme"})

    assert response.status_code == 401
    assert response.headers.get("www-authenticate") == "Bearer"
    # Envelope shape must also be correct (not just the header)
    body = response.json()
    assert {"code", "message", "trace_id"} <= body.keys()
```

---

## 6. OpenAPI contract test (§12)

One test per app that the generated schema is structurally valid.
This is already in `python-testing-api` — do not duplicate it.
If it is not yet present in the test suite, add it:

```python
from openapi_spec_validator import validate


def test_openapi_schema_is_valid(api_v1_client):
    """Generated OpenAPI schema passes structural validation."""
    response = api_v1_client.get("/openapi.json")

    assert response.status_code == 200
    validate(response.json())
```

---

## Clause coverage checklist (add to PR description)

| ADR-018 clause | Test exists? |
|---|---|
| §1 — plural URI | covered by router path (no dedicated test needed) |
| §3 — error envelope shape | `test_422_uses_error_envelope`, `test_500_envelope_contains_no_internal_detail` |
| §3 — exception handler intercepts (not FastAPI default) | `test_validation_handler_returns_envelope`, `test_unhandled_exception_returns_safe_500`, `test_401_headers_flow_through_envelope_handler` |
| §4 — 400 vs 422 | `test_400_for_malformed_json_body` |
| §6 — binary bytes, correct headers | `test_returns_docx_bytes_with_correct_headers` |
| §7 — 401 + `WWW-Authenticate` | `test_rejects_unauthenticated_with_401_and_www_authenticate` |
| §12 — OpenAPI generated | `test_openapi_schema_is_valid` |
