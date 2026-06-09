# Feature Specification: GCP Project Baseline

**Feature Branch**: `005-gcp-project-baseline`

**Created**: 2026-06-10

**Status**: Draft

**Input**: GitHub Issue #64 — Infra: GCP project + region (australia-southeast1) + billing baseline

**Blocked by**: #48 (Cloud Run ratification), #63 (Tier-1 infra ADR)

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Provision GCP project foundation (Priority: P1)

The infrastructure owner sets up the GCP project with the correct region, billing account,
and API surface so that all downstream deploy-chain work (#65–#72) can proceed without
hitting missing-project or missing-API errors.

**Why this priority**: Every other deploy-chain issue depends on this foundation. Without a
correctly configured project, no Cloud Run service, Artifact Registry, or IAP resource can
be created.

**Independent Test**: Run `gcloud projects describe <project-id>` and verify project exists,
billing is active, and all required APIs report ENABLED. No downstream resources are needed
to confirm this story.

**Acceptance Scenarios**:

1. **Given** no GCP project exists for the product, **When** provisioning completes,
   **Then** a project with ID matching the naming convention exists and is visible in the
   GCP console under the correct organisation/folder.

2. **Given** the project exists, **When** checking the default compute region,
   **Then** `australia-southeast1` is returned as the default region for all resource
   creation.

3. **Given** the project exists, **When** querying billing status,
   **Then** an active billing account is linked and the project is not in a suspended state.

4. **Given** the project exists with billing active, **When** listing enabled APIs,
   **Then** all APIs in the required list (FR-003) are in ENABLED state.

---

### User Story 2 — Consistent environment identity across deploy chain (Priority: P2)

Any team member or automated pipeline that references the GCP project ID, region, or
billing account obtains the same canonical values from a single source of truth.

**Why this priority**: Downstream issues (#68 Workload Identity, #69 CI/CD, #70 Cloud Run
deploy) embed the project ID and region. Inconsistent values cause silent failures.

**Independent Test**: Retrieve the project ID from the documented SSOT and confirm it
matches `gcloud config get-value project` in the provisioned environment.

**Acceptance Scenarios**:

1. **Given** the provisioned project, **When** reading the canonical project-ID record,
   **Then** it matches the project ID registered in GCP exactly (no trailing spaces,
   no alias drift).

2. **Given** multiple infrastructure scripts that reference the project ID, **When** all are
   run in sequence, **Then** each one targets the same project without manual ID correction.

---

### Edge Cases

- What happens when the billing account quota is exhausted at project creation time?
- How does provisioning handle an existing project with the same ID (idempotency)?
- What if the required APIs are restricted by an Organisation Policy at the folder level?
- What if `australia-southeast1` is unavailable for a specific API (not all services are
  available in every region)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Provisioning MUST create a GCP project with a stable, human-readable project
  ID following the agreed naming convention (`redmarklogic-<env>` or equivalent).
- **FR-002**: The project default region MUST be set to `australia-southeast1` for all
  resource-creating operations.
- **FR-003**: The following GCP APIs MUST be enabled on the project:
  - Cloud Run Admin API
  - Artifact Registry API
  - Cloud Build API
  - Secret Manager API
  - Identity-Aware Proxy API
  - Cloud DNS API
  - Compute Engine API (required by Cloud Run and Load Balancer)
  - IAM API
  - Resource Manager API
- **FR-004**: An active billing account MUST be linked to the project before any
  resource-provisioning step runs.
- **FR-005**: Provisioning MUST be idempotent — re-running it against an already-configured
  project MUST NOT create duplicate resources or alter existing settings.
- **FR-006**: The canonical project ID, region, and billing account ID MUST be recorded
  in a shared infrastructure inventory file accessible to all deploy-chain contributors.
- **FR-007**: Provisioning steps MUST be executable by a single operator with Owner-level
  IAM on the GCP organisation/folder, without requiring additional human approvals at each
  API-enable step.

### Key Entities

- **GCP Project**: The top-level resource container. Attributes: project ID, project number,
  billing account, organisation/folder anchor, default region.
- **Billing Account**: A GCP billing account that funds all resource usage. Linked to exactly
  one project at this stage.
- **API Enablement Record**: The set of GCP service APIs enabled on the project, each in
  ENABLED or DISABLED state.
- **Infrastructure Inventory**: A version-controlled file recording canonical project
  identifiers for downstream consume (project ID, region, billing account reference).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Provisioning completes end-to-end without manual intervention in under
  15 minutes from a clean state.
- **SC-002**: All FR-003 APIs report ENABLED status within 5 minutes of provisioning
  completing.
- **SC-003**: Every downstream deploy-chain issue (#65–#72) can reference the project ID
  and region from the inventory without contacting the infrastructure owner directly.
- **SC-004**: Re-running provisioning on an already-configured project produces zero
  resource changes and exits successfully (idempotency confirmed).
- **SC-005**: Billing link is verifiable via the GCP console and CLI within 2 minutes of
  provisioning completing.

## Assumptions

- A GCP organisation or folder already exists and the provisioning operator has Owner role
  on it.
- The billing account is already created and the operator has Billing Account User role.
- A single GCP project covers both staging and production at this baseline stage;
  environment separation (if needed) is deferred to a later spec.
- The project naming convention will be decided before provisioning runs; this spec does
  not mandate a specific name but requires one to be chosen.
- `australia-southeast1` is available for all FR-003 APIs (verified against GCP regional
  availability before provisioning).
- Issue #48 (Cloud Run ratification) and issue #63 (Tier-1 infra ADR) will be resolved
  before implementation begins; this spec is authored ahead of those gates.
