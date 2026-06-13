# Contract: Root Placeholder Page

The only external interface this slice exposes. Volatile per Constitution XIII (no
`# stable:` declaration) — #171 replaces the body with the auth-gated button page.

## GET /

| Aspect | Contract |
|---|---|
| Method / path | `GET /` |
| Auth | None. No session, cookie, or header required (FR-006) |
| Success | `200 OK`, `Content-Type: text/html` |
| Body | Minimal placeholder HTML. Content is NOT contractual beyond being non-empty; no client may parse it |
| Side effects | None — no database read/write, no session creation |
| Error envelope | ADR-018 envelope does NOT apply: this is the web page surface, not the JSON API surface. Envelope middleware arrives with #176 |

## Out of contract (this slice)

- `/admin/` exists (startproject default, kept per ADR-024 admin-at-launch) but is
  non-functional until #164 (database) and #165 (identity) land. Not a promise.
- The slice's only other unauthenticated endpoint is `GET /health/` — contract in
  [health-endpoint.md](health-endpoint.md). Together these two files are the complete
  inventory of the slice's exposed surface. The existing API health path is owned by
  `src/marker` until the pivot reaches it (ADR-018 surface, later tasks). *(RT F-010.)*
- HTTP method behaviour other than GET is framework default and explicitly out of
  contract: Django's URLconf is method-blind (all methods route to the view), and
  unsafe methods without a CSRF token are rejected with 403 by `CsrfViewMiddleware`
  before the view runs — there is no 405. #171 (auth-gated page) replaces this view
  wholesale and defines its own method contract. *(RT F-004 — corrected; the earlier
  "405/404" claim was wrong, and `@require_GET` was rejected: CSRF fires first and
  the decorator would 405 HEAD probes.)*
