# Sprint 3 Plan — Jun 15–21 2026

**Status**: Active. **Owner**: Founder.
**Generated**: 2026-06-11

---

## Sprint Goal

> Deploy a Django skeleton website at the company domain — IP-restricted, Google SSO login, post-login landing page, lead capture to Django DB, and a chosen analytics platform wired — proving the web deployment path is technically feasible end-to-end.

**Success looks like**: The founder opens the company domain in a browser, is greeted by a login screen, authenticates with a Google account, lands on a post-login page showing their email, and the login event is captured in both Django admin and an analytics platform dashboard.

**Failure looks like**: If by Wednesday Django is not serving at any public URL (not necessarily the company domain), the sprint is at risk — stop and diagnose before continuing.

**Stop rule**: If by Wednesday Django is not serving at any public URL, we stop and change course. DNS is allowed to overflow to Sprint 4 if propagation delays it — starting DNS setup is the commitment, not completing it.

**Bet**: Bet 1 — The Free Skeleton Wedge Beats Paid Acquisition
**OKR**: KR1 — Free-tier signal (leading indicator) — Sprint 3 unblocks Launch Day by proving the web deployment and SSO-gated signup path is feasible.

---

## Capacity

Last sprint completed: 14 tasks (yesterday's weather)
This sprint planning for: 9 tasks (buffer held for DNS propagation uncertainty and OAuth consent screen approval delay)

---

## Committed Tasks — WBS

| #   | Task / Sub-task | Agent | Description |
|-----|-----------------|-------|-------------|
| 1   | **DNS setup** | Brent | Register A-record pointing company domain to LB IP |
| 1.1 | — Confirm DNS provider + current records | Brent | Identify registrar, check existing records, confirm nothing breaks |
| 1.2 | — Create / update A-record | Brent | Point domain to load balancer IP |
| 1.3 | — Monitor propagation daily | Brent | Check resolution each morning; flag if not live by Thu |
| 2   | **Django scaffold** | Peter | Django web shell architecture spec — implementation agent builds |
| 2.1 | — Project structure + settings spec | Peter | Define settings split (base/dev/prod), package layout, .env contract — implementation agent builds |
| 2.2 | — Routing + health endpoint contract | Peter | URL config, `/health` contract per ADR-018 — done when `curl /health` returns 200 |
| 3   | **Dockerfile + CI/CD** | Brent | Containerise Django, extend existing GitHub Actions pipeline |
| 3.1 | — Dockerfile spec | Brent | Multi-stage image, non-root, static files via whitenoise — implementation agent builds |
| 3.2 | — CI pipeline extension | Brent | Extend GHA: build, test, push Django image to Artifact Registry — implementation agent builds |
| 3.3 | — Deploy to Cloud Run — GATE | Brent | Django live at Cloud Run URL; `curl /health` returns 200 — mid-sprint gate by Wed |
| 4   | **LB + IP allowlist** | Brent | HTTPS load balancer + Cloud Armor rule for founder's static IP |
| 4.1 | — Provision HTTPS load balancer | Brent | Terraform: LB, Google-managed SSL cert, backend to Cloud Run |
| 4.2 | — Cloud Armor IP allowlist | Brent | Default-deny policy; allow founder's static IP only |
| 4.3 | — Test restriction | Brent | Done when domain unreachable from non-whitelisted IP |
| 5   | **Google SSO** | Peter | Auth boundary spec (Django web shell layer) |
| 5.1 | — OAuth credentials provisioning | Brent | OAuth consent screen, client ID/secret, callback URL — Brent provisions in GCP |
| 5.2 | — django-allauth architecture spec | Peter | Auth boundary: session config, login/logout URLs, allauth settings contract — implementation agent builds |
| 5.3 | — End-to-end login test | Peter | Done when real Google account logs in at company domain and lands on post-login page |
| 6   | **Post-login page** | Mark | Product brief: what the user sees after login — implementation agent builds |
| 6.1 | — Post-login UX brief | Mark | What does the user see? What is the one action available? |
| 6.2 | — Django view + template spec | Peter | Web shell spec: route + view contract — done when logged-in user sees page with their email shown |
| 7   | **Lead capture** | Mark | Define what data to capture and why — Peter specs model, implementation agent builds |
| 7.1 | — Define fields to capture | Mark | Product decision: which fields serve the bet — email, name, first_login, last_login, login_count |
| 7.2 | — Platform state schema spec | Peter | UserProfile model + `user_logged_in` signal contract per Mark's field spec — implementation agent builds |
| 7.3 | — Verify captured data | Mark | Done when founder sees correct fields in Django admin after a test login |
| 8   | **Analytics research** | Mark | Evaluate PostHog, GA4, Plausible; produce one-page decision |
| 8.1 | — Define evaluation criteria | Ron | Which data decisions does this bet require? Criteria grounded in active bets |
| 8.2 | — Source platform documentation | Linda | Pull free-tier specs, integration docs, data residency info for shortlist |
| 8.3 | — Evaluate + recommend | Mark | Score options against Ron's criteria; Principal Engineer checks integration feasibility |
| 8.4 | — Document decision | Mark | Platform chosen, reason, integration method — hard stop Thu AM |
| 9   | **Analytics wire** | Mark | Define events to track — DevOps agent advises on script delivery, implementation agent wires |
| 9.1 | — Define events to track | Mark | Which UI interactions matter for bet decisions? Name each event explicitly |
| 9.2 | — Script delivery method | Brent | How does the tracking script load in Django templates? Tag or middleware? |
| 9.3 | — Web shell injection spec | Peter | Base template injection + event call contract — implementation agent builds |
| 9.4 | — Verify in dashboard | Mark | Done when founder sees named events in analytics platform after test login |

---

## Sequencing

```
          Mon                  Tue                  Wed                  Thu                  Fri
──────────────────────────────────────────────────────────────────────────────────────────────────────
  1       [(1) DNS setup] ──────────────────────── (propagating) ──────────────────────────────────

  2       [(2) Django scaffold] ── [(3) Dockerfile + CI] ── [GATE: live at public URL]

  3                                                                │
                                                                   └──── [(4) LB + IP allowlist]

  4                                                                └──── [(5) Wire SSO] ────────── [(5.3) Test login]

  5                                                                                                  [(6) Post-login page]

  6                                                                                                  [(7) Lead capture]

  7                                                           [(8) Analytics research] ───────────── [(9) Wire tags]
```

**Dependency order**:
- Task 2 (Django scaffold) → Task 3 (Dockerfile + CI) → GATE (Wed: Django live at public URL)
- GATE unblocks: Task 4 (LB + IP allowlist) and Task 5 (Google SSO) in parallel
- Task 5 unblocks: Task 6 (post-login page) and Task 7 (lead capture)
- Task 8 (analytics research) runs independently from Wed; must complete by Thu AM to unblock Task 9
- Task 1 (DNS) runs all week independently; allowed to overflow to Sprint 4

---

## Explicitly Out of Scope

| Task | Deferred to | Reason |
|------|-------------|--------|
| API health indicator on post-login page | Sprint 4+ | Keeps API and website decoupled; not needed to prove the web path |
| Real website content / marketing copy | Sprint 4+ | Skeleton sprint — scaffold only; content comes after infrastructure is proven |
| IAP (Identity-Aware Proxy) replacing IP restriction | Sprint 4+ | IP restriction is the walking-skeleton access control; IAP is the production upgrade |
| Quota enforcement on the Django web shell | Sprint 4+ | Requires platform state layer to be built out; not needed for this proof |
| Full analytics instrumentation (all 13 events) | Sprint 4+ | Sprint 3 wires basic post-login events only; full instrumentation follows |

---

## Sprint Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Google OAuth consent screen requires manual approval (24–48h wait) | High | High | Start OAuth credentials provisioning Mon AM; do not wait for Django to be live first |
| DNS propagation takes 48h, blocking happy-path test until Fri | High | Med | DNS is not a sprint gate — happy-path test uses Cloud Run URL directly until DNS resolves |
| Django static file serving on Cloud Run is non-trivial (no prior art in codebase) | Med | High | Peter specs whitenoise approach before Brent writes Dockerfile; spike if needed |
| Analytics platform research expands without timebox | Med | Med | Hard stop Thu AM; default to GA4 if no decision by then |
| IP restriction misconfiguration blocks founder's own IP on first test | Low | Med | Test from non-whitelisted IP first; verify founder IP is correctly allowlisted before declaring done |

---

## Kickoff Checklist

- [x] Sprint goal confirmed with founder
- [x] Stop rule confirmed: if by Wed Django is not serving at any public URL, stop and diagnose
- [ ] **[BLOCKING]** All committed tasks verified as board items (non-null `item_id` in `list_tasks()` output)
- [ ] **[BLOCKING]** Sprint field set on every committed board item — count confirmed
- [ ] **[BLOCKING]** `depends_on` populated on board for tasks with predecessors
- [ ] `blocked_by` populated for any task in Blocked status
- [ ] this-week.md regenerated
- [ ] DNS setup started Mon AM
- [ ] OAuth credentials provisioning started Mon AM (do not wait for Wed gate)
- [ ] Analytics research timeboxed: hard stop Thu AM
