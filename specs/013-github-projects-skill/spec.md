# Feature Specification: GitHub Projects Skill and Board Bootstrap

**Feature Branch**: `013-github-projects-skill`

**Created**: 2026-06-03

**Status**: Draft

**Input**: "What do we need to start mapping our tasks to GitHub Projects? Do we need to move the code repo to our org first? Can we create the project now? Do we need a skill? Who owns it?"

---

## Context

This spec covers five sequential phases to fully operationalise the GitHub Projects board:

1. **Repo transfer (Phase 0)** — transfer `harell/redline` to the `redmarklogic` organisation on GitHub. This unlocks `projects_v2_item` webhooks (org-only) and puts all work under the correct business identity.
2. **Board bootstrap (Phase 1)** — create the GitHub Project board under `redmarklogic`, seed it with the agreed schema (9 custom fields, 5 columns, 4 automations, 2 views, 4 milestones), and verify it is accessible via `gh` CLI.
3. **Skill creation (Phase 2)** — write the `github-projects` SKILL.md so agents can discover and load the correct procedures when interacting with the board.
4. **First-pass seeding (Phase 3)** — import the top open specs as parent issues using the Python tool at `.agents/tools/github_projects/`, giving the founder the first live view of the backlog.
5. **Field-level enforcement hooks (Phase 4)** — implement the three GitHub Actions checks that require `projects_v2_item` webhooks (now available because the board is an org project): Blocked-without-reason, Done-without-PR, spec-link validation.

Phases 0 and 1 are the two new additions requested. Phases 2–4 were already in the original scope.

---

## Answer to Pre-Spec Questions

### Do we need to move the repo to the org first?

**Yes — start with the transfer, then create the board in the org.**

