# Keyless GitHub Actions → GCP authentication via Workload Identity Federation (issue #68)
# No long-lived service account keys — GitHub's OIDC token is exchanged for a short-lived GCP credential.

# ── WIF Pool ─────────────────────────────────────────────────────────────────

resource "google_iam_workload_identity_pool" "github" {
  workload_identity_pool_id = "github-pool"
  display_name              = "GitHub Actions Pool"
  project                   = var.project_id
}

# ── WIF Provider ─────────────────────────────────────────────────────────────

resource "google_iam_workload_identity_pool_provider" "github" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.github.workload_identity_pool_id
  workload_identity_pool_provider_id = "github-provider"
  display_name                       = "GitHub Actions OIDC Provider"
  project                            = var.project_id

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }

  attribute_mapping = {
    "google.subject"        = "assertion.sub"
    "attribute.repository"  = "assertion.repository"
    "attribute.repository_id" = "assertion.repository_id"
  }

  # Scope token exchange to this repository only — prevents tokens from
  # other repos (including forks with the same name) from being accepted.
  attribute_condition = "assertion.repository == \"redmarklogic/redline\""
}

# ── GitHub Actions Service Account ───────────────────────────────────────────

resource "google_service_account" "github_actions_sa" {
  account_id   = "github-actions-sa"
  display_name = "GitHub Actions CI/CD Service Account"
  project      = var.project_id
}

# ── WIF Binding ──────────────────────────────────────────────────────────────
# Allows GitHub Actions jobs from this specific repository (by numeric ID, not
# name) to impersonate github-actions-sa. Numeric repository_id prevents
# account-squatting if the repo is renamed or a fork takes the same slug.

resource "google_service_account_iam_member" "github_wif_binding" {
  service_account_id = google_service_account.github_actions_sa.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github.name}/attribute.repository_id/1258762168"
}

# ── IAM Role Bindings ─────────────────────────────────────────────────────────

resource "google_project_iam_member" "github_actions_ar_writer" {
  project = var.project_id
  role    = "roles/artifactregistry.writer"
  member  = "serviceAccount:${google_service_account.github_actions_sa.email}"
}

resource "google_project_iam_member" "github_actions_run_developer" {
  project = var.project_id
  role    = "roles/run.developer"
  member  = "serviceAccount:${google_service_account.github_actions_sa.email}"
}

# Resource-level binding: allows github-actions-sa to act as cloud-run-api-sa
# when deploying a new Cloud Run revision (--service-account flag requires this).
resource "google_service_account_iam_member" "github_acts_as_cloud_run_sa" {
  service_account_id = google_service_account.cloud_run_sa.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${google_service_account.github_actions_sa.email}"
}
