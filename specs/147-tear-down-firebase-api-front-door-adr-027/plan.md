# Implementation Plan: Tear Down Firebase API Front Door (ADR-027)

**Date**: 2026-06-12 | **Spec**: [spec.md](./spec.md)
**Status**: Draft

## Summary

This is an infrastructure teardown executed entirely in Terraform HCL under
`deploy/infra/terraform/`. It removes the Firebase Hosting front door for
`api.redmarklogic.com` — a branded API address that Firebase Hosting caps at a hard
60-second request ceiling, making it a guaranteed-failure path for the product's
three-minute-plus synchronous calls (ADR-027, superseding ADR-026). Five Terraform
resources are destroyed in dependency order (release, version, custom domain, site,
then the Cloudflare `api` CNAME), their HCL blocks and accompanying configuration
(four outputs, one variable, one tfvars value, the `firebase.json` rewrite file) are
deleted in the same change, and the irreversible/reusable pieces (Firebase project
enablement, Cloudflare provider + zone data source, google-beta provider pin, the
Cloudflare API token secret) are deliberately retained for the Sprint-3 website. The
load-bearing safety obligation is proving the founder's live email on the same
`redmarklogic.com` zone is untouched: a full zone snapshot is taken before any change
and diffed against a post-change export to show exactly one record removed and zero
others changed. No application code (`src/`) is touched; this plan produces no Python,
no tests, no domain models.

## Technical Context

**Primary technology**: Terraform HCL (`>= 1.6`)
**Providers**: `hashicorp/google-beta ~> 6.0` (Firebase resources), `cloudflare/cloudflare ~> 5.19` (DNS), `hashicorp/google ~> 6.0` (retained, unaffected)
**Resource location**: `deploy/infra/terraform/`
**State backend**: GCS (per `backend.tf`)
**Auth**: Cloudflare provider reads `CLOUDFLARE_API_TOKEN` (from Secret Manager `prod-redline-cloudflare-api-token`) at plan/apply time; google-beta uses ADC
**Tooling**: `gcloud`/`terraform`/`gh` CLIs (CLI-first, Principle XII); `nslookup`/`curl` for verification
**Dev OS**: Windows | **Execution context**: reviewed `terraform apply` from operator workstation
**Python / pytest / Pydantic / import-linter**: N/A — no `src/` change, no domain layer touched
**Out of scope for this phase**: the actual `terraform apply` (gated on ADR-027 merge; this spec-kit phase produces docs only)

## Design Decisions

| #  | Decision | Choice | Rationale |
| -- | -------- | ------ | --------- |
| D1 | Destruction mechanism | Terraform destroy only (HCL block removal → `terraform plan`/`apply`) | ADR-020 / Principle XV: no console changes; the `api` CNAME deletion rides the same reviewed apply (ADR-020 forbids dashboard edits) |
| D2 | Destroy ordering | release → version → custom_domain → site → CNAME | Reverse-dependency order; Terraform computes it from `depends_on`, but the HCL is removed as one set and the plan is verified to show this |
| D3 | `firebase.json` removal | In scope (FR-010) | Reconciliation: ADR-027 D2 lists it; issue #147 omits it. ADR-027 governs scope. Rewrite intent no longer exists |
| D4 | Keep `google_firebase_project.default` | Retain in state + HCL | Provider implements no delete; irreversible; zero cost; Sprint-3 website reuses it. Destroying it is impossible and must not appear in the plan |
| D5 | Zone-safety proof | Pre/post full zone export + diff, saved artifact | Founder email lives on this zone; the single-CNAME deletion is the one sanctioned exception to additive-only DNS discipline — it requires positive proof of no collateral change |
| D6 | Variable/output cleanup | Remove `firebase_cname_target` (var + tfvars value) and four `firebase_*` outputs in same change | A dangling variable with a non-empty validation, or outputs referencing destroyed resources, breaks `terraform validate`/`plan` |
| D7 | Environment example | Conditional edit (FR-011) | Only edit `.env.example` files that actually reference the branded URL; declare `run.app` as POC base URL |

## Constitution Check

| Principle | Status | Note |
| --------- | ------ | ---- |
| XV — IaC for GCP Resources | PASS | All changes via Terraform HCL + reviewed apply; no console edits; `terraform.tfvars` updated as SSOT |
| XII — CLI-First Tool Selection | PASS | `terraform`, `gcloud`, `gh`, `nslookup`, `curl` — no MCP/API substitutes |
| ADR-020 additive-DNS discipline | PASS (sanctioned exception) | Single `api` CNAME deletion is the one allowed exception, guarded by the mandatory pre-change zone snapshot |
| I — Single Source of Truth | PASS | `terraform.tfvars` remains the SSOT for GCP identifiers; the removed `firebase_cname_target` had a single definition site |
| XVI — Process Environment as Sole Config | PASS | `.env.example` is a developer-ergonomic file only; edit declares the POC base URL, introduces no `load_dotenv` obligation |

