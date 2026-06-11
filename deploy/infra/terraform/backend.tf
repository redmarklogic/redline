# ADR-020: GCS remote state backend
# state_bucket value must match the bucket created by deploy/infra/bootstrap/bootstrap.sh
terraform {
  backend "gcs" {
    bucket = "redmarklogic-tf-state"
    prefix = "terraform/state"
  }
}
