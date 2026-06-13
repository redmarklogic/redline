# This Week — Sprint 3 (Jun 15–21, 2026)

_Synced: 2026-06-13_

**Goal**: Deploy the first Django app to staging Cloud Run and prove the SSO-gated signal loop — Google + Microsoft sign-in, 3 auth-gated buttons, click events captured and viewable.
**Tripwire**: "If by Wednesday we have not seen the Django app running in the cloud, we will change course."
**Bet**: Bet 1 (Free Skeleton Wedge) → KR1 (signups). Full plan: `docs/product/tasks/sprint-3-goal.md`.

> All work runs on **staging** (`run.app`, IP-restricted to founder). DNS + prod gates are Sprint 4.

## Done (pre-sprint)

| Issue | Task | Note |
|---|---|---|
| #159 | Django project skeleton | Merged. Unblocks #160, #161, #162, #177. |
| #71 | Lock Cloud Run ingress to founder static IP | Done. Superseded by #178 for staging specifically. |
| #75 | Infra: Cloud DNS + managed TLS cert | Done. Superseded by #111. DNS lives at Cloudflare, not GCP. |

## Backlog — committed this sprint (by parent)

- **#153 Django web shell scaffold** — #160 layer-guard · #161 settings · #162 HTMX
- **#154 Platform-state data layer** — #163 staging Cloud SQL · #164 DATABASES+migrate · #165 models · #166 audit-log
- **#155 Launch sign-in (allauth)** — #167 Google · #168 Microsoft · #169 session-establish · ⚠️ _#170 OAuth secrets: no Sprint 3 tag — board gap, fix before Monday_
- **#156 Auth-gated buttons + events** — #171 gated page · #172 click→capture · #173 team viewer
- **#157 Analytics platform** — #174 spike (★Day 1) · #175 wire _(cut line)_
- **#158 CI/CD + Cloud Run + IP lock** — #177 deploy-on-merge (★Wed tripwire) · #178 IP lock

## Cut line (yield first if the week tightens)

1. #175 external analytics wiring → 2. #176 error middleware → DNS already Sprint 4.

## Board gaps (fix before Monday)

- **#170** (OAuth secrets → Secret Manager, Brent, Low risk) — no Sprint 3 iteration tag. Assign before sprint start.
- #176 (error middleware ADR-018) — no Sprint 3 tag, consistent with cut-line intent. Likely intentional.

## Watch

- **Wed tripwire**: #177 — Django live on staging `run.app`.
- **Day 1 High-risk starts**: #163 (Cloud SQL, Brent) · #174 (analytics spike) · #161 (settings, blocks #164 chain).
- **Parallel infra track**: Brent runs #163 + #177 concurrently — independent of Founder coding track.
- **Cleanup**: confirm whether #71 closure supersedes #178 (or if both are needed).
