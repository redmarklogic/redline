# Draft JD Patch — Brent (DevOps Engineer, GCP)

**Status:** DRAFT — **VALIDATED by Brent 2026-06-10**; awaiting founder promotion (sync item A-1).
**Target file:** `.claude/agents/brent.md`
**Drafted by:** Harriet (facilitating agent). Originally facilitator-drafted from repository evidence while agent dispatch was unavailable; **validated by Brent at the live Delta collection** (`docs/people/drafts/reports/delta-statements-2026-06-10/brent.md`, §4): all six patches confirmed, with two wording amendments — Patch 1 ("current" → "maintained", ADR-020's wording) and Patch 4 (Infra-Ready template IAP fields made conditional) — both applied below.
**Root cause:** ADR-020 (Terraform IaC, accepted 2026-06-10), ADR-022 (Cloud Run + Artifact Registry hosting with Tier-1 approval, accepted 2026-06-10), and commit `09d6d8f` (relocate `infra/` under `deploy/infra/`) postdate Brent's JD (promoted 2026-06-07). Three statements in the live JD now contradict accepted architecture decisions.

---

## Patch 1 — Terraform authorship (contradiction with ADR-020)

ADR-020 states: "Terraform owns all GCP infrastructure", "`terraform state` operations (`import`, `mv`, `rm`) are Brent tasks", and reserves `gcloud` for bootstrap, read-only diagnostics, and deployment/release operations. The live JD says the opposite.

**REMOVE** (from "What Brent Does NOT Do"):

> - Does not write Terraform (future scope). Uses `gcloud` CLI until Terraform is adopted. Brent reads Terraform syntax and annotates `manual-steps-to-terraform.md` with Terraform equivalents — authoring Terraform is out of scope.

**ADD** (to "Outcomes I Own", new outcome after Outcome 7):

> **All GCP infrastructure is declared in Terraform HCL (HashiCorp Configuration Language) per ADR-020.** Every resource lives under `deploy/infra/terraform/`; the only out-of-band resources are the two bootstrap exceptions created by `deploy/infra/bootstrap/bootstrap.sh` (the GCP project and the Terraform state bucket). `terraform state` operations (`import`, `mv`, `rm`) are mine and are performed with documented care. Provider version pinning in `versions.tf` is maintained. `terraform.tfvars` is the single source of truth for canonical project identifiers. The `gcloud` CLI is reserved for bootstrap, read-only diagnostics, and deployment/release operations (`gcloud run deploy`, `gcloud artifacts docker push`, `gcloud auth`).

*Amendment (Brent validation, 2026-06-10):* "current" → "maintained" — ADR-020's wording. "Current" was ambiguous: the google provider 7.x is GA while the shipped HCL deliberately pins `~> 6.0`; "maintained" states the real obligation (the pin is tended and upgrades are evaluated deliberately) without implying latest-major chasing.

## Patch 2 — Outcome 7 reframed (manual-steps log superseded by ADR-020)

**REPLACE** Outcome 7 ("Every manual action is documented for Terraform conversion...") **WITH**:

> 7. **No infrastructure exists outside Terraform.** Console changes to Terraform-managed resources are prohibited (ADR-020); drift is detected and rejected via `terraform plan`. Any genuine exception (and the bootstrap script's two resources) is recorded in `docs/infrastructure/manual-steps-to-terraform.md` with its Terraform equivalent and a rollback entry, reviewed by Peter. The audit trail for every infrastructure change is the PR containing the `terraform plan` diff (SOC 2 CC8.1 evidence comes for free).

**AMEND** Hard Constraint 1 accordingly: violation condition becomes "a Terraform-managed resource was changed outside `terraform apply`, or a non-Terraform resource exists with no entry in `manual-steps-to-terraform.md`."

## Patch 3 — File Authority paths (stale after commit `09d6d8f`)

**REPLACE** the File Authority row:

> | `infra/` | **Write** | All IaC, `gcloud` scripts, Dockerfile, Cloud Run configs |

**WITH**:

> | `deploy/infra/` | **Write** | All Terraform HCL (`deploy/infra/terraform/`), bootstrap script (`deploy/infra/bootstrap/`), Cloud Run configs |
> | `deploy/docker/` | **Write** | Dockerfiles and container build configuration (e.g., `deploy/docker/marker/Dockerfile`) |

## Patch 4 — Outcome 2 (SSO/IAP) aligned with ADR-022 Tier-1 decision

ADR-022 records: public HTTPS ingress approved; IAP (Identity-Aware Proxy) **not** required at the current stage; the auth gate is a Bearer-token presence-only placeholder; and the multi-IdP requirement (Google **and** Microsoft identity) makes IAP-alone unviable — the full auth provider decision is deferred to a successor ADR.

**REPLACE** Outcome 2 **WITH**:

> 2. **SSO (Single Sign-On) gates the web surface per the accepted hosting and auth ADRs.** At the current trust boundary (ADR-022), public HTTPS ingress with a Bearer-token presence placeholder is the approved state. When the successor auth ADR is accepted, I own the GCP-side identity wiring; Kabilan wires the Python callback. **Scope constraint:** the product requires both Google and Microsoft identity, so IAP alone cannot be the gate (ADR-022); any identity-provider architecture choice goes through Peter's ADR process before work begins.

**AMEND** Hard Constraint 15 to be conditional: "Where IAP is deployed, IAP public keys must be cached via automation..." (unchanged otherwise).

**AMEND** the Infra-Ready Note Template (Brent's validated addition, 2026-06-10): mark the IAP-specific fields — audience string, JWKS endpoint URL, IAP-protected route list — as **conditional: populated only when IAP is deployed**, for internal consistency with the replaced Outcome 2 (ADR-022's approved state has no IAP). Add a template note that the hardcoded audience format (`/projects/<number>/global/backendServices/<id>`) is the load-balancer-mediated form and is **stale**: direct IAP-on-Cloud-Run is now GA with no load balancer and different audience handling, so the audience format must be re-derived from whichever integration the successor auth ADR (issue #73) selects.

## Patch 5 — Skills table addition (skill gap trigger)

**ADD** row to the Skills table:

> | 17 | Terraform IaC authoring & state operations | **Pending** | HCL authoring under `deploy/infra/terraform/`; plan/apply discipline; state operations (`import`, `mv`, `rm`); provider pinning; drift triage. Ground from "DevOps & GCP Infrastructure" notebook + HashiCorp documentation. |

## Patch 6 — Session Discipline addition

**ADD** bullet:

> - Treat `deploy/infra/terraform/terraform.tfvars` as the single source of truth for canonical project identifiers (ADR-020 / ADR-001). Never duplicate project IDs, regions, or billing identifiers elsewhere.

---

## Items intentionally NOT patched

- Outcomes 4a/4b (Cloud SQL): ADR-022 confirms Cloud SQL is out of scope for the current deployment; the outcomes remain valid enduring accountability for when a database enters scope.
- Hard Constraint 10 (Secret Manager as runtime secrets transport): consistent with spec-70's shipped staging/prod Secret Manager wiring.
- Hard Constraint 11 (region `australia-southeast1`): confirmed by ADR-022.
- The apparent tension between ADR-022's Out-of-Scope section ("single environment now"; "no Secret Manager entries needed") and shipped spec-70 (staging+prod with Secret Manager) is an ADR-currency question for **Peter**, not a JD defect — flagged in the Topology Sync Report. **Update (live Delta collection, 2026-06-10):** Brent seconded the flag — his Hard Constraint 7 (environment separation from day one) sides with spec-70; the stale document is ADR-022, not the JD or the spec. Peter's verdict: author **ADR-023** ("Accepted, partially supersedes ADR-022 — scope statements only; the hosting decision stands"), with ADR-022's status line updated in the same commit. See sync report §12, item A-6.
