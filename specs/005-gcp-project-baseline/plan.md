# Implementation Plan: GCP Project Baseline

**Branch**: `005-gcp-project-baseline` | **Date**: 2026-06-10 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/005-gcp-project-baseline/spec.md`

**Note**: This is an infrastructure provisioning feature. There is no Python application
code. Deliverables are provisioning scripts, a verification script, and an inventory file.

## Summary

Stand up the GCP project foundation required by all deploy-chain issues (#65-#72).
Provisioning sets the project ID, locks the default region to `australia-southeast1`,
enables nine required APIs, links a billing account, and records canonical identifiers
in a version-controlled inventory file that acts as the SSOT for downstream scripts.

## Technical Context

**Language/Version**: PowerShell 7+ (dev machine) — per ADR-019, dev scripts run on
Windows. CI equivalents (if needed) are Bash targeting Linux.

**Primary Dependencies**: `gcloud` CLI (google-cloud-sdk) — required by Constitution XII
(CLI-first tool selection, ADR-016). No Terraform at this stage; `gcloud` imperative
scripts are sufficient for a single-project bootstrap.

**Storage**: `infra/inventory.yml` — version-controlled YAML, single source of truth for
project ID, region, and billing account reference (Constitution I, ADR-001).

**Testing**: `gcloud` read-only verification commands (projects describe, services list,
billing info). No pytest. Manual verification via `infra/gcp/verify.ps1`.

**Target Platform**: GCP `australia-southeast1`. Dev execution: Windows PowerShell 7+.

**Project Type**: Infrastructure provisioning (bootstrap script + inventory).

**Performance Goals**: End-to-end provisioning under 15 minutes from clean state (SC-001).

**Constraints**:

- Idempotent execution -- re-run must produce zero changes on already-configured project
  (FR-005, SC-004).
- `gcloud` CLI only -- no GCP Console manual steps, no direct REST calls (Constitution XII).
- Billing account and organisation/folder must exist before provisioning runs (Assumptions).

**Scale/Scope**: Single GCP project. Staging/prod separation is deferred.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design.*

| Principle | Assessment | Action |

|-----------|-----------|--------|
| I. SSOT | `infra/inventory.yml` will be the canonical store for project ID, region, billing ref. No other file may define these. | Define schema in Phase 1. |
| II. Hook-First | No code rules to enforce via pre-commit. Not applicable to infra scripts. | N/A |
| VI. Data-Driven | Region and API list are configuration values -- must live in `inventory.yml` or a companion config, not hardcoded in the provisioning script. | Parameterise script from config. |
| XII. CLI-First | `gcloud` is the required tool for all GCP operations. No raw REST calls. | Enforced in script design. |
| XIV. Platform Obligation | Provisioning scripts run on Windows dev (PowerShell). Any CI equivalent targets Linux (Bash). Scripts separated by platform, not branched within one file. | Two script files per operation. |
| ADR before code | Cloud Run + Artifact Registry ADR (#63) must be accepted before implementation runs. | Gate task added in tasks.md. |

**No constitution violations.** Complexity Tracking section omitted.

## Project Structure

### Documentation (this feature)

```text
specs/005-gcp-project-baseline/
├── plan.md                      # This file
├── research.md                  # Phase 0 output
├── contracts/
│   └── inventory-schema.md      # Phase 1 -- inventory.yml contract
└── tasks.md                     # Phase 2 output (speckit.tasks)
```

### Source Code (repository root)

```text
infra/
├── gcp/
│   ├── bootstrap.ps1     # Provision: create project, set region, enable APIs, link billing
│   ├── bootstrap.sh      # CI equivalent (Linux/Bash -- mirrors bootstrap.ps1 exactly)
│   └── verify.ps1        # Verify: read-only checks confirming SC-001 through SC-005
└── inventory.yml         # SSOT: project_id, region, billing_account, enabled_apis[]
```

**Structure Decision**: Single `infra/gcp/` directory. No `src/` involvement -- this feature
has no application code. The `infra/inventory.yml` file is the only cross-feature artifact;
all other infra files are internal to the provisioning workflow.
