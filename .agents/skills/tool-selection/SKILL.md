---
name: tool-selection
description: Use when an agent must decide which CLI (gh, gws, gcloud) or direct API call to use for a given operation, or which agent-orchestration tier (solo, parallel dispatch, dynamic workflow) fits a fan-out task. Routes GitHub, Google Workspace, and GCP operations to the correct tool, and fan-out work to the correct orchestration tier. Also defines the binding CLI pre-flight authentication check and auth-failure protocol — load BEFORE first use of any external CLI in a session.
---

# Tool Selection — Routing

This skill routes two independent decisions:

1. **CLI / API routing** — which tool (`gh`, `gws`, `gcloud`, or a direct API call) performs an operation. The bulk of this skill.
2. **Agent-orchestration tier** — how many agents hold a task (solo, parallel dispatch, or dynamic workflow). A separate axis, at the end.

Pick the relevant axis; they do not interact.

## Boundary Contract

### Inputs
- An operation to perform (e.g. "list open PRs", "send email", "create Cloud SQL instance"), OR
- A fan-out task to size (e.g. "audit every endpoint", "fix 12 failing tests")

### Outputs
- The correct tool + exact command pattern (axis 1), OR
- The correct orchestration tier + which skill/pattern to apply (axis 2)

### Out of Scope
- Anything requiring a human UI (GitHub Actions approval gates, GCP Console billing setup)
- Operations not covered by any CLI — route those to direct REST/GraphQL API calls

---

## CLI Pre-Flight and Auth-Failure Protocol (BINDING)

Single source of truth for what every agent does before and during CLI use. JDs and
other skills point here — do not restate or override this protocol elsewhere.

### Rule 1 — Pre-flight check

Before the **first** use of a CLI in a session, verify it is installed and authenticated.
Each `procedures/*-routing.md` file opens with the exact pre-flight commands for its CLI.
For CLIs without a procedure file (e.g. `nlm`), use that CLI's own skill/doc for the check.

### Rule 2 — Never skip the CLI over auth (HARD RULE)

A missing or broken authentication is **never** a reason to abandon the CLI, silently
fall back to another method (MCP, direct API, manual instructions to the user), or skip
the operation. Auth problems are resolved, not routed around.

### Rule 3 — Failure triage

When a CLI call fails:

```text
Is it an authentication/authorization problem?
(auth errors, expired tokens, missing scopes, "login required", 401/403)
├── YES → try to fix it yourself using the remediation patterns in the
│         CLI's procedure file (e.g. `gh auth refresh -s <scope>`,
│         `gws auth setup`, `gcloud auth login --update-adc`).
│   ├── Fixed → re-run the original command and continue.
│   └── Needs human interaction (browser OAuth consent, button click,
│       2FA) → STOP and ask the user to complete that exact step;
│       give them the command/URL, wait, then continue with the CLI.
└── NO → STOP. Report the failing command, the full error, and what you
         ruled out. Do not improvise a workaround without the user.
```

### Rule 4 — Escalation wording

When asking the user to complete an auth step, state: which CLI, the exact command they
must run or URL to visit, what to click/approve, and that you will resume the CLI
operation once they confirm.

---

## Axis 1 — CLI / API Routing

### What each CLI covers

| CLI | Domain | Scope |
|---|---|---|
| `gh` | GitHub | Repos, PRs, issues, GitHub Actions runs, GitHub Projects boards, releases, gists, auth |
| `gws` | Google Workspace | Gmail, Drive, Calendar, Sheets, Docs, Chat, Admin, Apps Script |
| `gcloud` | Google Cloud Platform | Compute Engine, Cloud SQL, Cloud Run, Cloud Storage, IAM, projects, services, billing |

### Decision rule — pick the narrowest tool that fits

1. GitHub operation → `gh` — commands: `procedures/github-routing.md`
2. Google Workspace operation (email, files, calendar, docs) → `gws` — commands: `procedures/gws-routing.md`
3. GCP infrastructure operation → `gcloud` — commands: `procedures/gcloud-routing.md`
4. Operation unavailable in any CLI, or CLI unavailable in environment → direct API call (see below)

**Never use `gcloud` for Gmail or Drive.** `gcloud` is infrastructure; `gws` is productivity/collaboration.

### Quick decision tree

```text
What service?
├── GitHub (repos, PRs, issues, Actions, Projects) → gh
│   └── Projects board write? → check gh auth status for 'project' scope first
├── Google Workspace (Gmail, Drive, Calendar, Sheets, Docs, Chat) → gws
│   └── Email? → gws gmail      └── Files? → gws drive
│   └── Spreadsheet? → gws sheets  └── Calendar? → gws calendar
└── GCP infrastructure (databases, compute, storage, IAM, Run) → gcloud
    └── Cloud SQL? → gcloud sql  └── VM? → gcloud compute  └── Serverless? → gcloud run
```

Concrete command tables live in the `procedures/` files named above — load the one for the resolved tool.

### When to use direct API calls instead

