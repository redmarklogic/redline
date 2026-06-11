# Project-level org policy override: allow allUsers on IAM bindings
#
# Context: The GCP organisation enforces constraints/iam.allowedPolicyMemberDomains,
# which by default blocks the allUsers member (unauthenticated access) across all
# projects. This override restores the GCP default behaviour at the project level only
# — the org-wide policy is untouched and continues to protect all other projects.
#
# Why this is here: Feature #110 requires the staging Cloud Run service to be
# publicly reachable so the acceptance test (curl /health → HTTP 200) can run without
# authentication. Production does NOT receive an allUsers binding (see cloud_run.tf).
#
# Security posture: restoreDefault removes the domain restriction for THIS project.
# The production Cloud Run service is still IAM-private — no allUsers binding is granted
# on prod. This override is a prerequisite for the staging_public_invoker binding in
# cloud_run.tf. When auth ADRs #74/#75 are ratified, the staging invoker binding will
# be replaced with an authenticated mechanism; at that point this override can be
# re-evaluated.
#
# ADR-020: resource managed in Terraform, never via Console.
# SOC 2 evidence: PR containing terraform plan diff is the audit trail (CC8.1).

resource "google_project_organization_policy" "allow_all_iam_members" {
  project    = var.project_id
  constraint = "constraints/iam.allowedPolicyMemberDomains"

  restore_policy {
    default = true
  }
}
