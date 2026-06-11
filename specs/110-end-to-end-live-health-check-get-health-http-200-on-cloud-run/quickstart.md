# Quickstart: End-to-End Live Health Check on Cloud Run

Runbook for the staged delivery (issue #110). Stage 1 proves every link manually
on the feature branch; Stage 2 switches the trigger and merges. Commands assume
repo root; `terraform` commands run in `deploy/infra/terraform/`.

> Founder-reviewed `terraform plan` precedes every apply (Constitution XV).

## Stage 0 — Code edits (on the feature branch, before any GCP mutation)

1. `deploy/infra/terraform/secrets.tf`: replication `auto {}` → `user_managed`
   pinned to `australia-southeast1` (D1).
2. `deploy/infra/terraform/variables.tf`: `min_instances_prod` validation
   `>= 0 && <= 5`, default `0` (D3).
3. `deploy/infra/terraform/cloud_run.tf`: add `google_cloud_run_v2_service_iam_member`
   granting `roles/run.invoker` to `allUsers` on the staging service only (D11).
4. `.github/workflows/ci.yml`: replace the build/push stub per D4/D5 and
   `contracts/pipeline-outputs.md`; add deploy + health-check steps (D7/D8);
   deploy job gets `environment: production`. Do NOT touch the trigger yet (D10).
5. `.github/workflows/tests.yml`: trigger `main` → `master`.
6. `rtk terraform` is not a proxied command — run `terraform` directly;
   lint workflows with `actionlint`.

## Stage 1 — Manual wiring and live proof

```powershell
# 0. Verify starting state (US1 scenario 3)
gcloud run services list --region australia-southeast1   # expect: 0 items

# 1. Create the secrets first — pinned, empty — via a targeted reviewed apply.
#    They must EXIST (Sydney-pinned) before values can be added, and values must
#    exist before the services are created (else revisions fail on empty
#    secret 'latest' references). -target is normally discouraged; here it is a
#    one-off bootstrap-ordering necessity, reviewed like any apply.
#    If the secrets already exist unpinned from an earlier apply, the plan shows
#    a replace — free while they hold zero versions.
terraform init
terraform plan  -target='google_secret_manager_secret.secrets' -var image_tag=bootstrap   # review: 4 secrets only; "bootstrap" tag never reaches a service
terraform apply -target='google_secret_manager_secret.secrets' -var image_tag=bootstrap

# 2. Populate real secret values (4 secrets; values from founder, stdin only).
#    Secret IDs use the LOWERCASE binding keys (secrets.tf:27) — the uppercase
#    names are the container env vars, not the secret IDs.
"<value>" | gcloud secrets versions add staging-redline-db_password --data-file=-
"<value>" | gcloud secrets versions add staging-redline-api_key     --data-file=-
"<value>" | gcloud secrets versions add prod-redline-db_password    --data-file=-
"<value>" | gcloud secrets versions add prod-redline-api_key        --data-file=-
# verify: every secret has an accessible current version
gcloud secrets versions list staging-redline-db_password

# 3. Build and push the first image manually (operational, Constitution XV)
$sha = rtk git rev-parse HEAD
rtk docker build -f deploy/docker/marker/Dockerfile -t "australia-southeast1-docker.pkg.dev/redmarklogic-prod/redline-repo/redline-api:$sha" .
gcloud auth configure-docker australia-southeast1-docker.pkg.dev
rtk docker push "australia-southeast1-docker.pkg.dev/redmarklogic-prod/redline-repo/redline-api:$sha"

# 4. Single reviewed apply with the real tag — creates both services + staging invoker
terraform plan  -var image_tag=$sha   # review: 2 services, staging allUsers run.invoker (D11), min_instances_prod 0
terraform apply -var image_tag=$sha

# 5. Live acceptance (SC-001)
$url = terraform output -raw staging_url
curl.exe -i "$url/health"   # expect: HTTP/1.1 200, body {"status":"healthy"}
                            # (compact JSON — assert JSON-equality, not bytes)

# 6. GitHub environment wiring (D9, idempotent)
gh api -X PUT repos/redmarklogic/redline/environments/production
```

Sequencing rule (D1/D6): secrets must be pinned and populated, and the image must
exist in the registry, BEFORE the apply that creates the services — otherwise
revisions fail (empty secret `latest` reference / missing image).

By-design failure to preserve: `terraform plan` without `-var image_tag` fails —
do not add a default.

Evidence to capture for the verification gate: curl output (200 + body), `gcloud
run services list` showing both services Ready, registry listing with the SHA tag,
secret version listing, `terraform apply` summary.

## Stage 2 — Trigger switch and end-to-end merge

```powershell
# 7. Flip ci.yml trigger: main/release/** → master only (D10) — last commit on the branch
# 8. Push branch; CI on the PR proves nothing yet (trigger is push-to-master) —
#    actionlint + tests.yml run on pull_request as usual
# 9. Merge PR to master, then watch the full pipeline
gh pr create --fill
gh run watch   # after merge: test → build+push → deploy → health check all green (SC-006)
```

The CI health check waits for the service Ready condition, then polls up to
~120 s to absorb scale-to-zero cold start, and asserts HTTP 200 and JSON-equal
`{"status": "healthy"}` (contracts/health-endpoint.md).

Failed merge run (critique P1): a failed deploy or health check leaves the
previous revision serving — no user-facing outage. Recovery = fix-forward, or
redeploy the last green SHA: `gcloud run services update staging-redline-api
--image <registry-path>:<last-green-sha> --region australia-southeast1`.

## Drift note (D7)

CI updates the staging serving image via `gcloud run services update`; Terraform
state keeps the tag from the last apply. This is intentional: `image_tag` is
mandatory at every apply, so the next reviewed apply always states its tag
explicitly — no stale tag can re-apply silently.

The operator choosing that tag is the remaining failure point (critique E1):
before ANY manual apply, read the currently-serving image and pass its SHA
unless deliberately rolling back:

```powershell
gcloud run services describe staging-redline-api --region australia-southeast1 --format 'value(spec.template.spec.containers[0].image)'
```
