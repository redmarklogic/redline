# NotebookLM CLI — Detailed Reference

NotebookLM access is **CLI-only** via the [`nlm`](https://github.com/jacob-bd/notebooklm-mcp-cli)
command. There is no MCP server in this project (removed per ADR-016, prefer CLI over MCP).

## Inputs

- A terminal with the `nlm` CLI installed and authenticated

## Outputs

- Authenticated `nlm` CLI access to NotebookLM

## Out of Scope

- Query writing and prompt design (`rag-prompting`)
- Research workflow orchestration (`redline-research`)
- Notebook registry (`.agents/skills/redline-research/register.json`)

## File Upload Rule

> **Never refuse a file upload based on assumed format limitations.**
> `nlm source add --file` accepts at minimum: PDF, TXT, audio, and **video (MP4)**.
> When asked to upload any file, attempt the upload and let NotebookLM reject it if
> the format is truly unsupported. Do not preemptively block the user.

## Commands

| Command | Purpose |
| --- | --- |
| `nlm notebook query <id> "<question>"` | Query a notebook (primary use case). Scope to specific sources with `--source-ids <id,id>`. Add `--json` for parseable output. |
| `nlm notebook list --json` | List all notebooks (find notebook IDs) |
| `nlm notebook get <id>` | Get notebook details and source list |
| `nlm notebook describe <id>` | AI-generated notebook summary and suggested topics |
| `nlm source list <notebook>` | List sources in a notebook |
| `nlm source describe <source-id>` | AI-generated per-source summary and keywords |
| `nlm notebook create "<title>"` | Create a notebook — **Knowledge Operator only** (migration / provisioning) |
| `nlm source add <notebook> --url/--text/--file/--youtube/--drive` | Add a source — **Knowledge Operator only** (library ingestion). Verified file types: PDF, TXT, audio (MP3/M4A/WAV), **video (MP4)** |
| `nlm source delete <source-id> --confirm` | Remove a source — **Knowledge Operator only** (deduplication / file hygiene) |
| `nlm source rename <source-id> "<name>"` | Rename a source — **Knowledge Operator only** (canonical naming enforcement) |
| `nlm source stale <notebook>` / `nlm source sync <notebook> --confirm` | List / refresh stale Drive-linked sources |
| `nlm doctor` | Version, auth, and config diagnostics |

> Use `--json` on read commands when parsing output programmatically.
> `create`, `add`, `delete`, `rename` and `sync` are restricted to the Knowledge Operator.

## Procedure

### Step 1 — Install

Check whether `nlm` is available:

```powershell
nlm --version
```

If not installed:

```powershell
rtk uv tool install notebooklm-mcp-cli
```

This installs the `nlm` CLI. (The package also ships a `notebooklm-mcp` server executable;
we do **not** use it — CLI only.)

### Step 2 — Authenticate

```powershell
nlm login --check
```

If not authenticated:

1. Run `nlm login` in a terminal (opens browser).
2. Sign in to Google. Cookies saved locally (never committed to VCS).
3. Confirm: `nlm login --check` returns success.

Named profiles: `nlm login --profile work`, then pass `--profile work` to subsequent
commands. Switch the active default with `nlm login switch <profile>`. Diagnostics: `nlm doctor`.

### Step 3 — Query

Use `nlm notebook list --json` to find notebook IDs, then `nlm notebook query`.

**REQUIRED SUB-SKILL:** Load `rag-prompting` before writing any query.

### Step R1 — Check the register

Read `.agents/skills/redline-research/register.json` and check if any entry's `url` field matches the provided URL.
Also run `nlm notebook list --json` to verify the notebook exists in the user's NotebookLM account. If
the notebook is already registered, report that it exists and stop.

### Step R2 — Find the notebook ID and query for purpose

Run `nlm notebook list --json` to find the notebook. Match by URL or name. Note the `notebook_id`.

Then run `nlm notebook query <notebook_id>` with the following question:

```text
Explain for the uninitiated. Define any specialist term or acronym the
first time it appears. Keep citations. Avoid ambiguity.

What is the purpose of this notebook? What topics does it cover, what
kind of knowledge or documents does it contain, and when would someone
consult it?
```

From the answer extract: an `id` (kebab-case slug), a `name`, a one-paragraph `description`,
a `topic_area` (match an existing area from `register.json` or propose a new one), a flat
`topics` list (5-10), `content_types`, and 3-5 `use_cases`. Set `access` to `"open"` unless
the user specifies otherwise (e.g. `"advisory-board-only"`).

### Step R3 — Append to `.agents/skills/redline-research/register.json`

Append a new JSON object to the array in `.agents/skills/redline-research/register.json` with all fields from Step R2 plus
`"added": "YYYY-MM-DD"`. Ensure the JSON remains valid.

### Step R4 — Confirm

Report to the user:

- Notebook name and ID assigned.
- A one-sentence purpose summary.
- Confirmation that the entry was added to `.agents/skills/redline-research/register.json`.

Do **not** ask the user to provide any metadata — derive everything from the notebook query.

## Add Notebook to Register

When the user provides a NotebookLM URL and asks to add it to the register or knowledge base,
follow steps R1–R4 above in order. Do **not** skip steps or ask for metadata — discover
it from the notebook itself.

The canonical register is `.agents/skills/redline-research/register.json`. Every
notebook used by any skill (including `redline-research`) is listed there.

## Post-Source-Change Rule (mandatory)

After **any** operation that adds, removes, or renames a source in a notebook
(`nlm source add`, `nlm source delete`, `nlm source rename`), the Knowledge Operator **must** update
`<library-root>\index-notebooklm.xlsx` before the task is considered done.

Trigger: load the `notebooklm-index` skill and run the **single-notebook upsert**
for the affected notebook using its UUID. Do not run a full sync — upsert only the
notebook that changed.

This rule applies even when the source operation was part of a larger task
(e.g. library ingestion). The index update is the final step, not optional.

## Troubleshooting

See [`troubleshooting.md`](../troubleshooting.md) for known failure modes
and fixes (symptom-based lookup).

## Tips

- Notebook names are case-sensitive; match names exactly when querying.
- Authentication cookies expire every 2-4 weeks. Re-run `nlm login` when queries fail.
- Use `nlm doctor` to diagnose installation, auth, and config issues.
- Free-tier rate limit is ~50 queries/day.

## References

- [notebooklm-mcp-cli GitHub repo](https://github.com/jacob-bd/notebooklm-mcp-cli)
- [CLI Guide](https://github.com/jacob-bd/notebooklm-mcp-cli/blob/main/docs/CLI_GUIDE.md)
- [Authentication guide](https://github.com/jacob-bd/notebooklm-mcp-cli/blob/main/docs/AUTHENTICATION.md)
- Always confirm exact flags with `nlm <command> --help` — the published docs can lag the installed binary.