No constitution violations. No gate requires justification.

## Architecture

### Resource dependency graph (destroy order)

```
google_firebase_hosting_release.api      (1) ── depends on ──┐
google_firebase_hosting_version.api      (2) ◄───────────────┘
        │ depends on
        ▼
google_firebase_hosting_custom_domain.api (3)
        │ depends on
        ▼
google_firebase_hosting_site.api          (4)
        │ depends on
        ▼
google_firebase_project.default          [KEPT — never destroyed]

cloudflare_dns_record.firebase_cname      (5) ── independent; deleted with zone snapshot guard
```

### What changes, file by file

| File | Change |
| ---- | ------ |
| `deploy/infra/terraform/firebase_hosting.tf` | Delete blocks for site, custom_domain, version, release (resources 2–4b) + four `firebase_*` outputs. KEEP `google_firebase_project.default` block + its comment; retitle file header per ADR-027 |
| `deploy/infra/terraform/cloudflare_dns.tf` | Delete `cloudflare_dns_record.firebase_cname` block. KEEP provider + `data.cloudflare_zone.redmarklogic` |
| `deploy/infra/terraform/variables.tf` | Delete `variable "firebase_cname_target"` block |
| `deploy/infra/terraform/terraform.tfvars` | Delete `firebase_cname_target = "redmarklogic-api.web.app"` line |
| `deploy/firebase/firebase.json` | Delete (+ evaluate removing `deploy/firebase/public/.gitkeep` and the dir if no other consumer) |
| `.env.example` (and/or `deploy/docker/marker/.env.example`) | Conditional: declare `run.app` base URL if branded URL referenced |
| `docs/infrastructure/domain-dns-runbook.md` | Update to reflect removed front door |
| `docs/infrastructure/manual-steps-to-terraform.md` | Add rollback entry for this teardown |

## MoSCoW

| Category | Items |
| -------- | ----- |
| **Must have** | Destroy the 5 resources (FR-001–006); pre-change zone snapshot (FR-017); plan shows exactly 5 destroys/0 other changes verified before apply (FR-018); post-change zone diff (FR-019); founder email confirmed (FR-020); HCL/var/output/tfvars cleanup (FR-007–009); keep-list retained (FR-012–015); ADR-027-merge gate respected (FR-016) |
| **Should have** | `firebase.json` removal (FR-010); runbook + manual-steps rollback entry (FR-021–022); `.env.example` POC URL (FR-011) |
| **Could have** | Remove `deploy/firebase/` dir entirely if `public/.gitkeep` has no other purpose |
| **Won't have (this time)** | Branded API domain replacement (deferred per ADR-027 D4); Cloudflare Worker empirical test; global ALB front door |

## Phased Delivery

> TDD/pytest gates from the preset template do not apply — there is no Python under test.
> Each phase's gate is a Terraform/DNS verification, substituted below.

### Phase 0: Gate verification + zone snapshot (blocking)

**Goal**: Establish the two blocking preconditions before any HCL edit.

**Deliverables**:
1. Confirm ADR-027 is merged to master (FR-016).
2. Full Cloudflare zone export of `redmarklogic.com` saved as a pre-change artifact (FR-017) — under `docs/infrastructure/` or attached to the PR.

**Verification**:
```
# ADR-027 present on master; zone export captured (MX, SPF/TXT, api CNAME, all records)
```

