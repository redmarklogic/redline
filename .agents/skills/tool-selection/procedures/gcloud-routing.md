# GCP Infrastructure Operations (`gcloud`) — Command Reference

Loaded from `SKILL.md` when the routing rule resolves to `gcloud`.

| Operation | Command |
|---|---|
| **Cloud SQL — create instance** | `gcloud sql instances create <name> --database-version=POSTGRES_15 --tier=db-f1-micro --region=<region>` |
| **Cloud SQL — list instances** | `gcloud sql instances list` |
| **Cloud SQL — describe instance** | `gcloud sql instances describe <name>` |
| **Cloud SQL — create database** | `gcloud sql databases create <db-name> --instance=<instance-name>` |
| **Cloud SQL — list databases** | `gcloud sql databases list --instance=<instance-name>` |
| **Cloud SQL — connect** | `gcloud sql connect <instance-name> --user=postgres` |
| List Compute instances | `gcloud compute instances list` |
| Create Compute instance | `gcloud compute instances create <name> --zone=<zone> --machine-type=<type> --image-family=debian-12` |
| List Cloud Run services | `gcloud run services list --region=<region>` |
| Deploy to Cloud Run | `gcloud run deploy <service> --image=<image> --region=<region>` |
| List Cloud Storage buckets | `gcloud storage buckets list` |
| Create bucket | `gcloud storage buckets create gs://<name> --location=<region>` |
| List IAM service accounts | `gcloud iam service-accounts list` |
| Create service account | `gcloud iam service-accounts create <name> --display-name="..."` |
| Bind IAM role | `gcloud projects add-iam-policy-binding <project-id> --member=serviceAccount:<email> --role=roles/<role>` |
| List enabled APIs | `gcloud services list --enabled` |
| Enable an API | `gcloud services enable <api>.googleapis.com` |
| Set active project | `gcloud config set project <project-id>` |
| Check auth | `gcloud auth list` |
| Check quotas/billing | `gcloud projects describe <project-id>` (billing via Console or `gcloud billing accounts list`) |
