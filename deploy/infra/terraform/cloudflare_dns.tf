# Cloudflare DNS for redmarklogic.com
# ADR-027: the api CNAME (api.redmarklogic.com -> redmarklogic-api.web.app) was
#   REMOVED with the Firebase front-door teardown (ADR-027 D2). The deletion was the
#   single sanctioned exception to the additive-only DNS discipline (ADR-026 D3 /
#   ADR-020), guarded by a mandatory pre-change zone snapshot — the founder's live
#   email (MX/SPF) runs on this same zone.
# ADR-020: all DNS records declared in Terraform; no console/dashboard changes.
# ADR-003 (D3): Cloudflare API token sourced from Secret Manager / env var — never
#   hardcoded in HCL.
#
# What stays (ADR-027 D3): the cloudflare provider and the read-only zone data source
#   below. All future DNS automation (including the Sprint-3 website DNS work) depends
#   on them. The Cloudflare API token in Secret Manager (prod-redline-cloudflare-api-token)
#   and the cloudflare provider pin in versions.tf are likewise retained.
#
# Provider authentication: the Cloudflare provider reads the API token from the
# CLOUDFLARE_API_TOKEN environment variable at plan/apply time. The token is stored in
# Secret Manager as "prod-redline-cloudflare-api-token" (ADR-021 naming) and injected by
# the operator before running terraform; never stored in this file or in terraform.tfvars.

# ── Provider configuration ────────────────────────────────────────────────────
#
# Token is read from the environment variable CLOUDFLARE_API_TOKEN at runtime.
# Scope required: Zone:DNS:Edit + Zone:Zone:Read on redmarklogic.com only.

provider "cloudflare" {
  # api_token is read from CLOUDFLARE_API_TOKEN env var — do not set here.
}

# ── Zone data source (read-only; RETAINED — ADR-027 D3) ───────────────────────

data "cloudflare_zone" "redmarklogic" {
  filter = {
    name = "redmarklogic.com"
  }
}
