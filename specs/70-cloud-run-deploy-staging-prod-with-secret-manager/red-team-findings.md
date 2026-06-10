---
session_id: RT-70-cloud-run-deploy-staging-prod-with-secret-manager-2026-06-10
target: specs/70-cloud-run-deploy-staging-prod-with-secret-manager/spec.md
date: 2026-06-10
maintainer: Brent (DevOps)
lenses_run:
  - API Contract Adversary
lenses_excluded:
  - AI Output Integrity Adversary  # trigger_match: [ai_llm] — not triggered
  - Professional Liability Adversary  # trigger_match: [regulatory_path, ai_llm] — not triggered
  - Engineer-in-the-Loop Adversary  # trigger_match: [ai_llm, multi_party] — not triggered
selection_method: auto
matched_triggers: [money_path, contracts]
constitution_mode: bootstrap  # No ## Red Team Trigger Criteria in constitution
lens_diversity_warning: true  # Only 1 of 4 catalog lenses triggered; below recommended minimum of 3
supporting_context: none (no plan.md or contracts/ present yet)
---

# Red Team Findings — Feature 70: Cloud Run Deploy (Staging + Prod with Secret Manager)

## Pre-Session Notices

**WARNING: constitution does not yet declare red team trigger criteria** (expected at `## Red Team Trigger Criteria`). Proceeding in bootstrap mode using the six default categories.

**WARNING: lens diversity weak.** Only 1 lens triggered out of 4 in the catalog (`API Contract Adversary` via `contracts` trigger). The three remaining lenses — AI Output Integrity, Professional Liability, Engineer-in-the-Loop — require `ai_llm`, `regulatory_path`, or `multi_party` triggers that this infrastructure/DevOps spec does not exhibit. This is expected and honest: the spec does not touch LLM output, professional licensing, or multi-party approval workflows. Proceeding with single-lens session; gate requirement satisfied.

---

## §1 Session Summary

*(Maintainer fills post-review)*

---

## §2 Findings

### Lens: API Contract Adversary

*Attacks interface contracts — looks for implicit assumptions between rule engine, LLM layer, and output renderer that would silently break under valid inputs.*

| ID | Severity | Location | Description | Suggested Resolution |
|---|---|---|---|---|
| F-RT-70-001 | HIGH | FR-008 + Assumptions | **Secret naming contract is entirely implicit.** FR-008 requires staging and production to reference separate Secret Manager secret names but specifies no naming schema or convention. If the Terraform binding and the application code use different naming conventions (e.g., `staging/api-key` vs `staging-api-key`), the env-var binding silently fails at container startup — no deploy error, just a missing env var at runtime. | Define a canonical secret-naming convention in Terraform variables (e.g., `<env>-<service>-<credential>`) and document it as a contract in FR-008 or a new FR. Enforce via Terraform `locals` or a naming validation check. |
| F-RT-70-002 | HIGH | FR-006, FR-007, Edge Cases | **Health-check readiness contract is underspecified on the error side.** FR-006/007 define the success path (HTTP 200 → READY → traffic routed) but the error contract is missing: Cloud Run's health-check timeout, failure threshold, and initial-delay period are not specified. A partially-initialized service (e.g., secrets loaded but database not yet connected) could return 200 and pass the readiness gate, routing traffic to a broken service. | Add an FR or note to Assumptions specifying the Cloud Run health-check probe parameters (initial delay, timeout, failure threshold). Update the health-check contract to require the application to verify downstream dependencies before returning 200. |
| F-RT-70-003 | MEDIUM | FR-002, SC-002 | **Secret-in-state verification has no automated error contract.** FR-002 prohibits secret values in deployment manifests and source control. SC-002 verifies this "by inspection" — a human process. There is no automated check, no CI gate, and no definition of who inspects or when. A valid Terraform configuration that accidentally binds a secret value through a `locals` block would satisfy FR-002's intent but violate it in practice, and the only detection mechanism is manual. | Define the verification mechanism for SC-002 explicitly: either a `terraform plan` output scan, a `tfsec`/`checkov` rule, or a pre-apply hook. Record it as a testable acceptance criterion rather than "verified by inspection." |
| F-RT-70-004 | MEDIUM | FR-009 + Assumptions | **Idempotency contract breaks silently on secret rotation.** FR-009 requires that re-running the deploy with the same image produces the same service configuration. However, if a Secret Manager secret version is rotated between two deploy runs, the "same configuration" binds to different secret values. The spec treats secret version management as out-of-scope but does not acknowledge this as a known deviation from the idempotency guarantee. | Either scope FR-009 explicitly to exclude secret-version content (idempotency applies to service configuration, not to secret values), or add a note to Assumptions that secret-version pinning is required for strict idempotency and document the rotation procedure. |
| F-RT-70-005 | LOW | FR-010 + Assumptions | **Terraform input validation contract for upstream artifacts is absent.** The spec assumes container images are pre-published to Artifact Registry (Assumptions) and that the deploy references an existing image digest. The edge-case section covers what happens when the digest is missing, but no FR or acceptance scenario requires the Terraform/deploy tooling to validate image existence before attempting the update. A malformed digest (typographic error) could reach Cloud Run and produce an opaque failure. | Add an acceptance criterion or FR requiring the deploy procedure to validate image digest existence in Artifact Registry before applying the Cloud Run revision update (e.g., `gcloud artifacts docker images describe <digest>` as a pre-flight check). |

