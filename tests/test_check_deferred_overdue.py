"""Tests for hooks/check-deferred-overdue.py.

Tests the core logic: parsing frontmatter, detecting overdue items.
Written before the hook implementation (TDD).
"""

import importlib.util
import textwrap
from datetime import date
from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_hook(repo_root: Path):
    """Import the hook module without executing __main__ block."""
    hook_path = repo_root / "hooks" / "check-deferred-overdue.py"
    spec = importlib.util.spec_from_file_location("check_deferred_overdue", hook_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write_deferred_file(tmp_path: Path, name: str, content: str) -> Path:
    fp = tmp_path / name
    fp.write_text(textwrap.dedent(content), encoding="utf-8")
    return fp


# ---------------------------------------------------------------------------
# parse_frontmatter
# ---------------------------------------------------------------------------

class TestParseFrontmatter:
    def test_reads_status_and_revisit_by(self, repo_root: Path) -> None:
        hook = load_hook(repo_root)
        content = """\
            ---
            id: P-001
            type: strategic
            date_deferred: 2026-05-31
            status: open
            revisit_by: 2026-09-01
            owner_at_retrieval: "Founder"
            unfreeze_condition: >-
              Something specific.
            ---
            # Title
        """
        fm = hook.parse_frontmatter(textwrap.dedent(content))
        assert fm["status"] == "open"
        assert fm["revisit_by"] == "2026-09-01"

    def test_missing_revisit_by_returns_none(self, repo_root: Path) -> None:
        hook = load_hook(repo_root)
        content = """\
            ---
            id: P-002
            status: open
            ---
            # Title
        """
        fm = hook.parse_frontmatter(textwrap.dedent(content))
        assert fm.get("revisit_by") is None

    def test_no_frontmatter_returns_empty(self, repo_root: Path) -> None:
        hook = load_hook(repo_root)
        content = "# Just a title\n\nNo frontmatter here.\n"
        fm = hook.parse_frontmatter(content)
        assert fm == {}

    def test_done_status_parsed(self, repo_root: Path) -> None:
        hook = load_hook(repo_root)
        content = """\
            ---
            id: P-028
            status: done
            revisit_by: 2026-01-01
            ---
            # Resolved item
        """
        fm = hook.parse_frontmatter(textwrap.dedent(content))
        assert fm["status"] == "done"


# ---------------------------------------------------------------------------
# find_overdue_items
# ---------------------------------------------------------------------------

class TestFindOverdueItems:
    def test_no_files_returns_empty(self, repo_root: Path, tmp_path: Path) -> None:
        hook = load_hook(repo_root)
        result = hook.find_overdue_items(tmp_path, date(2026, 5, 31))
        assert result == []

    def test_index_file_skipped(self, repo_root: Path, tmp_path: Path) -> None:
        hook = load_hook(repo_root)
        write_deferred_file(tmp_path, "_index.md", "# Index\n\n| ID | Title |\n|---|---|\n")
        result = hook.find_overdue_items(tmp_path, date(2026, 5, 31))
        assert result == []

    def test_future_revisit_by_not_flagged(self, repo_root: Path, tmp_path: Path) -> None:
        hook = load_hook(repo_root)
        write_deferred_file(tmp_path, "P-001-test.md", """\
            ---
            id: P-001
            status: open
            revisit_by: 2027-01-01
            ---
            # Test
        """)
        result = hook.find_overdue_items(tmp_path, date(2026, 5, 31))
        assert result == []

    def test_past_revisit_by_open_is_flagged(self, repo_root: Path, tmp_path: Path) -> None:
        hook = load_hook(repo_root)
        write_deferred_file(tmp_path, "P-002-test.md", """\
            ---
            id: P-002
            status: open
            revisit_by: 2025-01-01
            ---
            # Past item
        """)
        result = hook.find_overdue_items(tmp_path, date(2026, 5, 31))
        assert len(result) == 1
        assert result[0][0] == "P-002-test.md"

    def test_past_revisit_by_done_not_flagged(self, repo_root: Path, tmp_path: Path) -> None:
        hook = load_hook(repo_root)
        write_deferred_file(tmp_path, "P-028-resolved.md", """\
            ---
            id: P-028
            status: done
            revisit_by: 2025-01-01
            ---
            # Resolved
        """)
        result = hook.find_overdue_items(tmp_path, date(2026, 5, 31))
        assert result == []

    def test_no_revisit_by_not_flagged(self, repo_root: Path, tmp_path: Path) -> None:
        hook = load_hook(repo_root)
        write_deferred_file(tmp_path, "P-003-no-date.md", """\
            ---
            id: P-003
            status: open
            unfreeze_condition: >-
              When KR1 resolves.
            ---
            # Condition-only item
        """)
        result = hook.find_overdue_items(tmp_path, date(2026, 5, 31))
        assert result == []

    def test_multiple_files_only_overdue_flagged(
        self, repo_root: Path, tmp_path: Path
    ) -> None:
        hook = load_hook(repo_root)
        write_deferred_file(tmp_path, "P-010-overdue.md", """\
            ---
            id: P-010
            status: open
            revisit_by: 2025-06-01
            ---
            # Overdue
        """)
        write_deferred_file(tmp_path, "P-011-future.md", """\
            ---
            id: P-011
            status: open
            revisit_by: 2027-01-01
            ---
            # Future
        """)
        write_deferred_file(tmp_path, "P-012-no-date.md", """\
            ---
            id: P-012
            status: open
            ---
            # No date
        """)
        result = hook.find_overdue_items(tmp_path, date(2026, 5, 31))
        assert len(result) == 1
        assert "P-010" in result[0][0]

    def test_today_equal_to_revisit_by_not_flagged(
        self, repo_root: Path, tmp_path: Path
    ) -> None:
        """Item with revisit_by == today is not yet overdue."""
        hook = load_hook(repo_root)
        write_deferred_file(tmp_path, "P-020-today.md", """\
            ---
            id: P-020
            status: open
            revisit_by: 2026-05-31
            ---
            # Due today
        """)
        result = hook.find_overdue_items(tmp_path, date(2026, 5, 31))
        assert result == []
