# SSOT for GCP project identifiers
# References: ADR-001 (Single Source of Truth), ADR-020 (Terraform IaC for GCP)
#
# This file is the canonical identity record consumed by all deploy-chain issues #65-#72,
# CI/CD scripts, and Workload Identity config. No script or HCL resource block may
# hardcode any of these values.
#
# Safe to commit — billing_account is an account ID only, not a key.

project_id      = "redmarklogic-prod"
region          = "australia-southeast1"
billing_account = "017B95-5D02DE-B3B68F"

# Exactly one of folder_id or org_id must be set; comment out the other.
# folder_id = ""
org_id = "363330153915"

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
  "iamcredentials.googleapis.com",
  "cloudresourcemanager.googleapis.com",
  # ADR-026: Firebase Hosting as zero-cost API domain front door (issue #111)
  "firebase.googleapis.com",
  "firebasehosting.googleapis.com",
]

# ── Firebase Hosting + Cloudflare DNS (ADR-026, issue #111) ──────────────────
# These values are populated in two steps:
#   Step 1: Apply firebase_hosting.tf resources first (Cloudflare vars left empty).
#           Then read: terraform output firebase_custom_domain_required_dns_updates
#   Step 2: Set the values below from that output, then apply cloudflare_dns.tf.
#
# firebase_ownership_txt_value = "hosting-site=..."   # from required_dns_updates TXT entry
# firebase_a_record_ips        = ["199.36.158.100"]   # from required_dns_updates A entry/entries
