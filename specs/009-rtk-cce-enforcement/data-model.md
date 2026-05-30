# Data Model: RTK + CCE Enforcement

No domain entities. This feature produces tooling artifacts only (hooks, scripts, docs).

## Key Data Structures

### RTK Violation (hook output)

| Field | Type | Description |
| --- | --- | --- |
| file | Path | Markdown file containing violation |
| lineno | int | Line number of bare command |
| command | str | The bare command text |
| suggestion | str | RTK-prefixed version |

Implemented as `tuple[Path, int, str, str]` in `find_violations()` return value. No class needed.

### Compliance Report (audit output)

| Field | Type | Description |
| --- | --- | --- |
| session_id | str | Session identifier |
| total_terminal_commands | int | Total `run_in_terminal` calls |
| rtk_commands | int | Commands with `rtk` prefix |
| rtk_compliance_pct | float | `rtk_commands / total_terminal_commands * 100` |
| total_discovery_reads | int | `read_file` calls classified as discovery |
| context_search_calls | int | `context_search` calls |
| cce_adoption_ratio | float | `context_search / (context_search + discovery_reads)` |
| violations | list | Per-violation detail records |

Implemented as printed output (stdout), not a data class. Classification logic lives in pure functions for testability.

### RTK-Eligible Commands (constant)

```python
RTK_ELIGIBLE_COMMANDS = frozenset({
    "git", "pytest", "ruff", "docker", "uv", "pip", "mypy", "prek",
    "ls", "cat", "find", "grep",
})
```

### Shell Code Block Detection (regex)

```python
FENCE_OPEN = re.compile(r"^```(bash|sh|shell|console|powershell)?\s*$")
FENCE_CLOSE = re.compile(r"^```\s*$")
SUPPRESSION = "<!-- rtk:skip -->"
```
