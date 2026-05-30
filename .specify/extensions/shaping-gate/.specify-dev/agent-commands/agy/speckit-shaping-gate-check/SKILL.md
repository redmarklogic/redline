---
name: speckit-shaping-gate-check
description: 'Spec-kit workflow command: speckit-shaping-gate-check'
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: shaping-gate:commands/speckit.shaping-gate.check.md
---

# Shaping Gate (Lifecycle: before_specify)

<!-- Extension: shaping-gate -->

This hook fires before the `specify` workflow phase.

Before proceeding, verify a shaped Pitch exists for this feature.

## Check

Look for a Pitch file in `specs/shaped/` whose title or filename relates to this feature.

```powershell
Get-ChildItem specs/shaped/ -Filter "*.md" | Select-Object Name
```

## If a matching Pitch exists

Proceed. Reference the Pitch file when writing the spec — use it as the primary
scope boundary. Do not exceed its stated appetite.

## If no matching Pitch exists

Ask the founder:

> "No shaped Pitch was found in `specs/shaped/` for this feature. How would you
> like to proceed?"

Options:
1. **Provide a Pitch** — founder supplies the shaped document; proceed after reading it
2. **Shape first** — invoke the `shaping` skill to create a Pitch; return to `specify` after
3. **Waive shaping** — founder explicitly approves proceeding without a Pitch (appropriate
   for quick fixes, maintenance, or work already well-understood from context)

Record the waiver decision in the conversation before proceeding.

---

This gate is `optional: true` until `specs/shaped/` contains 3 or more Pitch files,
at which point the manifest should be updated to `optional: false`. See ADR-013.

This command is the sole SSOT for the shaping-gate rule (ADR-013, Option A).
