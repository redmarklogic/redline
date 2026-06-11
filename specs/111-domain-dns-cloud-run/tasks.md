# Tasks: Connect api.redmarklogic.com to Cloud Run Backend via Cloudflare DNS

**Input**: [plan.md](plan.md)
**Prerequisites**: Spec + plan in this directory; Cloudflare account access (founder);
Phase 2 additionally requires the deployed service from issue #110 (native blocked-by
link on the board).

> Infra feature: no Python function work, so the TDD test-first sections are replaced
> by evidence-capture tasks — every phase still ends in a hard Acceptance Gate with a
> runnable verification. User-story mapping: US1 -> Phase 2, US2 -> Phases 0-2
> (evidence), US3 -> Phase 3.

## Phase 0: Governance + evidence baseline

**Purpose**: ADR accepted and pre-change evidence captured — safe to touch infrastructure.

- [ ] T001 [Phase 0] Write ADR `docs/adr/adr-0NN-firebase-hosting-api-domain.md`: D1-D8 from plan.md Design Decisions (Firebase Hosting adoption, 60 s ceiling, grey-cloud rule, run.app bypass, $0 posture + $0.15/GB egress caveat, no-npm constraint); cross-reference ADR-020/021/022 and issue #73; explicitly amend ADR-022's "No Secret Manager entries needed at this stage" statement (the Cloudflare token in T002 is the first entry); run `check-adr-constitution-sync` hook outcome into the same commit if it demands a constitution update
- [ ] T002 [P] [Phase 0] Create scoped Cloudflare API token (dashboard — documented manual exception): Zone:DNS:Edit + Zone:Zone:Read on redmarklogic.com only; store as Secret Manager entry per ADR-021 naming; record the storage step (not the token) in `docs/infrastructure/domain-dns-runbook.md` draft
- [ ] T003 [Phase 0] Capture pre-change zone snapshot to `docs/infrastructure/zone-snapshot-pre-2026-06-DD.txt` via `GET /zones/{zone_id}/dns_records/export` (commands in [quickstart.md](quickstart.md)); commit; confirm MX records present in the file AND confirm no pre-existing record of any type exists on `api.redmarklogic.com` (spec edge case — abort and resolve with founder if one is found) (depends on T002)

### Acceptance Gate

- [ ] T004 [Phase 0] Verify: ADR merged with constitution-sync hook green; zone ID + snapshot committed; `curl -s ".../zones?name=redmarklogic.com"` with the stored token returns `success:true`

---

## Phase 1: Terraform — Firebase + Cloudflare DNS (no service dependency)

**Purpose**: Hostname attached and certificate provisioning underway, entirely from HCL.

- [ ] T005 [Phase 1] Verify provider schemas against registries before authoring (research.md open item 1): `google_firebase_hosting_version` rewrite `run` block support; `cloudflare_dns_record` (v5) vs `cloudflare_record` (v4) naming; record verdict + chosen pins in `deploy/infra/terraform/versions.tf` and note the D6 path taken (Terraform release vs standalone-binary CI fallback) in the runbook draft
- [ ] T006 [Phase 1] Author `deploy/infra/terraform/firebase_hosting.tf`: `google_firebase_project` (redmarklogic-prod), `google_firebase_hosting_site` (redmarklogic-api), `google_firebase_hosting_custom_domain` (api.redmarklogic.com, google-beta, `wait_dns_verification = false`), outputs exposing `required_dns_updates`; plus rewrite `hosting_version`/`_release` if T005 confirmed the schema (depends on T005)
- [ ] T007 [P] [Phase 1] Author `deploy/firebase/firebase.json` (site redmarklogic-api, rewrite `**` -> prod-redline-api @ australia-southeast1) + empty `deploy/firebase/public/.gitkeep`; committed regardless of D6 path (it is the CI-fallback artifact and the human-readable statement of the rewrite)
- [ ] T008 [Phase 1] Author `deploy/infra/terraform/cloudflare_dns.tf`: cloudflare provider (token via env/Secret Manager, never HCL), `cloudflare_zone` data source by name, ownership TXT + A record(s) for `api` wired from `required_dns_updates` outputs, all `proxied = false` (depends on T005, T006)
- [ ] T009 [Phase 1] Apply: `terraform plan` (review: additive-only, no resources outside the new files + versions.tf) then `terraform apply`; two-step converge — apply, create records, refresh until domain verification accepted; capture cert state (depends on T006, T007, T008; gate T004 passed)

