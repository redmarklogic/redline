# Research: Infra ADR + Tier-1 GCP Approval

**Branch**: `feature/63-infra-adr-tier-1-gcp-approval-cloud-run-artifact-registry`
**Date**: 2026-06-10
**Source**: Issue #48 brainstorm (2026-06-10) + code inspection

All decisions were resolved in the #48 architecture brainstorm before this spec
was written. This document records them as the canonical reference for plan and
tasks phases.

## Resolved Decisions

### 1. Runtime: Cloud Run

**Decision**: Cloud Run (australia-southeast1)
**Rationale**: Scales to zero; pay only for active compute; same-region pulls from
Artifact Registry are free; well within free tier for experimental use (~$0/month).
**Alternatives considered**: Azure Container Apps (discarded — project is on GCP),
GKE (discarded — over-engineered at this scale).

### 2. Registry: Artifact Registry

**Decision**: Artifact Registry (australia-southeast1, same region as Cloud Run)
**Rationale**: Same-region pulls to Cloud Run are zero-cost; native GCP integration;
IAM-based access control.
**Alternatives considered**: Docker Hub (discarded — private registry preferred for
production images), GCR (legacy — Artifact Registry is the current GCP standard).

### 3. CPU Allocation Mode: Throttled

**Decision**: CPU throttled (default)
**Rationale**: The FastAPI application has no background tasks. Code inspection of
`src/marker/` confirms: no `BackgroundTasks`, no `asyncio.create_task()`, no
worker threads. All requests are synchronous (request → response). CPU throttled
is cheaper and correct for this workload.
**Alternatives considered**: CPU always-allocated (discarded — only needed for
background tasks; would incur unnecessary cost).

### 4. Min-Instances: 0 (set to 1 pre-production)

**Decision**: `--min-instances=0` now; set to 1 before production launch
**Rationale**: Cold start for python:3.14-slim Alpine-style image is 1–5s from
zero. Acceptable for experimental use. Before production, 1 min-instance adds
~$15–20/month and eliminates cold starts.
**Alternatives considered**: 1 now (discarded — unnecessary cost for experimental
stage).

### 5. Request Timeout: 300s

**Decision**: 300s (Cloud Run default)
**Rationale**: DOCX generation and LLM calls may be slow; 300s provides adequate
headroom.
**Alternatives considered**: Lower timeout (discarded — risk of premature timeout
for large reports).

### 6. Concurrency: 80 requests/instance

**Decision**: 80 concurrent requests/instance (Cloud Run default)
**Rationale**: Default is acceptable for initial deployment. Must be load-tested
before production — OOM risk if requests hold large payloads in memory.
**Alternatives considered**: Lower concurrency (reserved for post-load-test tuning).

### 7. Container Image: python:3.14-slim + multi-stage

**Decision**: python:3.14-slim with builder/runtime multi-stage build
**Rationale**: Already implemented in `deploy/docker/marker/Dockerfile`. Produces a
~80–150 MB image. Slim (Debian-based) chosen over Alpine for broader binary
compatibility.
**Alternatives considered**: python:3.12 base (discarded — ~1 GB, slow cold starts),
pure Alpine (deferred — slim is sufficient; Alpine may cause C extension issues).

### 8. Runtime Secrets: None (APP_ENV only)

**Decision**: No Secret Manager entries needed at this stage. `APP_ENV` is the only
runtime environment variable and is non-secret.
**Rationale**: Auth is a Bearer presence-only placeholder. No database, no external
API keys, no signing secrets. All config flows through process environment per
ADR-021.
**Alternatives considered**: Secret Manager for APP_ENV (discarded — non-secret
value does not warrant Secret Manager overhead).

### 9. IAP / Auth Gate: Not sole gate; B-1b scope

**Decision**: IAP is not provisioned at this stage. Bearer presence-only auth is
the current gate. Full SSO/IdP wiring is B-1b scope (#73).
**Rationale**: IAP authenticates Google accounts only. The product serves both
Microsoft and Google identity users. Multi-IdP support requires a separate auth
provider decision.
**Alternatives considered**: IAP as sole gate (discarded — multi-IdP requirement
makes this unviable).

### 10. Environments: Single (prod)

**Decision**: Single environment (prod) now. Experiment/prod split planned later.
**Rationale**: Simplifies initial deploy chain. No feature flags or environment
routing needed at this stage.
**Alternatives considered**: Experiment + prod from day one (deferred — unnecessary
complexity for walking-skeleton).

### 11. ADR Numbering

**Decision**: ADR-022 (next sequential after ADR-021)
**Rationale**: `docs/adr/` scan confirms highest existing ADR is ADR-021.
