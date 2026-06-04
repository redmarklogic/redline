---
name: github-projects
description: Use when creating, updating, moving, or querying tasks on the Redline GitHub Projects board (redmarklogic/redline)
---

# GitHub Projects — Board Task Management

Load this skill when an agent needs to interact with the Redline GitHub Project board
at `github.com/orgs/redmarklogic/projects`.

**Steward**: PM agent. Schema changes (new field, renamed option) go to the PM agent before any other agent acts on them.

## Prerequisites

Before any write operation:

```sh
# Verify project scope is present
gh auth status
# If 'project' is missing:
gh auth refresh -s project
```

`project_config.json` must exist at `.agents/tools/github_projects/project_config.json`.
If absent, run the `resolve-config` procedure first.

## Python Tool

All procedures invoke the Python package at `.agents/tools/github_projects/`.
Import pattern:

```python
from agents.tools.github_projects import (
    resolve_project_config,
    create_task,
    get_task,
    list_tasks,
    update_task,
    move_task,
    delete_task,
)
from agents.tools.github_projects.schema import TaskCreate, TaskUpdate
```

`project_config.json` is the only persistent state. Commit it after `resolve-config` runs.

---

## Guard Conditions

These conditions are checked before or during every procedure. A procedure MUST abort
and surface the error if any guard fails.

| # | Condition | Checked when |
|---|---|---|
| G1 | `gh auth status` lists `project` in scopes | Before any write (create, update, move, archive) |
| G2 | `project_config.json` exists and is ≤ 24 h old | Before any board operation |
| G3 | `agents` frozenset has at least one member | At `TaskCreate` construction (Pydantic enforces) |
| G4 | `blocked_by` is non-empty when `status == "Blocked"` | At `TaskCreate`/`TaskUpdate` construction and `move-status` call |
| G5 | Agents MUST NOT set `status = "Done"` | At `move-status` call (tool returns 403) |
| G6 | `start_date <= target_date` | At `TaskCreate`/`TaskUpdate` construction (Pydantic enforces) |
| G7 | `archive-item` removes from board view only; the GitHub Issue stays open | Before calling `archive-item` — never use to close an issue |

---

## Agent Access Table

| Procedure | PM | Dev | Designer | Marketing | Engineer | Founder |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| create-task | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| update-task | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| move-status | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| list-tasks | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| get-task | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| archive-item | ✓ | — | — | — | — | ✓ |
| resolve-config | ✓ | ✓ | — | — | ✓ | ✓ |
| sync-this-week | ✓ | — | — | — | — | ✓ |
| seed-backlog | ✓ | ✓ | — | — | — | ✓ |

---

## Procedures

### 1. create-task

Create a GitHub issue in `redmarklogic/redline` and add it to the board with all 9 custom fields set.

**Guards**: G1, G2, G3, G4, G6

```python
from datetime import date
config = resolve_project_config(project_number=N, owner="redmarklogic")

task = TaskCreate(
    title="Implement skeleton-generator PDF export",
    task_type="Feature",
    start_date=date(2026, 6, 9),
    target_date=date(2026, 6, 22),
    purpose="Enables PDF export — serves *free-tier-signal* bet.",
    done_when="PR merged and spec task 001-T4 checked off.",
    source="specs/001-skeleton-generator/",
    agents=frozenset({"<implementing-agent>"}),
    status="Backlog",
)
result = create_task(task, config)
# result.ok == True → result.issue_url, result.item_id populated
# result.status_code == 207 → issue created but some fields failed; check result.message
```

Issue body is auto-generated with `## Purpose`, `## Source`, `## Done when`, `## Agents`,
and `## Depends on` sections. Pass `body=` explicitly only when using a full per-type template.

---

### 2. update-task

Update one or more fields on an existing board item. Only non-`None` fields are written.

**Guards**: G1, G2, G4, G6 (when both dates are in the payload)

```python
from agents.tools.github_projects.schema import TaskUpdate
update = TaskUpdate(
    item_id="PVTI_lADOANN5s84ACbL0zgBVd94",
    sprint="Sprint 2 - Jun 15-28",
    target_date=date(2026, 6, 28),
)
result = update_task(update, config)
```

Do not pass `status="Done"` — agents cannot set Done via `update-task` (use a merged PR).

---

### 3. move-status

Move a task to a new column. Blocked requires a reason. Done is write-protected.

**Guards**: G1, G2, G4, G5

