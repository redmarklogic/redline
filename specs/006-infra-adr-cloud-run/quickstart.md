# Quickstart: Verify Infra ADR + Connection-Strategy Deliverables

## Purpose

Verify the two deliverables for issue #63 are correct and complete before merging.

## Steps

### 1. Verify ADR-022 exists and is accepted

```text
docs/adr/adr-022-cloud-run-artifact-registry-hosting.md
```

Open the file and confirm:
- Status line reads: `Accepted`
- Date: 2026-06-10 (or the date of authoring)
- Sections present: Summary, Status, Decision, Context, Options Considered,
  Consequences, Out of Scope, Cross-References

### 2. Verify ADR-022 records all #48 brainstorm decisions

Check each item from research.md is present in the ADR:
- Cloud Run, australia-southeast1
- Artifact Registry, australia-southeast1
- CPU throttled
- Min-instances: 0 (1 pre-production)
- Request timeout: 300s
- Concurrency: 80 req/instance
- python:3.14-slim multi-stage image

### 3. Verify Tier-1 trust-boundary approval is recorded

Confirm the ADR contains an explicit Tier-1 approval statement covering:
- Public HTTPS ingress approved
- IAP not required at this stage
- Bearer presence-only auth is current gate
- Auth placeholder is intentional (pending B-1b)

### 4. Verify cross-references

Confirm ADR-022 references:
- ADR-018 (HTTP API contract) — not merged
- ADR-020 (Terraform IaC) — not merged

### 5. Verify connection-strategy document

```text
docs/infrastructure/cloud-run-connection-strategy.md
```

Confirm sections present:
- Inbound: public HTTPS, Cloud Run managed TLS, ingress=all
- Image pull: Artifact Registry same-region, artifactregistry.reader role
- Outbound: none currently; VPC connector trigger conditions documented
- Clearance: explicit statement Brent cleared to provision Cloud Run + AR + ingress

### 6. Verify issue #63 is closed (post-merge)

After the PR merges: check GitHub issue #63 status = Closed.
