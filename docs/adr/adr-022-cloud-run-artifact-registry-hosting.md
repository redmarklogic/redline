# ADR-022 — Cloud Run + Artifact Registry Hosting

## Summary

Redline's backend API runs on Google Cloud Run (australia-southeast1) with container
images stored in Artifact Registry (same region). This ADR records the hosting
decision, the runtime configuration constraints, and the Tier-1 trust-boundary
approval that permits public HTTPS ingress without an Identity-Aware Proxy gate.
It is the governance gate for the walking-skeleton deploy chain (#63–#72).

**Deciders**: Peter (architecture), Brent (DevOps), Founder

## Status

Accepted — 2026-06-10. Partially superseded by ADR-023 — 2026-06-11 (scope statements
only: the Out-of-Scope items "Multi-environment split" and "Secret Manager entries",
the related single-environment and no-Secret-Manager statements in Context and
Consequences, and Decision point 4 (min-instances). The hosting decision stands.)

## Decision

1. **Runtime**: Google Cloud Run (region: australia-southeast1). Serverless;
   scales to zero; billed only for active compute.

2. **Registry**: Google Artifact Registry (region: australia-southeast1). Same-region
   image pulls to Cloud Run incur zero egress cost.

3. **CPU allocation mode**: Throttled (default). The FastAPI application is purely
   request/response with no background tasks. CPU throttled is correct and cheaper
   than always-allocated for this workload.

4. **Min-instances**: 0. Cold start from zero is 1–5 s for the current image, which
   is acceptable for experimental use. Set to 1 before production launch (~$15–20/month
   additional cost) to eliminate cold starts.

5. **Request timeout**: 300 s (Cloud Run default). Provides adequate headroom for
   DOCX generation and future LLM calls.

6. **Concurrency**: 80 concurrent requests per instance (Cloud Run default). Must be
   load-tested before production — OOM risk exists if requests hold large payloads in
   memory simultaneously.

7. **Container image**: `python:3.14-slim` with multi-stage build (builder + runtime
   stages). Produces an ~80–150 MB image. Already implemented at
   `deploy/docker/marker/Dockerfile`.

8. **Tier-1 trust-boundary approval**:
   - Public HTTPS ingress is approved. Cloud Run managed TLS; no load balancer at
     this stage; ingress setting: `all`.
   - Identity-Aware Proxy (IAP) is not required at this stage. IAP wiring is B-1b
     scope (issue #73).
   - The current auth gate is Bearer token presence-only (no token verification).
     This is an intentional placeholder pending SSO/IdP wiring in B-1b. It is not a
     security gap that blocks Tier-1 approval.

## Context

The walking-skeleton deploy chain (#63–#72) requires a runtime and registry decision
before Brent can provision any GCP resources. Issue #48 ratified Cloud Run and
Artifact Registry as the chosen services. This ADR records the full decision with
all runtime constraints so the rationale is preserved independently of the issue
thread.

**Key constraints informing the decision:**

- GCP project region: australia-southeast1 (low-latency for Australian users; Tier 2
  pricing applies for always-on workloads — ~$40–55/month for 2 instances at ~100
  concurrent users).
- Experimental cost target: ~$0/month (scales to zero; well inside GCP free tier:
  180k vCPU-seconds, 360k GiB-seconds, 2M requests/month).
- Auth provider must support both Google and Microsoft identity (IAP cannot be sole
  gate — see Out of Scope).
- Infrastructure is managed via Terraform (ADR-020). This ADR records what is
  provisioned; the Terraform HCL declaring how is in `deploy/infra/terraform/`.
- All runtime config flows through process environment (ADR-021). No Secret Manager
  entries are needed at this stage — `APP_ENV` is the only runtime environment
  variable and is non-secret.

## Options Considered

| Option | Decision | Reason |
|--------|----------|--------|
| **Cloud Run** (selected) | Runtime | Scales to zero; pay-per-use; same-region AR pulls free; no cluster management |
| GKE | Rejected | Over-engineered at this scale; cluster overhead; higher fixed cost |
| Cloud Functions | Rejected | Less suited to FastAPI application pattern; less control over runtime |
| **Artifact Registry** (selected) | Registry | Native GCP integration; same-region pull is free; IAM-based access control |
| Docker Hub | Rejected | External dependency; private registry preferred for production images |
| GCR (legacy) | Rejected | Artifact Registry is the current GCP standard; GCR is deprecated |
| CPU always-allocated | Rejected | Only needed for background tasks; app has none (confirmed by code inspection) |
| Min-instances = 1 now | Deferred | Unnecessary cost for experimental stage; set before production |

## Consequences

**Immediate:**
- Brent is cleared to provision: Cloud Run service, Artifact Registry repository,
  public HTTPS ingress. See `docs/infrastructure/cloud-run-connection-strategy.md`
  for connection details.
- No Secret Manager provisioning needed at this stage.
- No VPC connector needed at this stage.
- No CI/CD pipeline in scope for this ADR.

**Before production:**
- Set `--min-instances=1` to eliminate cold starts (~$15–20/month additional).
- Load-test and tune concurrency per-instance to avoid OOM on large payloads.
- Verify CPU allocation mode remains correct (throttled) after any background task
  is introduced.

**Ongoing:**
- Any change to IAP, auth provider, VPC connector, or multi-environment split
  requires a new or amended ADR — those are not covered here.

## Out of Scope

The following are explicitly excluded from this ADR:

- **IAP / SSO wiring** — B-1b scope, issue #73. Multi-IdP requirement (Google +
  Microsoft identity) makes IAP-alone unviable; full auth provider decision deferred.
- **VPC connector** — only needed when Cloud Run reaches a private GCP resource
  (Cloud SQL, Memorystore, internal services). Not in scope now.
- **CI/CD pipeline** — manual `gcloud run deploy` is acceptable for the first smoke
  test. Pipeline is a separate task in the deploy chain.
- **Cloud SQL** — no database in scope for this deployment.
- **Multi-environment split** — single environment (prod) now; experiment/prod split
  is a future concern.
- **Secret Manager entries** — no secrets at this stage. If signing keys, API tokens,
  or database credentials are introduced, they must be stored in Secret Manager and
  loaded via process environment per ADR-021.

## Cross-References

- **ADR-018** — External HTTP API Contract Conventions. Governs the HTTP surface the
  Cloud Run service exposes. Not duplicated here.
- **ADR-020** — Infrastructure as Code with Terraform for GCP. Governs how all GCP
  resources (including Cloud Run and Artifact Registry) are declared in HCL. Not
  duplicated here.
- **ADR-021** — Process Environment as Sole Config Source. Governs how runtime
  configuration reaches the Cloud Run service. Not duplicated here.
- **Issue #48** — Cloud Run + Artifact Registry ratification (CLOSED). Source of the
  architecture brainstorm decisions recorded in this ADR.
- **Issue #63** — Infra ADR + Tier-1 GCP Approval governance gate. Closed by this
  ADR's merge.
- **Issue #73** — B-1b SSO/IdP wiring (future). Completes the auth gate left open
  by this ADR's Tier-1 approval.
