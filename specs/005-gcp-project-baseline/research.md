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

**Decision**: `gcloud` imperative scripts for this baseline.

**Rationale**: Terraform adds state management overhead (remote state backend, lock
files, provider versions) that is unnecessary for a one-time project bootstrap.
The spec requires idempotency; `gcloud` achieves this with `--quiet` flags and
conditional checks. Terraform can be introduced at a later spec if the number of
managed resources warrants it.

**Alternatives considered**:
- Terraform — deferred, overhead not justified for single bootstrap.
- GCP Console manual steps — rejected, not reproducible, violates CLI-first principle.

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
