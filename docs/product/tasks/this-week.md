# This Week — Sprint 3 (Jun 15–21, 2026)

_Synced: 2026-06-12_

**Goal**: Deploy the first Django app to staging Cloud Run and prove the SSO-gated signal loop — Google + Microsoft sign-in, 3 auth-gated buttons, click events captured and viewable.
**Tripwire**: "If by Wednesday we have not seen the Django app running in the cloud, we will change course."
**Bet**: Bet 1 (Free Skeleton Wedge) → KR1 (signups). Full plan: `docs/product/tasks/sprint-3-goal.md`.

> All work runs on **staging** (`run.app`, IP-restricted to founder). DNS + prod gates are Sprint 4.

## Start Monday (day-1, High-risk, zero prior art)

| Issue | Task | Owner |
|---|---|---|
| #159 | Django project skeleton | Peter / Kabilan impl |
| #163 | Provision staging Cloud SQL (Auth Proxy) | Brent |
| #165 | User + identity models `(provider,subject)` | Peter / Kabilan impl |
| #167 | allauth Google sign-in | Peter / Kabilan impl |
| #168 | allauth Microsoft sign-in | Peter / Kabilan impl |
| #174 | Analytics platform spike (CLI/MCP/API; pick same-day) | Peter |

## Backlog — committed this sprint (by parent)

- **#153 Django web shell scaffold** — #159 skeleton · #160 layer-guard · #161 settings · #162 HTMX
- **#154 Platform-state data layer** — #163 staging Cloud SQL · #164 DATABASES+migrate · #165 models · #166 audit-log
- **#155 Launch sign-in (allauth)** — #167 Google · #168 Microsoft · #169 session-establish · #170 OAuth secrets
- **#156 Auth-gated buttons + events** — #171 gated page · #172 click→capture · #173 team viewer
- **#157 Analytics platform** — #174 spike · #175 wire _(cut line)_
- **#158 CI/CD + Cloud Run + IP lock** — #176 error middleware _(cut line)_ · #177 deploy-on-merge (★Wed tripwire) · #178 IP lock

## Cut line (yield first if the week tightens)

1. #175 external analytics wiring (DB floor stands) → 2. #176 error middleware → DNS already Sprint 4.

## Watch

- **Wed tripwire**: #177 — Django live on staging `run.app`.
- **Parallel prod-gate**: Peter authors the Cloud SQL connection-strategy ADR (from Brent's analysis) — gates prod, not this sprint.
- **Cleanup**: close #71 (duplicate of #178).
