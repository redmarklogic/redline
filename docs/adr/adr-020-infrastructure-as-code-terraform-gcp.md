# ADR-020 — Infrastructure as Code with Terraform for GCP

## Summary

All GCP infrastructure is defined and managed via Terraform (HashiCorp Configuration
Language). A single one-off shell script handles the chicken-and-egg bootstrap (GCP
project creation and Terraform state bucket). After that initial bootstrap, no human
operator or CI job modifies GCP infrastructure except through `terraform apply` on
reviewed HCL. The `gcloud` CLI remains in use for operational commands that are not
infrastructure (deployments, image pushes, diagnostics).

**Deciders**: Peter (architecture), Brent (DevOps)

## Status

Accepted — 2026-06-10

## Decision

1. **Terraform owns all GCP infrastructure** after the bootstrap step. Every resource
   (API enablement, billing linkage, Cloud Run service, Artifact Registry, IAP, DNS,
   Secret Manager, IAM bindings, Load Balancer) is declared in HCL under `infra/terraform/`.

2. **Bootstrap exception** — exactly two resources are created outside Terraform because
   Terraform requires them before it can initialise:
   - The GCP project itself (`gcloud projects create`)
   - The GCS bucket for Terraform remote state (`gcloud storage buckets create`)

   Both are created by `infra/bootstrap/bootstrap.sh`. This script runs once, ever.
   Subsequent runs are idempotent (check-before-create guards). After it completes,
   Terraform manages all further configuration of the project.

3. **`gcloud` CLI is reserved for**:
   - The bootstrap script above.
   - Read-only / diagnostic operations (`describe`, `list`, `get`) — at any time.
   - Operational commands not owned by Terraform: `gcloud run deploy`, `gcloud artifacts
     docker push`, `gcloud auth` — these are deployment/release actions, not
     infrastructure definitions.

4. **Console changes to Terraform-managed resources are prohibited.** Any change made
   via the GCP Console to a resource Terraform manages will be reverted on the next
   `terraform apply`. This is enforced by policy, not tooling, at this stage.

5. **HCL files are platform-agnostic.** The `terraform` CLI runs identically on Windows
   and Linux. This supersedes the dual-script pattern (`.ps1` + `.sh`) for infra work
   that ADR-019 would otherwise imply — the bootstrap shell script is the only remaining
   platform concern for infra.

## Context

The walking-skeleton deploy chain (#63–#72) requires provisioning roughly a dozen GCP
resources. Two implementation approaches were evaluated:

**Option A — Imperative `gcloud` scripts**: Write `bootstrap.ps1` (Windows dev) and
`bootstrap.sh` (Linux CI) that call `gcloud` commands in sequence. Idempotency is
hand-coded. No state tracking. Drift from manual console changes is invisible.

**Option B — Terraform IaC (selected)**: Declare resources in HCL. Terraform tracks
state, produces a diff on every `plan`, detects and rejects drift, and handles
idempotency automatically. HCL is platform-agnostic — one set of files for Windows and
Linux. The only imperative code is the two-command bootstrap script.

ADR-016 (CLI-first) addresses agent tool selection (gh / gws / gcloud for Claude Code
operations). It does not govern infrastructure provisioning tooling. Terraform is not an
agent action tool — it is a dedicated IaC runtime. ADR-016 and ADR-020 are orthogonal.

## Options Considered

- **Imperative gcloud scripts (Option A)**: Discarded. Two scripts to maintain
  (PS1 + Bash), hand-coded idempotency, no drift detection, no audit diff on apply.
  The only advantage — no state bucket required — is outweighed by the operational risk.

- **Terraform (Option B, selected)**: Declarative, state-tracked, drift-detecting,
  platform-agnostic. SOC 2 change-management evidence comes for free: every infra change
  is a PR with a `terraform plan` diff. The state bucket has negligible cost (fractions
  of a cent/month for small state files).

- **Pulumi / CDK**: More capable but introduce Python/TypeScript dependency for infra
  code. Terraform HCL is the industry standard for GCP/multi-cloud IaC and produces the
  most readable diffs. Rejected at this scale.

## Decision Rationale

Three drivers:

1. **SOC 2 change management (CC8.1) at zero marginal effort**: Every `terraform apply`
   requires a `terraform plan` diff in a PR. Git history is the audit trail. No extra
   tooling needed.

2. **Drift detection**: Terraform detects when a resource in GCP diverges from the
   declared state. Imperative scripts cannot do this — a manual console change is
   invisible until something breaks.

3. **Platform cost of dual scripts eliminated**: ADR-019 required `.ps1` + `.sh` pairs
   for any script that must run on both Windows and Linux. Terraform HCL removes this
   overhead entirely — one file set, two platforms.

## Consequences

**Positive:**
- All infrastructure changes are reviewed via PR before applying — satisfies SOC 2 CC8.1.
- `terraform plan` in CI produces a human-readable diff before every apply.
- Drift detection: `terraform plan` will flag any out-of-band console changes.
- Platform-agnostic: developers on Windows and Linux CI use identical commands.
- Idempotency is automatic — `terraform apply` is safe to re-run.

**Negative / constraints:**
- GCS state bucket must exist before `terraform init`. The bootstrap script handles this
  and must be documented clearly as the one-off exception.
- `terraform state` operations (`import`, `mv`, `rm`) are Brent tasks requiring care —
  state file corruption is recoverable but disruptive.
- Terraform provider version pinning must be maintained in `versions.tf`.
- Console changes to Terraform-managed resources will be reverted on next apply.
  Team members must be informed of this constraint before gaining GCP console access.

## Structure

```text
infra/
├── bootstrap/
│   └── bootstrap.sh        # One-off: gcloud project create + state bucket create
└── terraform/
    ├── backend.tf           # GCS remote state configuration
    ├── main.tf              # Google provider, project data source
    ├── variables.tf         # Input variable declarations
    ├── terraform.tfvars     # Canonical values (project_id, region, billing_account, etc.)
    ├── outputs.tf           # Exported values consumed by downstream infra
    ├── apis.tf              # google_project_service resources (FR-003 API list)
    └── billing.tf           # google_billing_project_info
```

`infra/terraform/terraform.tfvars` is the SSOT for all canonical project identifiers,
replacing the `inventory.yml` concept from earlier drafts (ADR-001 applies).

## References

- ADR-001 — Single Source of Truth (`terraform.tfvars` as the identity SSOT)
- ADR-016 — CLI-First Tool Selection (agent operations; orthogonal to this ADR)
- ADR-019 — Windows-dev / Linux deployment boundary (HCL supersedes dual-script pattern
  for infrastructure; bootstrap.sh is the only remaining infra platform concern)
- Issue #63 — Tier-1 infra ADR (must be accepted before `terraform apply` runs)
- Issue #64 — GCP project baseline (first feature implemented under this ADR)
