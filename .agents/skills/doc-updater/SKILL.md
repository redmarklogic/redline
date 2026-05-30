---
name: doc-updater
description: Use when updating codemaps or documentation to match the Python codebase -- scanning packages, FastAPI/MCP routes, scripts, or README
---

# Documentation & Codemap Specialist

This skill is for updating documentation so it matches the current state of the codebase.

The priority is accuracy over prose: docs that mention files, endpoints, or commands must be verifiably correct.

## Boundary Contract


See `procedures/doc-updater.md` for detailed rules, examples, and extended reference.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Updating docs without verifying the referenced paths actually exist | Confirm every path in a codemap is reachable; broken paths are worse than no docs |
| Leaving stale function names after a refactor | Re-scan the package after refactors; do not assume the old codemap is still accurate |
| Documenting internal helpers in the public codemap | Only document the public API surface; internals belong in inline comments |