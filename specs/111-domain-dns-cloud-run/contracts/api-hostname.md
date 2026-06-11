# Contract: Public API Hostname

The external interface this feature exposes is an addressing contract, not a new HTTP
API (the HTTP surface itself is governed by ADR-018).

## Contract

| Item | Value |
|------|-------|
| Canonical public base URL | `https://api.redmarklogic.com` |
| Stability | Volatile by default (Constitution XIII) until declared stable by ADR; clients told to treat the hostname (not the run.app URL) as the address |
| TLS | Google-managed certificate, auto-renewing; HTTPS only |
| Plain HTTP | Firebase Hosting redirects HTTP to HTTPS (301) — FR-003 satisfied; verify at cutover |
| Request duration ceiling | 60 seconds at this hostname; longer requests receive HTTP 504 from the proxy layer (accepted POC constraint, recorded in the ADR) |
| Cookies | Stripped except the literal name `__session`; header auth (`Authorization: Bearer ...`) unaffected |
| WebSockets | Not supported through this hostname |
| Effective max body | Assume 32 MB (Cloud Run limit; proxy layer undocumented) |
| Bypass path | `https://prod-redline-api-*.run.app` remains reachable and is NOT part of this contract; same app-level auth applies |

## Consumer guidance

- Configure clients against `api.redmarklogic.com` only; the run.app URL can change
  if the service is recreated.
- Long-running operations (>60 s) are not served at this hostname until the front
  door is upgraded (separate, founder-approved task).
