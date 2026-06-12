# Contract: Infra-to-App Environment Variables

**Owner**: Brent (DevOps)
**Consumers**: App team (issue #51), any developer connecting to Cloud Run
**Stability**: Volatile per ADR-017 — until LB/DNS (#74/#75) land
**SSOT**: `.env.example` (root)

## Variables

| Variable | Secret? | Canonical value | How to obtain |
|----------|---------|-----------------|---------------|
| `API_BASE_URL` | Non-secret | `https://{env}-redline-api-<hash>-ts.a.run.app` | `gcloud run services describe {env}-redline-api --region=australia-southeast1 --format='value(status.url)'` |
| `GCP_OIDC_AUDIENCE` | Non-secret | Same as `API_BASE_URL` for same env | Same as above — Cloud Run issues OIDC tokens with the service URL as audience |
| `CLOUD_RUN_SA_EMAIL` | Non-secret | `cloud-run-api-sa@redmarklogic-prod.iam.gserviceaccount.com` | `terraform output cloud_run_sa_email` |

## Notes

- `API_BASE_URL` changes if the Cloud Run service is deleted and recreated (ADR-027 D1 accepted risk).
  Always read from the live service; never hard-code the hash segment.
- IAP is not provisioned (ADR-022 out of scope). No IAP client ID variable exists.
- Secret values (`DB_PASSWORD`, `API_KEY`) are in Secret Manager — not in this contract.
- This contract becomes stable when the branded domain lands (#74/#75); at that point
  `API_BASE_URL` switches to `https://app.<domain>` and the hash URL is retired.
