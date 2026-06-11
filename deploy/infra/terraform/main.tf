# ADR-020: Google provider configuration and project data source
#
# IMPORTANT: google_project is a DATA SOURCE here, not a resource.
# The project was created by deploy/infra/bootstrap/bootstrap.sh to avoid the
# state-backend chicken-and-egg problem. Terraform reads the existing project;
# it does not manage its lifecycle.

provider "google" {
  project = var.project_id
  region  = var.region
}

# google-beta requires user_project_override + billing_project for Firebase APIs
# (firebase.googleapis.com validates quota against the billing project, not the ADC default)
provider "google-beta" {
  project                = var.project_id
  region                 = var.region
  user_project_override  = true
  billing_project        = var.project_id
}

data "google_project" "project" {
  project_id = var.project_id
}
