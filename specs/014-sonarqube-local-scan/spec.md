# Feature Specification: Local RedMark SonarQube + Branch Scan Workflow

**Branch**: `014-sonarqube-local-scan` (not yet created; spec scaffolded on the active branch — create the branch at implementation time)
**Created**: 2026-06-05
**Status**: Draft

## Summary

Stand up a local-only SonarQube code-quality instance for the `redline` repository,
derived from an existing third-party "SonarQube Emulator", and wire it into the
development workflow so that a branch can be analysed and its issues triaged by an
agent before a pull request is opened or merged.

The work has two homes:

1. **The SonarQube service** — the existing emulator folder, rebranded to RedMark
   Logic, stripped of all cloud/production deployment machinery, run locally via Docker
   and set to start automatically with the Docker runtime.
2. **The `redline` repository** — scan configuration sourced from `pyproject.toml`, the
   official SonarQube MCP server wired under `.vscode/`, secrets in an untracked `.env`,
   and a standalone Claude Code skill that drives the scan-and-triage loop.

The scan runs **locally and directly** (the same logic a CI workflow would run), not by
emulating a CI / GitHub-Actions runner. This feature is scoped to the single `redline`
repository. Multi-repository support, shared/hosted instances, a CI/GitHub-Actions
integration, and any cloud deployment are explicitly out of scope.

## Scenarios (mandatory)

These scenarios form a strict dependency chain (each depends on the one before), so
delivery order follows the chain rather than descending RICE score. RICE is recorded
per scenario for prioritisation transparency; the dependency order is the authoritative
build order and gives the founder a reviewable checkpoint after each one.

### Scenario 1 -- Rebranded, local-only service

The founder converts the third-party SonarQube emulator into a RedMark Logic service:
every "Tonkin & Taylor" identifier is removed, RedMark Logic branding is applied where an
organisation identity is required, and all Azure/production deployment assets are deleted,
leaving only the local Docker stack.

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| ----- | -------------- | -------------- | -------------------- | ---------- |
| 20    | 3              | 90             | 1.5                  | 36         |

**Independent test**: Search the converted service for prior-organisation identifiers
and confirm none remain; confirm the Azure/deploy assets are gone; confirm the remaining
local stack still builds (`docker compose build`) without referencing deleted files.

**Acceptance criteria**:

1. **Given** the converted service, **When** the founder searches for prior-organisation
   identifiers (org name, job number, atlassian/azure URLs, GitHub App references),
   **Then** none are found.
2. **Given** the converted service, **When** the founder inspects project/author metadata
   and the README, **Then** RedMark Logic branding is present and consistent.
3. **Given** the production/Azure assets are removed, **When** the local Docker stack is
   built, **Then** the build succeeds with no missing-file or broken-reference errors.

---

### Scenario 2 -- Local instance runs with persistent data and auto-start

The founder starts the stack with one documented command, reaches the SonarQube UI at a
fixed local address, logs in with the documented local credentials, confirms that data
survives a stop/start cycle, and confirms the instance comes back automatically after the
Docker runtime restarts.

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| ----- | -------------- | -------------- | -------------------- | ---------- |
| 20    | 3              | 85             | 0.5                  | 102        |

**Independent test**: Run the setup command, open the UI, log in; create a marker (e.g.
a project), stop the stack, start it again, and confirm the marker is still present; then
restart Docker Desktop and confirm the instance returns on its own.

**Acceptance criteria**:

1. **Given** Docker is running, **When** the founder runs the documented setup command,
   **Then** SonarQube becomes reachable at `http://localhost:9000` and the admin password
   is set to the documented local value automatically.
2. **Given** a running instance with data, **When** the stack is stopped and started again
   (without an explicit destructive wipe), **Then** all prior analysis data and accounts
   remain intact.
3. **Given** the documented database location, **When** the founder inspects it, **Then**
   the database persists at a stable, known location rather than an ephemeral one.
4. **Given** the host or Docker Desktop has been restarted, **When** Docker is running
   again, **Then** the instance comes back up automatically with no manual start step —
   only an explicit manual stop keeps it down.

---

### Scenario 3 -- Analyse the current redline branch

From a redline working copy on any branch, the founder (or an agent) runs the analyser
and sees a `redline` project populated in the local SonarQube, with issues attributed to
the analysed branch.

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| ----- | -------------- | -------------- | -------------------- | ---------- |
| 20    | 3              | 80             | 1.0                  | 48         |

**Independent test**: With the instance running (Scenario 2), analyse a branch with a
known lint/quality problem and confirm the issue appears in the UI under that branch.

**Acceptance criteria**:

1. **Given** the local instance is running, **When** the analyser runs against the current
   branch, **Then** a `redline` project appears (or updates) in SonarQube with results
   attributed to that branch name.
