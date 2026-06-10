# Tasks: Infra ADR + Tier-1 GCP Approval (Cloud Run + Artifact Registry)

**Input**: [plan.md](plan.md)
**Prerequisites**: Branch `feature/63-infra-adr-tier-1-gcp-approval-cloud-run-artifact-registry` checked out; issue #48 closed (Cloud Run + Artifact Registry ratified).

<!-- Task sizing rule: each task is a VERTICAL SLICE -- front-to-back, one complete
     new behaviour, nothing left dangling. Documentation tasks are complete when a
     reviewer can verify the content without referring to the source issue. -->

## Phase 1: Setup

**Purpose**: Create the `docs/infrastructure/` directory so both deliverables can be written.

- [ ] T001 [Phase 1] Create `docs/infrastructure/` directory

### Acceptance Gate

- [ ] T002 [Phase 1] Verify `docs/infrastructure/` exists in the repo root

---

## Phase 2: ADR-022 — Cloud Run + Artifact Registry Hosting [US1]

**Purpose**: Author and accept ADR-022, recording all #48 brainstorm decisions and the Tier-1 trust-boundary approval.

### Implementation

- [ ] T003 [US1] Create `docs/adr/adr-022-cloud-run-artifact-registry-hosting.md` using existing ADR conventions; include sections: Summary, Status (Accepted), Decision, Context, Options Considered, Consequences, Out of Scope, Cross-References
- [ ] T004 [US1] Decision section: record Cloud Run (australia-southeast1), Artifact Registry (australia-southeast1), CPU throttled, 0 min-instances (1 pre-production), 300s request timeout, 80 concurrency/instance, python:3.14-slim multi-stage image
- [ ] T005 [US1] Tier-1 trust-boundary section: record public HTTPS ingress approved; IAP not required at this stage; Bearer presence-only auth is current gate; auth placeholder is intentional (pending B-1b, #73)
- [ ] T006 [US1] Out of Scope section: explicitly list IAP/SSO (B-1b, #73), VPC connector, CI/CD pipeline, Cloud SQL, multi-environment split, Secret Manager entries
- [ ] T007 [US1] Cross-References section: link ADR-018 (HTTP API contract), ADR-020 (Terraform IaC), ADR-021 (process environment config), issue #48 (ratification), issue #63 (governance gate) -- do not merge or duplicate content from those ADRs

### Acceptance Gate

- [ ] T008 [US1] Verify against quickstart.md steps 1-4: ADR-022 present, status Accepted, all brainstorm decisions recorded, Tier-1 approval present, cross-references correct

---

## Phase 3: Connection-Strategy Analysis [US2]

**Purpose**: File Brent's connection-strategy document giving explicit provisioning clearance.

### Implementation

- [ ] T009 [US2] Create `docs/infrastructure/cloud-run-connection-strategy.md` with sections: Purpose, Inbound Connections, Image Pull Chain, Outbound Connections, Future: VPC Connector, Provisioning Clearance
- [ ] T010 [US2] Inbound section: public HTTPS port 443, Cloud Run managed TLS, no load balancer at this stage, ingress=`all`, no IAP
- [ ] T011 [US2] Image Pull Chain section: Artifact Registry australia-southeast1, same-region pull (zero egress cost), Cloud Run service account requires `roles/artifactregistry.reader`
- [ ] T012 [US2] Outbound section: no outbound calls currently (pure request/response); VPC connector required when private GCP resources added (Cloud SQL, Memorystore, internal services)
- [ ] T013 [US2] Provisioning Clearance section: explicit statement -- Brent is cleared to provision Cloud Run service, Artifact Registry repository, and public ingress

### Acceptance Gate

- [ ] T014 [US2] Verify against quickstart.md step 5: all required sections present and content correct

---

## Phase 4: Polish

- [ ] T015 [P] [Phase 4] Cross-check ADR-022 and connection-strategy doc for consistency -- no contradictions, no duplicate content
- [ ] T016 [Phase 4] Confirm `docs/infrastructure/` directory and both files are staged for commit

### Acceptance Gate

- [ ] T017 [Phase 4] Run full quickstart.md checklist (steps 1-5) -- all steps pass before opening PR
- [ ] T018 [Phase 4] Open PR against master; reference issue #63 in PR description (e.g., "Closes #63")

---

## Dependencies

```text
T001 → T003-T007 (directory must exist before writing ADR... actually ADR is in docs/adr/ not docs/infrastructure/, so T001 only blocks T009-T013)
T001 → T009
T003 → T004 → T005 → T006 → T007 (ADR sections in order)
T008 (gate after T003-T007)
T009 → T010 → T011 → T012 → T013 (connection-strategy sections in order)
T014 (gate after T009-T013)
T008 + T014 → T015 → T016 → T017 → T018
```

## Execution Notes

- `[P]` = parallelizable (different files, no dependencies)
- `[US1]` = User Story 1 (ADR-022)
- `[US2]` = User Story 2 (connection-strategy doc)
- No test tasks -- documentation deliverables; verification is manual per quickstart.md
- The Acceptance Gate at the end of each phase is a hard stop
- Commit after each phase completes its gate
- Use `finishing-a-development-branch` skill after T018 to complete the work
