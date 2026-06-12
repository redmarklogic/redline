# Feature Specification: Lock Cloud Run Ingress to Founder Static IP

**Feature Branch**: `feature/71-lock-cloud-run-ingress-to-founder-static-ip`

**Created**: 2026-06-12

**Status**: Draft

**Input**: GitHub issue #71 — Walking-skeleton access control: allow only the founder's static IP; block all other inbound. Disposable scaffolding superseded by IAP (B10) next sprint.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Founder reaches API from their IP (Priority: P1)

The founder sends a request to the Cloud Run service URL from their registered static IP address. The request is accepted and a valid response is returned.

**Why this priority**: This is the only authorised access path. If the founder cannot reach the service, the walking-skeleton is blocked.

**Independent Test**: Send a request to the Cloud Run service URL from the founder's static IP. Verify a non-4xx/non-403 response is received.

**Acceptance Scenarios**:

1. **Given** the Cloud Run service is deployed with ingress restricted, **When** the founder sends a HTTPS request from their registered static IP, **Then** the request reaches the application and returns a valid response (2xx or application-level error, not a network block)
2. **Given** the Cloud Run service is deployed with ingress restricted, **When** the founder accesses the service from a different network (e.g. mobile data), **Then** requests from the non-whitelisted IP are blocked

---

### User Story 2 - Non-whitelisted traffic is silently rejected (Priority: P1)

Any HTTPS request originating from an IP address that is not the founder's static IP is rejected at the network/ingress layer before it reaches the application.

**Why this priority**: The purpose of this feature is to prevent all other access during the walking-skeleton phase. This is the security invariant.

**Independent Test**: Send a request from any IP other than the whitelisted IP (e.g. from a CI runner, a VPN exit node, or a different machine). Verify the request is blocked at the ingress layer.

**Acceptance Scenarios**:

1. **Given** the ingress restriction is active, **When** a request arrives from any IP not in the allowlist, **Then** the request is rejected with a non-descriptive error (no application response is returned)
2. **Given** the ingress restriction is active, **When** a request arrives without a recognised source IP (e.g. from a proxy), **Then** the request is rejected

---

### User Story 3 - IP allowlist is updatable without code changes (Priority: P2)

The founder's static IP is stored in a configurable location. Updating it does not require modifying application code or rebuilding the container image — only an infrastructure change is needed.

**Why this priority**: Static IPs can change. The update path must not be disruptive.

**Independent Test**: Change the allowlisted IP value in the infrastructure configuration, apply the change, and confirm only the new IP is accepted.

**Acceptance Scenarios**:

1. **Given** the ingress restriction is active, **When** the allowlisted IP is updated in the infrastructure configuration and the change is applied, **Then** only the new IP is accepted and the old IP is rejected

---

### Edge Cases

- What happens if the founder's ISP changes their static IP without notice? The service becomes inaccessible until the allowlist is updated. The update path (single infrastructure variable change) must be documented.
- What happens when the restriction is removed for IAP handover? The ingress setting must revert cleanly to `all` (or to IAP-controlled) with no residual configuration.
- What happens if the founder's IP is a /32 CIDR vs a bare IP? The system must accept both forms and treat them equivalently.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST reject all inbound HTTPS requests originating from IP addresses outside the configured allowlist before returning any application response
- **FR-002**: System MUST accept all inbound HTTPS requests originating from IP addresses within the configured allowlist
- **FR-003**: The IP allowlist MUST be defined in a single, version-controlled location
- **FR-004**: The IP allowlist MUST be updatable by changing a single configuration value — no rebuild of the container image required
- **FR-005**: Rejected requests MUST receive a generic error response that does not reveal the existence of an IP allowlist
- **FR-006**: The restriction MUST be fully removable via a single change to restore unrestricted access for the IAP handover

### Key Entities *(include if feature involves data)*

- **IP Allowlist**: A set of one or more CIDR ranges representing authorised source IPs. Initially one entry: the founder's static IP as a /32 CIDR. Stored as an infrastructure variable, not in application code.
- **Ingress Rule**: The network-level access control that evaluates source IP against the allowlist before forwarding traffic to the Cloud Run service.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of requests from non-allowlisted IPs are blocked before reaching the application (verifiable by inspecting Cloud Run request logs — no log entries from blocked IPs)
- **SC-002**: 100% of requests from the founder's allowlisted IP are forwarded to the application
- **SC-003**: Updating the allowlisted IP requires a change to exactly one configuration value — no container image rebuild and no other files change
- **SC-004**: The restriction is fully removed by deleting one middleware module and one environment variable

## Assumptions

- The founder has a known, stable static IP address; it will be supplied as a deployment configuration value
- This restriction is explicitly temporary scaffolding; it will be superseded by IAP (issue #73) and must be designed for easy removal
- The Cloud Run service is already provisioned per ADR-022; Cloud Run ingress remains open to all (`INGRESS_TRAFFIC_ALL`) — the check happens inside the application before any response is returned
- The enforcement mechanism is application-layer (middleware), not network-layer — Cloud Armor and a load balancer are not required and were rejected as over-engineered for one sprint of scaffolding
- Mobile data, VPN, and CI runner IPs are not in scope for the allowlist at this stage