2. **Given** two different branches are analysed, **When** the founder views the project,
   **Then** issues are distinguishable per branch.
3. **Given** the analyser needs to authenticate, **When** it runs, **Then** it uses a
   token that is not committed to either repository.
4. **Given** a coverage report exists, **When** the analyser runs, **Then** coverage is
   reflected in the project (when available; absence of a report does not fail the scan).
5. **Given** the scan, **When** it runs, **Then** it runs directly on the developer
   machine (no CI / GitHub-Actions runner or emulation layer is required).

---

### Scenario 4 -- Retrieve issues programmatically for an agent

An agent connects to the local SonarQube through the official SonarQube MCP server
(configured under `.vscode/`) and retrieves the issues for the redline project and current
branch, with enough detail (rule, severity, file, line, message, status) to reason about
each one.

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| ----- | -------------- | -------------- | -------------------- | ---------- |
| 20    | 2              | 75             | 0.5                  | 60         |

**Independent test**: After a scan, invoke the MCP issue-retrieval tool and confirm the
returned issue set matches what the UI shows for the same branch.

**Acceptance criteria**:

1. **Given** a completed analysis, **When** the agent requests issues for the redline
   project/branch via the MCP, **Then** the full open-issue set is returned.
2. **Given** an issue is returned, **When** the agent inspects it, **Then** it includes
   rule, severity, file path, line, message, and status.
3. **Given** the MCP authenticates to SonarQube, **When** it connects, **Then** it uses a
   token read from an untracked `.env`, while its non-secret settings live in committed
   `.vscode/` configuration.

---

### Scenario 5 -- One-command standalone scan-and-triage before a PR

Before opening or merging a PR, the founder (or an agent) invokes a single standalone
Claude Code skill that scans the current branch, waits for analysis to finish, retrieves
the issues via the MCP, and presents them for triage so each can be marked false-positive
or actionable and rectified. The skill is callable on its own today and is designed to be
called by a future umbrella pre-PR checks skill (out of scope here).

| Reach | Impact (0.5-3) | Confidence (%) | Effort (person-days) | RICE Score |
| ----- | -------------- | -------------- | -------------------- | ---------- |
| 20    | 3              | 70             | 1.5                  | 56         |

**Independent test**: On a branch with a mix of real and spurious findings, invoke the
skill once and confirm it produces a per-issue triage list ending in a clear set of
actionable items; separately, with the instance stopped, confirm it raises a clear,
typed error rather than passing silently.

**Acceptance criteria**:

1. **Given** a redline branch with code changes, **When** the founder invokes the scan
   skill, **Then** it runs the analysis, retrieves the issues, and presents them grouped
   for triage without further manual steps.
2. **Given** the triage list, **When** the agent classifies an issue as a false positive,
   **Then** that decision can be recorded so it is not re-surfaced on the next scan.
3. **Given** SonarQube is not running or not reachable at its configured address, **When**
   the skill is invoked, **Then** it raises a typed, named error that surfaces to the
   developer with how to start the instance — it never passes silently, returns an empty
   result, or otherwise hides the failure.
4. **Given** the skill exists, **When** another (future) skill needs a SonarQube check as
   one of several pre-PR steps, **Then** it can call this skill as a self-contained
   sub-step without modification.

---

### Edge Cases

- What happens when the analyser runs but the instance is still starting up (not yet
  `UP`)? The workflow should wait/poll within a bound and report a timeout clearly.
- What happens on the very first scan of a brand-new branch with no prior baseline?
  All findings are "new"; the workflow should still complete and present them.
- What happens when a destructive wipe (`down -v`) is run by mistake? Data is lost by
  design; the setup command must be re-runnable to rebuild from empty.
- What happens when the third-party branch-analysis plugin image tag is unavailable?
  The stack should fail fast with a clear message; main-branch-only analysis is the
  fallback.
- What happens when no quality issues are found? The skill should report a clean result,
  not an error.
- What happens when the dev machine lacks sufficient memory for the JVM/search engine?
  Startup may fail; memory requirements must be documented.
- What happens when Docker Desktop itself is not running? The availability check raises a
  typed error telling the developer to start Docker Desktop / the stack — never a silent
  pass and never an empty "no issues" result.

## Requirements (mandatory)

### Functional Requirements

Rebrand and strip (Scenario 1):

- **FR-001**: The service MUST contain no prior-organisation identifiers — organisation
  name, job/account numbers, Jira/Confluence/Azure URLs, GitHub App references, or author
  metadata belonging to the original owner.
- **FR-002**: The service MUST present RedMark Logic identity wherever an organisation
  identity is required (repository/project name, author/maintainer metadata, README title
  and badges).
