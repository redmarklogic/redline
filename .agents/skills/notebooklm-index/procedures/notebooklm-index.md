# Notebooklm Index — Detailed Reference

### Inputs
- A NotebookLM notebook URL or UUID, **or** no input (triggers full sync)

### Outputs
- Updated `<library-root>\index-notebooklm.xlsx` (worksheets: `notebooks`, `sources`)
- Per-notebook status report

### Out of Scope
- Querying notebooks for research (`redline-research`)
- CLI setup or authentication (`notebooklm-mcp`)
- Physical library indexing (`library-management`)
- Writing notes into the notebook itself (out of scope)

### Upsert a notebook (add or overwrite)

```powershell
echo '{"index_path": "<library-root>\\index-notebooklm.xlsx",
       "operation": "upsert",
       "notebook": {"notebook_id": "<UUID>",
                    "title": "<title>",
                    "url": "https://notebooklm.google.com/notebook/<UUID>",
                    "source_count": <N>,
                    "summary": "<summary>",
                    "suggested_topics": "<topic1 | topic2>"},
       "sources": [{"source_id": "<UUID>",
                    "source_title": "<title>",
                    "source_summary": "<summary>",
                    "source_keywords": "<kw1 | kw2>"}]}' |
.venv\Scripts\python .agents/tools/library/upsert_notebooklm_index.py
```

### the Product Manager a notebook as deleted

```powershell
echo '{"index_path": "<library-root>\\index-notebooklm.xlsx",
       "operation": "mark_deleted",
       "notebook_id": "<UUID>"}' |
.venv\Scripts\python .agents/tools/library/upsert_notebooklm_index.py
```

### Rules for this tool

- `index_path` is **required** in every payload — always pass the absolute path explicitly.
- Use `.venv\Scripts\python`, not a bare `python`, to ensure the correct environment.
- The script exits with code 1 and an `ERROR:` message on `stderr` if `index_path` is missing or the file does not exist.
- Always check the printed result for the row counts to confirm success.

---

### Single notebook (URL given)

1. `nlm notebook get` — retrieve notebook ID, title, URL, source count, and source list
2. `nlm notebook describe` — retrieve AI-generated summary and suggested topics
3. `nlm source describe` — call once per source returned by `nlm notebook get`

### Full sync (no URL given)

1. `nlm notebook list` — retrieve all notebooks
2. `nlm notebook get` — call per notebook (always, for diff check)
3. `nlm notebook describe` — call only for **new** notebooks
4. `nlm source describe` — call only for sources not already in the index

`nlm source describe` calls may run in parallel. Do not run any other `nlm` commands.

### Worksheet: `notebooks`

| Column | Source | Format |
|---|---|---|
| `notebook_id` | `nlm notebook get` | UUID string |
| `title` | `nlm notebook get` | plain text |
| `url` | `nlm notebook get` | full URL |
| `source_count` | `nlm notebook get` | integer |
| `summary` | `nlm notebook describe` | plain text |
| `suggested_topics` | `nlm notebook describe` | pipe-separated (`topic1 \| topic2`), empty string if none |
| `last_updated` | set at index time | `YYYY-MM-DD` |
| `status` | set at index time | `active` or `deleted` |

### Worksheet: `sources`

| Column | Source | Format |
|---|---|---|
| `notebook_id` | `nlm notebook get` | UUID string (FK to `notebooks`) |
| `notebook_title` | `nlm notebook get` | plain text (denormalized) |
| `source_id` | `nlm notebook get` | UUID string |
| `source_title` | `nlm notebook get` | plain text |
| `source_summary` | `nlm source describe` | plain text |
| `source_keywords` | `nlm source describe` | pipe-separated (`kw1 \| kw2`) |

### Deleted notebooks

If `nlm notebook get` fails (notebook no longer exists):
1. Find the row in `notebooks` by `notebook_id`
2. Set `status` to `deleted`
3. Set `last_updated` to today
4. Do **not** delete rows from `sources` (preserve historical data)

## Full Sync (no URL given)

When the user says "update the index" without providing a notebook URL, run a full sync.

### Procedure

1. Call `nlm notebook list` to get all notebooks from NotebookLM
2. Read the existing `notebooks` and `sources` worksheets from the Excel index
3. Classify every notebook into one of three categories:

| Category | Condition | Action |
|---|---|---|
| **New** | In NotebookLM, not in index | Full index (steps 4a–4c) |
| **Existing** | In both NotebookLM and index | Diff check (step 5) |
| **Stale** | In index, not in NotebookLM | the Product Manager `status = deleted`, update `last_updated` |

