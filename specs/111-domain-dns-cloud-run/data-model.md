# Data Model: api.redmarklogic.com Domain Connection

No application data model — no Pydantic/Pandera models, no `src/` changes. The
"entities" of this feature are infrastructure objects and their states, listed here so
tasks and verification can reference them unambiguously.

## Infrastructure entities

| Entity | Declared in | Key attributes | States that matter |
|--------|------------|----------------|--------------------|
| Firebase project link | `firebase_hosting.tf` (`google_firebase_project`) | project = redmarklogic-prod | enabled |
| Hosting site | `firebase_hosting.tf` (`google_firebase_hosting_site`) | site_id = redmarklogic-api | exists |
| Custom domain | `firebase_hosting.tf` (`google_firebase_hosting_custom_domain`) | domain = api.redmarklogic.com; `required_dns_updates` output (authoritative record list); cert state | PENDING -> CERT_ACTIVE (target); allow 24 h |
| Rewrite release | `firebase_hosting.tf` (`hosting_version`/`_release`) or CI fallback | source `**` -> run.serviceId = prod-redline-api, region = australia-southeast1 | live |
| Ownership TXT record | `cloudflare_dns.tf` | name `api`, value from `required_dns_updates`, proxied = false | resolvable |
| A record(s) | `cloudflare_dns.tf` | name `api`, value from `required_dns_updates`, proxied = false | resolvable, grey |
| Zone snapshot (evidence) | `docs/infrastructure/zone-snapshot-pre-<date>.txt` | BIND export, pre-change | immutable evidence; post-change diff must be additive-only |
| Cloudflare API token | Secret Manager (creation is a documented manual exception) | scope Zone:DNS:Edit + Zone:Zone:Read, redmarklogic.com only | never in repo |

## Invariants (validation rules)

1. Every Cloudflare record this feature creates has `proxied = false` (grey cloud is
   load-bearing — cert issuance/renewal).
2. Post-change zone export minus pre-change snapshot contains only `api.*` additions;
   MX and all other pre-existing lines byte-identical (FR-004).
3. Cloud Run service keeps `ingress = all` and unauthenticated invoke (D7) — the
   rewrite breaks otherwise.
4. `public/` directory in the Hosting config stays empty — a static file would shadow
   the rewrite for its path.
5. DNS record values come from `required_dns_updates` output, never hard-coded from
   documentation pages.

## State transitions (cutover)

```text
[no records] --Phase 1 apply--> [TXT + A live, cert PENDING]
            --cert issuance (<=24 h)--> [CERT_ACTIVE, rewrite live]
            --Phase 2 (needs #110 service)--> [branded URL serves backend 200]
```