- **FR-003**: The service MUST retain only local-execution assets. All cloud/production
  deployment assets — infrastructure-as-code, deploy/update/migrate/rollback automation,
  cloud identity/secret configuration, and production-infrastructure documentation — MUST
  be removed.
- **FR-004**: Removal of production assets MUST NOT break local startup; the local stack
  MUST still build and run after the strip.

Local run, persistence, and auto-start (Scenario 2):

- **FR-005**: The service MUST start a local SonarQube instance reachable at a fixed,
  documented local address through a single documented command.
- **FR-006**: Analysis data, accounts, and the database MUST persist across ordinary
  stop/start cycles; only an explicit destructive wipe may remove them.
- **FR-007**: The database MUST be stored at a defined, stable location that is documented
  to the operator.
- **FR-008**: Local credentials MUST be local-only, documented, and distinct from any
  production system; setup MUST set the known admin password automatically and be
  re-runnable after a wipe.
- **FR-020**: The stack MUST be configured to start automatically whenever the Docker
  runtime (Docker Desktop) starts — so the instance is available after a host reboot or
  Docker Desktop launch with no manual step. Only an explicit manual stop keeps it down.

Scan integration (Scenario 3):

- **FR-009**: The redline repository MUST provide analysis configuration declaring the
  project key, source locations (the `marker` and `rl` packages under `src/`), test
  locations, and language so the analyser knows what to scan.
