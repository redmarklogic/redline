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
