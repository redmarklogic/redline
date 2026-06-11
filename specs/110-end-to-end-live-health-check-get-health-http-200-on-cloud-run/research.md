# Research: End-to-End Live Health Check on Cloud Run

**Date**: 2026-06-11 | **Spec**: [spec.md](spec.md)

All Technical Context unknowns resolved. Decisions below carry forward founder
rulings (2026-06-11 Q&A) and ratified prior art (launch-topology doc, spec-69 task
design, ADR-020).

## D1 — Secret replication pinning order

**Decision**: Change `secrets.tf` replication from `auto {}` to `user_managed`
pinned to `australia-southeast1` FIRST, apply it, and only then add secret values.

**Rationale**: Changing replication on an existing secret is a destructive replace,
not an in-place update (topology doc, section 8). Today the secrets exist with zero
versions, so the replace costs nothing. If values were added first, every secret
would need replace + re-add. Ratified follow-up #4 mandates pinning "before any
real user secret lands" — the founder chose real values now, which fires that
prerequisite.

**Alternatives considered**: Populate first, pin later (rejected: forces a
replace-and-re-add cycle and stores real secret material unpinned, violating the
ratified data-residency decision); placeholder values (rejected by founder).

## D2 — Secret value population mechanism

**Decision**: `gcloud secrets versions add <secret-id> --data-file=-` per secret
(4 total: `{staging,prod}-redline-{DB_PASSWORD,API_KEY}` per the `secret_id`
pattern in `secrets.tf`). Values supplied by the founder at execution time; never
written to disk or committed.

**Rationale**: `secrets.tf` deliberately manages no `google_secret_manager_secret_version`
resources (E1/FR-002 of spec-70) — versions are out-of-band by design. Constitution
XV explicitly permits `gcloud` for operational commands that are not infrastructure
definitions. For not-yet-existing backing services (no database is provisioned),
the value generated now becomes the canonical credential (spec assumption).

**Alternatives considered**: Terraform-managed secret versions (rejected: secret
material would enter state; contradicts spec-70 E1 design); GitHub Actions secret
sync (rejected: out of scope, adds a second writer).

## D3 — Scale-to-zero fix

**Decision**: In `variables.tf`, change `min_instances_prod` validation to
`>= 0 && <= 5` and default to `0`.

**Rationale**: Founder-ratified cold-start policy ("sleep by default everywhere",
topology doc round 2) and follow-up #7, which assigns this exact change to "next
Terraform change" — this feature is that change. Demo warm-up remains a deliberate
tfvars edit + plan + apply, as documented in the topology doc.

**Alternatives considered**: Keep `>= 1` and pay for warmth (rejected by founder);
`-target` apply excluding prod (rejected: fragile, leaves partial state).

## D4 — CI build-and-push design

**Decision**: Replace the `ci.yml` stub with: `google-github-actions/setup-gcloud`
plus `gcloud auth configure-docker australia-southeast1-docker.pkg.dev`,
`docker/setup-buildx-action`, `docker/build-push-action` building
`deploy/docker/marker/Dockerfile` for `linux/amd64`, tagged
`australia-southeast1-docker.pkg.dev/redmarklogic-prod/redline-repo/redline-api:${{ github.sha }}`,
with the step's `outputs.digest` exposed as job output `image_digest` and a
`$GITHUB_STEP_SUMMARY` line. All `uses:` SHA-pinned (repo convention).

**Rationale**: This is spec-69's ratified task design (T007–T013) carried forward
unchanged — spec-69's tasks were authored but never executed (stub still on
master); issue #110 gap 1 absorbs them. Tag-by-commit-SHA satisfies FR-002
(immutable tags); the digest output is the provenance handoff for the deploy step.

**Alternatives considered**: `gcloud builds submit` (rejected: moves build into
Cloud Build, new billing surface, diverges from spec-69 design); `latest` tag
(rejected: mutable tags deliberately refused by the tfvars design note).

## D5 — Registry identifiers in ci.yml vs SSOT

**Decision**: Define registry host, project, repo, and image name once in the
workflow's top-level `env:` block with a comment naming
`deploy/infra/terraform/terraform.tfvars` as SSOT, and reference `${{ env.* }}`
everywhere below.

**Rationale**: GitHub Actions cannot read tfvars. The tfvars header forbids
scripts hardcoding identifiers; a single annotated `env:` block is the minimal
duplication, consistent with how `WIF_PROVIDER`/`GHA_SA_EMAIL` are already
externalised as repo variables. Recorded as a justified Constitution I deviation
in plan.md Complexity Tracking.

**Alternatives considered**: GitHub repo variables for all identifiers (rejected:
moves SSOT drift into invisible repo settings; harder to review than a tracked
file); generating ci.yml from tfvars (rejected: build-step machinery for a
walking skeleton — appetite violation).

## D6 — First apply and deploy sequencing (Stage 1, manual)

