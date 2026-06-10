# Feature Specification: Cloud Run Deploy — Staging + Prod with Secret Manager

**Feature Branch**: `feature/70-cloud-run-deploy-staging-prod-with-secret-manager`

**Created**: 2026-06-10

**Status**: Draft

**Input**: User description: "Deploy backend serverless; secrets via Secret Manager; min/max instances; health check. Owner: Brent (DevOps). Blocked by B6."

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Staging environment accepts live traffic (Priority: P1)

Brent deploys the backend API to the staging Cloud Run service. The service starts, passes its health check, and responds to requests. Secrets are injected from Secret Manager — no secrets appear in plain text in the service configuration or source control.

**Why this priority**: Staging is the first proof that the full deploy pipeline works end-to-end. Nothing else can be validated without a running environment.

**Independent Test**: Brent runs the deploy command targeting staging. He then issues an HTTP request to the staging service URL and receives a valid 200 response. The health-check endpoint returns a healthy status. Secret values are confirmed present inside the running container but absent from all config files and environment variable literals in the deployment manifest.

**Acceptance Scenarios**:

1. **Given** a container image exists in Artifact Registry, **When** Brent deploys to staging, **Then** the Cloud Run service becomes READY within 3 minutes and the health-check endpoint returns HTTP 200.
2. **Given** a secret (e.g., an API key) is stored in Secret Manager, **When** the staging service starts, **Then** the secret value is available to the application as an environment variable without appearing in any deployment manifest or log output.
3. **Given** the staging service is deployed with min-instances = 0, **When** no traffic flows for several minutes, **Then** the service scales to zero instances without error.

---

### User Story 2 — Production environment deployed with cold-start mitigation (Priority: P2)

Brent promotes the same verified container image from staging to the production Cloud Run service. Production is configured with min-instances ≥ 1 to avoid cold starts for real users. Secrets for production are separate from staging secrets in Secret Manager.

**Why this priority**: Production availability is the business outcome. Staging without prod delivery is incomplete.

**Independent Test**: Brent deploys to production using the same image digest that passed staging validation. He verifies the health-check endpoint on the production URL returns HTTP 200 and that the service maintains at least one warm instance.

**Acceptance Scenarios**:

1. **Given** a validated image is in Artifact Registry, **When** Brent deploys to production, **Then** the production Cloud Run service becomes READY and the health-check endpoint returns HTTP 200.
2. **Given** production is configured with min-instances ≥ 1, **When** no traffic flows for 10 minutes, **Then** at least one instance remains active (no cold start on next request).
3. **Given** production and staging are separate environments, **When** a staging secret is updated, **Then** the production service is unaffected.

---

### User Story 3 — Max-instances cap prevents runaway cost (Priority: P3)

Both staging and production Cloud Run services have a maximum-instance cap configured. If a traffic spike or misconfiguration causes requests to surge, the platform will not scale beyond the cap.

**Why this priority**: Cost protection is operationally essential; it is not a blocker for initial deploy but must be present before any external traffic.

**Independent Test**: The deployed service configuration shows a max-instances value that limits scale-out. The value is documented and consistent with the agreed cost target.

**Acceptance Scenarios**:

1. **Given** a staging or production service is deployed, **When** the service configuration is inspected, **Then** a max-instances limit is set and matches the agreed value for that environment.
2. **Given** max-instances = N, **When** traffic exceeds capacity of N instances, **Then** the platform returns HTTP 429 (or queues requests) rather than spawning additional instances.

---

### Edge Cases

