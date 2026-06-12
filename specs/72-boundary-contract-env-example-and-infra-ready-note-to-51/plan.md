# Implementation Plan: Boundary Contract — .env.example and Infra-Ready Note

**Branch**: `feature/72-boundary-contract-env-example-and-infra-ready-note-to-51` | **Date**: 2026-06-12 | **Spec**: [spec.md](spec.md)

## Summary

Add three annotated entries to root `.env.example` (`API_BASE_URL`, `GCP_OIDC_AUDIENCE`,
`CLOUD_RUN_SA_EMAIL`) and post a structured infra-ready comment on issue #51, formally
signalling that the Cloud Run infrastructure is ready for the app team to connect.
No Python source changes. All values read from `terraform output` and `gcloud` — no
invented or hard-coded constants.

## Technical Context

**Language/Version**: N/A — documentation and CLI commands only

**Primary Dependencies**: `terraform output`, `gcloud run services describe`, `gh issue comment`

**Storage**: N/A

**Testing**: Manual — `.env.example` passes `detect-secrets scan`; GitHub comment visible on #51

**Target Platform**: Developer workstation + GitHub

**Project Type**: Infrastructure documentation + GitHub comment

**Performance Goals**: N/A

**Constraints**: No secret values in committed files; detect-secrets scan must find zero new genuine secrets

**Scale/Scope**: One file changed (`.env.example`), one GitHub comment posted

## Constitution Check

| Principle | Check | Status |
|-----------|-------|--------|
| I — SSOT | `terraform.tfvars` is SSOT for project identifiers; we reference, not duplicate. `.env.example` remains SSOT for env vars. | Pass |
| VIII — Determinism | All values from `terraform output` or `gcloud` (deterministic). No LLM-inferred constants. | Pass |
| XII — CLI-first | `terraform output`, `gcloud run services describe`, `gh issue comment` — all CLI. | Pass |
| XV — IaC | No Terraform changes. `.env.example` is documentation, not an infra resource. | Pass |
| XVI — Process Environment | `.env.example` is the correct developer ergonomic tool. No `load_dotenv()` in source. | Pass |

No violations. No complexity justification required.

## Project Structure

### Documentation (this feature)

```text
specs/72-boundary-contract-env-example-and-infra-ready-note-to-51/
├── plan.md              (this file)
├── contracts/
│   └── env-contract.md  (canonical list of infra-to-app env vars)
└── tasks.md             (speckit.tasks output)
```

### Deliverables (repository root)

```text
.env.example             # Updated — confirm API_BASE_URL + add GCP_OIDC_AUDIENCE + CLOUD_RUN_SA_EMAIL
```

Plus: one `gh issue comment` on issue #51 (not committed — manual step after B7 clears).

## Phase 0: Research — Resolved Unknowns

No NEEDS CLARIFICATION markers in spec. All values deterministic.

| Item | Value | Source |
|------|-------|--------|
| Cloud Run service name pattern | `{env}-redline-api` | `cloud_run.tf` |
| Cloud Run region | `australia-southeast1` | `terraform.tfvars` |
| Cloud Run SA email | `cloud-run-api-sa@redmarklogic-prod.iam.gserviceaccount.com` | `terraform output cloud_run_sa_email` |
| OIDC audience | Equals Cloud Run service URL (GCP default for Google-issued tokens) | `cloud-run-connection-strategy.md`; GCP docs |
| IAP | Not provisioned — no IAP client ID variable needed | ADR-022, `cloud-run-connection-strategy.md` |
| API_BASE_URL | Already in `.env.example` from ADR-027; annotation may need updating | Current `.env.example` |
| Secret annotation style | Blank value + `SECRET` tag + source instruction (existing pattern) | Current `.env.example` |

**Decision — OIDC audience equals API_BASE_URL:** `GCP_OIDC_AUDIENCE` will document this
explicitly rather than being omitted. The duplication is intentional and must be visible.

## Phase 1: Design and Contracts

### Infra-to-app environment variable contract

Three entries to add under a new `Issue #72 — Cloud Run infra boundary` section in `.env.example`:

| Variable | Secret? | Value guidance |
|----------|---------|----------------|
| `API_BASE_URL` | Non-secret | Already present (ADR-027); confirm annotation is accurate |
| `GCP_OIDC_AUDIENCE` | Non-secret | Equals the Cloud Run service URL; read from `gcloud run services describe` |
| `CLOUD_RUN_SA_EMAIL` | Non-secret | `cloud-run-api-sa@redmarklogic-prod.iam.gserviceaccount.com`; verify via `terraform output cloud_run_sa_email` |

Full contract: [contracts/env-contract.md](contracts/env-contract.md)

### Infra-ready comment template (for issue #51, posted after B7 clears)

```markdown
## Infra ready (#72)

Cloud Run infrastructure is provisioned and ready for the app team to connect.

### Non-secret values (staging)

| Variable | Value |
|----------|-------|
| `API_BASE_URL` | `<live value from gcloud>` — read: `gcloud run services describe staging-redline-api --region=australia-southeast1 --format='value(status.url)'` |
| `GCP_OIDC_AUDIENCE` | Same as `API_BASE_URL` (Cloud Run OIDC tokens use the service URL as audience by default) |
| `CLOUD_RUN_SA_EMAIL` | `cloud-run-api-sa@redmarklogic-prod.iam.gserviceaccount.com` |

### Secrets

`DB_PASSWORD` and `API_KEY` are in Secret Manager (`staging-redline-db_password`,
`staging-redline-api_key`). Access: `gcloud secrets versions access latest --secret=<name>`.

### Caveats

- `API_BASE_URL` hash changes if Cloud Run service is deleted and recreated (ADR-027 D1 accepted risk).
  Always read from live service; do not hard-code.
- Post this comment only after blocker B7 is cleared.
```

## Implementation Phases

### Phase A — Update `.env.example` (no B7 dependency; ships in this PR)

1. Confirm `API_BASE_URL` entry is correct and annotation matches ADR-027 wording.
2. Add `GCP_OIDC_AUDIENCE` entry immediately after `API_BASE_URL`, tagged `Non-secret`.
3. Add `CLOUD_RUN_SA_EMAIL` entry, tagged `Non-secret`, with canonical value and `terraform output` source instruction.
4. Run `detect-secrets scan .env.example` — zero new genuine secrets.

### Phase B — Post infra-ready comment on issue #51 (manual; after B7 clears)

1. Verify B7 cleared.
2. Read live staging URL via `gcloud`.
3. Substitute into template and post via `gh issue comment 51 --repo redmarklogic/redline`.

Phase B does not block the PR. It is a manual operational step by Brent post-merge.
