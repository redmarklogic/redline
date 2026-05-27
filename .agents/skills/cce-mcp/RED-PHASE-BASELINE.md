# RED Phase Baseline: cce-mcp

**Date**: 2026-05-26
**Status**: Baseline established (skill created alongside baseline — pre-existing gap)

## Observed Failure (without skill)

Without this skill, agents asked to reduce token consumption during codebase exploration
default to `read_file` on every hook or source file. In a 10-phase implementation plan
(e.g. hook-first-enforcement), this produces repeated full-file reads of the same hook
scripts at the start of every phase session, costing thousands of input tokens per session.

Specific failures observed:
- Agent reads `hooks/check-banned-words.py` in full to understand the pattern, rather than
  using `context_search "hook argparse main return int"` to retrieve only the relevant chunks.
- Agent re-reads all 8 hook files at the start of Phase 3 despite having processed them in
  Phase 1, because no `record_decision` was called after Phase 1.
- Agent does not call `reindex` after creating a new hook file, so Phase 2's hook is
  invisible to `context_search` in Phase 3.

## Expected Behaviour (with skill)

- Agent calls `context_search` before any exploratory `read_file`.
- Agent calls `record_decision` after establishing the canonical hook structure in Phase 1.
- Agent calls `session_recall "hook structure pattern"` at the start of Phases 2–10.
- Agent calls `reindex <file>` immediately after creating each new file.
