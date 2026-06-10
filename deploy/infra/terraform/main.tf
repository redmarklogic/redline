# ADR-020: Google provider configuration and project data source
#
# IMPORTANT: google_project is a DATA SOURCE here, not a resource.
# The project was created by infra/bootstrap/bootstrap.sh to avoid the
# state-backend chicken-and-egg problem. Terraform reads the existing project;
# it does not manage its lifecycle.

provider "google" {
  project = var.project_id
  region  = var.region
}

data "google_project" "project" {
  project_id = var.project_id
}
