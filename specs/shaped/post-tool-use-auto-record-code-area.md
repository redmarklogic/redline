---
title: "Pitch: PostToolUse auto-record-code-area"
status: shaped
shaped-by: Peter (Principal Engineer)
shaped-date: 2026-06-03
handed-to: Kabilan (Python Developer), Harriet (Agent Development)
appetite: S
branch: feature/company-register
---

# Pitch: PostToolUse Auto-`record_code_area`

## Problem

CCE's `record_code_area` is supposed to give future sessions a file-touch map: "these files were worked on, for this reason." In practice, it is called only when the invoking agent remembers to call it — which is almost never during implementation, and inconsistently during session close. The `session-handover` skill calls `record_decision` but does not call `record_code_area`. The result is that CCE's cross-session recall for file context is sparse and unreliable.

The consequence is concrete: when Kabilan starts a new session, `session_recall` returns decisions but not the files where those decisions were enacted. The agent re-discovers the relevant files via semantic search or grepping instead of reading a pre-built index. This costs tokens, increases latency, and risks missing files that were modified but not committed at the time of the search.

`record_code_area` requires two inputs: a file path and a description. The file path is always available at write-time (the tool output contains it). The description — a human-intelligible explanation of *why* the file was modified — is available only to the agent that made the decision, not at write-time. This asymmetry is the architectural crux. It means a fully automated solution and a fully manual solution are both wrong: automation gets the path with no context; manual gets the context but is skipped under time pressure. The solution must be a two-layer hybrid.

## Appetite

**Small.** Two deliverables:
1. A modification to `session-track-writes.ps1` (Kabilan) — adds a single MCP call per qualifying write.
2. An addition to `session-handover/procedures/session-handover.md` (Harriet) — adds Step 6b to the existing Step 6 (CCE writes).

No new scripts. No new hooks. No new infrastructure. No new skill files. This sits entirely within the existing `PostToolUse` hook mechanism and the existing `session-handover` skill procedure.

Rationale for Small: the hook infrastructure is already running. `session-track-writes.ps1` already detects qualifying file writes. The only question is whether to append a `record_code_area` call inside that hook. Harriet's change is a single-step addition to an existing procedure. Neither change requires design work — this Pitch answers the only open architectural question (the hybrid split) so both implementers can proceed directly.

## Solution

Two layers work together to give CCE a complete file-touch map:

**Layer 1 — PostToolUse breadcrumb (automatic, low-fidelity).**
`session-track-writes.ps1` already fires after any tool call that produces a qualifying file write (currently: `replace_string_in_file`, `edit_notebook_file`, `create_file`, `multi_replace_string_in_file`). After writing the flag file (current behaviour, unchanged), the script calls:

```
record_code_area(file_path, "modified by [tool_name] in session [session_id]")
```

The description is deliberately minimal. It records *that* the file was touched, *which tool* touched it, and *which session* it was in. It does not explain why. This is intentional — see Rabbit Holes.

**Layer 2 — Handover supplement (manual, high-fidelity).**
The `session-handover` skill's Step 6 ("Write decisions to CCE") gains a sub-step 6b:

> For each file that appears in the bounded git log and has a meaningful reason attached (a decision, a scope change, a refactor motivation), call `record_code_area(file_path, "<human-intelligible description>")`.

This supplements the Layer 1 breadcrumb with the *why*. CCE now holds both entries: the automatic path-only record from the session, and the agent-reasoned description from the handover. Future `session_recall` calls return both, giving the next agent a richer starting picture.

**What this does NOT replace:**
The existing `record_decision` call in Step 6 is unchanged. `record_code_area` and `record_decision` are orthogonal: one records files, the other records choices. Both must run.

## Breadboard

```
[Tool fires: replace_string_in_file / edit_notebook_file / create_file / multi_replace]
        |
[PostToolUse: session-track-writes.ps1]
        |-- writes flag file (existing behaviour, unchanged)
        |-- calls record_code_area(path, "modified by [tool] in session [id]")   <-- Layer 1
        |
        ...session continues...
        |
[User invokes session-handover skill]
        |
[Step 1-5: existing (SHA bound, git log, four-section note...)]
        |
[Step 6a: record_decision for qualifying decisions]   <-- unchanged
[Step 6b: record_code_area for files with attached reasoning]   <-- Layer 2 (NEW)
        |
[CCE now holds: path-only breadcrumbs (L1) + reasoned descriptions (L2)]
        |
[Next session: session_recall returns both layers for any file or topic]
```

Connections NOT in scope: CCE reindex, cross-session deduplication of `record_code_area` entries, surfacing Layer 1 records in the handover note display.

## Rabbit Holes

