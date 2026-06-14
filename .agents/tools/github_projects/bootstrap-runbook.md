# GitHub Projects Board Bootstrap Runbook

Covers Phases 0 and 1 from `specs/013-github-projects-skill/spec.md`.

**Pre-condition**: `redmarklogic` org exists and `harell` has Owner-level access.

---

## Phase 0 — Transfer Repo to redmarklogic

**Why first**: The board owner cannot be changed after creation. Starting under the org
avoids a full rebuild if the repo moves later.

1. Open `https://github.com/harell/redline/settings`
2. Scroll to **Danger Zone → Transfer repository**
3. Enter `redmarklogic` as the receiving organisation; confirm with repo name
4. GitHub sends a confirmation email — approve it
5. Verify: `gh repo view redmarklogic/redline --json name,owner`
   Expected: `{"name": "redline", "owner": {"login": "redmarklogic"}}`
6. Update local remote:
   ```sh
   git remote set-url origin https://github.com/redmarklogic/redline.git
   git fetch origin
   ```

---

## Phase 1 — Board Bootstrap

### 1.1 — Authenticate with project scope

```sh
gh auth refresh -s project
gh auth status   # confirm 'project' appears in scopes
```

### 1.2 — Create the project

```sh
gh project create \
  --owner redmarklogic \
  --title "Redline" \
  --format json
# Note the project number N from the output
```

### 1.3 — Add custom fields

Run each command, substituting `N` for the project number.

```sh
# Type (single-select)
gh project field-create N \
  --owner redmarklogic \
  --name "Type" \
  --data-type SINGLE_SELECT \
  --single-select-options "Feature,Design,Content,Ops,Research"

# Sprint (iteration — GitHub creates it as an iteration field)
gh project field-create N \
  --owner redmarklogic \
  --name "Sprint" \
  --data-type ITERATION

# Agent (single-select — closed set matching AgentName in schema.py)
gh project field-create N \
  --owner redmarklogic \
  --name "Agent" \
  --data-type SINGLE_SELECT \
  --single-select-options "Kabilan,Mark,Matt,John,Peter,Ron,Graeme,Linda,Harriet,Founder"

# Start date (date field)
gh project field-create N \
  --owner redmarklogic \
  --name "Start date" \
  --data-type DATE

# Target date (date field)
gh project field-create N \
  --owner redmarklogic \
  --name "Target date" \
  --data-type DATE

# Blocked by (text field)
gh project field-create N \
  --owner redmarklogic \
  --name "Blocked by" \
  --data-type TEXT

# Source (text field)
gh project field-create N \
  --owner redmarklogic \
  --name "Source" \
  --data-type TEXT

# Depends on (text field — GitHub has no native dependency field)
gh project field-create N \
  --owner redmarklogic \
  --name "Depends on" \
  --data-type TEXT
```

> `Status` is a built-in field created automatically by GitHub Projects.
> Rename the default columns to match the required schema (next step).

### 1.4 — Configure Status columns (GitHub UI)

Navigate to `https://github.com/orgs/redmarklogic/projects/N` and configure Status options:

Required columns (in order): **Backlog**, **In Progress**, **Blocked**, **To Review**, **Done**

Delete any default columns that don't match (e.g., "Todo", "No Status").

### 1.5 — Enable built-in automations (GitHub UI)

In the project settings under **Workflows**, enable:

| Trigger | Action |
|---|---|
| Pull request opened | Set item status to **To Review** |
| Pull request merged | Set item status to **Done** |
| Item closed | Set item status to **Done** |
| Item reopened | Set item status to **In Progress** |

### 1.6 — Create milestones in redmarklogic/redline

```sh
gh api repos/redmarklogic/redline/milestones \
  --method POST \
  --field title="KR1 — 50 verified-email signups" \
  --field due_on="2026-08-01T00:00:00Z" \
  --field description="Linked to docs/product/strategy/okrs/2026-h2.md"

gh api repos/redmarklogic/redline/milestones \
  --method POST \
  --field title="KR2 — 15 qualified discovery conversations" \
  --field due_on="2026-09-01T00:00:00Z" \
  --field description="Linked to docs/product/strategy/okrs/2026-h2.md"

gh api repos/redmarklogic/redline/milestones \
  --method POST \
  --field title="Kill-horizon" \
  --field due_on="2026-09-01T00:00:00Z" \
  --field description="Linked to docs/product/strategy/okrs/2026-h2.md"

gh api repos/redmarklogic/redline/milestones \
  --method POST \
  --field title="KR5 — Wedge unit economics ≤ \$1.00" \
  --field due_on="2026-11-01T00:00:00Z" \
  --field description="Linked to docs/product/strategy/okrs/2026-h2.md"
```

### 1.7 — Create saved views (GitHub UI)

In the project settings or the board UI, create two saved views:

| View name | Filter | Default? |
|---|---|---|
| Engineering | `-type:Ops` | Yes |
| Ops | `type:Ops` | No |

### 1.8 — Resolve and commit project config

```python
from github_projects import resolve_project_config

config = resolve_project_config(
    project_number=N,       # replace N with the actual project number
    owner="redmarklogic",
    force_refresh=True,
)
print(config.model_dump_json(indent=2))
```

Commit `project_config.json`:
```sh
git add .agents/tools/github_projects/project_config.json
git commit -m "chore(board): add project_config.json for redmarklogic project N"
```

### 1.9 — Verify

```sh
# Board is visible
gh project list --owner "redmarklogic"

# Fields are populated
gh project field-list N --owner redmarklogic --format json | jq '.fields[].name'
```

Expected fields: `Status`, `Title`, `Assignees`, `Labels`, `Linked pull requests`,
`Milestone`, `Repository`, `Type`, `Sprint`, `Agent`, `Start date`, `Target date`,
`Blocked by`, `Source`, `Depends on`

---

## Phase 3 — Seed Backlog (after board is live)

Use the `seed-backlog` procedure in `.agents/skills/github-projects/SKILL.md`.
Verify the board is empty of duplicates before running.
