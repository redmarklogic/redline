# Feature Specification: Connect api.redmarklogic.com to Cloud Run Backend via Cloudflare DNS

**Feature Branch**: `feature/111-domain-dns-cloud-run`

**Created**: 2026-06-11

**Status**: Draft

**Input**: Board task #111 — "Connect api.redmarklogic.com to Cloud Run backend via Cloudflare DNS". Founder decisions (2026-06-11 session): domain is redmarklogic.com (registered at Cloudflare Registrar, already on Cloudflare nameservers); first hostname is api.redmarklogic.com pointing at the Cloud Run backend; apex stays free for a future website (brand-facing landing site is out of scope here — backlog #77). Scope is API only, at zero monthly cost (POC stage): the free proxy route with its 60-second request ceiling is explicitly accepted; the paid load-balancer route is rejected until traffic justifies it. Automate with CLI tooling where available (gcloud/firebase CLI on the GCP side; Cloudflare has no maintained DNS CLI, so its API with a narrowly scoped token, otherwise documented step-by-step instructions).

## Source Reconciliation

Canonical values extracted before spec writing (primary authority listed per row):

| Item | Value | Source |
|------|-------|--------|
| Domain | redmarklogic.com | Company naming decision (git 8248dd7); founder confirmation 2026-06-11 |
| Hostname | api.redmarklogic.com | Founder decision 2026-06-11 |
| DNS host / registrar | Cloudflare (NS: eve/kanye.ns.cloudflare.com) | DNS lookup 2026-06-11 |
| Backend runtime | Google Cloud Run, region australia-southeast1 | ADR-022 |
| GCP project | redmarklogic-prod | gcloud config 2026-06-11 |
| Ingress | Public HTTPS, ingress `all`, managed TLS, **no load balancer at this stage** | ADR-022, Decision 8 |
| Infrastructure as Code | Terraform (`deploy/infra/terraform/`) | ADR-020 |
| Deployment status | No Cloud Run service deployed yet (verified 2026-06-11); CI pushes images to Artifact Registry only | gcloud check 2026-06-11 |
| Email on this domain | Active (founder mailbox `harel@redmarklogic.com`) — existing DNS records are live and load-bearing | Account config |

**Tension — RESOLVED (founder, 2026-06-11):** ADR-022 approves public ingress *without*
a load balancer, and Cloud Run's free domain-mapping feature is verified unavailable in
australia-southeast1 (DevOps research, `.agents/tmp/dns-domain-research-2026-06-11/`).
The founder rejected the paid load-balancer route (~USD 20-25/month) for POC stage and
selected the free Firebase Hosting rewrite proxy, accepting its 60-second request
ceiling at the branded address. No-LB posture of ADR-022 stands; introducing Firebase
Hosting as a new platform service still requires the Tier-1 governance gate (FR-009).

**Superseded backlog item:** issue #75 (Cloud DNS + managed cert) was closed 2026-06-11
as superseded by this feature — its Google-Cloud-DNS premise contradicted the Cloudflare
reality.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - API reachable on the branded address (Priority: P1)

An API consumer (pilot client, internal tool, or the future frontend) calls the Redline
backend at `https://api.redmarklogic.com` and gets the same response they would get from
the provider-generated service address. The branded address is stable: future re-deploys
or service re-creations do not change it.

**Why this priority**: This is the entire point of the task — a stable, professional,
provider-independent address for the backend. Everything else supports it.

**Independent Test**: Issue a request to a known endpoint (e.g., the health endpoint)
at `https://api.redmarklogic.com` from the public internet and receive a successful
response served by the Redline backend.

**Acceptance Scenarios**:

1. **Given** the backend service is deployed and healthy, **When** a client requests
   `https://api.redmarklogic.com/<health endpoint>`, **Then** the response is the
   backend's normal healthy response with a valid, trusted TLS certificate.
2. **Given** the domain connection is live, **When** the backend container is
   re-deployed with a new image, **Then** `api.redmarklogic.com` continues to serve
   the backend without any DNS change.

---

### User Story 2 - Existing domain services keep working (Priority: P1)

The founder continues to send and receive email at `harel@redmarklogic.com`, and any other
pre-existing DNS records on redmarklogic.com keep resolving exactly as before. Connecting
the API subdomain is purely additive.

**Why this priority**: The domain carries live email. Breaking MX or other records is a
business-critical regression that outweighs the value of the new subdomain.

**Independent Test**: After the DNS change, send and receive a test email through the
founder mailbox; verify pre-change DNS records are unchanged.

**Acceptance Scenarios**:

1. **Given** the API subdomain records have been added, **When** existing DNS records
   for redmarklogic.com are listed and compared against the pre-change snapshot,
   **Then** no pre-existing record was modified or deleted.
2. **Given** the DNS change is live, **When** a test email is sent to and from the
   founder mailbox, **Then** delivery succeeds in both directions.

---

### User Story 3 - Setup is reproducible from documentation (Priority: P2)

The founder (or a future operator) can re-create or audit the entire domain connection —
GCP side and Cloudflare side — from a documented, step-by-step procedure that prefers
CLI commands over dashboard clicks. Where a step has no CLI path, the manual dashboard
steps are written down explicitly.

**Why this priority**: Solo-founder operation; undocumented one-off dashboard work is
unauditable and unrepeatable. Required by the IaC governance posture (ADR-020).

**Independent Test**: A reader follows the documented procedure top to bottom and can
identify, for each step, the command (or dashboard action) and its expected outcome,
without consulting any other source.

**Acceptance Scenarios**:

1. **Given** the documented procedure, **When** each step is executed in order against
   a clean state, **Then** the end state is the working domain connection described in
   User Story 1.
