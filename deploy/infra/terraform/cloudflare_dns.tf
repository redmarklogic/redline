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
# Two-step converge (ADR-026 D1):
#   Step 1: terraform apply (firebase_hosting.tf resources only, records don't exist yet)
#           Read firebase_custom_domain_required_dns_updates output — this is the
#           authoritative record list. Verify content values below match.
#   Step 2: terraform apply (this file creates the records) -> Firebase verifies ownership
#           -> re-apply / terraform refresh until cert_state = CERT_ACTIVE
#
# WARNING: Do NOT change proxied = false on any record in this file. Firebase domain
# verification and TLS certificate renewal both require DNS-only (grey cloud) mode.

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

# ── Domain ownership TXT record ───────────────────────────────────────────────
#
# IMPORTANT: The `content` value below is a placeholder.
# After the first `terraform apply` of firebase_hosting.tf, run:
#   terraform output firebase_custom_domain_required_dns_updates
# and replace the placeholder with the exact TXT value Firebase requires.
# Do NOT run `terraform apply` of this file until you have the real value.
#
# The content will look like: "hosting-site=redmarklogic-api" or a similar
# Google-generated ownership token — always use the output, never guess.

resource "cloudflare_dns_record" "firebase_ownership_txt" {
  zone_id = data.cloudflare_zone.redmarklogic.zone_id
  name    = "api"
  type    = "TXT"
  # Replace with value from: terraform output firebase_custom_domain_required_dns_updates
  content = var.firebase_ownership_txt_value
  ttl     = 3600
  proxied = false # Grey cloud — load-bearing. DO NOT change to true.

  comment = "Firebase Hosting domain ownership verification (ADR-026). proxied=false is required — do not change."
}

# ── Firebase Hosting A record(s) ──────────────────────────────────────────────
#
# Firebase Hosting edge IPs are provided in the required_dns_updates output.
# Classic value: 199.36.158.100 — however, always use the output-authoritative value.
# If Firebase returns multiple A records, add one resource block per address or
# use a for_each over var.firebase_a_record_ips.
#
# Both records use proxied = false (grey cloud — see warning above).

resource "cloudflare_dns_record" "firebase_a" {
  for_each = toset(var.firebase_a_record_ips)

  zone_id = data.cloudflare_zone.redmarklogic.zone_id
  name    = "api"
  type    = "A"
  content = each.value
  ttl     = 3600
  proxied = false # Grey cloud — load-bearing. DO NOT change to true.

  comment = "Firebase Hosting edge IP for api.redmarklogic.com (ADR-026). proxied=false is required."
}
