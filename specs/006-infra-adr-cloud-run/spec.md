# Feature Specification: Infra ADR + Tier-1 GCP Approval (Cloud Run + Artifact Registry)

**Feature Branch**: `feature/63-infra-adr-tier-1-gcp-approval-cloud-run-artifact-registry`

**GitHub Issue**: #63

**Created**: 2026-06-10

**Status**: Draft

**Input**: Issue #63 body + Issue #48 brainstorm decisions (2026-06-10)

## User Scenarios & Testing *(mandatory)*

### User Story 1 — ADR-022 authored and accepted (Priority: P1)

The engineering team needs an Architecture Decision Record that captures the
Cloud Run + Artifact Registry hosting decision, the Tier-1 trust-boundary
approval, and all constraints recorded during the #48 brainstorm. Without this
record, Brent cannot provision any GCP resources and the deploy chain is blocked.

**Why this priority**: Governance gate. Nothing in the deploy chain (Cloud Run
service, Artifact Registry repo, ingress) can be provisioned until the ADR is
accepted. It is the single blocking artifact for all downstream infra work.

**Independent Test**: ADR-022 file exists at `docs/adr/adr-022-*.md`, status is
Accepted, and a reviewer can verify every decision from the #48 brainstorm is
recorded without reading the issue.

**Acceptance Scenarios**:

1. **Given** the `docs/adr/` directory, **When** ADR-022 is present with status
   Accepted, **Then** it records: Cloud Run (australia-southeast1), Artifact
   Registry (same region), CPU-throttled allocation, 0 min-instances (1
   pre-production), 300s request timeout, 80 concurrent requests/instance,
   Alpine/slim multi-stage image.

2. **Given** ADR-022, **When** a reviewer reads the trust-boundary section,
   **Then** it explicitly records: public HTTPS ingress approved, IAP not
   required at this stage (B-1b scope), Bearer presence-only auth is the current
   gate, auth placeholder is intentional and not a gap.

3. **Given** ADR-022, **When** a reviewer reads the cross-references section,
   **Then** it references ADR-018 (HTTP API contract) and ADR-020 (Terraform IaC)
   without duplicating or merging their content.

4. **Given** ADR-022, **When** a reviewer reads the out-of-scope section, **Then**
   it explicitly excludes: IAP/SSO wiring (B-1b), VPC connector, CI/CD pipeline,
   Cloud SQL, multi-environment split, Secret Manager entries.

---

### User Story 2 — Brent's connection-strategy analysis filed (Priority: P2)

Brent needs a structured analysis document that maps every connection in and out
of the Cloud Run service so provisioning decisions are grounded and reviewable.
Without this document Brent cannot justify ingress/egress choices or get sign-off
before running `terraform apply`.

**Why this priority**: Operational clarity. The ADR records the decision; this
document records how the service connects to the world. Together they constitute
the Tier-1 approval package.

**Independent Test**: File exists at
`docs/infrastructure/cloud-run-connection-strategy.md` and covers: inbound path,
image pull chain, outbound connections, future VPC connector trigger conditions.

**Acceptance Scenarios**:

1. **Given** `docs/infrastructure/cloud-run-connection-strategy.md`, **When** a
   reviewer reads the inbound section, **Then** it describes: public HTTPS on
   port 443, Cloud Run managed TLS, no load balancer at this stage, ingress set
   to `all`.

2. **Given** the document, **When** a reviewer reads the image pull section,
   **Then** it records: Artifact Registry in australia-southeast1, same-region
   pull (zero egress cost), Cloud Run service account granted
   `roles/artifactregistry.reader`.

3. **Given** the document, **When** a reviewer reads the outbound section, **Then**
   it states: no outbound calls at this stage (pure request/response); VPC
   connector will be required if private GCP resources (Cloud SQL, Memorystore,
   internal services) are added in future.

4. **Given** the document, **When** a reviewer reads the clearance section, **Then**
   it explicitly states Brent is cleared to provision: Cloud Run service, Artifact
   Registry repository, and public ingress.

---

### User Story 3 — Issue #63 closed (Priority: P3)

