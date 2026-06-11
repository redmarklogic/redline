# Outputs consumed by downstream deploy-chain issues (#65-#72)
# project_number: GCP-assigned numeric ID required by IAM and Workload Identity configs
# Use `terraform output <name>` to read these values after apply.

output "project_number" {
  description = "GCP-assigned numeric project ID (consumed by downstream Terraform modules)"
  value       = data.google_project.project.number
}

output "project_id" {
  description = "GCP project ID (SSOT: also in terraform.tfvars)"
  value       = var.project_id
}

output "region" {
  description = "Default GCP region (SSOT: also in terraform.tfvars)"
  value       = var.region
}

output "state_bucket" {
  description = "Name of the GCS bucket holding Terraform state"
  value       = var.state_bucket
}

# ── Cloud Run outputs (spec-70) ───────────────────────────────────────────────
# staging_url, prod_url   — declared in cloud_run.tf alongside the resource (T021)
# cloud_run_sa_email      — declared in iam.tf alongside the resource (T011)

# ── Workload Identity Federation outputs (issue #68) ─────────────────────────

output "wif_provider_name" {
  description = "Full resource name of the WIF provider — set as GHA repo var WIF_PROVIDER"
  value       = google_iam_workload_identity_pool_provider.github.name
}

output "github_actions_sa_email" {
  description = "Email of the GitHub Actions CI/CD service account — set as GHA repo var GHA_SA_EMAIL"
  value       = google_service_account.github_actions_sa.email
}
