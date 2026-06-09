---
name: github-projects
description: Use when creating, updating, moving, or querying tasks on the Redline GitHub Projects board (redmarklogic/redline)
---

# GitHub Projects — Board Task Management

Skill for interacting with the Redline GitHub Project board at `github.com/orgs/redmarklogic/projects`.

**Steward**: PM agent. Schema changes (new field, renamed option) and Structuring-Doctrine
changes go to the PM agent before any other agent acts on them.

## Boundary Contract

### Applies To
- Board items in `redmarklogic/redline` (create, update, move, list, get, archive)
- Native issue dependencies and native sub-issues (parent/child links)
- The structuring decision of whether to split a task into sub-issues at all

### Produces
- Board items with all 9 custom fields set, via the Python tool below
- `project_config.json` (cached field/option node IDs)
- `docs/product/tasks/this-week.md` (via `sync-this-week`)

### Does Not Cover
- Closing or deleting the underlying GitHub Issue (use `gh issue close <number>`)
- Cross-repo dependencies (unsupported by the API)
- Sprint cadence policy itself → `docs/product/operations/cadences.md`

## Prerequisites

Before any write operation:

```sh
# Verify project scope is present
gh auth status
# If 'project' is missing:
gh auth refresh -s project
```

`project_config.json` must exist at `.agents/tools/github_projects/project_config.json`.
If absent, run the `resolve-config` procedure first. Commit the file after it runs — node IDs are not secrets.

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

## Guard Conditions

Every procedure MUST abort and surface the error if any applicable guard fails.

| # | Condition | Checked when |
|---|---|---|
| G1 | `gh auth status` lists `project` in scopes | Before any write (create, update, move, archive) |
| G2 | `project_config.json` exists and is ≤ 24 h old | Before any board operation |
| G3 | `agents` frozenset has at least one member | At `TaskCreate` construction (Pydantic enforces) |
| G4 | `blocked_by` is non-empty when `status == "Blocked"` | At `TaskCreate`/`TaskUpdate` construction and `move-status` call |
| G5 | Agents MUST NOT set `status = "Done"` | At `move-status` call (tool returns 403) |
| G6 | `start_date <= target_date` | At `TaskCreate`/`TaskUpdate` construction (Pydantic enforces) |
| G7 | `archive-item` removes from board view only; the GitHub Issue stays open | Before calling `archive-item` — never use to close an issue |

## Agent Access Table

| Procedure | PM | Dev | Designer | Marketing | Engineer | Founder |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| create-task | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| update-task | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| move-status | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| list-tasks | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| get-task | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| set-dependencies | ✓ | ✓ | — | — | ✓ | ✓ |
| set-parent | ✓ | ✓ | — | — | ✓ | ✓ |
| archive-item | ✓ | — | — | — | — | ✓ |
| resolve-config | ✓ | ✓ | — | — | ✓ | ✓ |
| sync-this-week | ✓ | — | — | — | — | ✓ |
| seed-backlog | ✓ | ✓ | — | — | — | ✓ |

## Structuring Doctrine — Sub-issues vs. One Issue

Apply this test *before* creating a parent + sub-issues (procedure `set-parent`), and when
auditing existing flat issues or over-decomposed trees. **The default is one issue**; sub-issues
must earn their keep.

A *sub-issue* is GitHub's native parent/child link (the **Parent issue** and **Sub-issues
progress** fields are already on the board). It is a heavier structure than a Markdown task-list
checklist inside a single issue. Reach for it only when the checklist cannot carry the work.

**PROMOTE** a single task to a parent issue + sub-issues when MOST of these hold:

| # | Signal |
|---|---|
| P1 | A piece is independently assignable to another owner/agent. |
| P2 | A piece needs its own status / review / PR. |
| P3 | Pieces span repos or span sprints. |
| P4 | The parent is too broad to close in one pass. |
| P5 | You need dependency / sequencing visibility at the board level. |

**KEEP** as one issue (checklist, or nothing) when:

| # | Signal |
|---|---|
| K1 | Pieces are acceptance criteria of one deliverable, one owner, one PR. |
| K2 | A piece is minutes of work needing no independent tracking. |
| K3 | The whole fits one sprint + one owner. |
| K4 | Splitting would create shallow, context-poor shards. |

**Redline filter (overrides the generic rule).** Sprint Conventions mandate splitting **only
when work won't fit in one week** (→ triggers P3). At solo-founder scale the cross-person wins
(P1–P3) are largely *theoretical* — there is one implementer. So sub-issues earn their keep
**only where they stop something falling through the cracks on the critical path**: a multi-week
deploy chain, a dependency fan-out that must be sequenced, or work that genuinely hands off
between the founder and an external/Tier-1 gate. When P1–P5 and K1–K4 are evenly matched, the
Redline filter breaks the tie toward **keep flat**.

**Sources:** Sprint Conventions — `docs/product/operations/cadences.md` → *Sprint Conventions*
("Tasks do not cross sprint boundaries… must be split into sub-tasks"). GitHub sub-issues are
the native mechanism for parent/child decomposition (Issues sub-issues feature, GA 2025).
Founder-accepted decision criteria, Sprint-2 sub-issue analysis, 2026-06-09.

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

