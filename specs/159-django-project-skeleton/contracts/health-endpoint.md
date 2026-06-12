# Contract: Health Endpoint

Infrastructure liveness probe. Not user-facing; consumed by `tasks/run-app.ps1` (dev)
and Cloud Run startup probes (#177, production).

The ADR-018 JSON envelope does NOT apply — this endpoint is not on the API surface
(`src/marker`). It is a bare liveness signal on the web surface (`src/web`), consistent
with the pattern established by `src/marker/api/health.py`.

## GET /health/

| Aspect | Contract |
|---|---|
| Method / path | `GET /health/` — the trailing-slash form is the ONLY contractual path; see Probe path rule |
| Auth | None. No session, cookie, or header required |
| Host precondition | The endpoint answers only when the request's Host header passes Django's `ALLOWED_HOSTS` validation. With the startproject baseline this slice ships (`ALLOWED_HOSTS = []`, `DEBUG=True`), only localhost variants pass; with `DEBUG=False` and an empty list, EVERY request — including probes — returns 400. The deployed value is owned by #177 (deploy-time env) and #161 (durable env-sourced setting). *(RT finding F-001/F-006.)* |
| Success | `200 OK`, `Content-Type: application/json` |
| Body | `{"status": "healthy"}` — JSON-equality asserted, not byte-equality (serialiser whitespace may vary) |
| Side effects | None — no DB read/write, no session creation |

## Probe path rule (binding on #177)

Probes MUST request the literal `/health/`. The no-slash `/health` form is FORBIDDEN
for probes: Cloud Run treats any 2xx/3xx as success without following redirects, so
the `APPEND_SLASH` 301 would pass the probe without ever executing the view — a
broken view still probes healthy. The redirect itself is not contractual: it exists
only while `CommonMiddleware` is installed and `APPEND_SLASH = True`, both of which
may be touched by #161 (settings rewrite) and #176 (envelope middleware), and Django
does not pin the redirect status code. Additionally, the probe bypasses Cloud Run's
front door (measured 2026-06-12: link-local connect, no request-log entry), so its
Host header carries no front-end guarantee and its default is undocumented — the
Terraform probe MUST therefore also pin an explicit Host via `httpHeaders` matching
an `ALLOWED_HOSTS` entry, or the deploy can fail at the probe itself. *(RT finding F-003; the staging Terraform probe is
currently `path = "/health"` for the FastAPI image — it must change to `/health/` in
the same change that swaps the image, `cloud_run.tf` at #177.)*

## Comparison rule

Assert JSON-equality (parse, then compare the object), never byte-equality.
`JsonResponse` default serialises compact; a literal string match against
pretty-printed spec form will fail.

## Consumers

| Consumer | Tolerance |
|---|---|
| `tasks/run-app.ps1` (no parameters — always starts both apps, FR-008) | Polls up to 30 × 1 s; 200 = ready, else the script exits non-zero |
| `tests/web/test_skeleton.py` | Asserts 200 + `application/json` + JSON-equal body |
| Cloud Run startup probe (#177) | Literal `/health/` only (Probe path rule); 10 s initial delay, 3 failures × 5 s timeout (same as marker probe) |

## Out of contract

- No `{"checks": [...]}` sub-system detail (database, cache) — that is a later task
  once #164 (database) lands. This probe is liveness only, not readiness.
- No rate-limit exemption header needed at dev time; Cloud Run does not rate-limit
  its own startup probes.
