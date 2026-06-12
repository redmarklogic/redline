#!/usr/bin/env bash
# Capture a full Cloudflare zone snapshot for redmarklogic.com (ADR-027 / issue #147).
# Phase 0 (pre-change) and Phase 2 (post-change) both run this; pass the phase tag.
#
# PREREQUISITE: gcloud ADC must be valid. If you see "Reauthentication failed",
# run `gcloud auth login` (interactive) first — that is the gate that blocked Brent's
# automated run on 2026-06-12.
#
# Usage:
#   ./capture-zone-snapshot.sh pre     # before terraform apply (Phase 0, FR-017)
#   ./capture-zone-snapshot.sh post    # after terraform apply  (Phase 2, FR-019)
#
# Output: docs/infrastructure/zone-snapshots/redmarklogic-zone-<phase>-<UTC>.json
#         (full record list, sorted, so a pre/post `diff` shows exactly the api CNAME removed)

set -euo pipefail

PHASE="${1:?usage: capture-zone-snapshot.sh <pre|post>}"
PROJECT="redmarklogic-prod"
SECRET="prod-redline-cloudflare-api-token"
OUTDIR="$(cd "$(dirname "$0")" && pwd)"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
OUT="${OUTDIR}/redmarklogic-zone-${PHASE}-${STAMP}.json"

# Pull the Cloudflare token from Secret Manager WITHOUT echoing it.
CLOUDFLARE_API_TOKEN="$(gcloud secrets versions access latest --secret="${SECRET}" --project="${PROJECT}")"
if [ -z "${CLOUDFLARE_API_TOKEN}" ]; then
  echo "ERROR: empty Cloudflare token from Secret Manager (${SECRET}). Check version/access." >&2
  exit 1
fi
export CLOUDFLARE_API_TOKEN

# Resolve the zone id, then export ALL DNS records (MX, SPF/TXT, the api CNAME, everything),
# sorted deterministically so pre/post diffs are byte-stable.
ZONE_ID="$(curl -s "https://api.cloudflare.com/client/v4/zones?name=redmarklogic.com" \
  -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" | jq -r '.result[0].id')"
if [ -z "${ZONE_ID}" ] || [ "${ZONE_ID}" = "null" ]; then
  echo "ERROR: could not resolve zone id for redmarklogic.com" >&2
  exit 1
fi

curl -s "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/dns_records?per_page=500" \
  -H "Authorization: Bearer ${CLOUDFLARE_API_TOKEN}" \
| jq -S '[.result[] | {name, type, content, ttl, proxied, priority, id}] | sort_by(.type, .name, .content)' \
> "${OUT}"

echo "Wrote ${OUT}"
echo "Record count: $(jq 'length' "${OUT}")"
echo "api CNAME present: $(jq '[.[] | select(.name=="api.redmarklogic.com" and .type=="CNAME")] | length' "${OUT}")"
echo
echo "To diff pre vs post (expect EXACTLY one removed line — the api CNAME, id 6b051d1e36a71373819c95a89d1db64d):"
echo "  diff redmarklogic-zone-pre-*.json redmarklogic-zone-post-*.json"
