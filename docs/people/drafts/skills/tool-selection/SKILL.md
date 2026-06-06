---
name: tool-selection
description: Use when an agent must decide which CLI (gh, gws, gcloud) or direct API call to use for a given operation. Routes GitHub, Google Workspace, and GCP operations to the correct tool.
---

# Tool Selection — CLI and API Routing

## Boundary Contract

### Inputs
- An operation the agent needs to perform (e.g., "list open PRs", "send email", "create Cloud SQL instance")

### Outputs
- The correct tool and exact command pattern to use

### Out of Scope
- Authentication setup procedures (see individual tool docs)
- Anything requiring a human UI (GitHub Actions approval gates, GCP Console billing setup)
- Operations not covered by any CLI — route those to direct REST/GraphQL API calls

---

## General Section — What Each CLI Covers

| CLI | Domain | Scope |
|---|---|---|
| `gh` | GitHub | Repos, PRs, issues, GitHub Actions runs, GitHub Projects boards, releases, gists, auth |
| `gws` | Google Workspace | Gmail, Drive, Calendar, Sheets, Docs, Chat, Admin, Apps Script |
| `gcloud` | Google Cloud Platform | Compute Engine, Cloud SQL, Cloud Run, Cloud Storage, IAM, projects, services, billing |

**Decision rule — pick the narrowest tool that fits:**
1. GitHub operation → `gh`
2. Google Workspace operation (email, files, calendar, docs) → `gws`
3. GCP infrastructure operation → `gcloud`
4. Operation unavailable in any CLI, or CLI unavailable in environment → direct API call

**Never use `gcloud` for Gmail or Drive.** `gcloud` is infrastructure; `gws` is productivity/collaboration.

---

## Concrete Routing Table

### GitHub Operations (`gh`)

| Operation | Command |
|---|---|
| List open PRs | `gh pr list --state open --repo <owner>/<repo>` |
| View a PR | `gh pr view <number>` |
| Create a PR | `gh pr create --title "..." --body "..."` |
| Merge a PR | `gh pr merge <number> --squash` |
| Check PR CI status | `gh pr checks <number>` |
| Create an issue | `gh issue create --title "..." --body "..."` |
| List issues | `gh issue list --state open` |
| View an issue | `gh issue view <number>` |
| Close an issue | `gh issue close <number>` |
| Clone a repo | `gh repo clone <owner>/<repo>` |
| View repo | `gh repo view <owner>/<repo>` |
| List Actions runs | `gh run list` |
| View a run | `gh run view <run-id>` |
| Watch a run live | `gh run watch <run-id>` |
| Re-run failed jobs | `gh run rerun <run-id> --failed` |
| List releases | `gh release list` |
| Create a release | `gh release create <tag> --notes "..."` |
| Check auth status | `gh auth status` |

#### GitHub Projects (board operations)

**Critical:** GitHub Projects requires the `project` OAuth scope, which is NOT included in the default `gh auth login`. Always verify before any board write.

```sh
gh auth status          # check if 'project' appears in scopes
gh auth refresh -s project   # add project scope if missing
```

| Operation | Command |
|---|---|
| List project items | `gh project item-list <project-number> --owner <org>` |
| Add issue to project | `gh project item-add <project-number> --owner <org> --url <issue-url>` |
| Update a project field | `gh project item-edit --id <item-id> --field-id <field-id> --project-id <proj-id> --text "..."` |
| List project fields | `gh project field-list <project-number> --owner <org>` |
| Archive a project item | `gh project item-archive <project-number> --owner <org> --id <item-id>` |

> For complex field updates (custom single-select, iteration fields), prefer the Python tool at `.agents/tools/github_projects/` — it wraps the GraphQL API and handles field type resolution. See `github-projects` skill.

---

### Google Workspace Operations (`gws`)

Command pattern: `gws <service> <resource> <method> [flags]`
Helper shortcuts use `+` prefix: `gws gmail +send`, `gws drive +upload`

**Auth setup (once per environment):**
```sh
gws auth setup    # automated, requires gcloud installed
gws auth login    # manual OAuth fallback
```

> **Shell requirement:** `gws --params` uses single-quoted JSON. Use Bash, not PowerShell — PS5.1 mangles curly-brace quoting and the command fails with "key must be a string".

