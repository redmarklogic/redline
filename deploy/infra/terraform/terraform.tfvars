# SSOT for GCP project identifiers
# References: ADR-001 (Single Source of Truth), ADR-020 (Terraform IaC for GCP)
#
# This file is the canonical identity record consumed by all deploy-chain issues #65-#72,
# CI/CD scripts, and Workload Identity config. No script or HCL resource block may
# hardcode any of these values.
#
# TODO (Brent): Replace placeholder values for billing_account and folder_id before
# running infra/bootstrap/bootstrap.sh. These are Brent's domain (DevOps).
# Safe to commit — billing_account is an account ID only, not a key.

project_id      = "redmarklogic-prod"
region          = "australia-southeast1"
billing_account = "XXXXXX-XXXXXX-XXXXXX"

# Exactly one of folder_id or org_id must be set; comment out the other.
folder_id = "000000000000"
# org_id  = "000000000000"

state_bucket = "redmarklogic-tf-state"

# ── Cloud Run deployment variables (spec-70) ─────────────────────────────────
# image_tag is NOT set here — must be supplied at plan/apply time as a CLI -var
# to prevent mutable tags being silently accepted.
artifact_registry_repo = "redline-repo"
max_instances_staging  = 3
max_instances_prod     = 10

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