| Hole | Why to avoid |
|---|---|
| Making the PostToolUse description meaningful | The agent has no reasoning context inside a PowerShell hook. Attempting to infer "why" from the file path or tool name produces noise, not signal. Minimal description is correct — Layer 2 adds the meaning. |
| Calling `record_decision` from PostToolUse | `record_decision` requires agent judgment: was this a decision, or just a mechanical edit? A hook cannot make that judgment. Automating it would pollute the decision record with noise and undermine the value of CCE decision recall. This constraint is absolute. |
| Deduplicating Layer 1 and Layer 2 records in CCE | CCE already handles multiple records per file. Deduplication logic in the hook or the skill adds complexity for no recall benefit — both entries are useful. Avoid. |
| Latency from MCP calls in PostToolUse | The hook fires synchronously inside the agent loop. Adding a blocking MCP network call per write adds latency to every tool invocation. Mitigate by keeping the Layer 1 call unconditional and cheap — one call, no retry, fire-and-forget. Do not add error handling that blocks or retries. |
| Filtering which files "deserve" a Layer 1 record | The current hook already filters to qualifying tool names. No additional filter is needed. Adding file-extension or directory filters creates maintenance burden and risks missing files. Record all qualifying writes. |
| Calling `record_code_area` for every file in the git log at handover | Layer 2 is not a bulk-file-recorder. It is a reasoning supplement. If the agent cannot attach a meaningful description to a file, skip it — Layer 1 already recorded the touch. Bulk recording with empty or generic descriptions degrades CCE precision. |
| Making `session-track-writes.ps1` parse file content | The hook must not read file content. It must not infer module names, function names, or change summaries from the written file. Path and tool name only. |

## No-Gos

Hard constraints both Kabilan and Harriet must not violate:

1. **PostToolUse must not call `record_decision`.** This is a judgment call only. Automating it is explicitly forbidden.
2. **Layer 1 description must be minimal.** Format: `"modified by [tool_name] in session [session_id]"`. No other format is acceptable without a new shaping session.
3. **Layer 2 must not replace Layer 1.** The handover skill must not skip `record_code_area` calls on the assumption that PostToolUse already recorded the file. Both layers run independently.
4. **`session-track-writes.ps1` must not block on MCP call failure.** If CCE is unavailable, the hook logs the failure and continues. It does not abort the tool response cycle.
5. **No new filtering logic in the hook.** Use the existing qualifying-tool filter unchanged. Do not add path, extension, or directory filters.
6. **Layer 2 Step 6b is only for files with attached reasoning.** Harriet must not instruct agents to bulk-call `record_code_area` for every file in the git log without a meaningful description. The procedure must state this constraint explicitly.
7. **The hook JSON configuration is not changed.** Only `session-track-writes.ps1` is modified. No changes to `.github/hooks/` config files.
8. **Windows/PowerShell only.** `session-track-writes.ps1` is PowerShell. Kabilan does not port it or add a bash equivalent.

## Handover

### Kabilan — `session-track-writes.ps1` modification

**What Kabilan is changing:**
Inside the existing qualifying-write detection block in `session-track-writes.ps1`, after the flag-file write, add a single MCP call:

```
record_code_area(
    file_path = <path extracted from tool output>,
    description = "modified by {tool_name} in session {session_id}"
)
```

`session_id` is already available (it is written to the flag file or readable from `/memories/session/session-start.md`). `tool_name` is the PostToolUse event's tool name. `file_path` is extracted from the tool output using the same logic already used for the flag file.

**What Kabilan is NOT doing:**
- Not modifying the flag-file write (leave existing behaviour intact)
- Not adding retry or error-handling logic beyond a log-and-continue on MCP failure
- Not filtering by file extension or directory
- Not calling `record_decision`
- Not modifying any hook JSON config

**Acceptance test (informal):**
After modification, run a session that touches three files with `replace_string_in_file`. At session end, query CCE with the file paths and confirm three Layer 1 `record_code_area` entries exist with the expected minimal description format. No existing hook behaviour should change.

---

### Harriet — `session-handover` procedure update

**What Harriet is adding:**
In `session-handover/procedures/session-handover.md`, find Step 6 ("Write decisions to CCE"). Add a sub-step immediately after the `record_decision` instructions:

> **Step 6b — Supplement file-touch records.**
> For each file in the bounded git log where you can attach a meaningful, human-intelligible reason for the modification (a decision, a refactor motivation, a scope change), call:
> `record_code_area(file_path, "<description of why this file was modified>")`
> Skip files where you cannot articulate a meaningful reason — Layer 1 already recorded the touch. Do not call `record_code_area` for every file in the log indiscriminately.

**What Harriet is NOT doing:**
- Not changing Step 6a (`record_decision`) in any way
- Not adding new skill files or new procedure files
- Not modifying `session-track-writes.ps1`

**Acceptance test (informal):**
After the procedure update, an agent loading the skill cold and working through the steps should produce at least one `record_code_area` call for any session where a file was modified with a stated reason, and zero calls for mechanical edits (whitespace, formatting, config tweaks) where no reason is available. The count should be smaller than the total number of files in the git log.
