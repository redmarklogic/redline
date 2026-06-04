---
name: python-testing-api
description: Use when writing API component tests or contract tests for FastAPI endpoints in this repo
paths: "src/**/*.py,tests/**/*.py"
---

## Boundary Contract

### Applies To
- FastAPI endpoint tests (component tests and contract tests) under `tests/`

### Produces
- Isolated API tests with schema enforcement via Pydantic and OpenAPI

### Does Not Cover
- General unit testing conventions (`python-testing-unit`)
- TDD workflow (`test-driven-development`)
- Function design (`python-function-design`)

## Quick Reference

| Aspect                        | Convention                                                  |
| ----------------------------- | ----------------------------------------------------------- |
| **Test framework**            | `pytest`                                                    |
| **HTTP client (component)**   | `fastapi.testclient.TestClient` (sync)                      |
| **HTTP client (integration)** | `httpx.AsyncClient` (async, hits running server)            |
| **DI mocking**                | `app.dependency_overrides` for `Depends()` callables        |
| **Function mocking**          | `mocker.patch()` via `pytest-mock`                          |
| **Outbound HTTP mocking**     | `pytest-httpx`                                              |
| **Marker (API v1)**           | `pytestmark = pytest.mark.api_v1`                           | <!-- hook: allow -->
| **Marker (MCP v1)**           | `pytestmark = pytest.mark.mcp_v1`                           | <!-- hook: allow -->
| **DTO contract tests**        | Test Pydantic models directly with `ValidationError`        |
| **OpenAPI contract test**     | `openapi-spec-validator` against `/openapi.json`            |
| **SSE parsing**               | Module-level `parse_sse_events()` helper                    |
| **Test grouping**             | One class per router (e.g., `TestHealth`, `TestCreateItem`) |
| **Auth rejection**            | One `test_rejects_without_api_key` per router module        |


See `procedures/python-testing-api.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Testing internal implementation details instead of the HTTP contract | Test request/response shape, status codes, and headers — not internal service calls |
| Using a real database in an API component test | Use an in-memory or test database with fixtures; isolate the API layer from persistence |
| Asserting on the full response body when only one field matters | Assert on the specific field; brittle full-body assertions break on unrelated changes |