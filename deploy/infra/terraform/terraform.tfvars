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
# Transcribed from the authoritative output after the first apply:
#   terraform output firebase_custom_domain_required_dns_updates
#   (check_time 2026-06-11T09:53:31Z — single CNAME, required_action ADD;
#    Firebase's current subdomain flow uses CNAME, not the legacy TXT + A pair)
firebase_cname_target = "redmarklogic-api.web.app"
