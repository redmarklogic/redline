# Implementation Plan: GCP Project Baseline

**Branch**: `005-gcp-project-baseline` | **Date**: 2026-06-10 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/005-gcp-project-baseline/spec.md`

**Note**: This is an infrastructure provisioning feature. There is no Python application
code. Deliverables are provisioning scripts, a verification script, and an inventory file.

## Summary

Stand up the GCP project foundation required by all deploy-chain issues (#65-#72).
Provisioning sets the project ID, locks the default region to `australia-southeast1`,
enables nine required APIs, links a billing account, and records canonical identifiers
in a version-controlled inventory file that acts as the SSOT for downstream scripts.

## Technical Context

**Language/Version**: Terraform 1.x (HCL) — platform-agnostic, runs identically on
Windows (dev) and Linux (CI). Supersedes the PS1/Bash dual-script pattern from ADR-019
for infrastructure work (ADR-020). Bootstrap step uses a single Bash script (Linux/CI)
for the two pre-Terraform `gcloud` commands.

**Primary Dependencies**:

- `terraform` CLI with `hashicorp/google` provider (pinned in `versions.tf`)
- `gcloud` CLI for bootstrap and operational commands (ADR-016, ADR-020)

**Storage**: `infra/terraform/terraform.tfvars` — version-controlled, SSOT for all
canonical GCP project identifiers (project_id, region, billing_account, folder_id).
Replaces the `inventory.yml` concept (Constitution I, ADR-001, ADR-020). Terraform
remote state stored in a GCS bucket created during bootstrap.

**Testing**: `terraform plan` (diff-based verification before every apply). Post-apply
verification via `gcloud` read-only commands. No pytest.

**Target Platform**: GCP `australia-southeast1`. HCL is platform-agnostic; bootstrap
script targets Linux/CI (Bash).

**Project Type**: Infrastructure as Code (Terraform) with one-off bootstrap script.

**Performance Goals**: End-to-end provisioning under 15 minutes from clean state (SC-001).

**Constraints**:

- Idempotent execution -- Terraform handles this automatically via state tracking (FR-005,
  SC-004). Bootstrap script uses check-before-create guards.
- No GCP Console changes to Terraform-managed resources (ADR-020, Constitution XV).
- Billing account and organisation/folder must exist before bootstrap runs (Assumptions).
- ADR gates: #48 and #63 must be accepted before `terraform apply` runs.

**Scale/Scope**: Single GCP project. Staging/prod separation is deferred.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design.*

| Principle | Assessment | Action |

|-----------|-----------|--------|
| I. SSOT | `infra/terraform/terraform.tfvars` is the canonical store for project ID, region, billing ref. No other file may define these (ADR-001, ADR-020). | Enforced by schema. |
| II. Hook-First | No application code rules to enforce. Not applicable. | N/A |
| VI. Data-Driven | Region, API list, and project identifiers live in `terraform.tfvars` — never hardcoded in HCL resource blocks. | Variables declared in `variables.tf`. |
| XII. CLI-First | `gcloud` used for bootstrap + operational commands. Terraform provider calls same APIs for infra. ADR-016 and ADR-020 are orthogonal (ADR-020 governs infra tooling). | Enforced by ADR-020. |
| XIV. Platform Obligation | HCL is platform-agnostic — no PS1/Bash split needed for infra. Bootstrap script is Bash (Linux/CI target). ADR-020 supersedes dual-script pattern for infra. | Single bootstrap.sh. |
| XV. IaC | All GCP infra declared in Terraform post-bootstrap. Console changes prohibited. | Enforced by ADR-020. |
| ADR before code | #48 and #63 must be accepted before `terraform apply` runs. | Gate task in tasks.md. |

**No constitution violations.** Complexity Tracking section omitted.

## Project Structure

### Documentation (this feature)

```text
specs/005-gcp-project-baseline/
├── plan.md                        # This file
├── research.md                    # Phase 0 output
├── contracts/
│   └── terraform-variables.md    # Phase 1 -- terraform.tfvars schema contract
└── tasks.md                       # Phase 2 output (speckit.tasks)
```

### Source Code (repository root)

```text
infra/
├── bootstrap/
│   └── bootstrap.sh      # One-off: gcloud project create + state bucket create (Bash)
└── terraform/
    ├── backend.tf         # GCS remote state configuration
    ├── main.tf            # Google provider config + project data source
    ├── variables.tf       # Input variable declarations
    ├── terraform.tfvars   # SSOT: project_id, region, billing_account, folder_id, apis[]
    ├── outputs.tf         # Exported values (project_number, state_bucket)
    ├── apis.tf            # google_project_service resources (FR-003 list)
    └── billing.tf         # google_billing_project_info
```

**Structure Decision**: `infra/bootstrap/` for the one-off script; `infra/terraform/` for
all IaC. No `src/` involvement — this feature has no application code. `terraform.tfvars`
is the only cross-feature artifact (SSOT per ADR-001, ADR-020); all other files are
internal to the Terraform module.