2. **Given** the documented procedure, **When** the GCP-side resources are inspected,
   **Then** every GCP resource created for this feature is accounted for in the
   infrastructure-as-code repository or explicitly documented as a manual exception
   with rationale.

---

### Edge Cases

- TLS certificate provisioning is asynchronous and can take minutes to hours: what is
  the observable state while pending, and when is the cutover considered failed?
- Cloudflare's proxy mode (orange cloud) can interfere with the certificate issuance
  and host verification of the upstream provider: the procedure must state explicitly
  which proxy mode each record uses and why.
- The backend service does not exist yet (deploy chain #63-#72 in progress): domain
  attachment steps that require a live service must be sequenced after deployment, and
  the task must surface this dependency rather than fail silently.
- DNS propagation delay: clients may resolve stale records for up to the record TTL;
  verification must allow for this window.
- A wrong or conflicting record already existing at `api.redmarklogic.com` (e.g., a
  leftover placeholder): the procedure must check before creating.
- HTTP (non-TLS) requests to the branded address: behavior must be defined (redirect
  to HTTPS or rejected), not left accidental.
- Requests longer than 60 seconds at the branded address fail (accepted POC
  constraint of the free proxy route): long-running operations must be documented as
  reachable via the direct service URL until the front door is upgraded, and the
  constraint must be recorded where API consumers will find it.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Requests to `https://api.redmarklogic.com` MUST be served by the Redline
  backend running on the approved hosting platform (ADR-022).
- **FR-002**: The branded address MUST present a valid, automatically renewing TLS
  certificate trusted by mainstream clients; no manual certificate lifecycle management.
- **FR-003**: Plain HTTP requests to the branded address MUST NOT silently fail:
  they are either redirected to HTTPS or rejected with a clear error.
- **FR-004**: All pre-existing DNS records on redmarklogic.com (including MX and
  related email-authentication records) MUST remain byte-for-byte unchanged; the
  change is additive only. A pre-change snapshot of the zone MUST be captured.
- **FR-005**: The complete setup procedure MUST be documented step by step: CLI
  commands where a CLI path exists (GCP side via gcloud/Terraform; Cloudflare side via
  its API or CLI if one exists), explicit dashboard instructions where it does not.
- **FR-006**: GCP-side resources created for this feature MUST be recorded in the
  project's infrastructure-as-code per ADR-020, or documented as explicit exceptions
  with rationale.
- **FR-007**: The domain attachment MUST be stable across backend re-deployments:
  re-deploying the service image requires no DNS or certificate change.
- **FR-008**: The procedure MUST define a verification checklist proving User Stories
  1 and 2 (branded endpoint healthy; pre-existing records intact; email round-trip OK).
- **FR-009**: Introducing any new platform service or public ingress path for the
  attachment mechanism MUST pass the Tier-1 governance gate (ADR amendment or
  addendum recording the decision, its cost posture, and the accepted 60-second
  constraint) before implementation, not be worked around silently.
- **FR-010**: The branded address MUST add no recurring monthly cost at POC stage
  (free-tier route); any future upgrade to a paid front door is a separate,
  founder-approved task.

### Key Entities

- **DNS zone (redmarklogic.com)**: The Cloudflare-hosted record set; carries live email
  records (load-bearing) plus the new API subdomain record(s).
- **Branded API hostname (api.redmarklogic.com)**: The stable public name for the
  backend; the only hostname in scope.
- **Backend service**: The Cloud Run service (not yet deployed) that the hostname must
  reach; owned by the walking-skeleton deploy chain, a dependency of this feature.
- **Domain-attachment resource**: Whatever GCP-side object binds hostname to service
  (mechanism selected in plan phase); must live in IaC.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A public-internet request to the backend health endpoint via the branded
  address succeeds with a trusted certificate within 48 hours of starting the cutover.
- **SC-002**: Zero pre-existing DNS records modified or deleted (pre/post zone snapshot
  diff is empty except for the added record(s)).
- **SC-003**: Email to and from the founder mailbox works throughout and after the
  change (test round-trip succeeds; no delivery gap attributable to the change).
- **SC-004**: A backend re-deploy after cutover requires zero DNS/certificate touches
  and the branded address keeps serving (verified once post-cutover).
- **SC-005**: The documented procedure covers 100% of executed steps — an auditor can
  map every created resource/record to a documented step.

## Assumptions

- The founder has (or can create) Cloudflare API credentials with permission to edit
  DNS for redmarklogic.com; account access is available for any dashboard-only step.
- The walking-skeleton deploy chain (#63-#72) delivers a running Cloud Run service in
  redmarklogic-prod / australia-southeast1; this feature depends on it and does not
  deploy the service itself.
- redmarklogic.com remains on Cloudflare nameservers; no registrar or nameserver
  migration is in scope.
- Only `api.redmarklogic.com` is in scope. Apex (`redmarklogic.com`), `www`, and any
  future frontend hostnames are out of scope.
- Cost posture per ADR-022 stands: experimental stage targets ~$0/month. The founder
  explicitly rejected the paid load-balancer route (2026-06-11); the selected free
  proxy route's 60-second request ceiling is an accepted POC trade-off, revisited only
  when real traffic or long-running branded-address requests demand it.

## Dependencies

- **Blocking**: A deployed Cloud Run backend service (walking-skeleton deploy chain
  #63-#72). DNS/verification steps that need a live service cannot complete before it.
- **Governance**: ADR-020 (Terraform IaC), ADR-022 (hosting, ingress, no-LB posture),
  ADR-023 (environment split, where applicable).
- **Research input**: DevOps findings on Cloudflare CLI/API options and the supported
  Cloud Run domain-attachment mechanisms for australia-southeast1 (in progress,
  `.agents/tmp/dns-domain-research-2026-06-11/findings.md`) — feeds the plan phase.
