# Red Team Findings — RT-159-django-project-skeleton-2026-06-12

| | |
|---|---|
| **Session ID** | RT-159-django-project-skeleton-2026-06-12 |
| **Target** | `specs/159-django-project-skeleton/spec.md` |
| **Date** | 2026-06-12 |
| **Maintainer** | Founder (Harel Lustiger) |
| **Lenses** | API Contract Adversary (sev-weight 7), Infrastructure Security Adversary (sev-weight 8) |
| **Selection method** | trigger-matched (`contracts` genuine; `regulatory_path`/`immutability_audit` hits judged incidental per §3.3) — **weak-diversity warning**: 2 lenses < 3-lens floor; proceeded on founder request; remaining catalog lenses attack LLM/geotechnical/money surfaces absent from this slice |
| **Supporting context** | plan.md, tasks.md, research.md, quickstart.md, contracts/, ADR-024, `tasks/run-app.ps1`, `deploy/docker/marker/Dockerfile`, pyproject.toml |
| **Grounding** | NotebookLM `django-application-development` (rebuilt 2026-06-12, Django 5.2-pinned) — 5 notebook queries across both adversaries |
| **Wall-clock** | ~6.5 min (parallel dispatch; lens A 5:05, lens B 6:23) |
| **Prior sessions** | None (before_plan gate was waived [red-team-skipped] on 2026-06-12; this session discharges that waiver) |

## 1. Session Summary

*(Maintainer to fill post-review.)*

Counts: 0 CRITICAL / 4 HIGH / 5 MEDIUM / 1 LOW. Dominant theme: the slice's own
done-when ("plain `manage.py check` clean") is structurally blind to the
deploy-blocking and security-relevant defaults the skeleton ships (ALLOWED_HOSTS,
DEBUG, SECRET_KEY), and the launcher/probe tooling around it fails open rather than
closed. Most fixes land as handoff amendments to #161/#177/#178, not changes to this
slice's code.

## 2. Findings

### Lens: API Contract Adversary

| ID | Sev | Location | Finding | Suggested resolution |
|---|---|---|---|---|
| F-001 | HIGH | FR-002 / FR-007 / contracts/health-endpoint.md | Plain `check` (the spec's regression tripwire) skips the deploy/security check class entirely. The exact change #161 owns (DEBUG=False) combined with the startproject `ALLOWED_HOSTS = []` makes EVERY request — including the Cloud Run probe and all real traffic — return 400, while `check` stays green: silent false-pass on valid input. No task owns ALLOWED_HOSTS validation before #177; the health contract never states its Host-header precondition. *(Notebook: deploy-only IDs security.W004/W008/W009/W012/W016; "If DEBUG is False ... failing to set ALLOWED_HOSTS will result in all requests being returned as Bad Request (400)".)* | State in the #161 handoff that plain `check` does not cover deploy checks; make `check --deploy` clean (or explicit ALLOWED_HOSTS validation) part of #161's done-when; add a Host/ALLOWED_HOSTS precondition row to the health contract. |
| F-002 | HIGH | FR-008 / SC-005 / `tasks/run-app.ps1` | The launcher fails open twice: (a) `Wait-ForHealth` failure produces `Write-Warning` and the script still exits 0, so any caller reading the exit code treats a dead server as a successful launch; (b) the port guard filters `Get-NetTCPConnection -LocalAddress 127.0.0.1`, so a foreign process bound to the wildcard address (`0.0.0.0:8766` — a valid bind) bypasses the guard; runserver then fails to bind in its detached window, and a foreign 200-responder would be reported as "ready". | FR-008 + script: non-zero exit when any health poll fails; port guard must count wildcard (0.0.0.0/::) listeners as occupying the port; optionally assert the responder PID is the spawned process. |
| F-003 | MEDIUM | contracts/health-endpoint.md (Redirect + Consumers) | The contract tells callers to "follow redirects", but its named consumer — Cloud Run startup probes — does not follow redirects; it counts any 2xx/3xx as success. A probe configured as `/health` (the no-slash form the sibling marker app uses on the adjacent line of run-app.ps1) passes via the APPEND_SLASH 301 without ever executing the health view — a 500ing view still probes healthy. The redirect also silently depends on CommonMiddleware presence/order, which #161/#176 may alter; the docs do not even guarantee the specific 301 code. *(Notebook: APPEND_SLASH issues "an HTTP redirect" only when CommonMiddleware is installed and the slashless URL matches no pattern.)* | Pin the probe path to the literal `/health/` in the Cloud Run consumer row (forbid the no-slash form for probes); note the CommonMiddleware/APPEND_SLASH dependency so #161/#176 own preserving it. |
| F-004 | MEDIUM | contracts/root-page.md ("Out of contract": 405/404 claim) | The stated error contract is factually wrong for the designed implementation: Django's URLconf routes ALL methods to the same function view (T012 has no decorators), so POST `/` returns 403 via CsrfViewMiddleware — not 405 — and PUT/DELETE return the 200 placeholder. Anything written against the documented 405 expectation (e.g. #171's replacement tests, scanner baselines) encodes behaviour the skeleton never had. *(Notebook: "The URLconf doesn't look at the request method ... all request methods will be routed to the same function"; CSRF middleware rejects token-less POST with 403.)* | Either correct the contract row to real defaults (all methods execute; POST → 403 CSRF) or add `@require_GET` to the root view so the documented 405 becomes true (recommended — one decorator). |
| F-005 | MEDIUM | spec Assumptions / research.md D3 / plan pytest wiring | `manage.py`/`asgi.py`/`wsgi.py` use `os.environ.setdefault(...)` and pytest-django gives the environment variable precedence over the pyproject ini value — so the whole verification chain implicitly assumes `DJANGO_SETTINGS_MODULE` is unset in every shell and CI runner, and nobody validates that. A developer with the variable inherited from another Django project silently boots, checks, and tests against foreign settings with no error. | Record the assumption; have run-app.ps1 (or quickstart) warn/fail when `DJANGO_SETTINGS_MODULE` is set to anything other than `web.settings`. |

