# This Week — Sprint 3: Jun 15–21

_Synced: 2026-06-11_

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

### Backlog (this sprint)

| Agent | Title | Issue | Depends on |
|-------|-------|-------|------------|
| Brent | Infra: Cloud DNS + managed TLS cert for company domain | [#75](https://github.com/redmarklogic/redline/issues/75) | — |
| Peter | Platform P — web scaffold: project init, routing, env config | [#49](https://github.com/redmarklogic/redline/issues/49) | — |
| Brent | Infra: HTTPS Load Balancer + Cloud Armor IP allowlist | [#74](https://github.com/redmarklogic/redline/issues/74) | #49 |
| Peter | Platform P — SSO integration: auth provider wired, login/logout | [#50](https://github.com/redmarklogic/redline/issues/50) | #49 |
| Mark  | Configure and activate product analytics (KR6) | [#22](https://github.com/redmarklogic/redline/issues/22) | — |
| Peter | Platform P — post-login page: minimal Django view after auth | [#116](https://github.com/redmarklogic/redline/issues/116) | #50 |
| Mark  | Platform P — lead capture: persist user email and login events to Django DB | [#117](https://github.com/redmarklogic/redline/issues/117) | #50, #116 |
| Mark  | Platform P — analytics wire: tracking script + post-login events | [#118](https://github.com/redmarklogic/redline/issues/118) | #116, #22 |

---

### Sequencing reminder

```text
Mon: Start DNS (#75) + Django scaffold (#49) immediately
Wed: GATE — Django must be live at any public URL
Wed+: LB/IP (#74) and SSO (#50) unblock in parallel after gate
Wed+: Analytics research (#22) runs independently — hard stop Thu AM
Fri: Post-login (#116), lead capture (#117), analytics wire (#118)
```

---

### Key risks this sprint

| Risk | Signal to watch |
|------|-----------------|
| OAuth consent screen approval delay (24–48h) | Start Mon AM — do not wait for Wed gate |
| DNS propagation (24–48h) | Not a gate — use Cloud Run URL directly until DNS resolves |
| Analytics decision stalls | Default to GA4 if no decision by Thu AM |
