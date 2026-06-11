# Version Guard Report — Skipped

No dependency sources found (no lockfile, package.json, or tech stack decision record).

Generated: 2026-06-11

## Note (project context)

This is a Python/uv project (`uv.lock` present); the version guard's npm-registry
check does not apply. Versions relevant to this feature are pinned outside npm:

| Item | Pinned where | Value |
|------|--------------|-------|
| Base image | `deploy/docker/marker/Dockerfile` | `python:3.14-slim` |
| uv | Dockerfile builder stage | `ghcr.io/astral-sh/uv:latest` (build-time only) |
| Python deps | `uv.lock` (frozen sync) | exact resolved versions |
| Terraform google provider | `deploy/infra/terraform/versions.tf` | `~> 6.0` (ADR-020) |

No compatibility rules generated. Existing version-guard comments in
`deploy/infra/terraform/cloud_run.tf` remain authoritative for Terraform patterns.
