#!/usr/bin/env bash
# bootstrap.sh — One-off GCP project + Terraform state bucket creation
# ADR-020: Bootstrap exception — these two resources must exist before terraform init.
#          This script runs once, ever. Subsequent runs are idempotent (check-before-create).
#          After this script completes, all further GCP changes go through terraform apply.
#
# Usage:
#   export PROJECT_ID="redmarklogic-prod"
#   export FOLDER_ID="000000000000"        # set one of FOLDER_ID or ORG_ID, not both
#   # export ORG_ID="000000000000"
#   export STATE_BUCKET="redmarklogic-tf-state"
#   export REGION="australia-southeast1"
#   ./infra/bootstrap/bootstrap.sh
#
# Alternatively, values are parsed from infra/terraform/terraform.tfvars when env vars
# are not set.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TFVARS="${SCRIPT_DIR}/../terraform/terraform.tfvars"

# ---------------------------------------------------------------------------
# Helper: parse a scalar value from terraform.tfvars
# Usage: parse_tfvar <key>
# ---------------------------------------------------------------------------
parse_tfvar() {
  local key="$1"
  grep -E "^${key}\s*=" "${TFVARS}" \
    | head -n 1 \
    | sed 's/.*=\s*"\(.*\)".*/\1/'
}

# ---------------------------------------------------------------------------
# Resolve values — env var takes precedence over tfvars
# ---------------------------------------------------------------------------
PROJECT_ID="${PROJECT_ID:-$(parse_tfvar project_id)}"
STATE_BUCKET="${STATE_BUCKET:-$(parse_tfvar state_bucket)}"
REGION="${REGION:-$(parse_tfvar region)}"

# For FOLDER_ID / ORG_ID: use env var if set, else parse tfvars (folder_id preferred)
if [[ -z "${FOLDER_ID:-}" && -z "${ORG_ID:-}" ]]; then
  FOLDER_ID="$(parse_tfvar folder_id)"
  ORG_ID=""
fi

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
if [[ -z "${PROJECT_ID}" ]]; then
  echo "ERROR: PROJECT_ID is empty. Set env var or populate terraform.tfvars." >&2
  exit 1
fi
if [[ -z "${STATE_BUCKET}" ]]; then
  echo "ERROR: STATE_BUCKET is empty. Set env var or populate terraform.tfvars." >&2
  exit 1
fi
if [[ -z "${REGION}" ]]; then
  echo "ERROR: REGION is empty. Set env var or populate terraform.tfvars." >&2
  exit 1
fi
if [[ -z "${FOLDER_ID:-}" && -z "${ORG_ID:-}" ]]; then
  echo "ERROR: Exactly one of FOLDER_ID or ORG_ID must be set." >&2
  exit 1
fi
if [[ -n "${FOLDER_ID:-}" && -n "${ORG_ID:-}" ]]; then
  echo "ERROR: Only one of FOLDER_ID or ORG_ID may be set, not both." >&2
  exit 1
fi

echo "Bootstrap configuration:"
echo "  PROJECT_ID   = ${PROJECT_ID}"
echo "  STATE_BUCKET = ${STATE_BUCKET}"
echo "  REGION       = ${REGION}"
if [[ -n "${FOLDER_ID:-}" ]]; then
  echo "  FOLDER_ID    = ${FOLDER_ID}"
else
  echo "  ORG_ID       = ${ORG_ID}"
fi
echo ""

# ---------------------------------------------------------------------------
# Step 1: Idempotent project create
# ---------------------------------------------------------------------------
echo "Step 1: Ensuring GCP project '${PROJECT_ID}' exists..."
if gcloud projects describe "${PROJECT_ID}" >/dev/null 2>&1; then
  echo "  Project '${PROJECT_ID}' already exists — skipping create."
else
  if [[ -n "${FOLDER_ID:-}" ]]; then
    gcloud projects create "${PROJECT_ID}" --folder "${FOLDER_ID}"
  else
    gcloud projects create "${PROJECT_ID}" --organization "${ORG_ID}"
  fi
  echo "  Project '${PROJECT_ID}' created."
fi

# ---------------------------------------------------------------------------
# Step 2: Idempotent state bucket create
# ---------------------------------------------------------------------------
echo "Step 2: Ensuring Terraform state bucket 'gs://${STATE_BUCKET}' exists..."
if gcloud storage buckets describe "gs://${STATE_BUCKET}" >/dev/null 2>&1; then
  echo "  Bucket 'gs://${STATE_BUCKET}' already exists — skipping create."
else
  gcloud storage buckets create "gs://${STATE_BUCKET}" \
    --project "${PROJECT_ID}" \
    --location "${REGION}"
  echo "  Bucket 'gs://${STATE_BUCKET}' created."
fi

echo ""
echo "Bootstrap complete. Run 'terraform init' from infra/terraform/ to continue."
