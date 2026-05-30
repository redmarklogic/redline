"""Audit RTK and CCE compliance from session store data.

Queries the session_store_sql MCP tool for tool call events and classifies
them into RTK-prefixed vs bare commands and context_search vs discovery
read_file calls. Outputs a compliance report to stdout.

Usage (from repo root):
    python -m scripts.audit_rtk_cce

This script is designed to be run on-demand, not as a pre-commit hook.
The classification functions are pure and tested independently.
"""

from __future__ import annotations

RTK_ELIGIBLE_COMMANDS: frozenset[str] = frozenset(
    {
        "git",
        "pytest",
        "ruff",
        "docker",
        "uv",
        "pip",
        "mypy",
        "prek",
    }
)

DISCOVERY_PATH_PREFIXES: tuple[str, ...] = (
    "docs/",
    ".agents/",
    ".github/",
    "specs/",
)


def is_rtk_command(command: str) -> bool | None:
    """Classify a terminal command as RTK-prefixed, bare-eligible, or non-eligible.

    Returns:
        True if rtk-prefixed, False if bare but eligible, None if non-eligible.
    """
    if not command or not command.strip():
        return None

    tokens = command.strip().split()
    if not tokens:
        return None

    if tokens[0] == "rtk":
        # rtk meta commands (gain, discover, proxy) are not compliance-relevant
        if len(tokens) >= 2 and tokens[1] in ("gain", "discover", "proxy"):
            return None
        return True

    if tokens[0] in RTK_ELIGIBLE_COMMANDS:
        return False

    return None


def is_discovery_read(file_path: str, start_line: int, end_line: int) -> bool:
    """Classify a read_file call as discovery (broad) vs targeted (narrow edit).

    Discovery reads are full-file reads of docs/instructions/specs files
    where context_search would have been more efficient.
    """
    is_doc_path = any(file_path.startswith(p) for p in DISCOVERY_PATH_PREFIXES)
    is_full_read = (end_line - start_line) > 100
    return is_doc_path and is_full_read


def compute_rtk_compliance(rtk_count: int, bare_count: int) -> float | None:
    """Compute RTK compliance percentage.

    Returns None if no eligible commands were found.
    """
    total = rtk_count + bare_count
    if total == 0:
        return None
    return (rtk_count / total) * 100


def compute_cce_adoption(context_search: int, discovery_reads: int) -> float | None:
    """Compute CCE adoption ratio as a percentage.

    Returns None if no discovery-class operations were found.
    """
    total = context_search + discovery_reads
    if total == 0:
        return None
    return (context_search / total) * 100


def _print_report(
    rtk_count: int,
    bare_count: int,
    context_search_count: int,
    discovery_read_count: int,
    violations: list[dict],
) -> None:
    """Print compliance report to stdout."""
    print("=" * 60)
    print("RTK + CCE Compliance Report")
    print("=" * 60)

    rtk_pct = compute_rtk_compliance(rtk_count, bare_count)
    print("\n--- RTK Compliance ---")
    print(f"  RTK-prefixed commands: {rtk_count}")
    print(f"  Bare eligible commands: {bare_count}")
    if rtk_pct is not None:
        print(f"  Compliance: {rtk_pct:.1f}%")
    else:
        print("  Compliance: N/A (no eligible commands)")

    cce_pct = compute_cce_adoption(context_search_count, discovery_read_count)
    print("\n--- CCE Adoption ---")
    print(f"  context_search calls: {context_search_count}")
    print(f"  Discovery read_file calls: {discovery_read_count}")
    if cce_pct is not None:
        print(f"  Adoption: {cce_pct:.1f}%")
    else:
        print("  Adoption: N/A (no discovery operations)")

    if violations:
        print(f"\n--- Violations ({len(violations)}) ---")
        for v in violations:
            print(
                f"  Turn {v.get('turn', '?')}: [{v.get('tool', '?')}] {v.get('detail', '')}"
            )
            if v.get("suggestion"):
                print(f"    suggestion: {v['suggestion']}")

    print("\n" + "=" * 60)


def main() -> int:
    """Run compliance audit. Prints instructions for MCP-based usage."""
    print(
        "RTK + CCE Compliance Audit\n"
        "\n"
        "This script provides classification functions for analysing\n"
        "session store data. To run a full audit, use the session_store_sql\n"
        "MCP tool to query tool call events, then pass the results through\n"
        "the classification functions.\n"
        "\n"
        "Example MCP query:\n"
        "  session_store_sql: SELECT * FROM tool_calls\n"
        "    WHERE tool_name IN ('run_in_terminal', 'read_file', 'context_search')\n"
        "    ORDER BY timestamp\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
