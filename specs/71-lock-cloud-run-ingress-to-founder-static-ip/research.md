# Research: Lock Cloud Run Ingress to Founder Static IP

**Feature**: specs/71-lock-cloud-run-ingress-to-founder-static-ip
**Date**: 2026-06-12

---

## Q1: Does Cloud Run V2 support native IP restriction without a load balancer?

**Decision**: No — Cloud Run V2 has no IP-level access control at the service resource itself.

**Rationale**: The `google_cloud_run_v2_service` `ingress` argument accepts only three values:

- `INGRESS_TRAFFIC_ALL` — all internet traffic (current state)
- `INGRESS_TRAFFIC_INTERNAL_ONLY` — traffic from VPC or same-project services only
- `INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER` — VPC + load balancer traffic only

None of these values enforce an IP allowlist. IAM conditions on `roles/run.invoker` do not support IP-based conditions in Cloud Run V2. A network-layer IP filter requires an external component.

---

## Q2: What is the lightest Terraform approach for temporary IP restriction on Cloud Run?

Three options were evaluated:

### Option A — Cloud Armor + Serverless NEG + Global HTTPS LB (selected)

**Architecture**: Add a global HTTPS load balancer with a serverless NEG backend pointing at the Cloud Run service. Attach a Cloud Armor security policy with a single allowlist rule permitting the founder's IP and a default-deny rule.

**Resources added**:

- `google_compute_global_address` — reserve static global IP
- `google_compute_managed_ssl_certificate` — managed TLS cert for a custom domain
- `google_compute_backend_service` — backend service with Cloud Armor policy attached
- `google_compute_url_map` — URL map routing all traffic to the backend service
- `google_compute_target_https_proxy` — HTTPS proxy
- `google_compute_global_forwarding_rule` — forwarding rule (HTTPS port 443)
- `google_compute_security_policy` — Cloud Armor policy with allow/deny rules
- `google_cloud_run_v2_service` change — ingress from `INGRESS_TRAFFIC_ALL` to `INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER`

**Reverting for IAP handover**: Change `ingress` back to `INGRESS_TRAFFIC_ALL`, remove Cloud Armor policy and LB resources, or replace the Cloud Armor policy with an IAP-backed backend service. All changes are in HCL — single terraform apply.

**Cost**: ~$15–20/month (global forwarding rule ~$0.008/hr = ~$5.84/month per rule; Cloud Armor security policy ~$5/month; managed cert is free).

**Pros**: Proper GCP infrastructure layer enforcement; no direct `.run.app` URL bypass possible once ingress is changed; aligns with ADR-020; Cloud Armor policy is directly reusable for future geo-restriction or rate limiting.

**Cons**: Seven new Terraform resources for temporary scaffolding; ~$15–20/month for one sprint; requires a custom domain name for the managed cert.

### Option B — Cloudflare WAF (not selected)

**Architecture**: Add a Cloudflare proxied DNS record pointing to the Cloud Run URL. Add a Cloudflare WAF/firewall rule restricting to founder's IP.

**Why not selected**: Does not restrict access to the direct `*.run.app` URL. Anyone who discovers the Cloud Run service URL (e.g., from a `terraform output`) bypasses Cloudflare entirely. This does not satisfy FR-001 (block must be at the network layer before the application receives the request). Only viable if the `.run.app` URL is never exposed outside the team — not a reliable enforcement guarantee.

### Option C — FastAPI ASGI middleware (not selected)

**Architecture**: Add a 10-line IP check middleware to the FastAPI application. Read the allowlisted IP from an environment variable (`ALLOWED_IP_CIDR`). Return HTTP 403 for any request whose `X-Forwarded-For` or source IP does not match.

**Why not selected**: Application-code solution for a DevOps-owned issue. Violates the spec assumption that enforcement is at the GCP infrastructure layer (Assumption 5 in spec.md). Additionally, `X-Forwarded-For` can be spoofed if the service is directly reachable without a proxy — same bypass problem as Option B without ingress restriction.

---

## Q3: How is the founder's static IP supplied — variable or tfvars?

**Decision**: Terraform input variable `founder_allowed_cidr`, supplied via `terraform.tfvars` as a /32 CIDR string (e.g. `"203.0.113.45/32"`).

**Rationale**: Consistent with ADR-020 (`terraform.tfvars` is SSOT for all canonical identifiers) and ADR-001 (single source of truth). The IP is not a secret (it is an allowlisted network address, not a credential), so Secret Manager is not required. A single variable change + terraform apply updates the restriction with no code changes.

---

## Q4: Which Cloud Run environments are restricted — staging, prod, or both?

**Decision**: Prod only.

**Rationale**: `cloud_run.tf` already grants `allUsers` `roles/run.invoker` on staging for acceptance test accessibility (the walking skeleton smoke test must be reachable from CI). Restricting staging would break the acceptance test. The prod service has no `allUsers` binding — but its URL is still publicly reachable because `ingress = "INGRESS_TRAFFIC_ALL"`. The prod environment is what this feature locks down.

---

## Summary of Decisions

| Question | Decision |
|----------|----------|
| Native Cloud Run IP restriction? | Not available — requires external component OR application middleware |
| Enforcement mechanism | FastAPI middleware (Option C) — selected after cost/complexity review |
| Cloud Armor + LB rejected | $11/month, 7 new resources for one sprint of scaffolding — over-engineered |
| IP storage | `founder_allowed_ip` in `terraform.tfvars` (plain IP string); env var `FOUNDER_ALLOWED_IP` on prod Cloud Run service |
| Scope | Prod Cloud Run service only; staging and local dev unaffected (middleware opt-in via env var presence) |
| Removal path | Delete `middleware.py`, remove `add_middleware` call from `main.py`, remove Terraform env var |

**Note**: Option C (application middleware) was initially rejected in this research doc under the assumption that enforcement must be at the GCP infrastructure layer. That assumption was wrong — it was added by the spec author, not required by the issue. The founder clarified: "I don't mind people knocking as long as only I am allowed to get inside based on my IP." Application-layer enforcement satisfies this directly.
