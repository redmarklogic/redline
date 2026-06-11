# Secret Manager secrets for Cloud Run environment injection
# Spec: specs/70-cloud-run-deploy-staging-prod-with-secret-manager/spec.md
# E1 / FR-002: no google_secret_manager_secret_version resource here — versions managed out-of-band via gcloud

# ── SSOT: FR-008 secret bindings map ─────────────────────────────────────────

locals {
  # Cross-file dependency: local.environments and local.secret_bindings are consumed by cloud_run.tf — do not move or split.
  environments = ["staging", "prod"]

  # Maps Terraform key (used in resource names) → container env-var name.
  # To add a new secret: add one entry here. No other file needs changing.
  secret_bindings = {
    "db_password" = "DB_PASSWORD"
    "api_key"     = "API_KEY"
  }
}

# ── Secret Manager secrets (shell only — no secret_version resource) ─────────

resource "google_secret_manager_secret" "secrets" {
  for_each = {
    for pair in setproduct(local.environments, keys(local.secret_bindings)) :
    "${pair[0]}-${pair[1]}" => { env = pair[0], credential = pair[1] }
  }

  secret_id = "${each.value.env}-redline-${each.value.credential}"
  project   = var.project_id

  replication {
    auto {}
  }
}

# ── Cloudflare API token (ADR-026, ADR-022 amendment) ─────────────────────────
# This is the first Secret Manager entry — amends ADR-022's "no Secret Manager
# entries needed at this stage" statement.
# Token scope: Zone:DNS:Edit + Zone:Zone:Read on redmarklogic.com only.
# Value is stored out-of-band via gcloud (see domain-dns-runbook.md Phase 0 Step 1).
# Terraform manages the secret shell only; no secret_version resource here.

resource "google_secret_manager_secret" "cloudflare_api_token" {
  secret_id = "prod-redline-cloudflare-api-token"
  project   = var.project_id

  replication {
    auto {}
  }
}
