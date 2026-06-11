# Version Guard Report — Skipped

No dependency sources found (no lockfile, package.json, or tech stack decision record).

Note (orchestrator): this feature touches no npm packages. The relevant version
constraints for its actual stack are already pinned in-repo and carry into the plan:

- Terraform `>= 1.6`, `hashicorp/google ~> 6.0` (`deploy/infra/terraform/versions.tf`)
- Google provider 6.x version-guard rules documented at `deploy/infra/terraform/cloud_run.tf` header
  (explicit `deletion_protection = false`; explicit `startup_probe`; list-style `env` blocks)
- GitHub Actions steps pinned by full commit SHA (`.github/workflows/ci.yml`)