Use direct REST or GraphQL API when:
- The CLI is not installed in the environment (check with `which gh` / `which gws` / `which gcloud`)
- The operation requires capabilities not exposed by the CLI (e.g. GitHub GraphQL mutations for Projects field types not supported by `gh project item-edit`)
- Rate-limit or batching requirements exceed CLI ergonomics
- You are inside a Python tool that already has an authenticated HTTP client

**Never invent CLI flags.** If `--help` does not list the flag, use a direct API call or the Python tool wrapper.

### Common mistakes (axis 1)

| Mistake | Consequence | Fix |
|---|---|---|
| Using `gcloud` for Gmail | `gcloud` has no Gmail commands — fails immediately | Use `gws gmail` |
| Using `gh` for Google Drive | No such capability in `gh` | Use `gws drive` |
| Using `gws` for Cloud SQL | `gws` covers Workspace productivity, not GCP infra | Use `gcloud sql` |
| Omitting `--page-all` on `gws` list commands | Returns only first page (default 10–20 items) | Add `--page-all` for full result sets |
| Hardcoding `userId` in Gmail commands | Breaks on service accounts | Use `me` as userId for authenticated user |
| Skipping the CLI because auth fails | Violates the binding protocol above | Triage per Rule 3 — fix auth or escalate, never route around |

Auth-specific failures (missing scopes, expired tokens) are covered by the Pre-Flight
and Auth-Failure Protocol above and the pre-flight blocks in each procedure file.

---

## Axis 2 — Agent Orchestration Tier (Solo vs. Parallel Dispatch vs. Workflow)

A separate axis from CLI routing: once you know *which tool*, decide *how many agents* hold the work. Three tiers, escalating in scale and token cost. **Pick the lowest tier that fits — each step up multiplies token spend.**

| Tier | What it is | Holds the plan | Use when |
|---|---|---|---|
| **Solo** | Do it yourself, no subagents | You, this turn | One context can hold the whole task |
| **Parallel dispatch** | Fan out via Agent tool / `dispatching-parallel-agents` | You, turn by turn; results land in your context | 2–~8 independent tasks, no shared state, results fit one context |
| **Dynamic workflow** | A JS script the runtime executes (background, resumable) | The script; intermediate results stay in script variables | 10+ independent agents, OR a repeatable adversarial-verify / multi-angle pattern, OR a cross-file sweep too large for one context |

### Decision gate

```text
Is the work a single pass one context can hold?
├── yes → SOLO
└── no → Are the sub-tasks independent (no shared mutable state)?
    ├── no → SOLO (sequential reasoning; shared state can't fan out safely)
    └── yes → How many, and is the orchestration worth codifying?
        ├── few (2–~8), one-off, results fit context → PARALLEL DISPATCH
        │                                              (dispatching-parallel-agents)
        └── many (10+) OR repeatable adversarial/multi-angle pattern
            OR cross-file sweep exceeding one context → DYNAMIC WORKFLOW
```

**Escalate to a workflow ONLY when at least one holds:**
- **Scale** — tens to hundreds of independent agents (codebase-wide sweep, large migration).
- **Adversarial verification** — findings must be independently cross-checked before being reported, or a plan drafted from several angles and weighed. High cost-of-wrong-answer.
- **Codified + repeatable** — the orchestration runs identically every time and is worth saving as a `/command`.

**Do NOT escalate to a workflow when:**
- The task is a single pass, or needs mid-run human sign-off (workflows forbid mid-run input — split each gate into its own workflow).
- The work is judgment, not scale (strategy, PRDs, design, prose) — these stay solo regardless of length.
- You haven't gauged spend. Run on a small slice first (one directory, one narrow question); workflows are a deliberate token multiplier, never a default.

**Triggering a workflow:** include `ultracode` in the prompt, or ask in plain words ("use a workflow"). Requires Dynamic Workflows enabled in `/config`. Bundled: `/deep-research`. Save a good run as a `/command` for reuse.

**Where saved workflows live** (created on save, not pre-built):

| Scope | Path | Visibility |
|---|---|---|
| **Project** | `.claude/workflows/` | Committed, shared with everyone who clones the repo — treat like a skill |
| **Personal** | `~/.claude/workflows/` | Yours only, available in every project |

Project workflows are shared orchestration — **commit them** (same rationale as skills). If a project and personal workflow share a name, the project one wins.

**Which workflow shape?** Once the gate says "workflow", pick the pattern that fits — see `procedures/workflow-patterns.md`.

### Spec-Kit `[P]`-block trigger

Spec-Kit's `tasks.md` already marks parallelizable tasks with **`[P]`** — its native, upgrade-safe fan-out signal. **Do not teach speckit-plan/speckit-tasks about workflows** (vendor-generated, edit via `.specify/extensions.yml` only). Instead, consume the signal at **implement** time:

- When `speckit-implement` reaches a block of `[P]` tasks, run *this* gate on that block. Count of independent `[P]` tasks + repeatable/adversarial nature → solo / parallel dispatch / workflow.
- Execution strategy is an **implement-time** decision, not a plan-time one. Planning stays execution-agnostic; the `[P]` marker carries the only signal needed.
