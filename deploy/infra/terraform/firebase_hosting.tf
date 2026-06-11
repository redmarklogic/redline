# Firebase Hosting: api.redmarklogic.com -> Cloud Run backend
# ADR-026: Firebase Hosting rewrite proxy (zero-cost front door at POC stage)
# ADR-020: all GCP resources declared in Terraform HCL
#
# Resource sequence:
#   1. google_firebase_project       — enable Firebase on the existing GCP project
#   2. google_firebase_hosting_site  — dedicated site "redmarklogic-api"
#   3. google_firebase_hosting_custom_domain — attach api.redmarklogic.com
#        wait_dns_verification = false on first apply (DNS records don't exist yet)
#        Two-step converge required: apply -> Cloudflare records created -> re-apply/refresh
#   4. google_firebase_hosting_version + _release — activate the Cloud Run rewrite rule
#        D6 primary path confirmed: schema supports run { service_id, region } block
#
# All resources use provider = google-beta (Firebase APIs are beta).
# The rewrite target is prod-redline-api (issue #110 service name per plan.md).
# Ingress must stay INGRESS_TRAFFIC_ALL on the Cloud Run service (D7: Firebase is not
# a Cloud Load Balancer; internal-only ingress would block Firebase traffic).

# ── 1. Enable Firebase on the existing GCP project ───────────────────────────

resource "google_firebase_project" "default" {
  provider = google-beta
  project  = var.project_id
}

# ── 2. Dedicated Hosting site ─────────────────────────────────────────────────

resource "google_firebase_hosting_site" "api" {
  provider = google-beta
  project  = var.project_id
  site_id  = "redmarklogic-api"

  depends_on = [google_firebase_project.default]
}

# ── 3. Custom domain attachment ───────────────────────────────────────────────
#
# IMPORTANT: wait_dns_verification = false is required on the first apply because
# the DNS records declared in cloudflare_dns.tf do not exist yet. After Terraform
# creates those records, run `terraform apply` (or `terraform refresh`) a second
# time to let Firebase verify ownership and progress to CERT_ACTIVE.
#
# The required_dns_updates attribute output is the AUTHORITATIVE list of DNS records
# Firebase needs — use it to verify the records in cloudflare_dns.tf match exactly.
# Do NOT hard-code IP addresses from docs; always read from this output after apply.

resource "google_firebase_hosting_custom_domain" "api" {
  provider = google-beta
  project  = var.project_id
  site_id  = google_firebase_hosting_site.api.site_id

  custom_domain        = "api.redmarklogic.com"
  wait_dns_verification = false

  depends_on = [google_firebase_hosting_site.api]
}

# ── 4a. Hosting version — declares the Cloud Run rewrite rule ─────────────────
#
# Rewrite: all paths (**) forwarded to prod-redline-api in australia-southeast1.
# The `region` argument is mandatory in practice; omitting it defaults to us-central1
# which would route to the wrong region.
#
# NOTE: This resource references the Cloud Run service by name only (no direct
# Terraform dependency on google_cloud_run_v2_service) because the service is not
# deployed yet (issue #110 hard dependency for Phase 2). On Phase 2, verify the
# actual service name matches "prod-redline-api" before applying this version/release.

resource "google_firebase_hosting_version" "api" {
  provider = google-beta
  site_id  = google_firebase_hosting_site.api.site_id

  config {
    rewrites {
      glob = "**"
      run {
        service_id = "prod-redline-api"
        region     = var.region
      }
    }
  }

  depends_on = [google_firebase_hosting_site.api]
}

# ── 4b. Hosting release — makes the version live ──────────────────────────────

resource "google_firebase_hosting_release" "api" {
  provider     = google-beta
  site_id      = google_firebase_hosting_site.api.site_id
  version_name = google_firebase_hosting_version.api.name
  message      = "Cloud Run rewrite: prod-redline-api (issue #111)"

  depends_on = [google_firebase_hosting_version.api]
}

# ── Outputs ───────────────────────────────────────────────────────────────────

output "firebase_hosting_site_id" {
  description = "Firebase Hosting site ID (redmarklogic-api)"
  value       = google_firebase_hosting_site.api.site_id
}

output "firebase_hosting_default_url" {
  description = "Firebase Hosting default URL for the site (*.web.app)"
  value       = google_firebase_hosting_site.api.default_url
}

output "firebase_custom_domain_required_dns_updates" {
  description = <<-EOT
    Authoritative DNS records Firebase needs for domain ownership and routing.
    Read this output after the first apply and verify it matches the records
    in cloudflare_dns.tf before running the second apply/refresh.
    Structure: list of { desired: [{ domain_name, type, rdata }] }
  EOT
  value = google_firebase_hosting_custom_domain.api.required_dns_updates
}

output "firebase_custom_domain_cert_state" {
  description = "Certificate provisioning state (cert block) and host_state. Target host_state: HOST_ACTIVE (allow up to 24 h; SC-001 budgets 48 h)."
  value = {
    cert       = google_firebase_hosting_custom_domain.api.cert
    host_state = google_firebase_hosting_custom_domain.api.host_state
  }
}
