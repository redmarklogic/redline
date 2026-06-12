# Tasks: Lock Cloud Run Ingress to Founder Static IP

**Input**: [plan.md](plan.md)
**Prerequisites**: Cloud Run prod service deployed (`specs/70`); founder static IP known

<!-- Approach: FastAPI middleware, not Cloud Armor + LB.
     Cloud Armor rejected: $11/month, 7 new resources, overkill for one sprint.
     Middleware: $0, ~15 lines Python, removed in 3 lines at IAP handover.
     See plan.md D1 for full rationale. -->

## Phase 1: Tests (write first — must fail before implementation begins)

**Purpose**: Failing tests that define the middleware contract before any code is written

- [ ] T001 [Phase 1] Create `tests/unit/api/test_middleware.py` with three test cases: (1) request from allowed IP passes through and returns 200; (2) request from any other IP returns 403; (3) request with no `X-Forwarded-For` header returns 403
- [ ] T002 [Phase 1] Confirm tests fail: `uv run pytest tests/unit/api/test_middleware.py -v` — expect ImportError or 3 failures (no implementation yet)

### Acceptance Gate

- [ ] T003 [Phase 1] All three tests collected and failing (not erroring on syntax)

---

## Phase 2: Middleware Implementation (US1, US2)

**Purpose**: `IPAllowlistMiddleware` exists; requests from non-matching IPs return 403; prod Cloud Run service has `FOUNDER_ALLOWED_IP` in its environment

### Implementation

- [ ] T004 [Phase 2] [US1] [US2] Create `src/marker/api/middleware.py` — `IPAllowlistMiddleware(BaseHTTPMiddleware)` that reads `X-Forwarded-For` first entry, compares to `self.allowed_ip`, returns `Response(status_code=403)` on mismatch; no default for `allowed_ip` (must be passed explicitly)
- [ ] T005 [Phase 2] [US1] [US2] In `src/marker/api/main.py` `create_app()`, add: `if allowed_ip := os.environ.get("FOUNDER_ALLOWED_IP"): app.add_middleware(IPAllowlistMiddleware, allowed_ip=allowed_ip)` — **note**: `os.environ.get()` is an accepted ADR-021 variance for disposable scaffolding; add inline comment `# ADR-021 variance: opt-in middleware for disposable scaffolding (#71)`
- [ ] T006 [P] [Phase 2] Add `founder_allowed_ip` variable to `deploy/infra/terraform/variables.tf` — type string, no default, description "Founder static IP (plain IP, not CIDR) — used as FOUNDER_ALLOWED_IP on prod Cloud Run service (issue #71, disposable scaffolding)"
- [ ] T007 [P] [Phase 2] In `deploy/infra/terraform/cloud_run.tf`, add a plain env var to the prod service only: `dynamic "env" { for_each = each.key == "prod" ? [var.founder_allowed_ip] : [] content { name = "FOUNDER_ALLOWED_IP"; value = env.value } }` — add comment "# issue #71 disposable scaffolding — remove at IAP handover (#73)"

### Acceptance Gate

- [ ] T008 [Phase 2] `uv run pytest tests/unit/api/test_middleware.py -v` — all 3 tests green
- [ ] T009 [Phase 2] Add `founder_allowed_ip = "<your-ip>"` to `terraform.tfvars`; run `terraform -chdir=deploy/infra/terraform plan` — expect 1 resource changed (prod Cloud Run service env var added); staging must not appear in diff
- [ ] T010 [Phase 2] Run `terraform -chdir=deploy/infra/terraform apply` — exits 0; redeploy prod image so new env var takes effect

---

## Phase 3: Update Path Verification (US3)

**Purpose**: Confirm updating the IP requires only a `terraform.tfvars` change + apply — no code change, no rebuild

- [ ] T011 [Phase 3] [US3] Change `founder_allowed_ip` in `terraform.tfvars` to a different value; run `terraform -chdir=deploy/infra/terraform plan` — confirm only the Cloud Run prod service env var changes; revert after confirming

### Acceptance Gate

- [ ] T012 [Phase 3] Plan diff shows exactly one attribute change; no other resources affected

---

## Phase 4: Polish

- [ ] T013 [P] [Phase 4] Run full unit test suite: `uv run pytest tests/ -v` — all green, no regressions
- [ ] T014 [P] [Phase 4] Run static checks: `uv run ruff check src/marker/api/middleware.py src/marker/api/main.py`

### Acceptance Gate

- [ ] T015 [Phase 4] All tests green, lint clean; open `/make-pr` to close

---

## Execution Notes

- `[P]` = parallelizable (different files, no dependencies)
- T004 and T005 must be done in order (middleware class before `main.py` import)
- T006 and T007 are parallelizable — independent files
- TDD is mandatory: T001–T003 (red) must complete before T004–T005 (green)
- Commit after each phase's acceptance gate passes
- Use `/make-pr` after T015 passes
