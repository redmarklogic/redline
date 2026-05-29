

<!-- Extension: static-checks -->
<!-- Config: .specify/extensions/static-checks/ -->
# Static Checks (Lifecycle: after_implement)

<!-- Extension: static-checks -->

This hook fires at the end of the `implement` workflow phase.

Load and apply the `python-static-checks` skill. Run:

```bash
uv run prek run -a
```

Fix **all** errors and warnings before claiming the implement phase complete.
Both errors and warnings must be resolved — do not suppress without justification.

---

This command is a lifecycle dispatcher (ADR-013, Option C).
The authoritative procedure is `.agents/skills/python-static-checks/SKILL.md`.
