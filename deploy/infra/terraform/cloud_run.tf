# Cloud Run services for staging and production environments
# Spec: specs/70-cloud-run-deploy-staging-prod-with-secret-manager/spec.md
# ADR-020: hashicorp/google ~> 6.0
# Version-guard rules:
#   1. deletion_protection = false — explicit (6.x default changed to true; must be explicit)
#   2. startup_probe — explicit (liveness_probe intentionally absent per plan.md E2)
#   3. containers.env — list-style dynamic block iteration

# ── Cloud Run V2 services (staging + prod via for_each) ──────────────────────

resource "google_cloud_run_v2_service" "api" {
  for_each = toset(local.environments)

  name                = "${each.key}-redline-api"
  location            = var.region
  project             = var.project_id
  ingress             = "INGRESS_TRAFFIC_ALL"
  deletion_protection = false

  template {
    service_account = google_service_account.cloud_run_sa.email

    timeout = "300s"

    scaling {
      min_instance_count = each.key == "prod" ? var.min_instances_prod : 0
      max_instance_count = each.key == "prod" ? var.max_instances_prod : var.max_instances_staging
    }

    containers {
      image = "${var.region}-docker.pkg.dev/${var.project_id}/${var.artifact_registry_repo}/${var.image_name}:${var.image_tag}"

      dynamic "env" {
        for_each = local.secret_bindings
        content {
          name = env.value
          value_source {
            secret_key_ref {
              secret  = google_secret_manager_secret.secrets["${each.key}-${env.key}"].secret_id
              version = "latest"
            }
          }
        }
      }

      startup_probe {
        initial_delay_seconds = 10
        timeout_seconds       = 5
        failure_threshold     = 3
        http_get {
          path = "/health"
          port = 8080
        }
      }
    }
  }
}

# ── Staging public invoker (FR-011; prod stays IAM-private until #74/#75) ────
# allUsers invoker is granted on staging ONLY — the entire staging API surface is
# public by design (no real data in the walking skeleton). Production receives no
# traffic in this feature and must not be exposed.

resource "google_cloud_run_v2_service_iam_member" "staging_public_invoker" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.api["staging"].name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# ── Cloud Run URL outputs ─────────────────────────────────────────────────────

output "staging_url" {
  description = "Cloud Run staging service URI"
  value       = google_cloud_run_v2_service.api["staging"].uri
}

output "prod_url" {
  description = "Cloud Run production service URI"
  value       = google_cloud_run_v2_service.api["prod"].uri
}
