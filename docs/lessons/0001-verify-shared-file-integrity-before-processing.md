# 0001 — Verify shared file integrity before starting any processing workflow

**Date**: 2026-04-25

**Skill**: `library-management` ([../../.agents/skills/library-management/SKILL.md](../../.agents/skills/library-management/SKILL.md))

**Context**: Indexing `G:\My Drive\Library\Engineering\Standards` into `library-index.xlsx`. The first action was to scan the folder (Phase 0), not to verify the index file. When Phase 1 ran `openpyxl.load_workbook()`, it failed immediately with `zipfile.BadZipFile: File is not a zip file` — the index was corrupted (valid ZIP header but truncated End of Central Directory record). All prior indexing work was lost and the file had to be recreated from scratch.

**Root Cause**: The workflow assumed the shared index file was healthy. Phase 0 (pre-scan) only checks the *source* folder. Nothing in the workflow checks the *target* file before work begins. The corruption had likely occurred in a prior session and sat undetected.

**Principle**: Before starting any multi-step workflow that reads a shared file as a prerequisite, verify that file is openable and structurally valid as the very first step — before scanning, before counting, before anything else. A corrupted prerequisite means all subsequent work is lost on first write. For Excel files specifically: try `openpyxl.load_workbook()` in read-only mode and confirm the expected worksheets are present. If this fails, stop and resolve before proceeding.

**Source**: Session conversation, 2026-04-25 — Linda indexing Engineering/Standards