---

## §3 Resolutions Log

*(Walk through each finding and categorise below.)*

### F-RT-70-001 — Secret naming contract implicit

- **Status**: resolved
- **Resolution category**: spec-fix
- **Downstream ref**: FR-008 updated
- **Notes**: Added canonical naming convention `{env}-redline-{credential}` and required a shared Terraform `locals` block for env-var mapping.

### F-RT-70-002 — Health-check readiness contract underspecified

- **Status**: resolved
- **Resolution category**: spec-fix
- **Downstream ref**: FR-006, FR-007 updated
- **Notes**: FR-006 requires 200 only when fully ready (no partial-init pass). FR-007 now declares explicit probe parameters (initial delay ≥ 10 s, timeout 5 s, failure threshold 3).

### F-RT-70-003 — Secret-in-state verification no automated contract

- **Status**: resolved
- **Resolution category**: spec-fix
- **Downstream ref**: SC-002 updated
- **Notes**: SC-002 now requires checkov/tfsec pre-apply gate; manual inspection alone no longer satisfies the criterion.

### F-RT-70-004 — Idempotency breaks on secret rotation

- **Status**: resolved
- **Resolution category**: spec-fix
- **Downstream ref**: FR-009 updated
- **Notes**: FR-009 now explicitly scopes idempotency to service configuration and accepts secret-rotation deviation as a known caveat.

### F-RT-70-005 — No image-existence pre-flight validation

- **Status**: open
- **Resolution category**: new-OQ
- **Downstream ref**: plan.md (to be addressed in deploy procedure tasks)
- **Notes**: Edge case already noted in spec. Pre-flight `gcloud artifacts docker images describe` check to be specified as a task in plan/tasks phase.

---

## §5 Session Metadata

```yaml
session_id: RT-70-cloud-run-deploy-staging-prod-with-secret-manager-2026-06-10
target: specs/70-cloud-run-deploy-staging-prod-with-secret-manager/spec.md
date: 2026-06-10
lenses_run: [API Contract Adversary]
lenses_excluded:
  AI Output Integrity Adversary: trigger_match [ai_llm] not present
  Professional Liability Adversary: trigger_match [regulatory_path, ai_llm] not present
  Engineer-in-the-Loop Adversary: trigger_match [ai_llm, multi_party] not present
selection_method: auto
matched_triggers: [money_path, contracts]
findings_total: 5
findings_by_severity:
  CRITICAL: 0
  HIGH: 2
  MEDIUM: 2
  LOW: 1
findings_by_lens:
  API Contract Adversary: 5
lens_failures: []
dropped_findings: 0
resolutions:
  spec-fix: 0
  new-OQ: 0
  accepted-risk: 0
  out-of-scope: 0
unresolved: 5
notes: >
  Single-lens session; catalog has no lenses covering money_path in isolation —
  cost-cap concern (User Story 3, SC-005) is noted but no lens attacked it directly.
  Constitution bootstrap mode active (no ## Red Team Trigger Criteria declared).
  Lens diversity warning: below recommended minimum of 3 lenses.
```