| Operation | Command |
|---|---|
| Unread inbox summary | `gws gmail +triage` |
| List Gmail inbox | `gws gmail users messages list --params '{"labelIds":["INBOX"],"maxResults":20}'` |
| Read a message (extract body/headers) | `gws gmail +read --message-id <id>` |
| Send email | `gws gmail +send --to user@example.com --subject "Subject" --body "Body"` |
| Reply to email | `gws gmail +reply --message-id <id> --body "..."` |
| Reply-all | `gws gmail +reply-all --message-id <id> --body "..."` |
| Forward a message | `gws gmail +forward --message-id <id> --to user@example.com` |
| Watch inbox (streaming) | `gws gmail +watch` |
| List Drive files | `gws drive files list --params '{"pageSize":20}'` |
| Upload a file | `gws drive +upload --file path/to/file.pdf` |
| Share a file | `gws drive permissions create --params '{"fileId":"...","role":"reader","type":"user"}'` |
| List calendar events | `gws calendar events list --params '{"calendarId":"primary","timeMin":"..."}'` |
| Create calendar event | `gws calendar +insert --summary "Meeting" --start "2026-06-10T10:00:00Z" --end "..."` |
| Read a Sheet | `gws sheets +read --spreadsheet <id> --range "Sheet1!A1:D10"` |
| Append to a Sheet | `gws sheets +append --spreadsheet <id> --values "row data"` |
| Read a Doc | `gws docs documents get --params '{"documentId":"..."}'` |
| Write to a Doc | `gws docs +write --document <id> --content "..."` |
| Send Chat message | `gws chat +send --space <space-id> --text "..."` |
| List Workspace users (Admin) | `gws admin directory users list --params '{"domain":"example.com"}'` |

**Output format flag:** append `--format json` (or `table`, `yaml`, `csv`) to any command.
**Paginate all results:** append `--page-all` for automatic pagination as NDJSON.
**Dry run:** append `--dry-run` to preview without executing.

---

### GCP Infrastructure Operations (`gcloud`)

| Operation | Command |
|---|---|
| **Cloud SQL — create instance** | `gcloud sql instances create <name> --database-version=POSTGRES_15 --tier=db-f1-micro --region=<region>` |
| **Cloud SQL — list instances** | `gcloud sql instances list` |
| **Cloud SQL — describe instance** | `gcloud sql instances describe <name>` |
| **Cloud SQL — create database** | `gcloud sql databases create <db-name> --instance=<instance-name>` |
| **Cloud SQL — list databases** | `gcloud sql databases list --instance=<instance-name>` |
| **Cloud SQL — connect** | `gcloud sql connect <instance-name> --user=postgres` |
| List Compute instances | `gcloud compute instances list` |
| Create Compute instance | `gcloud compute instances create <name> --zone=<zone> --machine-type=<type> --image-family=debian-12` |
| List Cloud Run services | `gcloud run services list --region=<region>` |
| Deploy to Cloud Run | `gcloud run deploy <service> --image=<image> --region=<region>` |
| List Cloud Storage buckets | `gcloud storage buckets list` |
| Create bucket | `gcloud storage buckets create gs://<name> --location=<region>` |
| List IAM service accounts | `gcloud iam service-accounts list` |
| Create service account | `gcloud iam service-accounts create <name> --display-name="..."` |
| Bind IAM role | `gcloud projects add-iam-policy-binding <project-id> --member=serviceAccount:<email> --role=roles/<role>` |
| List enabled APIs | `gcloud services list --enabled` |
| Enable an API | `gcloud services enable <api>.googleapis.com` |
| Set active project | `gcloud config set project <project-id>` |
| Check auth | `gcloud auth list` |
| Check quotas/billing | `gcloud projects describe <project-id>` (billing via Console or `gcloud billing accounts list`) |

---

## When to Use Direct API Calls Instead

Use direct REST or GraphQL API when:
- The CLI is not installed in the environment (check with `which gh` / `which gws` / `which gcloud`)
- The operation requires capabilities not exposed by the CLI (e.g., GitHub GraphQL mutations for Projects field types not supported by `gh project item-edit`)
- Rate-limit or batching requirements exceed CLI ergonomics
- You are inside a Python tool that already has an authenticated HTTP client

**Never invent CLI flags.** If `--help` does not list the flag, use a direct API call or the Python tool wrapper.

---

## Common Mistakes

| Mistake | Consequence | Fix |
|---|---|---|
| Using `gcloud` for Gmail | `gcloud` has no Gmail commands — fails immediately | Use `gws gmail` |
| Using `gh` for Google Drive | No such capability in `gh` | Use `gws drive` |
| Running `gh project item-edit` without `project` scope | Authentication error | Run `gh auth refresh -s project` first |
| Using `gws` for Cloud SQL | `gws` covers Workspace productivity, not GCP infra | Use `gcloud sql` |
| Omitting `--page-all` on `gws` list commands | Returns only first page (default 10–20 items) | Add `--page-all` for full result sets |
| Hardcoding `userId` in Gmail commands | Breaks on service accounts | Use `me` as userId for authenticated user |
| Using `gws` without verifying OAuth scope coverage | Unverified apps hit ~25-scope limit; some commands fail silently | Run `gws auth setup` and add test user in OAuth consent screen |

---

## Quick Decision Tree

```
What service?
├── GitHub (repos, PRs, issues, Actions, Projects) → gh
│   └── Projects board write? → check gh auth status for 'project' scope first
├── Google Workspace (Gmail, Drive, Calendar, Sheets, Docs, Chat) → gws
│   └── Email? → gws gmail
│   └── Files? → gws drive
│   └── Spreadsheet? → gws sheets
│   └── Calendar? → gws calendar
└── GCP infrastructure (databases, compute, storage, IAM, Run) → gcloud
    └── Cloud SQL? → gcloud sql
    └── VM? → gcloud compute
    └── Serverless? → gcloud run
```