**Decision**: Stage 1 order: (1) targeted reviewed apply of the four
`google_secret_manager_secret` resources only — they must exist, Sydney-pinned,
before values can be added; (2) populate secrets (D2); (3) build + push image
manually (docker build/push — operational, permitted by Constitution XV);
(4) full `terraform apply -var image_tag=<sha>` creating both services;
(5) `curl $(terraform output -raw staging_url)/health`.

**Rationale**: The startup probe and secret references mean services cannot go
Ready until the image exists in the registry and every referenced secret has a
version — both must precede the service-creating apply. But the secrets
themselves must be created (pinned) before `gcloud` can add versions, hence the
one-off `-target` bootstrap apply: a circular ordering no single full apply can
satisfy. After step 4, state is fully coherent; `-target` is never used again.

**Alternatives considered**: Apply infra first with a placeholder image (rejected:
no placeholder exists in the repo's registry; failed revisions add noise).

## D7 — CI deploy step mechanism (Stage 2)

**Decision**: CI deploys by `gcloud run services update staging-redline-api
--image <registry-path>:${{ github.sha }} --region australia-southeast1` after
push, then health-checks. CI does NOT run `terraform apply`.

**Rationale**: Constitution XV draws the line precisely here: "no human or CI job
modifies GCP infrastructure except through a reviewed `terraform apply`", while
`gcloud` IS permitted for "operational commands (deployments, image pushes) that
are not infrastructure definitions". Updating the serving image is an operational
deployment; service shape stays Terraform-owned. Consequence: Terraform state
records the image tag from the last apply — the serving tag intentionally drifts
forward via CI. `image_tag` is supplied fresh at every apply by design, so no
stale tag is ever silently re-applied; the drift is documented in quickstart.md.

**Alternatives considered**: `terraform apply` in CI (rejected: violates the
"reviewed apply" clause; needs state-bucket write grants for the CI SA); deploy
both services from CI (rejected: prod receives no traffic in this feature —
staging only, per issue scope).

## D8 — CI health check (Stage 2)

**Decision**: CI first polls the service Ready condition, then fetches the
staging URL via `gcloud run services describe staging-redline-api --region
australia-southeast1 --format 'value(status.url)'` and polls `GET <url>/health`
with curl (retry up to ~120 s total — critique E2) asserting HTTP 200 and body
JSON-equal to `{"status": "healthy"}`.

**Rationale**: CLI-first (Constitution XII); read-only `gcloud` is sanctioned;
avoids granting the CI SA Terraform state access just to read an output. Retry
absorbs cold-start latency on a scale-to-zero service (probe budget: 10 s initial
delay + 3 × 5 s).

**Alternatives considered**: `terraform output staging_url` in CI (rejected:
state-bucket read grant + terraform setup for one string); hardcoding the
deterministic run.app URL (rejected: opaque project-hash format, breaks if the
service is recreated).

## D9 — GitHub Actions `production` environment

**Decision**: Create the `production` environment via
`gh api -X PUT repos/redmarklogic/redline/environments/production`, then set
`environment: production` on the deploy job. Repo variables stay repo-level;
deployment-scoped secrets/vars move in only when one actually exists.

**Rationale**: Issue step 4 requires the environment wiring. `gh` CLI is the
required first choice (Constitution XII). PUT is idempotent.

**Alternatives considered**: Console-only setup (works but unrecorded; the gh
command is reproducible and scriptable).

## D10 — Trigger switch timing

**Decision**: `ci.yml` trigger changes `main`/`release/**` → `master`-only in the
final commit(s) of the feature branch, after Stage 1 evidence is captured
(staged delivery per issue plan and FR-009). `release/**` is removed, not kept —
POC is master-only; re-added by #107 (2026-06-22).

**Rationale**: Switching early would make every push to a stale-named branch a
no-op deploy risk while the pipeline is still being wired. Spec-69 T004/T005
already ratified master-only and the companion `tests.yml` fix.

**Alternatives considered**: Rename default branch to `main` (rejected: repo-wide
churn out of appetite for this issue).

## D11 — Public invoker for the staging service (analysis finding C2)

**Decision**: Add `google_cloud_run_v2_service_iam_member` granting
`roles/run.invoker` to `allUsers` on `staging-redline-api` ONLY, in
`deploy/infra/terraform/cloud_run.tf` alongside the service resource.
`prod-redline-api` gets no public invoker.

**Rationale**: Cloud Run requires invoker IAM for external callers regardless of
`ingress = INGRESS_TRAFFIC_ALL`; no invoker binding exists anywhere in the IaC,
so the acceptance curl would return HTTP 403. The issue's acceptance criterion is
an unauthenticated 200 on staging. Prod receives no traffic in this feature and
stays IAM-private until front-door work (#74/#75) decides its exposure — founder
ruling 2026-06-11. The startup probe is unaffected either way (probes bypass
invoker IAM).

**Alternatives considered**: allUsers on both services (rejected by founder:
exposes prod before any front-door/auth work); authenticated curl with identity
token (rejected: issue acceptance specifies a plain public curl; health endpoint
is contractually unauthenticated).
