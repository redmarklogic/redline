# Version Guard Report

Generated: 2026-06-10T00:00:00+00:00

## Scope Note

This project uses Python + GCP + Terraform (no npm packages). Version sources:
- **Python runtime deps**: `uv.lock` (exact pinned versions)
- **Infrastructure**: `deploy/infra/terraform/versions.tf` (declared constraints)

---

## Version Status

### Python Runtime (from uv.lock)

| Package | Locked | Latest Stable | Status |
|---------|--------|---------------|--------|
| fastapi | 0.136.3 | 0.136.3 | ✅ Current |
| pydantic | 2.13.4 | 2.13.4 | ✅ Current |
| uvicorn | 0.49.0 | 0.49.0 | ✅ Current |
| starlette | 1.2.1 | 1.2.1 | ✅ Current |
| python-docx | 1.2.0 | 1.2.0 | ✅ Current |
| pytest | 9.0.3 | 9.0.3 | ✅ Current |

### Infrastructure (from versions.tf)

| Component | Locked / Declared | Latest Stable | Status |
|-----------|-------------------|---------------|--------|
| Terraform CLI | `>= 1.6` (no upper bound) | 1.15.5 | ✅ Compatible (range satisfies latest) |
| hashicorp/google provider | `~> 5.0` (5.x only) | 7.36.0 (latest 5.x: 5.45.2) | ⚠️ Behind — two major versions |

---

## Known Issues

⚠️ Known issue lookups for GitHub Security Advisories were not performed for PyPI packages
(network fetch skipped; manual check via `pip audit` recommended before deployment).

No CVEs are known to the model at the time of writing for fastapi 0.136.3, pydantic 2.13.4,
uvicorn 0.49.0, or starlette 1.2.1.

⚠️ **Security vulnerabilities should be addressed promptly.** If a patched version exists,
consider upgrading. If upgrading is not possible, review the advisory for available workarounds.

| Package | Version | Severity | Type | Issue | Patched In |
|---------|---------|----------|------|-------|------------|
| — | — | — | — | No known issues found for locked Python versions | — |

---

## Compatibility Rules (mandatory)

These rules ensure generated Terraform and Python code works correctly with the **locked versions**.

### hashicorp/google provider (locked ~> 5.0 — latest is 7.x)

The provider is pinned to 5.x (`~> 5.0`). All Terraform code written for this feature MUST
target the 5.x API surface. Do NOT use resources, arguments, or defaults introduced in 6.x or 7.x.

| # | ❌ DON'T | ✅ DO instead |
|---|----------|--------------|
| 1 | Assume `google_cloud_run_v2_service` has `deletion_protection = false` as default (6.x changed this to `true`) | Explicitly set `deletion_protection = false` when Terraform needs to be able to destroy the service |
| 2 | Use hash-based access for `containers.env` entries (6.x changed env from list to set) | Use list-style iteration; index-based `containers.env[0]` references are valid in 5.x |
| 3 | Omit `liveness_probe` and rely on an API default (removed in 6.x) | Either include an explicit `liveness_probe` block or accept that no probe will be configured — both are explicit |
| 4 | Reference `public_repository` fields without explicit values (7.x removed defaults) | Not applicable in 5.x — but do not forward-port 7.x patterns |
| 5 | Use `template.containers.depends_on` in Cloud Run v2 Worker Pool resources (removed in 7.x) | Not applicable in 5.x — field exists, but avoid it for future compatibility |
| 6 | Target resource schemas from provider 6.x or 7.x documentation | Use the 5.x provider reference: https://registry.terraform.io/providers/hashicorp/google/5.45.2/docs |

### fastapi (locked 0.136.3 — ✅ current)

No compatibility constraints — locked version is current.

### pydantic (locked 2.13.4 — ✅ current)

No compatibility constraints — locked version is current.
The project uses Pydantic v2 throughout; do not write v1 patterns (`class Config:`, `@validator`).