- **FR-021**: This analysis configuration MUST be derived from a single in-repo source
  (the project's tool configuration in `pyproject.toml`) and generated to the scanner's
  properties file at scan time; the generated file MUST NOT be a second source of truth
  and MUST NOT be committed.
- **FR-022**: Local analysis MUST be runnable directly on the developer machine and MUST
  NOT require a CI runner or a GitHub-Actions emulation layer.
- **FR-010**: A developer or agent MUST be able to analyse the currently checked-out
  redline branch such that results appear under a single `redline` project with findings
  attributed to that branch and distinguishable between branches.
- **FR-011**: The analyser MUST authenticate to the local instance using a token that is
  not committed to version control.
- **FR-012**: The analyser SHOULD submit test-coverage data when a coverage report is
  available, and MUST NOT fail when one is absent.

MCP retrieval and configuration (Scenario 4):

- **FR-013**: The official SonarQube MCP server MUST be configured to connect to the local
  instance and authenticate via a token held outside version control.
- **FR-023**: The MCP server MUST be registered in committed `.vscode/` configuration with
  its non-secret settings (server URL, project key) hard-coded there; the secret user
  token MUST be read only from an untracked `.env` file. A committed `.env` template
  (documenting variable names with no secret values) MUST be provided.
- **FR-014**: An agent MUST be able to retrieve, via the MCP, the issue set for the redline
  project and current branch, with each issue exposing rule, severity, file, line, message,
  and status.

Standalone scan-and-triage skill (Scenario 5):

- **FR-015**: A standalone Claude Code skill MUST exist that, on demand, runs the branch
  analysis, waits for completion within a bounded time, retrieves issues via the MCP, and
  presents them for triage in one invocation.
- **FR-016**: The skill MUST support classifying each issue as false-positive or actionable
  and MUST guide rectification of actionable items before a PR is opened or merged.
- **FR-017**: The skill MUST detect when the instance is not running or unreachable and
  report how to start it.
- **FR-025**: When the instance is unreachable at its configured address, the skill MUST
  raise a typed, named error (e.g. `SonarQubeUnavailableError`) that surfaces to the
  developer. It MUST NOT pass silently, MUST NOT return an empty issue set, and MUST NOT
  otherwise hide the failure. (Constitution Principle X.)
- **FR-026**: The skill MUST be self-contained and independently invocable, and MUST be
  callable as a sub-step by a future umbrella pre-PR checks skill without modification. The
  umbrella skill itself is out of scope for this feature.
- **FR-018**: False-positive classifications SHOULD be recordable (via SonarQube issue
  status or a documented convention) so they are not re-surfaced on subsequent scans.

Scope:

- **FR-019**: The feature scope is the single `redline` repository. Multi-repository
  support, shared/hosted instances, and a CI/GitHub-Actions integration are out of scope.

### Key Entities

- **RedMark SonarQube service**: the converted, rebranded, local-only repository that
  defines and runs the instance (container definitions, setup script, version pin).
- **Local SonarQube instance**: the running server plus its database; holds projects,
  branches, issues, and accounts; configured to auto-start with the Docker runtime.
- **redline project**: the SonarQube project representing the redline codebase; has a
  project key and one entry per analysed branch.
- **Scan configuration source**: the single in-repo definition of what to scan
  (`pyproject.toml` tool config), from which the scanner properties file is generated.
- **Analysis (scan)**: a single run of the analyser against a branch; produces or updates
  the project's issues for that branch.
- **Issue**: a single finding — rule, severity, file, line, message, and status
  (open / false-positive / won't-fix / resolved).
- **Credential configuration**: the split between committed non-secret settings
  (`.vscode/` + `.env` template) and the untracked secret token (`.env`).
- **MCP server registration**: the SonarQube MCP server entry under `.vscode/` that an
  agent uses to read issues.
- **Scan-and-triage skill**: the standalone orchestrator that ties availability check,
  analysis, retrieval, and triage into one developer-facing action.

## Success Criteria (mandatory)

- **SC-001**: A developer can go from "nothing running" to a usable local code-quality
  instance in under 10 minutes by following the documented steps.
- **SC-002**: A search of the converted service returns zero prior-organisation
  identifiers.
- **SC-003**: Analysis results and accounts survive a full stop/start cycle with no data
  loss.
- **SC-004**: A developer can analyse the current branch and view its issues within 5
  minutes of finishing code changes, for the redline-sized codebase.
- **SC-005**: An agent retrieves 100% of the current branch's open issues programmatically,
  matching the set shown in the UI.
- **SC-006**: The full pre-PR loop (scan, retrieve, triage) completes from a single skill
  invocation, with every issue classifiable as false-positive or actionable.
- **SC-007**: No authentication tokens are committed to either repository (verifiable by
  search and by ignore rules).
- **SC-008**: After the Docker runtime is restarted, the instance is reachable again with
  no manual start step.
- **SC-009**: With the instance stopped, invoking the skill produces a visible typed error
  with remediation in 100% of attempts — never a silent pass or an empty result.

## Assumptions

- Brand identity is "RedMark Logic"; folder/slug `redmark-sonarqube`; domain
  `redmarklogic.com`. If the legal/display name differs, only branding strings change.
- "White-label it, then replace the white-label with our company name" is interpreted as a
  single rebrand to RedMark Logic, not the production of a separate neutral/reusable
  template. If a reusable template is also wanted, that is a separate effort.
- The service is converted in place (the existing emulator folder is rebranded and the
  folder renamed), per the founder's decision; the pristine original is not preserved
  separately.
- Docker Desktop is available on the development machine (Windows); it handles host kernel
  settings the search engine requires. The instance auto-starts via a container restart
  policy once it has been started once.
- The existing Community-Edition image with the community branch-analysis plugin is an
  acceptable basis for per-branch analysis; no commercial SonarQube licence is assumed.
- Usage is single-developer/single-agent and local; multi-user auth hardening is not
  required.
- Persistence uses named Docker volumes with stable names by default (data survives
  stop/start); an optional host bind-mount for the database is acceptable if a visible,
  backup-friendly location is preferred.
- Scan properties are generated from `[tool.usethis]` in `pyproject.toml` (mirroring the
  reference wallplanner project), keeping one source of truth; the analyser is the
  `sonar-scanner` CLI run directly against the local instance — the project's CI workflow
  logic is reused, but a CI/GitHub-Actions runner is NOT emulated locally.
- Issue retrieval uses the official SonarSource SonarQube MCP server (Docker image
  `mcp/sonarqube`, env `SONARQUBE_URL` + `SONARQUBE_TOKEN`, no organisation for a
  self-hosted Server); a thin Web-API-based skill is the fallback only if the official
  server cannot authenticate against the local instance.
- The scan is triggered on demand by a developer or agent (a standalone skill), not by an
  automatic git hook or CI job, for this feature.

## Risks

| Risk                                                            | Impact                                                                 | Mitigation                                                                              |
| -------------------------------------------------------------- | ---------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| SonarQube's JVM/search engine is heavy for a dev laptop        | Startup is slow or fails; the founder sees the instance stuck starting | Keep the existing constrained JVM profile; document minimum memory; expose tuning knobs |
| Per-branch analysis depends on a third-party plugin image      | A tag pull fails and analysis cannot start                             | Pin the image tag; document; fall back to main-branch-only analysis                     |
| Tokens could be committed by accident                          | Local credentials leak into git history                                | `.env` ignored; committed config holds non-secrets only; a search check in the gate     |
| Stripping cloud assets removes something the local stack needs | The local build breaks after the strip                                 | Re-verify `docker compose build` after each removal; keep removals reviewable           |
| The official MCP may not authenticate against a local instance | Agent issue-retrieval does not work as designed                        | Spike MCP connectivity early (Scenario 4); fall back to a thin Web-API skill            |
| Docker Desktop is not running when a scan is attempted         | The scan cannot reach the instance                                     | Availability check raises a typed error with remediation; restart policy auto-starts it |
| First scan floods the founder with pre-existing findings       | Triage feels overwhelming and the gate is ignored                      | Establish a baseline / focus on new code; document a triage convention                  |