4. **New notebooks** — full index, one at a time:
   - a. `nlm notebook get` — retrieve metadata and source list
   - b. `nlm notebook describe` — retrieve AI summary and suggested topics
   - c. `nlm source describe` — call for every source (may run in parallel)
   - d. Write notebook row + all source rows to Excel
   - e. Report: `"[notebook_title] — Successfully indexed N sources"`

5. **Existing notebooks** — diff check:
   - a. `nlm notebook get` — retrieve current source list
   - b. Compare source IDs from `nlm notebook get` against source IDs in the `sources` worksheet for that `notebook_id`
   - c. If source IDs match exactly → **skip**. Report: `"[notebook_title] — Skipped (no changes)"`
   - d. If source IDs differ:
     - Sources in notebook but **not** in index → call `nlm source describe` for each, add rows to `sources`
     - Sources in index but **not** in notebook → delete those rows from `sources`
     - Sources in both → keep existing rows unchanged (do not re-fetch)
     - Update `source_count` in the `notebooks` row (from `nlm notebook get`, already called)
     - Update `last_updated` to today
     - Do **not** re-call `nlm notebook describe` — keep existing summary
     - Write changes to Excel
     - Report: `"[notebook_title] — Updated: added X sources, removed Y sources"`

6. **Stale notebooks** — mark deleted: <!-- hook: allow -->
   - Set `status = deleted` and `last_updated` to today in `notebooks`
   - Do **not** delete source rows (preserve historical data)
   - Report: `"[notebook_title] — Marked deleted"`

7. Save to Excel **after each non-skipped notebook** (not at the end)

### Error handling

If `nlm notebook get` or `nlm source describe` fails for a specific notebook:
- Report: `"[notebook_title] — Failed: [error message]"`
- Continue to the next notebook (do not abort the full sync)

# NotebookLM Index

Index NotebookLM notebooks into a structured Excel register using the `nlm` CLI.

## Mandatory Trigger Rule

**This skill MUST be invoked immediately after any task that runs `nlm notebook create`.** Never declare a task complete if a new notebook was created without first running this skill to add it to the index. This is a non-negotiable workflow gate.

**Verification (TDD-style post-condition):** After running, open `<library-root>\index-notebooklm.xlsx` and confirm the `notebooks` worksheet contains a row with the new `notebook_id`. If the row is absent, the index update did not succeed — debug and re-run before finishing.

---

## Tool: upsert_notebooklm_index.py

the Knowledge Operator **must** use this tool to write to the Excel index — she cannot write Python code herself.

**Script path:** `.agents/tools/library/upsert_notebooklm_index.py`  
**Invocation:** pipe a JSON payload to the script via `run_in_terminal`.

## NotebookLM CLI

## Index File

**Path:** `<library-root>\index-notebooklm.xlsx`

## Data Rules

- **Multi-value separator:** pipe with spaces: ` | ` (never semicolons)
- **Missing values:** empty string `""` (never `None`, `null`, or `N/A`)
- **Match key:** always `notebook_id` (never title)

## Upsert Rules

Every "add" is an upsert. There is no distinction between add and update.

1. Read the existing `notebooks` worksheet
2. Search for the `notebook_id` in column A
3. **If found:** overwrite that row in `notebooks` and delete all rows for that `notebook_id` in `sources`, then re-insert current sources
4. **If not found:** append a new row to `notebooks` and append source rows to `sources`
5. Set `last_updated` to today (`YYYY-MM-DD`)
6. Set `status` to `active`

## Styling

Match existing workbook styling:
- Header row: bold white text, dark blue fill (`#1F4E79`)
- Data rows: wrap text, vertical align top
- Column widths: auto-sized, capped at 60 characters

## Prohibited Actions

- **NEVER write code of any kind.** the Knowledge Operator is an operator, not a developer. Do not write Python scripts, JSON data files, shell scripts, batch files, or any other executable or machine-readable code output — not even as a "helper file" or "script for the user to run". This is a hard, unconditional boundary that applies even when no approved tool exists for the task.
- If a task cannot be completed without writing code, **stop immediately and escalate to the engineering agent tier**. State explicitly what capability is missing and why you cannot proceed without it.
- Do **not** create new Python scripts, tool files, or helper modules — use the approved tool at `.agents/tools/library/upsert_notebooklm_index.py` (see the "Tool" section above for exact invocation)
- Do **not** create temporary files
- Do **not** modify `register.json` or any file other than the index spreadsheet
- Do **not** load the `library-management` skill — this skill is self-contained