### Lens: Infrastructure Security Adversary

| ID | Sev | Location | Finding | Suggested resolution |
|---|---|---|---|---|
| F-006 | HIGH | plan Constitution XVI Accepted Risk / tasks T006 / quickstart | The recorded insecure-baseline inventory is incomplete: it names SECRET_KEY and DEBUG=True but omits the third deploy-blocking default, `ALLOWED_HOSTS = []`. The sanctioned deploy-before-#161 path (#177) cannot serve a single request at the `*.run.app` hostname without an unplanned settings edit — and under Wednesday-tripwire pressure the path of least resistance is `ALLOWED_HOSTS = ['*']`, which disables Host-header-attack protection and, absent from every risk record, would persist unexamined into #161 and production. *(Notebook: empty list + DEBUG=True validates only localhost variants; DEBUG=False + empty list 400s everything; `'*'` shifts Host validation onto you.)* | Add ALLOWED_HOSTS to the XVI Accepted Risk inventory and the #161 handoff: env-sourced, per-environment explicit hostnames, `'*'` expressly forbidden; note in the deploy-order risk that #177 requires this value before any request succeeds. *(Cross-ref F-001.)* |
| F-007 | HIGH | plan "Deploy-order risk" | The accepted DEBUG=True staging window is conditioned entirely on the founder-IP ingress lock (#178), but nothing makes #178 a blocking precondition of #177 (SC-004 lists #177 as startable off this skeleton), and no artifact pins the Cloud Run ingress setting — the platform default is all-ingress on a public `*.run.app` URL. In that gap, every uncaught exception serves the DEBUG page (settings dump with only keyword-masked values, paths, tracebacks) to anyone — and the kept `/admin/` route is the trivially scannable trigger, since admin login POST with no database raises an exception under DEBUG=True. *(Notebook: DEBUG error page discloses traceback, environment metadata, and all settings with partial masking; "Never deploy a site into production with DEBUG turned on".)* | Make #178 (or an equivalent ingress restriction / IAM-gated invoker) a hard sequencing gate before #177 ships this skeleton; add to #177 acceptance: an unauthenticated request from a non-founder IP to the run.app URL must fail. Escalate to Brent + sprint plan. |
| F-008 | MEDIUM | plan XVI Accepted Risk / research D3 / Dockerfile precedent | The committed `django-insecure-...` SECRET_KEY is permanently burned: it lives in git history and, via the established `COPY src/` Dockerfile pattern, will be baked into every Artifact Registry image built during the window — readable by any principal with registry read access. SECRET_KEY signs sessions/CSRF/reset tokens, so possession enables forgery once #165 adds users. No record requires staging and production keys to be distinct from each other and from the committed value — "copy the working key into Secret Manager" is an unblocked failure path. | Record the committed key as burned in the risk note; add to #161 acceptance: per-environment keys generated independently, sourced from Secret Manager, asserted unequal to the committed value. |
| F-009 | MEDIUM | spec US2/FR-002 + run-app gate pattern | The slice institutionalises plain `check` as THE machine gate (tests, launcher, and — by pattern inheritance — #177's deploy pipeline), but plain `check` passes the fully insecure baseline; only `check --deploy` raises security.W004/W008/W009/W012/W016 (HSTS, SSL redirect, key strength, secure cookies). The security check class is structurally absent from the pipeline with nothing assigning it to any task. | One-line handoff note: deploy-time reuse of the check gate (#177) must run `manage.py check --deploy --fail-level WARNING` against production settings, expected clean as part of #161 acceptance. *(Cross-ref F-001/F-006.)* |
| F-010 | LOW | contracts/root-page.md vs FR-007/health-endpoint.md | The contract set contradicts itself on the unauthenticated-surface inventory: root-page.md says "No health endpoint is added or moved" while FR-007 + health-endpoint.md ship exactly that. A #177-time security review of "what unauthenticated endpoints exist" gets two conflicting records. | Fix root-page.md to reference health-endpoint.md as the only other unauthenticated endpoint, making contracts/ the single accurate surface inventory. |

### Aggregator consistency notes (out-of-band, not lens findings)

- N-1: spec Edge Cases still says "Both dev servers default to the same local port" — stale against FR-008's fixed-port convention (8765/8766). *(Fixed this session on founder instruction — see Resolutions.)*
- N-2: tasks.md T014 manual check still targets `http://127.0.0.1:8000/` — contradicts FR-008's "never 8000". *(Fixed this session on founder instruction.)*
- N-3 (cosmetic): tasks.md phase/ID ordering — Phase Z carries T016–T018 while later-executing Phases 3–4 carry T019–T024.

## 3. Resolutions Log

Status values: `proposed` (awaiting maintainer), `applied`, `accepted-risk`, `new-OQ`, `out-of-scope`.

Categorisation completed 2026-06-12 by joint Brent + Peter review, founder-approved.
Draft-artifact edits were applied with founder authorisation (all specs/159 artifacts
are uncommitted working drafts, not yet historical records).

- **F-001** — status: **applied (contract) / backlog-pending (gh)** — Host precondition row added to health-endpoint.md; #161 done-when amendment drafted below, awaiting founder approval before any `gh` edit.
- **F-002** — status: **applied** — `tasks/run-app.ps1` fail-closed: `-LocalAddress` filter dropped (wildcard binds now trip the guard), exit 1 on any failed health poll; FR-008 wording updated to match ("exit non-zero", wildcard rule). Severity: Brent HIGH / Peter MEDIUM — disposition identical, recorded as agreed FIX-NOW.
- **F-003** — status: **applied (contract) / backlog-pending (gh)** — Probe path rule added to health-endpoint.md (literal `/health/` binding on #177; redirect non-contractual). Brent: the no-slash probe is LIVE config today (`cloud_run.tf:51`); path changes in the same slice that swaps the image.
- **F-004** — status: **applied (amended)** — adversary's `@require_GET` suggestion REJECTED by Peter (CSRF middleware 403s unsafe methods before the view; the decorator would also 405 HEAD probes): contract text corrected instead — non-GET is framework default and explicitly out of contract; #171 writes its own method contract.
- **F-005** — status: **applied** — severity adjusted MEDIUM → LOW (joint review). `--ds=web.settings` added to T007 addopts; `DJANGO_SETTINGS_MODULE` guard added to run-app.ps1.
- **F-006** — status: **applied (plan) / backlog-pending (gh)** — ALLOWED_HOSTS added to plan XVI Accepted-Risk inventory and the deploy-order risk amendment; #161/#177 text drafted below. Probe-Host unknown RESOLVED (Brent, staging log test 2026-06-12): probes never reach Cloud Run's front door (link-local connect from `169.254.169.126`, no request-log entry, no front-end Host guarantee) and the default probe Host is undocumented — if it is not a localhost variant, the startproject baseline 400s the probe and **the deploy itself fails** (Cloud Run refuses to shift traffic). Mitigation makes the unknown moot: Terraform `startup_probe` pins an explicit Host via `httpHeaders` matching ALLOWED_HOSTS (one block in `cloud_run.tf`, folded into the #177 draft below).
- **F-007** — status: **agreed / backlog-pending (gh)** — joint position: #178 does NOT block #177; instead #177's acceptance gains the interim IAM gate (revoke the existing `allUsers` invoker grant — staging is explicitly public today per `cloud_run.tf:64-70` — the moment the Django image deploys; tripwire verified via `gcloud run services proxy`). Recorded in plan deploy-order risk. #178's mechanism itself needs Brent's options table (Cloud Run ingress cannot IP-filter natively; Cloud Armor ~USD 20+/mo vs app-level middleware).
- **F-008** — status: **agreed / backlog-pending (gh)** — lands in #161 (not #170, which stays OAuth-scoped); Brent provisions per-env SECRET_KEY Secret Manager entries under #161's window. Registry readers today: founder, CI service account, Cloud Run service agent.
- **F-009** — status: **agreed (amended) / backlog-pending (gh)** — Peter's scope-split adopted: #161 resolves only the DEBUG/SECRET_KEY/ALLOWED_HOSTS deploy warnings; remaining `--deploy` warnings each resolved or explicitly risk-accepted; the gate becomes blocking in #177's pipeline (Brent owns the workflow line).
- **F-010** — status: **applied** — root-page.md now references health-endpoint.md (complete unauthenticated-surface inventory); same pass fixed the stale `-App django` references in plan.md and the health contract consumer row (contradicted FR-008's no-parameters rule).
- **N-1 / N-2** — status: **applied** — consistency alignment with the founder's own port-convention edits (spec Edge Case line; tasks T014 port).
- **N-3** — status: **ignored** — unanimous: phase headers govern execution order; renumbering breaks this report's own T-ID citations for zero gain.

### Proposed Handoff Text (for #161, founder to apply)

> Additional done-when (from RT-159 session, 2026-06-12; amended per Peter's scope
> review): settings are env-only AND
> (a) `ALLOWED_HOSTS` env-sourced, explicit per environment, `'*'` forbidden;
> (b) per-environment `SECRET_KEY`s generated independently, sourced from Secret
> Manager, asserted unequal to the committed `django-insecure-` value (that key is
> burned — git history + container images);
> (c) the `check --deploy` warnings for DEBUG, SECRET_KEY, and ALLOWED_HOSTS are
> resolved in this task; every remaining `--deploy` warning is either resolved or
> explicitly risk-accepted with rationale (the full gate becomes blocking in #177's
> deploy pipeline, not here).

### Proposed acceptance addition (for #177, founder to apply)

> Additional acceptance (from RT-159 session + Brent/Peter review, 2026-06-12):
>
> (a) Deploy-time `ALLOWED_HOSTS` env value set to the service's `*.run.app`
> hostname — without it the skeleton 400s every request; `'*'` is forbidden
> (durable env-sourced fix is #161's).
>
> (b) Terraform `startup_probe`: path is the literal `/health/` (no-slash form
> forbidden — probes treat the 301 as success without executing the view) AND an
> explicit Host header via `httpHeaders` matching an `ALLOWED_HOSTS` entry — the
> probe bypasses Cloud Run's front door and its default Host is undocumented;
> without the pin the deploy can fail at the probe itself (measured 2026-06-12).
>
> (c) The existing `allUsers` invoker grant (staging is explicitly public today,
> `cloud_run.tf`) is revoked in the same change that deploys the Django image;
> tripwire verified via authenticated request (`gcloud run services proxy`). An
> unauthenticated request to the run.app URL must fail. #178 is NOT a blocker —
> this IAM gate is the interim control.
>
> (d) Deploy pipeline gate: `manage.py check --deploy --fail-level WARNING`,
> blocking; expected clean once #161 lands (until then its DEBUG/SECRET_KEY/
> ALLOWED_HOSTS warnings are the known, risk-accepted set).

## 5. Session metadata

```yaml
session_id: RT-159-django-project-skeleton-2026-06-12
target: specs/159-django-project-skeleton/spec.md
date: 2026-06-12
lenses:
  - name: API Contract Adversary
    findings: 5
    dropped: 0
    duration_s: 305
  - name: Infrastructure Security Adversary
    findings: 5
    dropped: 0
    duration_s: 383
selection_method: auto (trigger-matched, contracts; weak-diversity warning recorded)
lens_failures: []
grounding: nlm notebook 9cee3997-fdbb-49cd-ab95-663bf35fcba6 (django-application-development, rebuilt 2026-06-12)
counts: {critical: 0, high: 4, medium: 5, low: 1}  # F-005 later adjusted to LOW by joint review
resolutions: {applied: 6, backlog_pending: 4, ignored_notes: 1, accepted_risk: 0, new_oq: 0}
unresolved: 0  # categorisation complete (Brent + Peter joint review, founder-approved, 2026-06-12)
backlog_pending: [F-001, F-006, F-007, F-008, F-009]  # consolidated into #161/#177 amendments awaiting founder gh approval; F-003 #177 line rides the same edit
notes: >
  Discharges the [red-team-skipped] waiver recorded in plan.md Constitution Check.
  Spec gained FR-007/FR-008/SC-005 + health contract after the original waiver,
  adding genuine contract surface — the waiver's premise (placeholder-only slice)
  no longer fully held; this session closes that gap.
```
