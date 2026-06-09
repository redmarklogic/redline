# Infrastructure Identity — Canonical Values

**SSOT**: `infra/terraform/terraform.tfvars`

All GCP project identifiers are version-controlled in one file. Deploy-chain issues
(#65–#72) must read values from there — no other file may define or duplicate them
(ADR-001, ADR-020).

## Canonical values

| Identifier | Value | Where declared |
|---|---|---|
| `project_id` | `redmarklogic-prod` | `infra/terraform/terraform.tfvars` |
| `region` | `australia-southeast1` | `infra/terraform/terraform.tfvars` |
| `billing_account` | see tfvars (Brent) | `infra/terraform/terraform.tfvars` |
| `state_bucket` | `redmarklogic-tf-state` | `infra/terraform/terraform.tfvars` |
| `project_number` | GCP-assigned (post-apply) | `terraform output project_number` |

## How to consume

- **Static references** (scripts, CI config, HCL modules): read from
  `infra/terraform/terraform.tfvars`.
- **Post-apply values** (`project_number`): run `terraform output project_number`
  from `infra/terraform/`.

Do not ask the infrastructure owner for these values — they are in version control.

## References

- `infra/README.md` — full provisioning workflow
- ADR-020 — Infrastructure as Code with Terraform for GCP
- ADR-001 — Single Source of Truth
- Spec: `specs/005-gcp-project-baseline/spec.md`
