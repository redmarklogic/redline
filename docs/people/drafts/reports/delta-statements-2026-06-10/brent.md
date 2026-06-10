# Delta Statement — Brent (DevOps Engineer, GCP)

**Window:** 2026-06-07 (my onboarding sync) → 2026-06-10. **Drift level: I agree with the facilitator's HIGH rating** — all three flagged contradictions are real and evidence-backed.

## 1. What I own today

Cloud infrastructure on GCP (Google Cloud Platform): the Cloud Run deployment surface, IAM (Identity and Access Management) least-privilege, the infra boundary contract (`.env.example`), CI/CD (Continuous Integration / Continuous Deployment) pipelines, observability, cost controls, SOC 2 technical controls, and — per ADR-020, newly — the Terraform HCL (HashiCorp Configuration Language) under `deploy/infra/terraform/` plus `terraform state` operations. I own two knowledge notebooks per the register: "DevOps & GCP Infrastructure" (8 books, incl. Terraform IaC on GCP) and "GCP DevOps Tactical Playbook" (official Google docs). I do not write Python application code (Kabilan) or ADRs (Peter).

## 2. What changed in my domain since the last sync (evidence)

- **ADR-020 accepted 2026-06-10** (`docs/adr/adr-020-infrastructure-as-code-terraform-gcp.md`): Terraform owns all GCP infrastructure; two bootstrap exceptions (`deploy/infra/bootstrap/bootstrap.sh`); `terraform state` operations named as Brent tasks; `gcloud` reserved for bootstrap, read-only diagnostics, and deploy/release ops. I am a named decider.
- **ADR-021 accepted 2026-06-10**: process environment is the sole config source; `.env` files are local-developer-only and excluded from the Docker build context. My `.env.example` boundary contract remains valid as documentation — values now provably enter only at container start.
- **ADR-022 accepted 2026-06-10**: Cloud Run + Artifact Registry in `australia-southeast1`; Tier-1 approval for public HTTPS ingress; IAP (Identity-Aware Proxy) explicitly **not** required now; Bearer-token presence placeholder; multi-IdP requirement (Google **and** Microsoft identity) makes IAP-alone unviable; successor auth ADR deferred to issue #73.
- **Commit `09d6d8f` (2026-06-10)**: `infra/` relocated to `deploy/infra/` — verified on disk: `deploy/infra/terraform/` (now incl. `cloud_run.tf`, `iam.tf`, `secrets.tf`), `deploy/infra/bootstrap/`, `deploy/docker/marker/`.
- **Spec-70 shipped (PR #97 merged)**: Cloud Run staging/prod with Secret Manager wiring; provider pinned `~> 6.0` in `versions.tf` with `deletion_protection` (commit `103bc28`).
- **R3 finding 1 — Terraform Google provider 7.x is GA**: latest is 7.35.0 (2026-06-02); 7.0 GA'd with breaking changes and an official upgrade guide. Our deliberate `~> 6.0` pin is fine today but is now one major behind. *Impact: a 6.x→7.x upgrade evaluation belongs on my backlog; no JD change.* Sources: [Terraform Registry — google provider](https://registry.terraform.io/providers/hashicorp/google/latest), [7.0 upgrade guide](https://registry.terraform.io/providers/hashicorp/google/latest/docs/guides/version_7_upgrade), [HashiCorp blog — 7.0 GA](https://www.hashicorp.com/en/blog/terraform-provider-for-google-cloud-7-0-is-now-ga), [InfoQ](https://www.infoq.com/news/2025/10/terraform-google-provider-7-ga/).
- **R3 finding 2 — Direct IAP-on-Cloud-Run is GA** (no load balancer required, no added cost). *Impact: input for Peter's successor auth ADR (issue #73) — removes the load-balancer cost objection if IAP-plus-federated-identity is ever evaluated; does not invalidate ADR-022's multi-IdP reasoning. Also: my JD's Infra-Ready Note Template hardcodes the load-balancer-style IAP audience format (`/projects/…/backendServices/…`), which the direct integration does not use.* Sources: [Google Cloud blog — IAP integration with Cloud Run](https://cloud.google.com/blog/products/serverless/iap-integration-with-cloud-run), [Cloud Run docs — configure IAP](https://cloud.google.com/run/docs/securing/identity-aware-proxy-cloud-run?hl=en), [IAP docs — enabling for Cloud Run](https://docs.cloud.google.com/iap/docs/enabling-cloud-run).

## 3. Where my current JD is now incorrect

1. **"Does not write Terraform (future scope)"** — contradicts ADR-020, which makes Terraform the only way infrastructure gets defined and names `terraform state` operations as mine. My JD currently forbids the exact work the accepted architecture requires of me.
2. **File Authority `infra/`** — path no longer exists; everything moved to `deploy/infra/` (commit `09d6d8f`). My Dockerfile authority also has no current path (`deploy/docker/` is unlisted).
3. **Outcome 2 (IAP gates the web surface)** — contradicts ADR-022: public ingress is the approved state, IAP is deferred, and the Google-only scope constraint in my JD is inverted by the recorded Google+Microsoft requirement.
4. **Outcome 7 / Hard Constraint 1 (manual-steps-to-terraform log as primary mechanism)** — superseded in spirit by ADR-020: drift is now rejected by `terraform plan`, and the audit trail is the PR diff; the log shrinks to genuine exceptions plus the two bootstrap resources.
5. **Skills table** — no Terraform skill exists; ADR-020 makes that my largest skill gap.

## 4. Validation of the facilitator's draft JD patch (`docs/people/drafts/agents/brent.agent.md`)

| Patch | Verdict | Notes |
|---|---|---|
| 1 — Terraform authorship | **Confirm, one amendment** | Matches ADR-020 verbatim (ownership, bootstrap exceptions, state ops, `gcloud` reservation, tfvars SSOT). **Amend:** change "Provider version pinning in `versions.tf` is current" to "…is **maintained**" (ADR-020's wording). "Current" is ambiguous — provider 7.x is GA while we deliberately pin `~> 6.0`; "maintained" states the real obligation without implying latest-major chasing. |
| 2 — Outcome 7 reframe + HC1 amendment | **Confirm** | Matches ADR-020 decisions 4 and rationale 1 (CC8.1 via PR plan diff). Exception path with rollback entry and Peter review preserved. |
| 3 — File Authority paths | **Confirm** | Both rows verified on disk; `deploy/docker/marker/Dockerfile` matches ADR-022 item 7. |
| 4 — Outcome 2 (SSO) + HC15 conditional | **Confirm, one addition suggested** | Matches ADR-022 item 8 and Out-of-Scope. **Suggested addition (same patch):** mark the IAP-specific fields in my Infra-Ready Note Template (audience string, JWKS endpoint, IAP-protected routes) as "conditional — only when IAP is deployed", for internal consistency; note the audience format is load-balancer-specific and stale per R3 finding 2. |
| 5 — Skill 17 (Terraform) | **Confirm** | Grounding exists: my `devops-infrastructure` notebook contains Terraform IaC on GCP (Wang). |
| 6 — tfvars SSOT discipline | **Confirm** | Matches ADR-020 Structure section and ADR-001. |
| Items intentionally not patched | **Confirm all four** | I second the ADR-022 currency question for Peter: ADR-022's Out-of-Scope says "single environment now; no Secret Manager entries needed" while merged spec-70 shipped staging+prod **with** Secret Manager — and my own Hard Constraint 7 (environment separation from day one) sides with spec-70, not ADR-022. The stale document is ADR-022, not the JD or the spec. |

**Net verdict: I validate the patch for promotion** with the two wording amendments above (Patch 1 "maintained"; Patch 4 template-field conditionality). Neither amendment blocks promotion if Harriet prefers to land them as a follow-up.

## 5. Frameworks or guidelines to add or update

- **Add Skill 17 (Terraform IaC authoring and state operations)** — highest-priority skill gap; ground from my DevOps & GCP Infrastructure notebook plus HashiCorp documentation. Include plan/apply discipline, state surgery (`import`/`mv`/`rm`), provider-pinning maintenance, and a 6.x→7.x upgrade-evaluation checklist (breaking changes documented in the official upgrade guide).
- **Update Skill 5 (Cloud IAP and OAuth wiring)** before issue #73 work begins: the direct IAP-on-Cloud-Run GA changes the wiring model (no load balancer, different audience handling) versus what my JD template assumes.
- **No change** to my SOC 2, cost-control, or observability outcomes — ADR-020 strengthens the CC8.1 evidence story at zero marginal effort (PR plan diffs).

---

## Evidence & gaps footer

- **R1 (repo docs scan): COMPLETE.** Read `docs/product/strategy/strategic-bets.md`; all four ADRs created since 2026-06-07 (ADR-019, ADR-020, ADR-021, ADR-022); specs merged in window (spec-005 GCP baseline, spec-006 infra ADR, spec-70 Cloud Run staging/prod + Secret Manager); my JD `.claude/agents/brent.md`; the draft patch `docs/people/drafts/agents/brent.agent.md`; commit `09d6d8f` and the live `deploy/infra/` tree.
- **R2 (knowledge base query): NOT COMPLETED — environment gap.** No NotebookLM access exists in this session (the Code Context Engine MCP tools are deferred behind a ToolSearch capability this subagent does not have, and no NotebookLM tool is exposed). I identified my two owned notebooks from `.agents/skills/redline-research/register.json` but could not run the two mandated queries against them. The verbatim-output requirement is unmet; nothing was fabricated in its place. Follow-up: run the two R2 queries against `devops-infrastructure` and `gcp-devops-tactical-playbook` at the next session with notebook access.
- **R3 (online currency check): COMPLETE (two targeted checks).** Terraform Google provider currency and Cloud Run IAP state — sources linked inline in section 2. The notebook-first routing hook could not be satisfied for the same reason as R2; both questions were vendor version-currency checks unanswerable by static book corpora. Plan-file hygiene check: `tfplan.*` artifacts are not tracked in git (local only — no issue).
- **CCE `session_recall`: NOT EXECUTED** — same tool-loading gap as R2; prior-decision context came from the SubagentStart hook injection instead.
