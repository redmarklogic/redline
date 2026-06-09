# Contract: infra/terraform/terraform.tfvars

**Owner**: Brent (DevOps)
**Consumers**: All deploy-chain issues #65-#72, CI/CD scripts, Workload Identity config

**Stability**: Volatile (per ADR-017) until all deploy-chain issues are closed.

**Supersedes**: `inventory-schema.md` (removed — ADR-020 replaced inventory.yml with
`terraform.tfvars` as the canonical identity SSOT).

## Schema

```hcl
# infra/terraform/terraform.tfvars
# SSOT for GCP project identifiers — ADR-001, ADR-020

project_id      = "redmarklogic-prod"
region          = "australia-southeast1"
billing_account = "XXXXXX-XXXXXX-XXXXXX"

# Exactly one of folder_id or org_id must be set; comment out the other
folder_id = "000000000000"
# org_id  = "000000000000"

state_bucket = "redmarklogic-tf-state"

apis = [
  "run.googleapis.com",
  "artifactregistry.googleapis.com",
  "cloudbuild.googleapis.com",
  "secretmanager.googleapis.com",
  "iap.googleapis.com",
  "dns.googleapis.com",
  "compute.googleapis.com",
  "iam.googleapis.com",
  "cloudresourcemanager.googleapis.com",
]
```

## Corresponding variables.tf declarations

```hcl
variable "project_id"      { type = string }
variable "region"          { type = string }
variable "billing_account" { type = string }
variable "folder_id"       { type = string; default = "" }
variable "org_id"          { type = string; default = "" }
variable "state_bucket"    { type = string }
variable "apis"            { type = list(string) }
```

## Rules

- `project_id` is the SSOT consumed by all downstream Terraform modules and scripts.
  No HCL resource block or shell script may hardcode the project ID.
- `billing_account` stores the account ID only (no keys). Safe to version-control.
- `state_bucket` must match the bucket created by `infra/bootstrap/bootstrap.sh`.
- Exactly one of `folder_id` or `org_id` must be non-empty; both empty causes
  `gcloud projects create` in bootstrap.sh to fail.
- Additions to `apis` require a corresponding FR update in the governing spec.

## Outputs (from outputs.tf)

After `terraform apply`, the following values are available via `terraform output`:

| Output | Description |
|--------|-------------|
| `project_number` | GCP-assigned numeric project ID (consumed by downstream modules) |
| `state_bucket` | Name of the GCS bucket holding Terraform state |

## Breaking changes

Any rename of a top-level variable is a breaking change requiring updates to all
downstream Terraform modules and the bootstrap script in the same PR.
