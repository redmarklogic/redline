# Artifact Registry Docker repository for backend images (issue #66)
# ADR-020: Terraform IaC for GCP; values supplied via terraform.tfvars (ADR-001)

resource "google_artifact_registry_repository" "redline" {
  location      = var.region
  repository_id = var.artifact_registry_repo
  format        = "DOCKER"
  project       = var.project_id
}
