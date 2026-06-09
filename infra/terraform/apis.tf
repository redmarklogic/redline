# FR-003: Enable all required GCP service APIs on the project
# disable_on_destroy = false: prevents APIs being disabled if Terraform is ever destroyed.
# Safe default for a production project — API re-enablement is disruptive.
# ADR-020: all API changes produce a reviewable terraform plan diff before applying.

resource "google_project_service" "apis" {
  for_each = toset(var.apis)

  project = var.project_id
  service = each.value

  disable_on_destroy = false
}
