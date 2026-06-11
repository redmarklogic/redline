# Implementation Plan: End-to-End Live Health Check on Cloud Run

**Branch**: `feature/110-end-to-end-live-health-check-get-health-http-200-on-cloud-run` | **Date**: 2026-06-11 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/110-end-to-end-live-health-check-get-health-http-200-on-cloud-run/spec.md`

## Summary

Take the merged-but-never-applied deploy chain live: pin and populate Secret
Manager secrets (Sydney), fix the prod scale-to-zero default, build and push the
first real backend image, `terraform apply` the existing Cloud Run IaC with that
image tag, and verify `GET <staging_url>/health` returns HTTP 200
`{"status": "healthy"}`. Then wire CI to do build → push → deploy → health check
automatically and switch the trigger to `master` (staged: Stage 1 manual proof on
the feature branch, Stage 2 trigger switch + merge). No application code changes.

## Technical Context

**Language/Version**: No application code in scope. Terraform `>= 1.6` HCL
(`hashicorp/google ~> 6.0`, ADR-020); GitHub Actions YAML; Dockerfile (existing,
issue #67). Python 3.14 / uv / pytest appear only as the existing CI test gate.

**Primary Dependencies**: `gcloud` CLI (operational ops + verification), `gh` CLI
(environment wiring), `docker` buildx (image build), SHA-pinned GitHub Actions
(`google-github-actions/auth`, `setup-gcloud`, `docker/setup-buildx-action`,
`docker/build-push-action`).

**Storage**: GCS Terraform state (`redmarklogic-tf-state`); Artifact Registry
(`redline-repo`, Sydney); Secret Manager (4 secrets, Sydney-pinned after this
feature).

**Testing**: `actionlint` on workflows; `terraform validate` + founder-reviewed
`terraform plan`; live acceptance = curl health check (manual Stage 1, automated
in CI Stage 2). No pytest changes.

**Target Platform**: Cloud Run (`linux/amd64` containers, port 8080), GitHub-hosted
`ubuntu-latest` runners, `australia-southeast1`.

**Project Type**: Infrastructure / deploy chain (monorepo, hub package `rl` —
untouched).

**Performance Goals**: Health endpoint Ready within startup-probe budget
(10 s initial delay + 3 × 5 s); CI health check waits for service Ready, then
tolerates cold start (≤ ~120 s retry window — critique E2).

**Constraints**: Idle compute cost ~$0 (scale-to-zero both services); steady-state
within ratified ~$40–75/mo ceiling; secret material never leaves
`australia-southeast1`; image tags immutable commit SHAs; `image_tag` supplied
only at apply time.

**Scale/Scope**: 2 Cloud Run services, 4 secret versions, 1 workflow file
(+ companion `tests.yml` trigger fix), 3 Terraform file edits, 0 `src/` changes.

## Constitution Check

*GATE: evaluated pre-Phase-0; re-evaluated post-Phase-1 — PASS with two recorded
waivers and one justified deviation (Complexity Tracking).*

| Principle | Verdict | Note |
|-----------|---------|------|
| I — SSOT | DEVIATION (justified) | Registry identifiers duplicated into `ci.yml` `env:` block — GH Actions cannot read tfvars. Single annotated block referencing tfvars as SSOT. See Complexity Tracking. |
| II — Hook-first | PASS | No new agent rules introduced. |
| III — Defence-in-depth | PASS | No enforcement-layer changes. |
| V/VI/VII — Facades, config, taxonomy | N/A | No application code. |
| VIII/IX — Registries, citation-only | N/A | No standards data. |
| X/XI — Exceptions, arg order | N/A | No Python changes. |
| XII — CLI-first | PASS | `gh` for environment (D9), `gcloud` for ops/verification (D2, D7, D8); no MCP/API calls. |
| XIII — Interface volatility | PASS | Health endpoint contract fixed in `src/marker/api/health.py` ("body is fixed by contract"); no interface changes. |
| XIV — Platform obligation | PASS | All pipeline steps run on Linux runners; POSIX shell in workflow; local quickstart commands PowerShell-compatible. |
| XV — IaC for GCP | PASS | Infra shape changes (`variables.tf`, `secrets.tf`) via reviewed `terraform apply`; `gcloud` confined to operational commands (secret versions, image push, deploy, describe) exactly as the principle sanctions. CI never runs `terraform apply` (D7). |
| XVI — Env as sole config | PASS | Cloud Run env injected from Secret Manager; no dotenv anywhere. |
| XVII — All-Python toolchain | PASS | No new toolchain; YAML/HCL/Dockerfile are existing surfaces. |
| Workflow — ADR before code | PASS | All decisions ground in existing ADR-020/022/023 + ratified topology doc; no new system-level decision introduced. |
| Workflow — Shaped Pitch before SpecKit | WAIVED | Founder waiver 2026-06-11 (shaping-gate, optional): issue #110 staged plan + ratified topology doc substitute. |
| Red-team gate (Principle VIII of red-team protocol) | WAIVED — Accepted Risk `[red-team-skipped]` | Founder opt-out 2026-06-11. Reason (verbatim): keyword false positives on infra wiring feature — `compliance` ("compliance debt"), `immutable` (image-tag policy), `contract` (health-body contract); no money path, AI logic, or multi-party approval surface. |

## Project Structure

### Documentation (this feature)

```text
specs/110-end-to-end-live-health-check-get-health-http-200-on-cloud-run/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 — decisions D1–D10
├── data-model.md        # Phase 1 — deploy-chain entities
├── quickstart.md        # Phase 1 — Stage 1/2 runbook
├── contracts/
│   ├── health-endpoint.md   # GET /health response contract
│   └── pipeline-outputs.md  # CI job outputs + env identifiers contract
├── checklists/requirements.md
├── version-guard-report.md  # Skipped (no npm surface); HCL/Actions pins noted
└── tasks.md             # Phase 2 (/speckit.tasks — not created by plan)
```

### Source Code (repository root)

```text
.github/workflows/
├── ci.yml               # MODIFY: real build+push, deploy job (environment:
│                        #   production), health check, trigger → master (Stage 2)
└── tests.yml            # MODIFY: trigger main → master (spec-69 T005 carry-over)

