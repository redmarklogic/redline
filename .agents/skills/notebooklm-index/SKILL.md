---
name: notebooklm-index
description: Use when adding, updating, or auditing a NotebookLM notebook in the index spreadsheet at $library_root\index-notebooklm.xlsx.
arguments: [library_root]
argument-hint: "<path-to-library-root>"
---

## Boundary Contract


See `procedures/notebooklm-index.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Using semicolons as separator | Use pipe: ` \| ` |
| Storing `None` or leaving cell blank for missing fields | Write explicit empty string `""` |
| Loading `library-management` skill | This skill is self-contained |
| Writing notes into the notebook | Out of scope — do not write to the notebook |
| Matching by notebook title | Always match by `notebook_id` |
| Skipping `nlm source describe` | Must call for every source |
| Creating new Python scripts or temp files | Use the approved tool — see the "Tool" section above |
| Omitting `index_path` from the JSON payload | `index_path` is required; no default exists |
| Updating `register.json` | Out of scope — only update the Excel index |
| Not running this skill after `nlm notebook create` | **Oversight** — the mandatory trigger rule (top of this skill) is binding; always update the index before declaring a notebook-creation task complete |