### 6. set-dependencies (native issue dependencies)

Use GitHub's **native issue dependencies** (GA 2025-08-21) for "blocked by" / "blocking"
relationships — **not** the legacy `Depends on` custom text field. Native dependencies render
a **Blocked** badge on the board and support `is:blocked` / `blocked-by:<n>` / `blocking:<n>`
filters. The legacy `Depends on` / `Blocked by` text fields are deprecated for new tasks; leave
them blank.

**Direction:** POST to the *blocked* issue, naming the issue that blocks it.
**Scope:** same-repo only — cross-repo dependencies are not supported. Max 50 links per type.
**Auth:** the `repo` scope is sufficient (no extra scope needed).
**Internal-id gotcha:** the body field is `issue_id` — the **internal numeric database id**, NOT
the issue number. Fetch it first and send it as a typed integer (`gh api -F`, not `-f`, or the
API returns `422 not of type integer`).

```sh
REPO=redmarklogic/redline
# 1. resolve the BLOCKER's internal id (issue #4 here)
BLOCKER_ID=$(gh api repos/$REPO/issues/4 --jq .id)
# 2. mark the BLOCKED issue (#51) as blocked_by the blocker
gh api --method POST "repos/$REPO/issues/51/dependencies/blocked_by" -F "issue_id=$BLOCKER_ID"
# list / remove
gh api "repos/$REPO/issues/51/dependencies/blocked_by"                       # GET list
gh api --method DELETE "repos/$REPO/issues/51/dependencies/blocked_by/$BLOCKER_ID"
```

**Roadmap/Gantt caveat:** the Projects Roadmap view does **not** auto-sequence the Gantt from
dependencies — it orders bars by the **Start date / Target date** fields. Native dependencies
drive the Blocked badge and filters only. To make the Gantt read left-to-right in execution
order, set `start_date` / `target_date` along the dependency chain *in addition to* the
blocked_by links.

---

### 7. set-parent (native sub-issues)

Promote a flat issue into a parent + children using GitHub's **native sub-issues** (the
**Parent issue** / **Sub-issues progress** fields already exist on the board). Apply the
**Structuring Doctrine** above first — do not decompose work that K1–K4 say should stay flat.

**Direction:** POST to the *parent* issue, naming the child to nest under it.
**Internal-id gotcha:** the body field is `sub_issue_id` — the child's **internal numeric
database id**, NOT the issue number. Same trap as `set-dependencies`: fetch it first and send it
as a typed integer (`gh api -F`, not `-f`, or the API returns `422 not of type integer`).

```sh
REPO=redmarklogic/redline
PARENT=89
# nest child #63 under parent #89
CHILD_ID=$(gh api repos/$REPO/issues/63 --jq .id)          # internal id, not the number
gh api --method POST "repos/$REPO/issues/$PARENT/sub_issues" -F "sub_issue_id=$CHILD_ID"
# verify from the child side / read parent progress
gh api graphql -f query='query($o:String!,$r:String!,$n:Int!){repository(owner:$o,name:$r){issue(number:$n){parent{number}}}}' -F o=redmarklogic -F r=redline -F n=63
gh api repos/$REPO/issues/$PARENT --jq '.sub_issues_summary'   # {total, completed, percent_completed}
# remove a sub-issue link (does NOT close the child)
gh api --method DELETE "repos/$REPO/issues/$PARENT/sub_issue" -F "sub_issue_id=$CHILD_ID"
```

A child may have only one parent; re-parenting moves the link rather than duplicating it.
Re-parenting changes **no issue body** — it sets only the parent/child relationship.

---

### 8. archive-item

Remove an item from the board view. Does NOT close or delete the underlying GitHub Issue.
PM-only write; Founder may also call directly.

**Guards**: G1, G2, G7

```python
result = delete_task(item_id, config)
# The issue at result.issue_url remains open in redmarklogic/redline
```

To close the issue after archiving, call `gh issue close <number>` separately.

---

### 9. resolve-config

Resolve and cache project field and option node IDs. Writes `project_config.json`.
Run when the board schema changes (new field, renamed option) using `force_refresh=True`.

```python
# First-time setup or after schema change
config = resolve_project_config(
    project_number=N,
    owner="redmarklogic",
    force_refresh=True,
)
# Commit .agents/tools/github_projects/project_config.json after this runs
```

---

### 10. sync-this-week

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

### 11. seed-backlog

Import open specs as parent issues in Backlog. Run once per spec batch.

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
| Passing the issue *number* (or a string) to the dependencies or sub-issues API | `422 ... not of type integer` | Send the internal DB `id` (`gh api .../issues/N --jq .id`) as a typed integer via `gh api -F` — `issue_id` for `set-dependencies`, `sub_issue_id` for `set-parent` |
| Creating a parent + sub-issues when K1–K4 hold | Shallow, context-poor shards; tracking overhead with no payoff | Apply the Structuring Doctrine; default to one issue with a checklist |
| Recording dependencies in the `Depends on` text field | No Blocked badge, no `is:blocked` filter | Use native `set-dependencies` (procedure 6); leave the legacy text field blank |