deploy/infra/terraform/
├── variables.tf         # MODIFY: min_instances_prod validation >= 0, default 0
├── secrets.tf           # MODIFY: replication auto {} → user_managed Sydney
├── cloud_run.tf         # MODIFY: add allUsers run.invoker on staging only (D11)
└── (all other files)    # UNCHANGED — applied as-is

src/                     # UNCHANGED (no application code in scope)
```

**Structure Decision**: Monorepo layout untouched; this feature edits two existing
surfaces (workflows, terraform) and creates no new directories or packages.

## Stage Mapping (spec scenarios → plan phases)

| Spec item | Plan coverage |
|---|---|
| US1 (staging live, health 200) | D6 sequence, D11 invoker grant; quickstart Stage 1 steps 3–5 |
| US2 (secrets + cost posture) | D1, D2, D3; quickstart Stage 1 steps 1–2; terraform edits |
| US3 (CI publishes image) | D4, D5, D9; ci.yml build/push + environment wiring |
| US4 (master merge end-to-end) | D7, D8, D10; deploy + health-check steps, trigger switch, merge evidence |
| Edge: missing secret version | D1/D2 ordering; quickstart pre-apply verification step |
| Edge: missing image_tag | By-design failure preserved (no default added) — noted in quickstart |
| Edge: probe failure | D8 retry + CI failure surfacing |
| Edge: WIF failure | Existing auth step precedes push; failure short-circuits job |
| Edge: replication replace | D1 (pin while zero versions exist) |
| Edge: rate-limit exemption | No action — endpoint already exempt (health.py note) |

## MoSCoW

- **Must**: D1–D8, D11 (secrets pinned + populated, scale-to-zero fix, staging
  public invoker, image in registry, services Ready, staging health 200,
  CI build→push→deploy→check).
- **Should**: D9 (`production` environment wiring), `$GITHUB_STEP_SUMMARY`
  provenance line, digest job output.
- **Could**: actionlint local run, issue #69 reconciliation note (spec-69 T016).
- **Won't (this feature)**: custom domain/cert, prod traffic, budget safeguard
  wiring, Cloud SQL, OAuth secrets, `release/**` trigger restoration (#107).

## Domain Impact

None. No geotechnical surface — pure deploy-chain infrastructure. Graeme
consultation not required.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Constitution I: GCP identifiers (registry host/project/repo/image) duplicated into `ci.yml` `env:` block (D5) | GitHub Actions cannot read `terraform.tfvars` at workflow-parse time | Repo variables hide the values from review in invisible settings; generating `ci.yml` from tfvars is build-step machinery far beyond walking-skeleton appetite. Single `env:` block carries an SSOT-pointer comment; drift surface is one reviewed location. |
