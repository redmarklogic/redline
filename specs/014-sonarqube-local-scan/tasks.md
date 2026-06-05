# Tasks: Local RedMark SonarQube + Branch Scan Workflow

**Input**: [plan.md](plan.md) | [spec.md](spec.md)
**Prerequisites**: Docker Desktop running; the emulator folder at
`%USERPROFILE%\Documents\services\sonarqube.emulator`; `uv`, `gh`, and `rg` available.
Phases 0-1 act on the **service repo** (the converted emulator); Phases 2-4 act on the
**redline** repo. Each Acceptance Gate is a hard stop before the next phase.

<!-- Vertical-slice sizing: each task is one complete, reviewable behaviour. Infra/config
     tasks are verified by command; the Python helper follows fail-first TDD. -->

## Phase 0: Convert, rebrand, strip (service repo)

**Purpose**: The emulator becomes `redmark-sonarqube` — no prior-owner identifiers, RedMark
Logic branding, cloud/production assets removed, local stack still builds.

- [ ] T001 [Phase 0] (Recommended) Draft `docs/adr/ADR-015-local-sonarqube-quality-gate.md` in redline and get Peter/founder sign-off (ADR-before-code gate). Optional but advised.
- [ ] T002 [Phase 0] Rename folder `sonarqube.emulator` -> `redmark-sonarqube`; if confirmed (D9), re-init git for a fresh history.
- [ ] T003 [P] [Phase 0] Delete cloud/production assets: `infra/deploy/**`, `.github/workflows/sonarqube-*.yml`, `.github/scripts/update-sonarqube.sh`, `docs/project/production-infrastructure.md`, Azure-specific plan/lessons docs.
- [ ] T004 [P] [Phase 0] Rebrand `README.md`: title, badges, remove job number and atlassian/azure URLs; add RedMark Logic identity.
- [ ] T005 [P] [Phase 0] Rebrand `pyproject.toml` (package name, authors, towncrier/ruff URLs), `.copier-answers.yml`, `LICENSE.txt`.
- [ ] T006 [P] [Phase 0] Rebrand `infra/docker/docker-compose.yml` container/volume names (`sonarqube-emulator*` -> `redmark-sonarqube*`) and the `Dockerfile` comment.

### Acceptance Gate

- [ ] T007 [Phase 0] Verify no identifiers remain: `rg -i "tonkin|tonkintaylor|yyyttnz|azurewebsites|atlassian|t-t-sonarqube"` -> no matches.
- [ ] T008 [Phase 0] Verify the stack still builds: `rtk docker compose -f infra/docker/docker-compose.yml config` then `... build` -> success.

---

## Phase 1: Run locally, persistent, auto-start (service repo)

**Purpose**: One command brings SonarQube up at localhost:9000; data persists; the stack
auto-starts with the Docker runtime.

- [ ] T009 [Phase 1] Set `restart: unless-stopped` on both `sonarqube` and `sonarqube-db` services in `docker-compose.yml` (D12, FR-020).
- [ ] T010 [P] [Phase 1] (Optional) Bind-mount the Postgres data dir to a fixed host path (`<service>/data/postgres`); otherwise keep the named volume. Document the location.
- [ ] T011 [Phase 1] Run `./infra/docker/setup.ps1`; confirm UP + admin password set; document run, persistence, and auto-start in the README.

### Acceptance Gate

- [ ] T012 [Phase 1] Verify UP: `curl http://localhost:9000/api/system/status` -> `{"status":"UP",...}`.
- [ ] T013 [Phase 1] Verify persistence: create a project, `rtk docker compose ... down` then `up -d`, project still present.
- [ ] T014 [Phase 1] Verify auto-start: restart Docker Desktop -> the instance returns with no manual step.

---

## Phase 2: Analyse the current redline branch (redline repo)

**Purpose**: A scan of the current branch populates a `redline` project, with properties
generated from a single source and an uncommitted token.

- [ ] T015 [Phase 2] Add `[tool.usethis]` sonar config to redline `pyproject.toml`: `sonarqube.exclusions` (tests, scripts, notebooks, vendored), coverage + ruff report paths (mirror wallplanner). This is the SSOT (D10, FR-021).
- [ ] T016 [P] [Phase 2] Add `.gitignore` entries for the generated `sonar-project.properties` and `ruff-report.json` (`.env` is already ignored).
- [ ] T017 [P] [Phase 2] Add a committed `.env` template (e.g. `.env.example`) documenting `SONAR_PROJECT_KEY`, `SONAR_HOST_URL`, `SONAR_TOKEN`, `SONARQUBE_URL`, `SONARQUBE_TOKEN` — names only, no secret values.
- [ ] T018 [Phase 2] In the running SonarQube, create the `redline` project + a user token; write the token into untracked `.env` (one-time, manual).
- [ ] T019 [Phase 2] Write `scan.ps1` (+ `scan.sh`): load `.env`; derive the current git branch; `uvx usethis show sonarqube --output-file=sonar-project.properties` (env `SONAR_PROJECT_KEY=redline`); produce ruff + coverage reports; run `sonarsource/sonar-scanner-cli` (container) with `SONAR_HOST_URL=http://host.docker.internal:9000`, the token, and `-Dsonar.branch.name=<branch>`.