### Acceptance Gate

- [ ] T010 [Phase 1] Verify: `Resolve-DnsName api.redmarklogic.com -Type TXT` returns ownership value; re-export zone and `rtk git diff --no-index` vs snapshot shows only `api.*` additions with MX lines byte-identical (FR-004 evidence, commit the diff note); custom-domain resource progressing toward `CERT_ACTIVE`

---

## Phase 2: Cutover + end-to-end verification (BLOCKED BY #110)

**Purpose**: Branded address serves the live backend over valid TLS — US1 delivered.

- [ ] T011 [Phase 2] Preflight: confirm deployed service name + health path against the live service (`gcloud run services list --region australia-southeast1`; `/health` vs `/healthz` — research.md open item 2); confirm Cloud Run `ingress = all` + unauthenticated invoke unchanged; update firebase.json/HCL serviceId if #110 landed a different name
- [ ] T012 [Phase 2] Activate rewrite release (Terraform release resource per D6, or documented CI step with standalone Firebase binary); wait for `CERT_ACTIVE` (<=24 h; SC-001 budget 48 h)
- [ ] T013 [Phase 2] Run full verification from [quickstart.md](quickstart.md) and record evidence in the runbook: health 200 via `https://api.redmarklogic.com`; GTS cert correct host; HTTP->HTTPS redirect (FR-003); re-deploy service image and confirm branded URL unaffected (FR-007/SC-004); email round-trip via founder mailbox (SC-003); negative checks — >60 s request returns 504, direct run.app URL still answers; record observed `X-Forwarded-Host`/header actuals (research.md open item 4) (depends on T011, T012)

### Acceptance Gate

- [ ] T014 [Phase 2] Verify: every check in T013 has captured output in the runbook; final zone diff still additive-only; SC-001..SC-004 each have evidence

---

## Phase 3: Documentation close-out

**Purpose**: A reader can rebuild or audit the whole connection from the docs — US3 delivered.

- [ ] T015 [Phase 3] Finalize `docs/infrastructure/domain-dns-runbook.md`: complete step list (Terraform, API calls, the two manual exceptions: token creation + Console emergency fallback), rollback notes (delete records / `firebase hosting:rollback` / `terraform destroy -target`), accepted-constraints table (60 s, `__session`, no WebSockets, 32 MB, run.app bypass)
- [ ] T016 [P] [Phase 3] Publish the consumer-facing addressing contract (base URL, 60 s ceiling, bypass exclusion) from [contracts/api-hostname.md](contracts/api-hostname.md) to the API docs location governed by ADR-018 conventions
- [ ] T017 [Phase 3] Close the loop: PR merges close #111 (board Done via merged PR per board rules); verify #110 blocked-by link shows resolved; file lesson if any step deviated from this plan (`docs/lessons/` per template)

### Acceptance Gate

- [ ] T018 [Phase 3] Verify: SC-005 holds — every created resource/record maps to a documented step; spec checklist items all evidenced; no undocumented dashboard action occurred

## Dependencies

```text
Phase 0 (T001..T004)  -- no external dependency; can start immediately
  -> Phase 1 (T005..T010) -- no service dependency; certificate provisions in background
       -> Phase 2 (T011..T014) -- HARD DEPENDENCY: issue #110 (deployed Cloud Run service)
            -> Phase 3 (T015..T018)
Parallel within phases: T002 || T001; T007 || T006; T016 || T015
```

## Execution Notes

- `[P]` = parallelizable (different files, no dependencies)
- `[Phase N]` = plan.md phase the task belongs to
- No pytest gates: no Python function files are touched (template rule preserved — if
  any verification script is added under `scripts/`, the pytest gate reactivates)
- The Acceptance Gate at the end of each phase is a hard stop — do not start the next
  phase until it passes
- Commit after each task or logical group; PR per phase is acceptable (Phase 0 ADR
  should merge before Phase 1 applies anything — Constitution "ADR before code")
- Implementation owner: Founder executes (Brent-scoped work; board agent field =
  Founder); all code/HCL subject to founder review before push
- MVP scope: Phases 0-1 alone are a safe, useful increment (domain attached, cert
  ready) even while #110 is in flight
