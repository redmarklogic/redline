# Feature Specification: Settings + 12-Factor Config

**Feature Branch**: `feature/161-settings-12-factor-config`

**Created**: 2026-06-13

**Status**: Draft

**Input**: GitHub issue [#161](https://github.com/redmarklogic/redline/issues/161) — "Settings + 12-factor config". Purpose: serves Bet 1 (Free Skeleton Wedge) -> KR1 SSO-gated signup. Source: `docs/product/tasks/sprint-3-goal.md` (WBS 1.3). Done when: app boots reading all config from environment variables (ADR-021); the `DEBUG=False` path boots; no secret in code.

**Governing decisions**: ADR-021 (Process Environment as Sole Config Source) fixes *how* config is read — this spec does not re-litigate it. ADR-023 (staging/prod split, Secret Manager) governs where secret values originate. ADR-024 (Django web stack) fixed the framework. This slice converts the framework-default `startproject` settings the skeleton (#159) shipped into environment-only configuration and resolves the deploy-blocking insecure defaults the #159 red-team (RT-159, 2026-06-12) flagged for this task.

**Founder scope decisions (2026-06-13)**: (1) Database configuration cleanup lands here — DATABASES moves to environment-only now and the `# hook: allow` dev-default exemptions are removed; #164 keeps only migrations and connectivity proof. (2) The transport-security `check --deploy` warnings (HSTS, SSL redirect, secure cookies) are made environment-driven but default-off for the founder-IP-locked staging window and explicitly risk-accepted; only the DEBUG / SECRET_KEY / ALLOWED_HOSTS warnings are resolved outright here.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Boot entirely from the environment (Priority: P1)

An operator (or container runtime) starts the web application in a process whose environment carries every configuration value — secret key, debug flag, allowed hostnames, database connection. The application reads each value from the environment, starts successfully with debug disabled, and contains no configuration secret or environment-specific literal in its source. This is the issue's headline done-when and the precondition for every deploy task: #177 cannot ship an image that only boots on the original author's machine.

**Why this priority**: Issue done-when ("app boots reading all config from env vars; `DEBUG=False` boots; no secret in code"). #164 (migrate), #177 (deploy), and #178 (ingress) all consume an environment-configured settings module; none can start until it exists.

**Independent Test**: In a clean process with the required environment variables set and the debug flag disabled, start the development server and request `/` — observe HTTP 200. Separately, search the settings source for the secret key, host list, debug literal, and database credentials — observe none are hard-coded.

**Acceptance Scenarios**:

1. **Given** a process whose environment supplies all required configuration values with the debug flag set to a disabled value, **When** the application starts and `/` is requested, **Then** the response is HTTP 200 and the application is running with debug disabled.
2. **Given** the settings source after this change, **When** it is inspected for configuration values, **Then** the secret key, allowed-hosts list, debug flag, and database credentials are all read from the environment — no literal secret, host, or credential remains in source.
3. **Given** the application running with debug disabled and the configured allowed hosts, **When** a request arrives whose Host header matches a configured hostname, **Then** it is served (not rejected as a Bad Request).

---

### User Story 2 - Misconfiguration fails loudly at startup (Priority: P2)

An operator starts the application with a required configuration value missing or blank. Instead of silently falling back to an insecure built-in default and appearing healthy, the application refuses to start (or refuses to adopt the insecure value) and reports which variable is missing. The failure surfaces at startup in the misconfigured environment — not later, as a silent security weakness in a process that already passed its health check.

**Why this priority**: This is the core value of ADR-021 — "misconfigured environments fail loudly at startup, not silently at runtime." A `SECRET_KEY` that silently falls back to a predictable value, or a `DEBUG` that silently defaults on, is the exact failure mode the architecture decision exists to prevent. Without fail-fast behaviour, the env-only conversion is cosmetic.

**Independent Test**: Start the application with the secret-key variable unset; observe that it does not boot into a running state using a built-in or predictable key, and that the error names the missing variable.

**Acceptance Scenarios**:

1. **Given** a process whose environment is missing a required configuration variable, **When** the application starts, **Then** it aborts with a clear error identifying the missing variable and does not serve requests.
2. **Given** a process started with no debug variable set, **When** the application initialises, **Then** it does not silently run with debug enabled — it either fails fast or adopts the secure (disabled) value, never the insecure one.
3. **Given** the source after this change, **When** the configuration reads are inspected, **Then** no read supplies a fallback default to a security-relevant variable and no `.env`-file loader is imported in application source (ADR-021 enforcement hooks pass).

---

### User Story 3 - Deploy-safety is machine-checkable (Priority: P2)

A developer or CI job runs the framework's deployment configuration check against a production-like environment and gets a clean result for the three deploy-blocking defaults the skeleton shipped (weak secret key, debug on, empty/permissive allowed hosts). Every other deployment-check warning has a recorded disposition — fixed, or explicitly risk-accepted with a written rationale — so no security warning is silently ignored. The allowed-hosts value is explicit per environment and the wildcard `'*'` is forbidden.

**Why this priority**: RT-159 finding F-001/F-006/F-009 — the plain system check (#159's regression tripwire) does not cover deploy/security checks; the deploy check class was structurally absent from the pipeline with no task owning it. This task owns it. Under Wednesday-tripwire pressure the path of least resistance is `ALLOWED_HOSTS = ['*']`, which disables Host-header protection and would persist unexamined into production; the spec forbids it.

**Independent Test**: Run the deployment configuration check against a production-like environment (debug disabled, real secret key, explicit hosts); observe zero warnings in the secret-key, debug, and allowed-hosts classes, and a documented disposition for every remaining warning.

**Acceptance Scenarios**:

1. **Given** a production-like environment, **When** the deployment configuration check runs, **Then** it reports no warnings for the secret-key, debug, and allowed-hosts checks.
2. **Given** the allowed-hosts configuration, **When** it is set to the wildcard `'*'`, **Then** this is rejected/forbidden by the project's own validation (the wildcard is not an accepted value).
3. **Given** the deployment check output, **When** any remaining warning is present (for example transport-security warnings), **Then** a written disposition exists for it — either resolved, or risk-accepted with rationale recorded in the spec/plan — and none is left undocumented.

---

### User Story 4 - Per-environment secret isolation (Priority: P3)

The secret key the application runs with differs between environments, is sourced from the platform secret store (Secret Manager) rather than committed config, and is verifiably not the burned `django-insecure-` value that lives permanently in git history and in already-built images.

**Why this priority**: RT-159 finding F-008 — the committed `django-insecure-` key signs sessions, CSRF tokens, and password-reset tokens; it is burned (git history + Artifact Registry images) and possession enables forgery once #165 adds users. "Copy the working key into Secret Manager" is an unblocked failure path with nothing asserting the keys are distinct.

**Independent Test**: Assert the secret key the application loads is not equal to the committed `django-insecure-` literal in any non-throwaway environment; confirm per-environment secret-store entries are the injection source.

**Acceptance Scenarios**:

1. **Given** any non-throwaway environment (staging, production), **When** the application loads its secret key, **Then** the value is not equal to the committed `django-insecure-` literal.
2. **Given** the staging and production environments, **When** their secret keys are compared, **Then** they are independently generated values (not the same key copied across environments), injected from the platform secret store per ADR-023.

---

### Edge Cases

- **Required variable missing or blank**: absence of a required variable (secret key, allowed hosts, a database credential) fails fast at startup with the variable named — it does not boot using a built-in default (US2).
- **Debug flag with an ambiguous value**: a debug variable set to an unrecognised string (e.g. `"Yes"`, `"1 "`, empty) resolves deterministically and never silently enables debug; the accepted true/false forms are documented.
- **`DEBUG=False` with empty allowed hosts**: with debug disabled, an empty allowed-hosts list makes every request — including the Cloud Run startup probe — return Bad Request (400) while the plain system check stays green (RT-159 F-001). The configuration must therefore require at least one explicit hostname whenever debug is disabled.
- **Local developer with no `.env`**: removing the dev-default fallbacks means a developer who has not provided the variables (via a shell-loaded or Compose-loaded `.env`) gets a fail-fast startup error, not a silently-working app on built-in defaults — the `.env` itself is never loaded by application source (ADR-021).
- **Test runs**: the test settings module must supply its own configuration without depending on a developer's environment; any test fixture that exercises environment loading uses the sanctioned `# hook: allow` escape hatch (ADR-021), not a production-path default.
- **Wildcard host shortcut**: an operator setting allowed hosts to `'*'` under deploy pressure is rejected by the project's validation (US3) rather than silently accepted.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The web application MUST read every configuration value that varies by environment — secret key, debug flag, allowed hostnames, and database connection parameters — from the process environment. No environment-specific value may remain as a literal in settings source.
- **FR-002**: Configuration reads MUST NOT supply a fallback default to a security-relevant variable, and application source MUST NOT load a `.env` file or import a dotenv loader (ADR-021). A missing required variable MUST cause a fail-fast startup error that names the variable, not a silent fallback to a built-in value. The existing ADR-021 enforcement hooks (`check-no-env-loader`, `check-no-env-defaults`) MUST pass over the changed settings with no new `# hook: allow` exemptions in non-test source.
- **FR-003**: The application MUST start successfully with the debug flag disabled (`DEBUG=False` path boots) when the remaining required variables are present, and MUST never silently run with debug enabled when the debug variable is absent or unparseable.
- **FR-004**: Allowed hostnames MUST be sourced from the environment as an explicit per-environment list. The wildcard `'*'` MUST be forbidden by the project's own configuration handling (not merely discouraged). With debug disabled, at least one explicit hostname MUST be required so the application can serve requests (including the deploy probe) rather than returning 400 to everything.
- **FR-005**: The secret key MUST be sourced from the environment (injected from the platform secret store per ADR-023). The configured value MUST be verifiably not equal to the committed `django-insecure-` literal in any non-throwaway environment, and staging and production MUST use independently generated keys.
- **FR-006**: The database connection (engine, name, user, password, host, port) MUST be sourced from the environment with no dev-default fallbacks and no `# hook: allow` exemptions remaining in settings source. This slice covers database *configuration* only; running migrations and proving connectivity remain with #164.
- **FR-007**: The deployment configuration check MUST report zero warnings for the secret-key, debug, and allowed-hosts classes when run against a production-like environment. Every other deployment-check warning MUST have a recorded disposition — resolved, or explicitly risk-accepted with a written rationale captured in this feature's artifacts. Transport-security settings (HSTS, SSL redirect, secure session/CSRF cookies) MUST be environment-driven, default-off for the staging window, and their warnings risk-accepted with rationale (per founder decision; the full check becomes a blocking pipeline gate in #177, not here).
- **FR-008**: The change MUST be additive and non-regressing: the plain system check (`manage.py check`) stays clean, the pre-existing test suites (`src/marker`, `src/web`, `src/rl`) keep passing, and the local development workflow continues to work when the required variables are provided through the documented developer mechanism.
- **FR-009**: The set of required environment variables and their non-secret example forms MUST be documented in the committed environment template (`.env.example`) so a developer or operator can see exactly which variables the application requires, with secret values left blank.

### Out of Scope (this slice)

| Concern | Owned by |
|---|---|
| Running database migrations and proving connectivity (local + staging Cloud Run) | #164 |
| Provisioning the per-environment secret-store entries (Secret Manager) | Brent (infra) within this task's window — app only reads the injected value |
| Making the deployment configuration check a blocking pipeline gate | #177 |
| Setting the deploy-time allowed-hosts value to the live `*.run.app` hostname and pinning the startup-probe Host | #177 |
| Cloud Run ingress restriction / founder-IP lock | #178 |
| OAuth client secrets in Secret Manager | #170 |
| Turning transport security (HSTS, SSL redirect, secure cookies) ON for real production traffic | Enabled/tuned at deploy (#177); this slice only makes them environment-driven and default-off |
| User / identity models that depend on the secret key for token signing | #165 |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The application boots with debug disabled while reading 100% of its environment-varying configuration (secret key, debug, allowed hosts, database parameters) from the process environment; a source inspection finds zero configuration literals (secret key, host list, debug flag, database credentials) remaining in settings.
- **SC-002**: With any one required configuration variable absent, the application fails to start with an error that names the missing variable, and in no case starts in an insecure default state (predictable key, debug on, or permissive hosts).
- **SC-003**: The deployment configuration check reports 0 warnings in the secret-key, debug, and allowed-hosts classes against a production-like environment, and every remaining deployment-check warning has a written disposition (resolved or risk-accepted with rationale) — 0 undocumented warnings.
- **SC-004**: The secret key the application loads is verifiably different from the committed `django-insecure-` literal in every non-throwaway environment, and staging and production keys are distinct from each other.
- **SC-005**: The pre-existing system check and full test suite pass at the same rate as before this change (zero new failures), and #164 and #177 can consume the environment-only settings module without restructuring it.

## Assumptions

- ADR-021 governs the read mechanism and is binding: configuration is read with a fail-fast accessor or a structured settings loader with `.env`-file loading disabled; defaults to security-relevant variables and dotenv imports are banned in application source. The choice between a raw fail-fast accessor and a structured settings loader is a plan-phase decision.
- The DEBUG variable has no implicit silent default (ADR-021): each environment sets it explicitly. Where a default is unavoidable for a non-failing boot, the secure value (disabled) is the only acceptable one — an absent debug variable must never resolve to enabled. The exact accepted true/false string forms are a plan-phase decision documented in `.env.example`.
- Secret-store provisioning (creating the per-environment `SECRET_KEY` entries in Secret Manager) is infrastructure work performed by Brent within this task's window (RT-159 F-008); this feature's application code only reads the injected environment value and asserts it is not the burned literal. The injection wiring into the deployed container is #177's concern.
- The transport-security risk-acceptance is bounded to the staging window, which is founder-IP-locked (#178) and HTTPS-terminated at Cloud Run; the settings are made environment-driven now so #177 can enable them per environment without a code change.
- `.env` files remain a developer ergonomic loaded by the shell or Compose before the process starts, never by application source (ADR-021); the committed `.env.example` documents the new Django variables alongside the existing infrastructure variables.
- The test settings module (`src/web/settings_test.py`) supplies its own configuration and may use the sanctioned `# hook: allow` escape hatch for fixtures that exercise environment loading; production settings carry no such exemption.
- Implementation is performed by Kabilan on founder instruction (issue: "Kabilan implements"); this spec/plan/tasks pipeline stops before implementation.

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Removing database dev-default fallbacks breaks the local `manage.py check` / test run when the variables are not present in the shell or Compose environment | A developer pulls the branch and the system check or tests fail at startup with a missing-variable error | Document the required variables in `.env.example`; ensure the local Compose/`.env` developer path supplies them; keep the test settings module self-sufficient (FR-008) |
| `ALLOWED_HOSTS = ['*']` is taken as the deploy-pressure shortcut, silently disabling Host-header protection into production (RT-159 F-006) | Host-header attacks become possible; an insecure value persists unexamined | Forbid the wildcard in the project's own validation (FR-004); cover with a test asserting `'*'` is rejected |
| The burned `django-insecure-` key is "promoted" into Secret Manager as the working key (RT-159 F-008) | Session/CSRF/reset-token forgery once #165 adds users | Assert the loaded key is not equal to the committed literal (FR-005); require independently generated per-environment keys |
| Plain `manage.py check` stays green while `DEBUG=False` + empty allowed hosts 400s every request including the deploy probe (RT-159 F-001) | The deploy at #177 fails at the startup probe, or all traffic is rejected, with the regression tripwire showing healthy | Require at least one explicit hostname when debug is disabled (FR-004); make the deploy check cover the allowed-hosts class (FR-007) |
| Risk-accepting the transport-security warnings is read as "transport security is done" | HSTS/SSL-redirect/secure-cookies never get enabled for production traffic | Record each risk-acceptance with rationale and the explicit owner/trigger (#177 enables per environment); list it in Out of Scope, not as resolved |