### Acceptance Gate

- [ ] T020 [Phase 2] Run `./scan.ps1`; verify `curl "http://localhost:9000/api/projects/search?projects=redline"` shows the project and the UI lists issues for the branch.
- [ ] T021 [Phase 2] Verify no committed `sonar-project.properties` and no token in tracked files: `git status` clean of secrets; `git grep -i <token-prefix>` -> nothing.

---

## Phase 3: Retrieve issues via the official MCP (redline repo)

**Purpose**: An agent lists redline issues through the official MCP server, configured under
`.vscode/` with the secret in `.env`.

- [ ] T022 [Phase 3] Add a `sonarqube` server to `.vscode/mcp.json`: `command: docker`, `args: [run, --init, --pull=always, -i, --rm, -e, SONARQUBE_TOKEN, -e, SONARQUBE_URL, mcp/sonarqube]`, `env: { "SONARQUBE_URL": "http://localhost:9000" }`; load `SONARQUBE_TOKEN` from `.env` via `envFile` (fallback: `${input:sonar_token}` if the VS Code build lacks `envFile`).
- [ ] T023 [P] [Phase 3] Record `SONARQUBE_URL` + `SONARQUBE_TOKEN` in the `.env` template with a short note on the envFile/input fallback.

### Acceptance Gate

- [ ] T024 [Phase 3] Via the MCP, list issues for `project=redline` + current branch; compare to `curl "http://localhost:9000/api/issues/search?componentKeys=redline&branch=<branch>"` -> same set, with rule/severity/file/line/message/status.
- [ ] T025 [Phase 3] Verify non-secret MCP config is committed in `.vscode/`; the token exists only in untracked `.env`.

---

## Phase 4: Standalone scan-and-triage skill (redline repo)

**Purpose**: One invocation scans, retrieves, and triages; an unreachable instance raises a
typed error (never silent); the skill is standalone and composable.

### Tests (write first -- must fail before implementation begins)

- [ ] T026 [Phase 4] Write failing test: `ensure_available(url)` raises `SonarQubeUnavailableError` when the URL is unreachable, in `tests/.../sonar_scan/test_availability.py` (mirror the existing `github_projects` test location).
- [ ] T027 [Phase 4] Confirm it fails: `.venv\Scripts\activate; python -m pytest tests/.../sonar_scan/test_availability.py -v`.

### Implementation

- [ ] T028 [Phase 4] Implement `.agents/tools/sonar_scan/` (D16): `SonarQubeUnavailableError` (typed, Principle X), `ensure_available(url)`, current-branch detection, and issue-fetch glue — make T026 green. No sentinel returns.
- [ ] T029 [Phase 4] Create `.agents/skills/sonar-scan/SKILL.md` (boundary contract: pre-PR branch scanning -> triaged issue list) + `procedures/sonar-scan.md` (availability check; run `scan.ps1`; poll the compute-engine task; retrieve via MCP; group by file/severity; triage loop; record false positives via issue status). Keep it agent-agnostic (Principle IV) and note it is callable by a future umbrella pre-PR skill (FR-026).
- [ ] T030 [P] [Phase 4] Add a routing entry for the skill to the relevant agent JD (e.g. `kabilan.md`) — the skill must not name any agent.

### Acceptance Gate

- [ ] T031 [Phase 4] Run `.venv\Scripts\activate; python -m pytest tests/.../sonar_scan -v` -> all green.
- [ ] T032 [Phase 4] E2E: on a branch with a seeded issue, invoke the skill -> grouped triage list; mark one finding false-positive -> re-run -> it is not re-surfaced.
- [ ] T033 [Phase 4] Instance-down: stop the stack -> invoke the skill -> it raises `SonarQubeUnavailableError`, surfaced to the developer with remediation (no silent pass, no empty result).

---

## Phase Z: Polish

- [ ] T034 [P] [Phase Z] Finalise docs: service README (run/persist/auto-start) and a redline note on the scan workflow + `.env` setup; ensure the `.env` template documents every variable.
- [ ] T035 [Phase Z] Full check: `.venv\Scripts\activate; python -m pytest; python -m ruff check .agents/tools/sonar_scan`; add `usethis`/`sonarqube`/`pyproject` to the codespell ignore list if it flags them.
- [ ] T036 [Phase Z] End-to-end verification on a real branch: scan -> MCP retrieval -> triage, plus the instance-down typed-error path.

### Acceptance Gate

- [ ] T037 [Phase Z] All tests green, lint clean, end-to-end pass.

## Execution Notes

- `[P]` = parallelizable (different files, no dependencies); `[Phase N]` = owning plan phase.
- TDD is mandatory for the Python helper (`sonar_scan`): Red (write failing test), confirm it
  fails, Green (implement), refactor. Infra/config tasks are verified by their command.
- Each Acceptance Gate is a hard stop — do not start the next phase until it passes.
- Secrets never enter tracked files: the token lives only in untracked `.env`; committed config
  (`.vscode/`, `.env` template) holds non-secrets only.
- The skill stays agent-agnostic (Constitution Principle IV); agent JDs reference the skill.
- Commit after each task or logical group. Do not push without founder instruction.
- The umbrella pre-PR checks skill that composes this one is OUT OF SCOPE (see plan MoSCoW).