- What happens when a Secret Manager secret version is disabled or deleted while the service is running? Application should surface a startup failure with a clear error message.
- What happens when the container image digest referenced in the deploy command no longer exists in Artifact Registry? Deploy should fail with an explicit error before the service is replaced.
- What happens when the health-check path is unreachable (e.g., port misconfiguration)? Cloud Run should not mark the revision READY; the previous revision (if any) should continue serving traffic.
- What happens when max-instances is reached during a surge? Requests should receive a throttled response rather than silently hanging.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST deploy the backend service to two separate Cloud Run environments: staging and production.
- **FR-002**: Each environment MUST load all secret values (API keys, tokens, credentials) exclusively from Secret Manager; no secret value may appear in deployment manifests, environment variable literals, or source control.
- **FR-003**: The staging service MUST be configured with min-instances = 0 (scales to zero when idle).
- **FR-004**: The production service MUST be configured with min-instances ≥ 1 to eliminate cold starts for active users.
- **FR-005**: Both services MUST have a max-instances cap set to prevent unbounded scale-out.
- **FR-006**: The deployed service MUST expose a health-check endpoint that returns HTTP 200 when the service is ready to accept traffic.
- **FR-007**: Cloud Run MUST use the health-check endpoint to determine revision readiness before routing traffic to a new deployment.
- **FR-008**: Staging and production MUST reference separate Secret Manager secret names (or separate versions) so that secrets are environment-isolated.
- **FR-009**: The deploy procedure MUST be repeatable — running it again with the same image produces the same service configuration (idempotent).
- **FR-010**: All infrastructure configuration for both environments MUST be declared as code (Terraform), consistent with ADR-020.

### Key Entities

- **Cloud Run Service**: The serverless runtime unit hosting the API. One per environment (staging, production). Holds configuration for min/max instances, container image reference, environment variables, and secret bindings.
- **Secret Manager Secret**: A named, versioned secret stored in GCP. One logical secret per credential per environment (e.g., `staging/api-key`, `prod/api-key`). Bound to the Cloud Run service at deploy time.
- **Container Image**: The immutable, versioned artifact in Artifact Registry. The same image digest is deployed to staging first, then promoted to production.
- **Health-Check Endpoint**: An HTTP path on the running container (e.g., `/health`) that returns 200 when the service is operational. Used by Cloud Run for readiness gating.
- **Environment**: A logical deployment target (staging or production) with its own Cloud Run service, Secret Manager secrets, and instance configuration.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A deploy to staging completes and the service is fully available (health check passes) within 3 minutes of triggering the deploy command.
- **SC-002**: Zero secret values appear in plain text in Terraform state references, Cloud Run service configuration views, or deployment logs (verified by inspection).
- **SC-003**: The production service responds to its first request within 1 second when min-instances ≥ 1 (no cold-start delay under normal operation).
- **SC-004**: Running the deploy command twice in succession with the same image and configuration produces an identical service state (idempotency verified by diffing the Cloud Run service descriptions).
- **SC-005**: Both staging and production service configurations show a max-instances value ≤ the agreed cap documented in Terraform variables.
- **SC-006**: When a new revision fails its health check, the previous revision continues to serve 100% of traffic with no manual intervention.

## Assumptions

- The Cloud Run region is `australia-southeast1`, consistent with ADR-022.
- The application already implements a health-check endpoint (spec 004 delivered this).
- Container images are already published to Artifact Registry (spec 005 / issue #63 prerequisite).
- Terraform is the declared infrastructure-as-code tool (ADR-020); all Cloud Run and Secret Manager resources are declared in `deploy/infra/terraform/`.
- Secret Manager API and Cloud Run API are already enabled in the GCP project (covered by spec 005 GCP project baseline).
- Staging and production share the same GCP project (single-project, multi-environment pattern); environment isolation is achieved through separate Cloud Run services and separate Secret Manager secret names.
- The CPU allocation mode remains throttled (not always-allocated), consistent with ADR-022 §3.
- Request timeout of 300 s is inherited from ADR-022 and is not re-specified here.
- No VPC connector is required at this stage (ADR-022 out-of-scope).
- No CI/CD pipeline is in scope; Brent will invoke deploy commands manually for the first deployments.
- "Blocked by B6" refers to issue #63 (infra ADR + GCP approval gate); that ADR is now accepted and this spec may proceed.
