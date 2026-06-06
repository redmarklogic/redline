# Research: NotebookLM Account Migration (Spec 015)

**Date**: 2026-06-05
**Status**: Complete — no NEEDS CLARIFICATION items remain

---

## MCP Tool Availability

**Decision**: `notebook_create` is permitted for Linda (Knowledge Operator) following
spec-kit pre-plan review. `forbidden-tools.md` and `procedures/notebooklm-mcp.md` amended.

**Rationale**: The prior classification ("Destructive notebook management") was
over-broad. For the Knowledge Operator running a migration workflow with explicit Founder
instruction, notebook creation is an intentional, bounded operation. The amendment scopes
the exception narrowly — migration and provisioning workflows only.

**Alternatives considered**: (a) Founder creates all notebooks manually, Linda only adds
sources — rejected because it removes Linda's end-to-end accountability for the notebook
manifest. (b) `nlm` CLI notebook creation — possible but undocumented in skill; MCP is
the canonical path.

**Confirmed tool set for Phase 3–4:**

| Operation | MCP Tool | Caller |
| --- | --- | --- |
| Create notebook | `notebook_create` | Linda (Knowledge Operator) |
| Verify notebook exists | `notebook_list`, `notebook_get` | Linda |
| Add source file | `source_add` | Linda (Knowledge Operator) |
| Confirm source count | `notebook_get` | Linda |
| Refresh session | `refresh_auth` | Linda |

---

## register.json Schema

Source of truth: `.agents/skills/redline-research/register.json`

Each entry has the following fields:

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | kebab-case slug, unique across all entries |
| `name` | string | Display name shown in NotebookLM |
| `url` | string | Full NotebookLM notebook URL |
| `description` | string | One-paragraph description |
| `topic_area` | string | Coarse grouping (matches existing areas or proposes new one) |
| `topics` | string[] | 5–10 flat topic tags |
| `content_types` | string[] | Nature of sources (books, standards, guides, etc.) |
| `use_cases` | string[] | 3–5 agent-facing use cases |
| `access` | string | `"open"` or `"advisory-board-only"` |
| `added` | string | ISO date `YYYY-MM-DD` |

**Migration rule**: All fields except `url` are preserved from the old register entry.
`url` is the only field updated after recreation. `added` date is preserved (not reset to
migration date).

---

## Library-Management Skill (Phase 1 and Phase 2 tool)

**Skill**: `.agents/skills/library-management/SKILL.md`
**Index file**: `G:\My Drive\Library\index-notebooklm.xlsx` (canonical index of all library files)

**Phase 1 use (rough count for risk-flagging)**:

Query `library-index.xlsx` filtered by `topic_area` or LCC subfolder to get a file count
per notebook topic area. This is a read-only query — no files are moved or renamed.

```text
Operation: read library-index.xlsx, filter rows by topic keywords
Output: file count per notebook (integer estimate)
Tool: direct workbook read under WorkbookLock (read-only)
```

**Phase 2 use (full SourceFileRecord list)**:

For each notebook, query `library-index.xlsx` to retrieve the full list of matching file
paths and their metadata (filename, content_type, path). The result becomes the notebook's
`SourceFileRecord` list with `upload_status = pending`.

```text
Operation: read library-index.xlsx, filter rows → extract path + content_type per match
Output: list of {file_path, content_type} records per notebook
Tool: direct workbook read under WorkbookLock (read-only)
```

**What the skill does NOT do for this migration**: The `library-management` skill's
write path (metadata extraction, renaming, indexing new files) is not invoked during this
migration. Linda reads the existing index; she does not add or rename files.

---

## Library Structure (G:\My Drive\Library)

**Decision**: Linda confirms source counts during Phase 2 by inspecting the digital
library using the `library-management` skill. Exact file counts are not available at
spec authoring time.

**Known high-count risk areas** (from register.json descriptions):
- `engineering-standards`: NZ IDS, NZS 4431, NZGS guides, Canterbury regulatory docs.
  Number of individual PDFs unknown — must be counted in Phase 2.
- `ground-engineering-magazine`: 2014–2026 issues. If each issue is a separate PDF,
  count could reach 100+. Must be counted in Phase 2.

**Rationale**: Counting before the consultation (Phase 1) would allow Linda to answer
"what do we have?" queries accurately.

---

## Draft Staging Path

**Decision**: `docs/people/drafts/` is the staging area for all Phase 1–4 draft outputs.

Files created:
- `docs/people/drafts/015-proposed-notebook-manifest.md` (Phase 1 output)
- `docs/people/drafts/015-notebook-design-plan.md` (Phase 2 output)
- `docs/people/drafts/015-register-draft.json` (Phase 3 output, updated in Phase 4)

**Rationale**: Linda's maturity level is Draft-First. All register changes require Founder
promotion to the canonical path. The staging path exists and is used by other Linda
workflows.

---

## Constitution Check

| Principle | Verdict | Notes |
| --- | --- | --- |
| I — SSOT | Pass | `register.json` is the declared SSOT. Draft staging does not create a competing SSOT — it is a review artifact. |
| II — Hook-First | N/A | No code; no hooks needed. |
| VIII — Determinism | Pass | Source lookup uses physical library files (deterministic). Not LLM inference. |
| IX — Citation-Only | Pass | Notebook contents are uploaded files; no standards text is reproduced in code or config. |

No gate failures.
