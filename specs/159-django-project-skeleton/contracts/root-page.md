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
- No health endpoint is added or moved. The existing API health path is owned by
  `src/marker` until the pivot reaches it (ADR-018 surface, later tasks).
- HTTP method behaviour other than GET on `/` follows framework defaults (405/404);
  downstream tasks may change it without ceremony.