```python
# Move to In Progress
result = move_task(item_id, "In Progress", config)

# Move to Blocked (blocked_by is keyword-only and mandatory)
result = move_task(item_id, "Blocked", config, blocked_by="Waiting for client NDA — unblocks on receipt.")

# Move to Done — ALWAYS returns 403; use a merged PR instead
result = move_task(item_id, "Done", config)  # result.ok == False, status_code == 403
```

---

### 4. list-tasks

List board items with optional filters. Returns `list[TaskRecord]`.

**Guards**: G2

```python
# All tasks
all_tasks = list_tasks(config)

# Filtered
backlog = list_tasks(config, status="Backlog")
dev_sprint = list_tasks(config, agent="<agent-name>", sprint="Sprint 1 - Jun 1-14")
```

Use this procedure to answer "what is [agent] working on this sprint?":
`list_tasks(config, agent="<agent-name>", sprint="Sprint 1 - Jun 1-14")`.

---

### 5. get-task

Fetch a single board item by its project item node ID. Returns `TaskRecord | None`.

**Guards**: G2

```python
record = get_task("PVTI_lADOANN5s84ACbL0zgBVd94", config)
if record is None:
    # item not found on this board
    ...
```

---

### 6. archive-item

Remove an item from the board view. **Does NOT close or delete the underlying GitHub Issue.**
PM-only write. Founder may also call directly.

**Guards**: G1, G2, G7

```python
result = delete_task(item_id, config)
# The issue at result.issue_url remains open in redmarklogic/redline
```

To close the issue after archiving, the founder calls `gh issue close <number>` separately.
Deletion from GitHub entirely is founder-only via GitHub UI — never via this skill.

---

### 7. resolve-config

Resolve and cache project field and option node IDs. Writes `project_config.json`.
Run this when the board schema changes (new field, renamed option) using `force_refresh=True`.

```python
# First-time setup or after schema change
config = resolve_project_config(
    project_number=N,
    owner="redmarklogic",
    force_refresh=True,
)
# Commit .agents/tools/github_projects/project_config.json after this runs
```

`project_config.json` is safe to commit — node IDs are not secrets.

---

### 8. sync-this-week

**PM-only.** Read the board and write `docs/product/tasks/this-week.md`.
Run on Monday morning and after any material sprint change.

Steps:
1. `config = resolve_project_config(...)` (uses cache if fresh)
2. `sprint_tasks = list_tasks(config, sprint="Sprint N - <dates>")` for the current sprint
3. Group by status: In Progress, Blocked, To Review, Backlog
4. Write `docs/product/tasks/this-week.md` with:
   - Sprint name and date range
   - In Progress items (agent, title, target_date, source)
   - Blocked items (agent, title, blocked_by)
   - To Review items (agent, title, issue_url)
   - Backlog items planned for this sprint
5. Commit the file: `docs(tasks): sync this-week for Sprint N`

---

### 9. seed-backlog

Import open specs as parent issues in Backlog. Run once per spec batch (Phase 3 and future onboarding).

Steps:
1. `resolve-config` — ensure config is fresh
2. For each spec directory in `specs/NNN-*/`:
   - Read `spec.md` for title and purpose
   - Determine primary agent from spec context
   - Construct `TaskCreate` with `task_type="Feature"`, `status="Backlog"`, `source="specs/NNN-<name>/"`
   - Call `create-task`; log result
3. Skip specs with no `spec.md` (log which ones were skipped)
4. Do not deduplicate — verify before running that the board does not already have the issue

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Calling `move-status` with `status="Done"` | Returns 403 — task not moved | Use a merged PR or ask the founder to set Done |
| Constructing `TaskCreate` with `agents=frozenset()` | Pydantic raises `ValidationError` before any API call | Always provide at least one agent |
| Calling any write without `project` scope | `gh` CLI returns authentication error | Run `gh auth refresh -s project` first |
| Using stale `project_config.json` after a schema change | Field mutations silently fail or write to wrong field | Run `resolve_project_config(force_refresh=True)` and commit the updated config |
| Calling `archive-item` expecting the GitHub issue to close | Issue stays open; only the board view is cleared | Close the issue separately with `gh issue close <number>` |
| Setting `status="Blocked"` without `blocked_by` | Pydantic raises `ValidationError` on `TaskCreate`; `move-status` returns 400 | Always provide a `blocked_by` reason naming the specific unblock condition |
