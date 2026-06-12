# This Week — Sprint 3: Jun 15–21

_Synced: 2026-06-12_

## Sprint 3 — Jun 15–21

**Goal**: Deploy a Django skeleton website at the company domain — IP-restricted, Google SSO login, post-login landing page, lead capture to Django DB, and a chosen analytics platform wired — proving the web deployment path is technically feasible end-to-end.

**Mid-sprint gate**: Django must be serving at any public URL by Wednesday. If not, stop and diagnose.

---

### In Progress

_Nothing in progress yet — sprint starts Mon Jun 15._

---

### Blocked

_None._

---

### To Review

_None._

---

### Done (pre-sprint)

| Agent | Title | Issue |
|-------|-------|-------|
| Brent | Infra: Cloud DNS + managed TLS cert for company domain | [#75](https://github.com/redmarklogic/redline/issues/75) |

---

### Backlog (this sprint)

Dependencies are native GitHub blocked-by links (board renders the Blocked badge); each parent carries its WBS sub-issues.

| Agent | Title | Issue | Blocked by | Sub-issues |
|-------|-------|-------|------------|------------|
| Peter | Platform P — web scaffold: project init, routing, env config | [#49](https://github.com/redmarklogic/redline/issues/49) | — | #123, #124 |
| Brent | Dockerfile + CI/CD for Django web shell | [#119](https://github.com/redmarklogic/redline/issues/119) | #49 | #125, #126, #127 (GATE) |
| Brent | Infra: HTTPS Load Balancer + Cloud Armor IP allowlist | [#74](https://github.com/redmarklogic/redline/issues/74) | #119 (+#70, #63 infra) | #128, #129, #130 |
| Peter | Platform P — SSO integration: auth provider wired, login/logout | [#50](https://github.com/redmarklogic/redline/issues/50) | #119 | #131, #132, #133 |
| Mark  | Configure and activate product analytics (KR6) | [#22](https://github.com/redmarklogic/redline/issues/22) | — | #139, #140, #141, #142 |
| Peter | Platform P — post-login page: minimal Django view after auth | [#116](https://github.com/redmarklogic/redline/issues/116) | #50 | #134, #135 |
| Mark  | Platform P — lead capture: persist user email and login events to Django DB | [#117](https://github.com/redmarklogic/redline/issues/117) | #50 | #136, #137, #138 |
| Mark  | Platform P — analytics wire: tracking script + post-login events | [#118](https://github.com/redmarklogic/redline/issues/118) | #22 | #143, #144, #145, #146 |

---

### Sequencing reminder

```text
Mon: Django scaffold (#49) immediately; OAuth consent (#131) already in flight
Wed: GATE — Django must be live at any public URL (#127)
Wed+: LB/IP (#74) and SSO (#50) unblock in parallel after gate
Wed+: Analytics research (#22) runs independently — hard stop Thu AM
Fri: Post-login (#116), lead capture (#117), analytics wire (#118)
```

---

### Key risks this sprint

| Risk | Signal to watch |
|------|-----------------|
| OAuth consent screen approval delay (24–48h) | Initiated Fri Jun 12 (#131) — confirm approved before Wed |
| #74 must reuse the reserved IP that #75's DNS already points at | Fresh IP on the LB silently invalidates the Done DNS work |
| Analytics decision stalls | Default to GA4 if no decision by Thu AM |
