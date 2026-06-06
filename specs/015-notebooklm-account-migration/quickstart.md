# Quickstart: NotebookLM Account Migration (Spec 015)

---

## Prerequisites

Before Linda begins any phase, the Founder must complete Phase 0:

```text
1. Open NotebookLM in the old Google account.
2. Delete only the Redline notebooks (those listed in register.json — 26 entries).
   Leave notebooks belonging to other projects untouched.
3. Switch to the new Google account.
4. Run: nlm login   (browser opens — sign in to new Google account)
5. Run: nlm login --check   (must return success)
6. Run: nlm doctor           (confirm no errors)
7. Confirm to Linda: "mcp-notebooklm is operational in the new account."
```

Linda does not proceed to Phase 1 until this confirmation is received.

---

## Verify MCP is operational (Linda's check at Phase 1 start)

```text
notebook_list   → should return an empty list (no notebooks yet in new account)
server_info     → should return version and auth status
```

If `notebook_list` returns notebooks, stop — the new account is not empty and the
old-account deletion may not be complete. Notify Founder.

---

## Phase 1 consultation sequence

Consult agents in this order (open access first, then advisory-board-only):

1. Graeme (geotechnical domain — 6 notebooks, highest 100-source risk)
2. Peter (AI & software architecture — 5 notebooks)
3. Mark (process & product — 8 notebooks, includes shared notebooks)
4. Matt (UX & design — 1 notebook)
5. Ron (founder strategy — 3 advisory-board-only + `strategy-competitive-advantage`)
6. John (marketing — 1 advisory-board-only notebook)
7. Linda self-review (information-architecture-km, technical-communication)

For each consultation, follow the process in spec.md Phase 1.

---

## Phase 3 notebook creation (Linda)

For each notebook in the approved manifest:

```python
# Pseudocode for MCP call sequence
notebook_create(
    name="<name from manifest>",
    description="<description from manifest>"
)
# Record the returned notebook URL in 015-register-draft.json
```

Verify immediately after each creation:

```text
notebook_list   → confirm new notebook appears
notebook_get(id=<new_id>)   → confirm name and description match manifest
```

Creation order: all `open` notebooks first, then `advisory-board-only`.

---

## Phase 4 source population (Linda)

For each notebook, iterate the `SourceFileRecord` list from the Phase 2 design plan:

```python
# Pseudocode
for source_file in notebook_sources:
    source_add(
        notebook_id=<notebook_id>,
        source_type="file",
        file_path=source_file.file_path
    )
    # Update upload_status to "uploaded" or "failed"
```

After all sources added:

```text
notebook_get(id=<notebook_id>)   → confirm source count matches expected count
```

After all notebooks populated:

```text
# Promote register draft (Founder instruction required)
# Copy docs/people/drafts/015-register-draft.json
#   → .agents/skills/redline-research/register.json
```

---

## Auth refresh (if session expires mid-operation)

```text
refresh_auth   → call via MCP if tool calls start returning auth errors
nlm login      → fallback if refresh_auth fails; re-run nlm login --check after
```
