# Cloud Run Connection Strategy

**Author**: Brent (DevOps)
**Date**: 2026-06-10
**Relates to**: ADR-022, issue #63

## Purpose

Map every connection in and out of the Redline Cloud Run service so provisioning
decisions are grounded and reviewable before any `terraform apply` run. This
document is the operational companion to ADR-022 (hosting decision). Together they
constitute the Tier-1 approval package.

## Inbound Connections

| Property | Value |
|----------|-------|
| Protocol | HTTPS (TLS 1.2+) |
| Port | 443 (Cloud Run managed; container listens on 8000) |
| TLS management | Cloud Run managed certificate — no manual cert provisioning |
| Load balancer | None at this stage; Cloud Run serves directly |
| Ingress setting | `all` (public internet access) |
| Identity-Aware Proxy | Not provisioned — see ADR-022 Out of Scope |
| Current auth gate | Bearer token presence-only (placeholder); no token verification |

Cloud Run terminates TLS and proxies requests to the container on port 8000.
The `EXPOSE 8000` directive in the Dockerfile and the uvicorn `--host 0.0.0.0
--port 8000` CMD are consistent with this.

The Bearer presence-only auth gate is intentional. Full SSO/IdP wiring is B-1b
scope (issue #73). Until that lands, any request with a non-empty Authorization
header passes the gate.

## Image Pull Chain

| Step | Detail |
|------|--------|
| Registry | Artifact Registry, region: australia-southeast1 |
| Repository path | `australia-southeast1-docker.pkg.dev/<PROJECT_ID>/redline/marker` |
| Image name | `marker` |
| Pull cost | Zero — same-region pull from AR to Cloud Run incurs no egress charge |
| Required IAM role | Cloud Run service account needs `roles/artifactregistry.reader` on the repository |
| Authentication | Workload Identity (default Cloud Run service account); no long-lived keys |

The builder + runtime multi-stage Dockerfile at `deploy/docker/marker/Dockerfile`
produces the image. The runtime stage uses `python:3.14-slim` and runs as a
non-root user (`appuser`, UID 1000).

## Outbound Connections

**None at this stage.**

The Marker API is purely request/response. It receives an HTTP request, generates
a DOCX document in memory, and returns the binary response. It makes no outbound
calls to databases, external APIs, message queues, or other services.

If an outbound call is introduced (e.g., a database connection, an LLM API call,
or a call to an internal microservice), this document must be updated and the
connection reviewed before the change is deployed.

## Future: VPC Connector

A VPC connector will be required if the Cloud Run service needs to reach any
private GCP resource, including:

- Cloud SQL (relational database)
- Memorystore (Redis/Valkey)
- Internal GCP services on a private VPC

Until a private resource is added, no VPC connector is needed and no private IP
configuration is required. The trigger condition is: any new dependency on a
resource that is not reachable over the public internet.

When a VPC connector becomes necessary:
1. Provision a Serverless VPC Access connector in `australia-southeast1`.
2. Attach it to the Cloud Run service via the `--vpc-connector` flag (Terraform:
   `google_cloud_run_v2_service` `vpc_access` block).
3. Author a new or amended ADR recording the private resource and network topology.

## Provisioning Clearance

**Brent is cleared to provision the following GCP resources:**

1. **Artifact Registry repository** — `australia-southeast1`, Docker format, named
   `redline`. Grant the Cloud Run service account `roles/artifactregistry.reader`.
2. **Cloud Run service** — region `australia-southeast1`, image from the Artifact
   Registry repository above. Runtime settings per ADR-022: CPU throttled,
   min-instances 0, request timeout 300 s, max concurrency 80. Ingress: `all`.
3. **Public HTTPS ingress** — Cloud Run managed TLS, no load balancer, no IAP.

All three resources are declared in Terraform HCL under `deploy/infra/terraform/`
per ADR-020. No console changes are permitted after initial provisioning.

**Not cleared (pending separate decisions):**

- IAP / SSO configuration — B-1b scope, issue #73
- VPC connector — see Future section above
- CI/CD pipeline — separate deploy-chain task
- Secret Manager entries — not needed at this stage
