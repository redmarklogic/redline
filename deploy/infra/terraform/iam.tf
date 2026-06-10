# IAM bindings for Cloud Run API service account and Secret Manager access
# Spec: specs/70-cloud-run-deploy-staging-prod-with-secret-manager/spec.md
# Least-privilege: per-secret secretAccessor bindings only; no project-level IAM

# ── Service Account ───────────────────────────────────────────────────────────

resource "google_service_account" "cloud_run_sa" {
  account_id   = "cloud-run-api-sa"
  display_name = "Cloud Run API Service Account"
  project      = var.project_id
}

output "cloud_run_sa_email" {
  description = "Cloud Run service account email (for IAM audit)"
  value       = google_service_account.cloud_run_sa.email
}

# ── Secret Manager IAM bindings (least-privilege, per-secret) ─────────────────

resource "google_secret_manager_secret_iam_member" "secret_access" {
  for_each = {
    for pair in setproduct(local.environments, keys(local.secret_bindings)) :
    "${pair[0]}-${pair[1]}" => { env = pair[0], credential = pair[1] }
  }

  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.cloud_run_sa.email}"
  secret_id = google_secret_manager_secret.secrets[each.key].secret_id
  project   = var.project_id
}