**Acceptance Gate**:
- [ ] ADR-027 merged on master.
- [ ] Pre-change zone snapshot saved and complete (contains the founder's MX/SPF records and the `api` CNAME).

---

### Phase 1: HCL teardown edits

**Goal**: Remove the five resources' HCL + accompanying config so the next `terraform plan` proposes exactly five destroys and zero other changes.

**Deliverables** (see Architecture file table): edited `firebase_hosting.tf`, `cloudflare_dns.tf`, `variables.tf`, `terraform.tfvars`; deleted `deploy/firebase/firebase.json`.

**Verification**:
```
terraform validate          # passes — no dangling refs to removed var/outputs/resources
terraform plan              # EXACTLY 5 to destroy, 0 to add, 0 to change
```

**Acceptance Gate**:
- [ ] `terraform validate` passes.
- [ ] `terraform plan` shows exactly 5 destroys, 0 adds, 0 changes; no keep-list resource (esp. `google_firebase_project.default`) appears. Any deviation = stop-the-line.

---

### Phase 2: Reviewed apply + verification

**Goal**: Apply the teardown and prove the zone (and founder email) are intact.

**Deliverables**: applied teardown; post-change zone export; verification checklist results.

**Verification**:
```
# After reviewer confirms the Phase 1 plan diff:
terraform apply
terraform plan                                   # clean, no drift (SC-001)
nslookup api.redmarklogic.com                    # no CNAME (SC-002)
curl -s -o NUL -w "%{http_code}" https://<run.app-url>/health   # unchanged vs baseline (SC-003)
terraform output                                 # no firebase_* outputs (SC-006)
# Diff post-change zone export vs Phase 0 snapshot → exactly 1 record removed (SC-004)
# Founder send/receive email test (SC-005)
```

**Acceptance Gate**:
- [ ] Reviewer confirmed the plan diff before apply (FR-018).
- [ ] Post-apply `terraform plan` clean (SC-001).
- [ ] `api.redmarklogic.com` no longer resolves (SC-002); `run.app` health unchanged (SC-003).
- [ ] Zone diff = exactly one record removed, zero other changes (SC-004).
- [ ] Founder email send/receive confirmed (SC-005).
- [ ] No `firebase_*` outputs remain (SC-006).

---

### Phase 3: Documentation + rollback record

**Goal**: Leave a clean, documented state.

**Deliverables**: updated `domain-dns-runbook.md`; rollback entry in `manual-steps-to-terraform.md`; `.env.example` POC URL (if applicable).

**Verification**:
```
# Runbook reflects removed front door; manual-steps has a teardown rollback entry;
# .env.example declares run.app base URL (if it referenced the branded URL)
```

**Acceptance Gate**:
- [ ] Runbook updated (FR-021).
- [ ] Manual-steps rollback entry added (FR-022).
- [ ] `.env.example` updated if it referenced the branded URL (FR-011).

## File Inventory

| Phase | Files touched | Count |
| ----- | ------------- | ----- |
| 0 | zone snapshot artifact (new) | 1 |
| 1 | `firebase_hosting.tf`, `cloudflare_dns.tf`, `variables.tf`, `terraform.tfvars` (edit); `deploy/firebase/firebase.json` (delete) | 5 |
| 2 | post-change zone snapshot artifact (new) | 1 |
| 3 | `domain-dns-runbook.md`, `manual-steps-to-terraform.md`, `.env.example` (edit) | 3 |

**Resources destroyed**: exactly 5 | **Files deleted**: 1 (`firebase.json`, + optional dir) | **Files edited**: 6 | **Artifacts created**: 2 (zone snapshots)

## Library Best Practices

### terraform / providers

- **google-beta `~> 6.0`**: `google_firebase_project` has no delete operation — removing its HCL block does **not** destroy it; it must be retained in HCL to keep it in state without churn. Do not attempt `terraform state rm` unless intentionally orphaning (not wanted here).
- **cloudflare `~> 5.19`**: `cloudflare_dns_record` destroy removes the live DNS record. The provider needs `CLOUDFLARE_API_TOKEN` with `Zone:DNS:Edit` at apply time. The zone data source (`data.cloudflare_zone`) is read-only and retained.
- **Gotcha**: `firebase_cname_target` has a non-empty `validation` block; removing the variable and its tfvars value together avoids a validation error on the next plan.

## Risk Register

| Risk | Mitigation |
| ---- | ---------- |
| Collateral DNS change breaks founder email (MX/SPF) | Mandatory pre-change zone snapshot (Phase 0) + post-change diff (Phase 2); stop-the-line if any non-`api` record changes |
| Plan proposes destroying `google_firebase_project.default` | Keep its HCL block intact; treat any such plan line as a defect — stop and fix HCL before apply |
| Plan shows ≠ 5 destroys | Reviewer gate (FR-018) blocks apply until plan matches exactly |
| `terraform validate` fails on dangling reference | Remove variable + outputs + resources atomically in Phase 1 before validate |
| run.app address regresses | SC-003 baseline-vs-post health check; run.app is untouched by this change |
| Rollback needed | Documented revert + re-apply + two-step DNS converge; cert re-issuance ≤ 24 h (within 48 h budget) |

## Glossary

| Term | Definition |
| ---- | ---------- |
| Front door | The Firebase Hosting + DNS layer that mapped the branded `api.redmarklogic.com` address onto the Cloud Run backend. |
| run.app URL | The raw auto-generated Cloud Run service address; the POC's canonical API address per ADR-027. |
| Additive-only DNS discipline | The rule (ADR-020/026) that zone records are only added, never deleted, to protect the founder's live email — this teardown is its single sanctioned exception. |
| Zone snapshot | A full export of all `redmarklogic.com` DNS records, taken before and after the change to prove no collateral damage. |
| Keep-list | The irreversible/reusable resources deliberately retained through the teardown. |