| # | ❌ DON'T | ✅ DO instead |
|---|----------|--------------|
| 1 | Use `class Config:` inner class for model configuration (v1 pattern) | Use `model_config = ConfigDict(...)` |
| 2 | Use `@validator` decorator | Use `@field_validator` with `mode='before'/'after'` |

### uvicorn (locked 0.49.0 — ✅ current)

No compatibility constraints — locked version is current.

### Python runtime (requires-python = ">=3.14")

| # | ❌ DON'T | ✅ DO instead |
|---|----------|--------------|
| 1 | Use `typing.Union[X, Y]` or `Optional[X]` as annotations in new code | Use `X \| Y` and `X \| None` (PEP 604, native in 3.10+) |
| 2 | Use `typing.List`, `typing.Dict` etc. in annotations | Use `list[...]`, `dict[...]` builtins (PEP 585, native in 3.9+) |
| 3 | Target a Docker base image older than `python:3.14-slim` | Pin the Dockerfile `FROM` to `python:3.14-slim` (or a specific digest) |

---

## Upgrade Guidance (informational)

### hashicorp/google provider (5.45.2 → 7.36.0)

Two major versions behind. Key changes:

**5.x → 6.x breaking changes:**
- `deletion_protection = true` is now the default for `google_cloud_run_v2_service` and `_job`
- `containers.env` changed from list to set — index-based references break
- `liveness_probe` no longer receives an API default when omitted
- A `goog-terraform-provisioned = true` label is auto-added to resources (can be suppressed)

**6.x → 7.x breaking changes:**
- Artifact Registry `public_repository` fields have default values removed — must be explicit
- `google_cloud_run_v2_job/service` Worker Pool: `template.containers.depends_on` removed
- Import validation is stricter — malformed import IDs now rejected

**Upgrade path:** First upgrade `~> 5.0` → `~> 6.0` (apply 5→6 migration guide, run `terraform plan`),
then upgrade `~> 6.0` → `~> 7.0` (apply 6→7 migration guide). Do not skip major versions.

**Decision note:** Upgrading the provider is out of scope for this feature. The existing
`versions.tf` pin (`~> 5.0`) governs. Raise a separate issue to track the provider upgrade.

---

## Migration References

- **hashicorp/google provider** (locked 5.x): https://registry.terraform.io/providers/hashicorp/google/5.45.2/docs
- **hashicorp/google provider** (5→6 upgrade guide): https://github.com/hashicorp/terraform-provider-google/blob/main/website/docs/guides/version_6_upgrade.html.markdown
- **hashicorp/google provider** (6→7 upgrade guide): https://github.com/hashicorp/terraform-provider-google/blob/main/website/docs/guides/version_7_upgrade.html.markdown
- **Terraform CLI** (latest 1.15.5): https://developer.hashicorp.com/terraform/language

### Current-Version References (Python)

Documentation for locked versions — consult these before relying on training data:

- **fastapi** (0.136.3): https://fastapi.tiangolo.com/reference/
- **pydantic** (2.13.4): https://docs.pydantic.dev/latest/
- **uvicorn** (0.49.0): https://www.uvicorn.org/
- **starlette** (1.2.1): https://www.starlette.io/
- **pytest** (9.0.3): https://docs.pytest.org/en/stable/
- **python-docx** (1.2.0): https://python-docx.readthedocs.io/en/latest/

### GCP Service References

- **Cloud Run v2** (Terraform resource): https://registry.terraform.io/providers/hashicorp/google/5.45.2/docs/resources/cloud_run_v2_service
- **Secret Manager** (Terraform resource): https://registry.terraform.io/providers/hashicorp/google/5.45.2/docs/resources/secret_manager_secret
- **Artifact Registry** (Terraform resource): https://registry.terraform.io/providers/hashicorp/google/5.45.2/docs/resources/artifact_registry_repository
- **Cloud Run — secret env vars** (GCP docs): https://cloud.google.com/run/docs/configuring/secrets
- **Cloud Run — min/max instances** (GCP docs): https://cloud.google.com/run/docs/configuring/min-instances