GitHub Projects are not transferred when a repo moves. Creating the board under `harell` and migrating later means rebuilding the board from scratch (items are not carried over by GitHub's "Copy project" feature). Starting under `redmarklogic` avoids that rework entirely.

The org (`redmarklogic`) already exists. The transfer takes under 5 minutes. After transfer:
- The board is created as an org project (`github.com/orgs/redmarklogic/projects`).
- `projects_v2_item` webhooks become available, unlocking the three field-level enforcement checks (Phase 4).
- All `gh` CLI commands work identically — swap `owner="@me"` for `owner="redmarklogic"` in `resolve_project_config`.
- All existing PRs, issues, git history, and branch redirects are preserved by GitHub's transfer mechanism.

### Can we create the GitHub Project and issues now?

**Yes, immediately.** Prerequisites:

- `gh` CLI authenticated with `project` scope (`gh auth refresh -s project`)
- Confirmed with `gh auth status` — `project` must appear in scopes

No org, no transfer, no other dependencies.

### Do we need a skill?

**Yes.** Without a skill, agents have no authoritative reference for:
- which procedures they are permitted to invoke
- which guard conditions must run before any write
- the `primary_agent` derivation rule
- the `Depends on` and `Agents` body section format
- when to call `sync-this-week` vs when to just call `move-status`

A skill is also required for the agents' JD skill-routing tables. Without it, no agent knows to load the tool when they need to create a board item.

### Who owns the skill?

**Mark (sole steward).** Harriet's analysis: Mark designed the governance, authors the procedures, and runs `sync-this-week`. If the board schema changes (new field, renamed option), Mark updates the skill. Peter reviews CLI sequences before initial publication — a one-time gate, not ongoing ownership.

`owner_agent` array in `skills-lock.json`: `["mark", "kabilan", "matt", "john", "peter"]` — all agents who load the skill. Ron, Graeme, Linda, Harriet: excluded (no board write access; loading the skill has no use case for them).

---

## User Scenarios & Testing

### User Story 0 — Repo lives under redmarklogic (Priority: P1)

The founder transfers `harell/redline` to the `redmarklogic` organisation. After transfer, the repo is accessible at `github.com/redmarklogic/redline`. All existing git remotes redirect automatically. Local clones require a one-time `git remote set-url origin` update.

**Why this priority**: Must complete before the board is created. The board owner cannot be changed after creation — starting in the org prevents a future rebuild.

**Independent Test**: `gh repo view redmarklogic/redline` returns the repository metadata without error.

**Acceptance Scenarios**:

1. **Given** the founder initiates a transfer from `harell/redline` Settings → Danger Zone → Transfer, **When** the transfer completes, **Then** `gh repo view redmarklogic/redline --json name,owner` returns `{"name": "redline", "owner": {"login": "redmarklogic"}}`.
2. **Given** the transfer is complete, **When** `git fetch origin` is run from an existing local clone, **Then** git automatically follows the redirect with no manual remote update required.
3. **Given** the transfer is complete, **When** the local remote is updated to `https://github.com/redmarklogic/redline.git`, **Then** `git push origin` succeeds without error.

---

### User Story 1 — Founder opens GitHub and sees the Redline board under the org (Priority: P1)

The founder navigates to `github.com/orgs/redmarklogic/projects` and sees a board named "Redline" with five columns (Backlog, In Progress, Blocked, To Review, Done), a Roadmap view with four milestones, and an Engineering view that filters out ops tasks. The board is empty but fully configured.

**Why this priority**: Zero value until the board exists. Everything else depends on this.

**Independent Test**: Open `https://github.com/orgs/redmarklogic/projects` — Redline board is visible with the correct column structure and milestone dates.

**Acceptance Scenarios**:

1. **Given** `gh auth status` confirms `project` scope, **When** the board bootstrap procedure runs, **Then** `gh project list --owner "redmarklogic"` returns a project named "Redline" with number `N`.
2. **Given** the board exists, **When** the founder opens the Roadmap view, **Then** four milestones appear at the correct target dates: KR1 (2026-08-01), KR2 (2026-09-01), Kill-horizon (2026-09-01), KR5 (2026-11-01).
3. **Given** the board exists, **When** `resolve_project_config(project_number=N, owner="redmarklogic")` runs, **Then** it returns a `ProjectConfig` with all 9 custom field IDs populated and writes `project_config.json` to `.agents/tools/github_projects/`.

---

### User Story 2 — Mark creates a parent issue and the task appears on the board (Priority: P1)

Mark (or the founder telling Mark) calls `create_task()` with a `TaskCreate` object. A GitHub issue is created in `redmarklogic/redline`, added to the board, and all 9 custom fields are set correctly. The issue appears in the Backlog column.

**Why this priority**: Validates the full tool pipeline works end-to-end. Unblocks all subsequent task creation.

**Independent Test**: After one `create_task()` call, `list_tasks(config, status="Backlog")` returns the new task with correct fields including `source`, `start_date`, `target_date`, and `agents`.

**Acceptance Scenarios**:

1. **Given** a valid `TaskCreate` with `agents={"Kabilan"}`, `source="specs/001-skeleton-generator/"`, `start_date`, `target_date`, and `depends_on=None`, **When** `create_task(task, config)` runs, **Then** `result.ok == True` and `result.issue_url` is a valid GitHub issue URL.
2. **Given** the issue exists on the board, **When** the founder views it in GitHub, **Then** the issue body contains `## Purpose`, `## Source`, `## Done when`, and `## Agents: Kabilan` sections.
3. **Given** `task.status == "Blocked"` and `task.blocked_by == None`, **When** `TaskCreate(...)` is constructed, **Then** `ValidationError` is raised before any API call.

---

### User Story 3 — An agent (Kabilan) moves a task to "To Review" after opening a PR (Priority: P2)

Kabilan opens a PR with `Closes #N` in the body. The PR creation automatically triggers the board automation and moves the linked issue to "To Review". No manual step is needed from Kabilan.

**Why this priority**: Validates the PR → automation flow, which is the primary status-transition mechanism for engineering tasks.

**Independent Test**: Open a draft PR in `redmarklogic/redline` referencing an existing board issue with `Closes #N`. Verify the issue moves to "To Review" within 60 seconds (GitHub automation latency).

**Acceptance Scenarios**:

1. **Given** a GitHub issue exists in Backlog on the board, **When** a PR is opened with `Closes #N` in the body, **Then** the board item moves to "To Review" automatically via GitHub Projects built-in workflow.
2. **Given** the PR is merged to `master`, **When** GitHub processes the merge, **Then** the linked issue closes and the board item moves to "Done" automatically.
3. **Given** an agent calls `move_task(item_id, "Done", config)`, **When** the call executes, **Then** `result.ok == False` and `result.status_code == 403` with message "Agents may not set status to 'Done'."

---

### User Story 4 — The `github-projects` skill exists and agents can load it (Priority: P2)

The SKILL.md file exists at `.agents/skills/github-projects/SKILL.md`, contains all required procedures with their guard conditions and access table, references the Python tool, and is registered in `skills-lock.json` and `docs/architecture/skills-architecture.md`. Mark's JD references the skill with a trigger condition.

**Why this priority**: Without the skill, agents are relying on conversational memory of governance rules rather than a persistent, version-controlled reference. The skill is the durability mechanism.

**Independent Test**: Read `.agents/skills/github-projects/SKILL.md` — contains all 9 procedures, the access table, guard conditions, and the tool reference. Check `skills-lock.json` for `github-projects` entry with correct `owner_agent`, `tier`, and `layer`.

**Acceptance Scenarios**:

1. **Given** `.agents/skills/github-projects/SKILL.md` exists, **When** `prek` runs all hooks, **Then** `check-skills-documented.py`, `check-skill-dag.py`, and `check-orphan-skills.py` all pass with no errors.
2. **Given** `skills-lock.json` is updated, **When** `check-no-section-rules.py` and `check-skill-routing-redundancy.py` run, **Then** no violations are reported for the `github-projects` entry.
3. **Given** `rl.mark.agent.md` is updated with the skill trigger, **When** an agent session starts with a board-write intent, **Then** the skill loading instruction appears in the session context.

---

### User Story 5 — The backlog is seeded with the top open specs (Priority: P3)

The top 10 open specs (from `specs/001-skeleton-generator/` through `specs/012-dag-cycle-detection/`) are created as GitHub Issues in `harell/redline` and added to the board as parent issues in Backlog. Each issue has the correct `source`, `task_type`, `agents`, and `depends_on` fields set.

**Why this priority**: Gives the founder a live board view immediately. Low risk — issues can be deleted or archived; no irreversible changes.

**Independent Test**: `list_tasks(config, status="Backlog")` returns ≥ 10 items, each with a `source` value matching a `specs/NNN/` path.

**Acceptance Scenarios**:

1. **Given** 10 `TaskCreate` objects constructed from the existing specs, **When** `create_task()` is called for each, **Then** all 10 return `result.ok == True` or `result.status_code == 207`.
2. **Given** the board is seeded, **When** the founder opens the board's Engineering view, **Then** all 10 items are visible in Backlog with correct `Type`, `Source`, and `Agent` fields.

---

### Edge Cases

- What if `gh auth refresh -s project` fails (org-level restriction or token scope limit)? → blocked; surface error to founder before any board operation.
- What if a spec directory has no `spec.md` (malformed spec)? → skip that spec, log which ones were skipped, continue with the rest.
- What if the board already has an issue with the same title? → GitHub creates a duplicate issue; the tool does not deduplicate. Caller must verify before seeding.
- What if `project_config.json` has stale field IDs after a board schema change? → calls to `resolve_project_config(force_refresh=True)` regenerate it. All write functions fail with a clear error if field IDs are missing.
- What if `move_task` is called on an item already in the target status? → GitHub API accepts it silently; `result.ok == True`. No wasted side effect.

---

## Requirements

### Functional Requirements

- **FR-000**: The repository MUST be transferred from `harell/redline` to `redmarklogic/redline` before the board is created. The transfer MUST be initiated from GitHub repository Settings and confirmed by the receiving organisation.
- **FR-000b**: After transfer, the local git remote in the development environment MUST be updated to `https://github.com/redmarklogic/redline.git` and verified with a successful `git fetch`.
- **FR-001**: The GitHub Project board MUST be created under the `redmarklogic` organisation with the exact column structure: Backlog, In Progress, Blocked, To Review, Done.
- **FR-002**: The board MUST have 9 custom fields: Status (built-in), Type, Sprint, Agent, Start date, Target date, Blocked by, Source, Depends on.
- **FR-003**: The board MUST have 4 GitHub Projects built-in automations enabled: PR opened → To Review; PR merged → Done; item closed → Done; item reopened → In Progress.
- **FR-004**: The board MUST have 2 saved views: Engineering (default, filters `-type:Ops`) and Ops (`type:Ops`).
- **FR-005**: The board MUST have 4 milestones with correct target dates mapping to the active OKRs in `docs/product/strategy/okrs/2026-h2.md`.
- **FR-006**: The `project_config.json` file MUST be written to `.agents/tools/github_projects/` after `resolve_project_config` runs successfully, and MUST be committed to the repo.
- **FR-007**: `create_task()` MUST reject a `TaskCreate` with no agents (empty `frozenset`) at construction time, before any API call.
- **FR-008**: `move_task()` MUST return status_code 403 when called with `status="Done"` by any agent.
- **FR-009**: The `github-projects` SKILL.md MUST contain: all 9 procedure definitions, the agent access table, all 7 guard conditions, a reference to `.agents/tools/github_projects/`, and a "Prerequisites" section specifying `gh auth refresh -s project`.
- **FR-010**: `skills-lock.json` MUST be updated with a `github-projects` entry containing `tier: "functional"`, `layer: 6`, `owner_agent: ["mark", "kabilan", "matt", "john", "peter"]`, `status: "active"`.
- **FR-011**: The `delete-item` procedure MUST NOT appear in `SKILL.md`. Archiving (`archive-item`) is Mark's scope; deletion is founder-only via GitHub UI or direct CLI.
- **FR-012**: Every agent JD in the `owner_agent` array MUST be updated with a skill trigger condition for `github-projects`.
- **FR-013**: `docs/architecture/skills-architecture.md` MUST be updated to include the `github-projects` skill with its layer assignment before the feature is considered complete.

### Key Entities

- **GitHub Organisation**: `redmarklogic` — receives the repo transfer and owns the board.
- **GitHub Repository**: `redmarklogic/redline` — the transferred repo. All issues live here after transfer.
- **GitHub Project**: the board at `github.com/orgs/redmarklogic/projects/N`. Owns: columns (Status), custom fields, views, automations, milestones.
- **GitHub Issue**: the underlying record for each task. Lives in `redmarklogic/redline`. Board items link to issues.
- **ProjectConfig**: the Pydantic model caching field node IDs. Persisted to `.agents/tools/github_projects/project_config.json`.
- **SKILL.md**: the agent-readable procedure reference. Lives at `.agents/skills/github-projects/SKILL.md`.
- **skills-lock.json**: machine-readable registry. Updated with the new skill entry.

---

## Success Criteria

### Measurable Outcomes

- **SC-001a**: `gh repo view redmarklogic/redline` returns the correct repository metadata within 5 minutes of the transfer completing.
- **SC-001b**: The founder can open `github.com/orgs/redmarklogic/projects` and see the Redline board within 5 minutes of the bootstrap procedure completing — no manual GitHub UI configuration required.
- **SC-002**: `create_task()` successfully creates a GitHub issue and sets all 9 custom fields on the board item in a single invocation, with no manual follow-up step.
- **SC-003**: PR merge-to-master automatically moves the linked board item to Done within 60 seconds — no agent action required.
- **SC-004**: All prek hooks pass (`prek run`) with no violations after the skill is registered.
- **SC-005**: The top 10 open specs are visible on the board in Backlog within one Mark-agent session, with correct metadata.
- **SC-006**: The founder can ask "what is Kabilan working on this sprint?" and get an accurate answer by filtering the board by `Agent: Kabilan` and `Sprint: current`.

---

## Assumptions

- `gh` CLI version ≥ 2.40 is installed and authenticated as `harell` with `project` scope before this feature begins.
- The `redmarklogic` organisation already exists on GitHub and `harell` has Owner-level access to it.
- The repo transfer does not require the receiving org to have any special configuration beyond the founder having create-repository permission.
- GitHub automatically redirects git operations from `harell/redline` to `redmarklogic/redline` after transfer. Local clones continue to work but should have their remote URL updated to avoid relying on the redirect indefinitely.
- The org project (`orgs/redmarklogic/projects`) supports `projects_v2_item` webhooks, enabling the Phase 4 field-level enforcement checks.
- `project_config.json` contains no secrets (GitHub Projects node IDs are not sensitive) and can be committed to the repo.
- The `sync-this-week` procedure (Mark reads the board, writes `docs/product/tasks/this-week.md`) is not automated by this feature. It is a manual Mark invocation triggered on Monday and on material state changes.
- The board will be created with a Kanban layout initially; the Roadmap view is a second saved view (not the default).
- Milestone descriptions contain exactly one line: a link to `docs/product/strategy/okrs/2026-h2.md`. No OKR content is duplicated into GitHub.
- The `Depends on` field is stored as a text custom field on the board (comma-separated `#N` references) because GitHub Projects has no native dependency field. Parsing from the board field is best-effort; the issue body `## Depends on` section is the authoritative representation.

---

## Out of Scope

- Any GitHub Actions enforcement checks implemented as part of Phase 4 (deferred to a follow-on task after the org project is confirmed live).
- `sync-this-week` automation (webhook → Actions → auto-commit). Deferred to a future spec.
- Implementing the `speckit.implement` execution against tasks.md generated from this spec. This spec produces artifacts; it does not execute them.
- Any changes to existing hooks in `hooks/` beyond what is needed to register the new skill.
- Migration of any GitHub Actions workflows that reference `harell/redline` by URL — those are updated as they arise, not as a blocking step.
