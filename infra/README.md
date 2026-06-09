# infra/

GCP infrastructure for Redline. All resources are defined as Infrastructure as Code
per ADR-020. The GCP Console must not be used to modify Terraform-managed resources —
any console change will be reverted on the next `terraform apply`.

## Directory structure

```text
infra/
├── bootstrap/
│   └── bootstrap.sh        # One-off: creates GCP project + Terraform state bucket
└── terraform/
    ├── versions.tf          # Terraform and provider version constraints
    ├── backend.tf           # GCS remote state configuration
    ├── main.tf              # Google provider config + project data source
    ├── variables.tf         # Input variable declarations
    ├── terraform.tfvars     # SSOT: canonical project identifiers (ADR-001, ADR-020)
    ├── outputs.tf           # Post-apply values consumed by downstream infra
    ├── apis.tf              # google_project_service resources (FR-003 API list)
    └── billing.tf           # google_billing_project_info (billing linkage)
```

## bootstrap/

`bootstrap.sh` runs **once, ever**. It creates the two resources that must exist before
`terraform init` can run:

1. The GCP project (`gcloud projects create`)
2. The Terraform state bucket (`gcloud storage buckets create`)

Subsequent runs are idempotent — check-before-create guards skip creation if the
resource already exists.

**Before running bootstrap.sh**, replace the placeholder values in
`infra/terraform/terraform.tfvars`:
- `billing_account`: real billing account ID (format `XXXXXX-XXXXXX-XXXXXX`)
- `folder_id` or `org_id`: the GCP folder or organisation ID that owns the project

See the TODO comments in `terraform.tfvars`.

## terraform/

All GCP infrastructure after the bootstrap step is managed by Terraform.

### Consuming canonical values

| Use case | Where to read |
|---|---|
| Project ID, region, billing account (static references in scripts) | `infra/terraform/terraform.tfvars` |
| Project number, state bucket name (post-apply, GCP-assigned values) | `terraform output <name>` from `infra/terraform/` |

Do not hardcode project ID, region, or billing account in any HCL resource block or
shell script. Always reference `terraform.tfvars` or `var.*` variables.

### Workflow

```bash
# 1. One-off bootstrap (only needed once per environment)
cd infra/bootstrap
./bootstrap.sh

# 2. Initialise Terraform (connects to GCS remote state)
cd infra/terraform
terraform init

# 3. Preview changes
terraform plan

# 4. Apply changes (after PR review of the plan diff)
terraform apply

# 5. Read outputs
terraform output project_number
terraform output project_id
```

### ADR-020 constraint

No human operator or CI job may modify GCP infrastructure except through
`terraform apply` on reviewed HCL. Every infrastructure change is a PR with a
`terraform plan` diff before it is applied. This satisfies SOC 2 CC8.1 change
management evidence requirements.

## References

- ADR-001 — Single Source of Truth (`terraform.tfvars` as the identity SSOT)
- ADR-020 — Infrastructure as Code with Terraform for GCP
- spec: `specs/005-gcp-project-baseline/spec.md`
- Deploy-chain issues: #65–#72