Once both documents are merged to the main branch, issue #63 must be closed so
the sprint board reflects that the governance gate has been passed and downstream
issues (#67, #70, #76) can proceed.

**Why this priority**: Process hygiene. The ADR and analysis are the real
deliverables; closing the issue is the confirmation signal.

**Independent Test**: GitHub issue #63 status is Closed after the PR merging both
documents is merged.

**Acceptance Scenarios**:

1. **Given** a merged PR containing ADR-022 and the connection-strategy doc,
   **When** the PR is merged to master, **Then** issue #63 is closed (via PR
   reference or manual close).

---

### Edge Cases

- What if ADR-020 (Terraform IaC) constraints conflict with something in ADR-022?
  ADR-020 governs the provisioning tool; ADR-022 governs what is provisioned.
  They are orthogonal by design and must cross-reference without duplicating.

- What if the open questions from #48 (CPU allocation mode, secrets list) are not
  fully resolved before spec writing? Both are resolved: CPU throttled (no
  background tasks confirmed by code inspection); runtime secrets = APP_ENV only
  (no Secret Manager entries needed yet).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: ADR-022 MUST be created at `docs/adr/adr-022-cloud-run-artifact-registry-hosting.md`
  with status Accepted.

- **FR-002**: ADR-022 MUST record all decisions from the #48 brainstorm: Cloud Run
  (australia-southeast1), Artifact Registry (same region), CPU throttled, 0
  min-instances, 300s timeout, 80 concurrency, Alpine/slim multi-stage image.

- **FR-003**: ADR-022 MUST record the Tier-1 trust-boundary approval: public HTTPS
  ingress approved; IAP not required at this stage; Bearer presence-only auth is
  the current gate.

- **FR-004**: ADR-022 MUST cross-reference ADR-018 and ADR-020 without merging or
  duplicating their content.

- **FR-005**: ADR-022 MUST explicitly list what is out of scope: IAP/SSO (B-1b),
  VPC connector, CI/CD pipeline, Cloud SQL, multi-environment split, Secret
  Manager entries.

- **FR-006**: `docs/infrastructure/` directory MUST be created if it does not
  exist.

- **FR-007**: Connection-strategy document MUST be created at
  `docs/infrastructure/cloud-run-connection-strategy.md`.

- **FR-008**: Connection-strategy document MUST cover: inbound HTTPS path, image
  pull chain from Artifact Registry, outbound connections (none currently), VPC
  connector trigger conditions.

- **FR-009**: Connection-strategy document MUST include an explicit clearance
  statement: Brent is cleared to provision Cloud Run service, Artifact Registry
  repository, and public ingress.

- **FR-010**: Issue #63 MUST be closed after both documents are merged.

### Key Entities

- **ADR-022**: Architecture Decision Record for Cloud Run + Artifact Registry
  hosting. Lives in `docs/adr/`. Cross-references ADR-018 and ADR-020.

- **Connection-strategy document**: Operational analysis of every connection in
  and out of the Cloud Run service. Lives in `docs/infrastructure/`. Authored by
  Brent. Provides provisioning clearance.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Both documents exist on the main branch within one PR cycle — no
  follow-up work items are created to fill gaps in either document.

- **SC-002**: A reviewer unfamiliar with issues #48 and #63 can reconstruct the
  full hosting decision from ADR-022 alone without reading the issues.

- **SC-003**: Brent can begin Terraform provisioning of Cloud Run + Artifact
  Registry immediately after the PR is merged, with zero open questions remaining.

- **SC-004**: Issue #63 is closed within one working day of the PR merge.

## Assumptions

- Cloud Run and Artifact Registry are both available in australia-southeast1
  (confirmed by GCP documentation).

- The Dockerfile already uses a multi-stage slim build (`python:3.14-slim`); the
  ADR records this as the mandated image strategy, not a future requirement.

- No Secret Manager entries are needed at this stage; `APP_ENV` is the only
  runtime environment variable, and it is non-secret.

- CPU throttled allocation is correct for this app because the FastAPI application
  has no background tasks (confirmed by code inspection of `src/`).

- The auth placeholder (Bearer presence-only) is an intentional design choice
  pending B-1b, not a security gap that blocks Tier-1 approval.

- Terraform is the provisioning tool (ADR-020); the connection-strategy doc
  describes what will be provisioned, not how Terraform HCL will be structured.
