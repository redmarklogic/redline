# Contract: CI Pipeline Identifiers and Outputs

**Consumers**: downstream deploy issues (#74/#75 front door, #107 release
triggers), founder review.

## Workflow-level env block (`ci.yml`) — SSOT pointer required

```yaml
# SSOT: deploy/infra/terraform/terraform.tfvars — keep in sync (Constitution I deviation, plan.md Complexity Tracking)
env:
  GCP_REGION: australia-southeast1
  GCP_PROJECT: redmarklogic-prod
  AR_REPO: redline-repo
  IMAGE_NAME: redline-api
```

All registry references below the block MUST use `${{ env.* }}` — no second
literal occurrence of any identifier in the file.

## Image reference format

```
${GCP_REGION}-docker.pkg.dev/${GCP_PROJECT}/${AR_REPO}/${IMAGE_NAME}:${{ github.sha }}
```

## Job outputs

| Output | Source | Meaning |
|---|---|---|
| `image_digest` | build-push step `outputs.digest` | Immutable `sha256:...` digest of the pushed image; provenance handoff |

## Job ordering invariants

1. pytest gate precedes WIF auth / build / push — a red gate publishes nothing.
2. Deploy step (staging image update) runs only after a successful push.
3. Health-check step runs only after deploy; non-200 (or wrong body) fails the run.
4. No `continue-on-error: true` / `if: always()` on gate, push, deploy, or check.
5. Deploy job declares `environment: production`.

## Triggers (end state, Stage 2)

```yaml
on:
  workflow_call: {}
  push:
    branches: [master]
```

`release/**` removed (restored by #107, 2026-06-22). `tests.yml` trigger likewise
`main` → `master`.
