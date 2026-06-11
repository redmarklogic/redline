# Variable declarations matching the schema in contracts/terraform-variables.md
# ADR-020: All variable values are supplied via terraform.tfvars (SSOT per ADR-001)

variable "project_id" {
  description = "GCP project ID (SSOT: terraform.tfvars — do not hardcode elsewhere)"
  type        = string
}

variable "region" {
  description = "Default GCP region for all resource-creating operations (FR-002)"
  type        = string
}

variable "billing_account" {
  description = "GCP billing account ID in format XXXXXX-XXXXXX-XXXXXX (account ID only, not a key — safe to version-control)"
  type        = string
}

variable "folder_id" {
  description = "GCP folder ID under which the project is anchored. Exactly one of folder_id or org_id must be non-empty."
  type        = string
  default     = ""
}

variable "org_id" {
  description = "GCP organisation ID. Exactly one of folder_id or org_id must be non-empty."
  type        = string
  default     = ""
}

variable "state_bucket" {
  description = "Name of the GCS bucket holding Terraform remote state. Must match the bucket created by bootstrap.sh."
  type        = string
}

variable "apis" {
  description = "List of GCP service API identifiers to enable on the project (FR-003)"
  type        = list(string)
}

# ── Cloud Run deployment variables (spec-70) ─────────────────────────────────

variable "image_tag" {
  description = "Image digest to deploy — must be sha256:DIGEST, not a mutable tag"
  type        = string
}

variable "artifact_registry_repo" {
  description = "Artifact Registry repository name (e.g. redline-repo)"
  type        = string
}

variable "image_name" {
  description = "Container image name within the Artifact Registry repository"
  type        = string
  default     = "redline-api"
}

variable "min_instances_prod" {
  description = "Minimum warm instances for the production Cloud Run service (FR-004)"
  type        = number
  default     = 1

  validation {
    condition     = var.min_instances_prod >= 1 && var.min_instances_prod <= 5
    error_message = "min_instances_prod must be between 1 and 5."
  }
}

variable "max_instances_staging" {
  description = "Maximum instances for the staging Cloud Run service (FR-005)"
  type        = number
  default     = 3

  validation {
    condition     = var.max_instances_staging >= 1
    error_message = "max_instances_staging must be at least 1."
  }
}

variable "max_instances_prod" {
  description = "Maximum instances for the production Cloud Run service (FR-005)"
  type        = number
  default     = 10

  validation {
    condition     = var.max_instances_prod >= 1
    error_message = "max_instances_prod must be at least 1."
  }
}

# ── Firebase Hosting + Cloudflare DNS variables (ADR-026, issue #111) ─────────

variable "firebase_cname_target" {
  description = <<-EOT
    CNAME target Firebase Hosting requires for api.redmarklogic.com.
    Source: run `terraform output firebase_custom_domain_required_dns_updates` after the
    first apply of firebase_hosting.tf resources, then set this to the rdata of the
    CNAME entry Firebase returns (e.g. "redmarklogic-api.web.app").
    Verified 2026-06-11: Firebase's current subdomain flow requires this single CNAME,
    not the legacy TXT-ownership + A-record pair.
    This value is NOT secret — it is committed to terraform.tfvars once known.
  EOT
  type    = string
  default = ""

  validation {
    condition     = var.firebase_cname_target != ""
    error_message = "firebase_cname_target must be set before applying cloudflare_dns.tf. Read it from the firebase_custom_domain_required_dns_updates Terraform output."
  }
}
