# Firebase project enablement (retained per ADR-027 D3)
# ADR-027: the Firebase Hosting API front door (api.redmarklogic.com) is TORN DOWN.
#   The raw Cloud Run *.run.app URL is the POC API address (ADR-027 D1). Firebase
#   Hosting's hard 60-second request ceiling is incompatible with the product's
#   >= 180-second synchronous calls, so the front door was a guaranteed-failure path.
# ADR-020: all GCP resources declared in Terraform HCL.
#
# What was removed (ADR-027 D2): google_firebase_hosting_site.api,
#   google_firebase_hosting_custom_domain.api, google_firebase_hosting_version.api,
#   google_firebase_hosting_release.api, and the four firebase_* outputs. The
#   cloudflare_dns_record.firebase_cname (api CNAME) was removed from cloudflare_dns.tf.
#
# What stays (ADR-027 D3): google_firebase_project.default below. Firebase project
#   enablement is irreversible (the provider implements no delete; account-level ToS
#   acceptance is permanent), costs nothing, and the Sprint-3 static website will reuse
#   it under its own site ID. All resources use provider = google-beta (Firebase APIs
#   are beta); that provider pin in versions.tf is retained for the same reason.

# ── Enable Firebase on the existing GCP project (RETAINED — ADR-027 D3) ───────

resource "google_firebase_project" "default" {
  provider = google-beta
  project  = var.project_id
}
