# Contract: infra/inventory.yml

**Owner**: Brent (DevOps)
**Consumers**: All deploy-chain issues #65-#72, CI/CD scripts, Workload Identity config

**Stability**: Volatile (per ADR-017) until all deploy-chain issues are closed.

## Schema

```yaml
gcp:
  project_id: "redmarklogic-prod"          # GCP project ID (globally unique)
  project_number: "123456789012"           # GCP project number (read-only, set post-provision)
  region: "australia-southeast1"           # Default region for all resource creation
  billing_account: "XXXXXX-XXXXXX-XXXXXX" # GCP billing account ID
  # Exactly one of organisation_id or folder_id must be set; the other must be absent
  # organisation_id: "000000000000"        # GCP organisation ID (use if project anchors at org root)
  folder_id: "000000000000"               # GCP folder ID (use if project anchors under a folder)

  apis_enabled:
    - run.googleapis.com
    - artifactregistry.googleapis.com
    - cloudbuild.googleapis.com
    - secretmanager.googleapis.com
    - iap.googleapis.com
    - dns.googleapis.com
    - compute.googleapis.com
    - iam.googleapis.com
    - cloudresourcemanager.googleapis.com
```

## Rules

- `project_id` is the SSOT consumed by all downstream scripts. No script may hardcode
  the project ID directly.
- `billing_account` stores the account ID only (no sensitive keys). The value is safe
  to version-control.
- `project_number` is populated after provisioning (T015) and must not be hand-edited.
- Exactly one of `organisation_id` or `folder_id` must be present; `gcloud projects create`
  requires one to anchor the project in the resource hierarchy (FR-001).
- Additions to `apis_enabled` require a corresponding FR update in the governing spec.

## Breaking changes

Any rename of a top-level key is a breaking change. Downstream scripts must be updated
in the same PR that changes this schema.
