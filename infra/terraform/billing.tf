# FR-004: Link billing account to project
# google_billing_project_info is idempotent — re-applying when billing is already linked
# is a no-op. Safe to run on an already-configured project (FR-005, SC-004).
# ADR-020: billing linkage is managed by Terraform, not the GCP Console.

resource "google_billing_project_info" "billing" {
  project         = var.project_id
  billing_account = var.billing_account
}
