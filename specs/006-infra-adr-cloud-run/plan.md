# Implementation Plan: Infra ADR + Tier-1 GCP Approval (Cloud Run + Artifact Registry)

**Branch**: `feature/63-infra-adr-tier-1-gcp-approval-cloud-run-artifact-registry` | **Date**: 2026-06-10 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/006-infra-adr-cloud-run/spec.md`

## Summary

Author ADR-022 recording the Cloud Run + Artifact Registry hosting decision and
Tier-1 trust-boundary approval. File Brent's connection-strategy analysis covering
inbound/outbound/image-pull connections and explicit provisioning clearance. Both
documents constitute the governance gate that unblocks the rest of the deploy chain
(#67, #70, #76).

## Technical Context

**Language/Version**: N/A — documentation deliverables only (Markdown)

**Primary Dependencies**: N/A

**Storage**: `docs/adr/` (ADR-022) and `docs/infrastructure/` (connection-strategy)

**Testing**: Manual review against quickstart.md checklist; no automated tests
required for documentation

**Target Platform**: GCP — Cloud Run (australia-southeast1), Artifact Registry
(australia-southeast1)

**Project Type**: Governance/documentation — ADR + operational analysis

**Performance Goals**: N/A

**Constraints**:

- ADR-022 must not merge or duplicate ADR-018 (HTTP API contract) or ADR-020 (Terraform IaC)
- Auth placeholder (Bearer presence-only) is intentional — must be recorded as such, not flagged as a gap
- No Secret Manager entries in scope
- No VPC connector in scope (document trigger conditions only)
- No CI/CD pipeline in scope

**Scale/Scope**: Two Markdown files; one PR; one issue closed

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Verdict | Notes |
|-----------|---------|-------|
| I. Single Source of Truth | PASS | ADR-022 is the single authority for the hosting decision. Cross-references ADR-018 and ADR-020 without duplicating. |
| II. Hook-First Enforcement | N/A | Documentation only; no enforcement hook needed. |
| III. Defence-in-Depth | PASS | ADR records the decision; connection-strategy records the operational analysis. Two separate artifacts, two separate concerns. |
| IV. Dependency Direction | N/A | No skill/agent references introduced. |
| V. Facade Boundaries | N/A | No code changes. |
| VI. Data-Driven Configuration | N/A | No code changes. |
| VII. Shared Taxonomy | N/A | No taxonomy changes. |
| VIII. Determinism Over LLM Inference | PASS | All values sourced from confirmed brainstorm decisions and code inspection, not LLM inference. |
| IX. Citation-Only Knowledge Storage | N/A | No standards knowledge store changes. |

No violations. No complexity justification required.

## Project Structure

### Documentation (this feature)

```text
specs/006-infra-adr-cloud-run/
├── plan.md          # This file
├── research.md      # Resolved decisions from #48 brainstorm + code inspection
├── quickstart.md    # Verification checklist
└── tasks.md         # Phase 2 output (speckit.tasks)
```

### Deliverable Files (repository root)

```text
docs/
├── adr/
│   └── adr-022-cloud-run-artifact-registry-hosting.md   # NEW — ADR-022
└── infrastructure/                                        # NEW directory
    └── cloud-run-connection-strategy.md                   # NEW — connection strategy
```

No source code changes. No test files. No config changes.

## Phase 0: Research

Complete. All decisions resolved. See [research.md](research.md).

No NEEDS CLARIFICATION items. No dependencies requiring best-practice research.

## Phase 1: Design

### ADR-022 Structure

Standard ADR format following existing conventions in `docs/adr/`:

```text
# ADR-022 — Cloud Run + Artifact Registry Hosting

## Summary
## Status
## Decision
## Context
## Options Considered
## Consequences
## Out of Scope
## Cross-References
```

Key content per section:

**Decision**: Cloud Run (australia-southeast1) as serverless runtime; Artifact
Registry (australia-southeast1) as container registry. Tier-1 trust-boundary
approved: public HTTPS ingress, no IAP gate at this stage, Bearer presence-only
auth as current gate.

**Context**: Walking-skeleton deploy chain (#63-#72); issue #48 ratification;
ADR-020 Terraform IaC governance; ADR-021 process-environment config.

**Consequences**: Brent cleared to provision. CPU throttled. 0 min-instances.
300s timeout. 80 concurrency. python:3.14-slim multi-stage image. No Secret
Manager entries needed yet.

**Out of Scope**: IAP/SSO (B-1b, #73), VPC connector, CI/CD pipeline, Cloud SQL,
multi-environment split, Secret Manager entries.

**Cross-References**: ADR-018 (HTTP API contract), ADR-020 (Terraform IaC),
ADR-021 (process environment config), issue #48 (ratification), issue #63
(governance gate).

### Connection-Strategy Document Structure

```text
# Cloud Run Connection Strategy

## Purpose
## Inbound Connections
## Image Pull Chain
## Outbound Connections
## Future: VPC Connector
## Provisioning Clearance
```

Key content per section:

**Inbound**: Public HTTPS on port 443. Cloud Run managed TLS. No load balancer at
this stage. Ingress setting: `all`. No IAP.

**Image pull**: Artifact Registry (australia-southeast1). Same-region pull = zero
egress cost. Cloud Run service account requires `roles/artifactregistry.reader`.

**Outbound**: None currently. Purely request/response with no outbound calls. VPC
connector will be required when private GCP resources are added (Cloud SQL,
Memorystore, internal services).

**Clearance**: Explicit statement — Brent is cleared to provision Cloud Run
service, Artifact Registry repository, and public ingress.

## Phase 2: Implementation Tasks

See [tasks.md](tasks.md) (generated by speckit.tasks).
