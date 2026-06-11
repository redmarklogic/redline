# Cloudflare DNS records for api.redmarklogic.com
# ADR-026: grey-cloud (proxied=false) is load-bearing — orange-cloud breaks Firebase cert issuance/renewal
# ADR-020: all DNS records declared in Terraform; no console/dashboard changes
# ADR-003 (D3): Cloudflare API token sourced from Secret Manager / env var — never hardcoded in HCL
#
# Provider authentication: the Cloudflare provider reads the API token from the
# CLOUDFLARE_API_TOKEN environment variable at plan/apply time.
# The token is stored in Secret Manager as "prod-redline-cloudflare-api-token"
# (ADR-021 naming: <env>-redline-<credential>) and injected by the operator before
# running terraform; never stored in this file or in terraform.tfvars.
#
# RECORD TYPE (verified 2026-06-11 against the live required_dns_updates output):
# Firebase's current custom-domain flow for a subdomain requires a SINGLE CNAME —
#   api.redmarklogic.com CNAME redmarklogic-api.web.app (required_action: ADD)
# — not the legacy TXT-ownership + A-record pair the original plan assumed.
# Ownership verification and certificate issuance both ride on this one record.
# Authoritative source: terraform output firebase_custom_domain_required_dns_updates
#
# WARNING: Do NOT change proxied = false. Firebase domain verification and TLS
# certificate renewal both require DNS-only (grey cloud) mode.

# ── Provider configuration ────────────────────────────────────────────────────
#
# Token is read from the environment variable CLOUDFLARE_API_TOKEN at runtime.
# Scope required: Zone:DNS:Edit + Zone:Zone:Read on redmarklogic.com only.

provider "cloudflare" {
  # api_token is read from CLOUDFLARE_API_TOKEN env var — do not set here.
}

# ── Zone data source ──────────────────────────────────────────────────────────

data "cloudflare_zone" "redmarklogic" {
  filter = {
    name = "redmarklogic.com"
  }
}

# ── Firebase Hosting CNAME record ─────────────────────────────────────────────
#
# The content value is transcribed into terraform.tfvars from the authoritative
# output (firebase_custom_domain_required_dns_updates) — never guessed from docs.
# It is deliberately a variable, not a direct reference to
# google_firebase_hosting_custom_domain.api.required_dns_updates, because that
# attribute empties after verification completes and would break refresh.

resource "cloudflare_dns_record" "firebase_cname" {
  zone_id = data.cloudflare_zone.redmarklogic.zone_id
  name    = "api"
  type    = "CNAME"
  content = var.firebase_cname_target
  ttl     = 3600
  proxied = false # Grey cloud — load-bearing. DO NOT change to true.

  # Cloudflare limit: comment <= 100 chars
  comment = "Firebase Hosting custom domain (ADR-026). proxied=false required - do not change."
}
