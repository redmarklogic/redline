# Research: GCP Project Baseline

**Feature**: 005-gcp-project-baseline
**Date**: 2026-06-10

## Decisions

### Project naming convention

**Decision**: `redmarklogic-prod` for the initial single-environment project.

**Rationale**: GCP project IDs must be globally unique, 6-30 chars, lowercase letters,
digits, hyphens. `redmarklogic-prod` matches the organisation name and signals the
deployment target clearly. A separate `redmarklogic-staging` project is deferred until
the deploy chain is stable (see spec Assumption 3).

**Alternatives considered**:
- `redline-prod` — too generic, higher collision risk.
- `rl-prod` — too short, poor discoverability.
- Timestamp suffix — rejected, adds noise without benefit at single-project stage.

---

### gcloud vs Terraform

**Decision**: Terraform for all GCP infrastructure; one-off `gcloud` bootstrap for the
two resources Terraform needs before it can initialize (GCP project + GCS state bucket).
Recorded in ADR-020.

**Rationale**: Terraform provides drift detection, automatic idempotency via state
tracking, platform-agnostic HCL (eliminates the PS1/Bash dual-script overhead from
ADR-019), and a `terraform plan` diff that satisfies SOC 2 CC8.1 change management at
zero marginal effort. The state bucket cost is negligible (fractions of a cent/month).
The only imperative code is two `gcloud` commands in `bootstrap.sh`.

**Alternatives considered**:

- `gcloud` scripts only — rejected: hand-coded idempotency, no drift detection,
  dual PS1/Bash maintenance burden, no audit diff.
- Pulumi/CDK — rejected: introduce a Python/TypeScript dependency for infra code
  without benefit at this scale. Terraform HCL is the industry standard for GCP.
- GCP Console manual steps — rejected: not reproducible, no audit trail.

---

### Inventory file format

**Decision**: YAML (`infra/inventory.yml`), not `.env` or JSON.

**Rationale**: YAML is human-readable, supports comments (for documenting why each
value was chosen), and is natively parsed by the Python toolchain already in use.
JSON lacks comments. `.env` files have no schema and are conventionally excluded from
version control.

**Alternatives considered**:
- `.env` file — rejected (no schema, typically gitignored).
- `terraform.tfvars` — rejected (couples to Terraform before it is adopted).
- JSON — rejected (no comment support).

---

### API enablement scope

**Decision**: Enable all nine APIs listed in FR-003 in a single provisioning pass.

**Rationale**: All APIs are required by issues in the deploy chain (#65-#72). Enabling
them upfront avoids repeated permission errors during downstream provisioning. API
enablement is idempotent — enabling an already-enabled API is a no-op.

**Verified availability in `australia-southeast1`**: Cloud Run, Artifact Registry,
Cloud Build, Secret Manager, IAP, Cloud DNS, Compute Engine, IAM, Resource Manager
are all available in `australia-southeast1` as of 2026-06.

---

### Single vs dual project (staging/prod)

**Decision**: Single project at this baseline stage.

**Rationale**: The deploy chain issues (#65-#72) target a single environment. The spec
explicitly defers staging/prod separation. Introducing two projects now doubles
provisioning complexity and billing linkage steps without current benefit.

**Alternatives considered**:
- Dual project — deferred to a later spec when environment parity is required.
