# Cloudflare zone snapshots — redmarklogic.com (issue #147 / ADR-027)

These are the **safety evidence** for the Firebase front-door teardown. The founder's
live email (MX / SPF) runs on the `redmarklogic.com` zone, so the teardown's single
DNS deletion (the `api` CNAME) must be proven to be the *only* zone change.

- **Pre-change snapshot** (Phase 0, FR-017): captured BEFORE `terraform apply`.
- **Post-change snapshot** (Phase 2, FR-019): captured AFTER apply.
- The `diff` of the two must show **exactly one record removed** — the
  `api CNAME redmarklogic-api.web.app` (id `6b051d1e36a71373819c95a89d1db64d`) — and
  **zero other changes**. Any other delta is a stop-the-line event.

## How to capture

```bash
cd docs/infrastructure/zone-snapshots
./capture-zone-snapshot.sh pre     # Phase 0 — before apply
# ... founder reviews plan diff, terraform apply runs ...
./capture-zone-snapshot.sh post    # Phase 2 — after apply
diff redmarklogic-zone-pre-*.json redmarklogic-zone-post-*.json
```

## Status (2026-06-12)

**NOT YET CAPTURED.** The capture is blocked on `gcloud` reauthentication: the active
ADC credentials returned "Reauthentication failed. cannot prompt during
non-interactive execution" when Brent tried to read the Cloudflare token from Secret
Manager. The founder (or operator) must run `gcloud auth login` interactively, then
run the `pre` capture above. See the handoff note in
`.agents/tmp/firebase-teardown-2026-06-12/HANDOFF.md`.
