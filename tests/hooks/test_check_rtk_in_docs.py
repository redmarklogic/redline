"""Tests for hooks/check-rtk-in-docs.py — RTK prefix enforcement in Markdown."""

import importlib
import sys
from pathlib import Path
from textwrap import dedent

# Import the hook module (filename contains hyphens).
_HOOK_PATH = Path(__file__).resolve().parents[2] / "hooks" / "check-rtk-in-docs.py"
_spec = importlib.util.spec_from_file_location("check_rtk_in_docs", _HOOK_PATH)
_mod = importlib.util.module_from_spec(_spec)
sys.modules["check_rtk_in_docs"] = _mod
_spec.loader.exec_module(_mod)

find_violations = _mod.find_violations


def _write_md(tmp_path: Path, content: str) -> Path:
    md = tmp_path / "test.md"
    md.write_text(dedent(content), encoding="utf-8")
    return tmp_path


class TestViolationDetection:
    """Scenario 1 AC-1: bare commands flagged with line number + suggestion."""

    def test_bare_git_status_flagged(self, tmp_path: Path) -> None:
        _write_md(
            tmp_path,
            """\
            # Example
            ```bash
            git status
            ```
            """,
        )
        violations = find_violations([tmp_path])
        assert len(violations) == 1
        _path, lineno, cmd, suggestion = violations[0]
        assert lineno == 3
        assert "git status" in cmd
        assert "rtk git status" in suggestion

    def test_bare_pytest_flagged(self, tmp_path: Path) -> None:
        _write_md(
            tmp_path,
            """\
            ```sh
            pytest tests/ -v
            ```
            """,
        )
        violations = find_violations([tmp_path])
        assert len(violations) == 1
        assert "rtk pytest" in violations[0][3]

    def test_bare_ruff_check_flagged(self, tmp_path: Path) -> None:
        _write_md(
            tmp_path,
            """\
            ```bash
            ruff check src/
            ```
            """,
        )
        violations = find_violations([tmp_path])
        assert len(violations) == 1
        assert "rtk ruff" in violations[0][3]

    def test_multiple_violations_in_one_block(self, tmp_path: Path) -> None:
        _write_md(
            tmp_path,
            """\
            ```bash
            git status
            ruff check .
            docker ps
            ```
            """,
        )
        violations = find_violations([tmp_path])
        assert len(violations) == 3


class TestPassOnPrefixed:
    """Scenario 1 AC-2: already-prefixed commands pass."""

    def test_rtk_prefixed_passes(self, tmp_path: Path) -> None:
        _write_md(
            tmp_path,
            """\
            ```bash
            rtk git status
            ```
            """,
        )
        violations = find_violations([tmp_path])
        assert violations == []

    def test_mixed_prefixed_and_bare(self, tmp_path: Path) -> None:
        _write_md(
            tmp_path,
            """\
            ```bash
            rtk git status
            ruff check .
            ```
            """,
        )
        violations = find_violations([tmp_path])
        assert len(violations) == 1
        assert "ruff" in violations[0][2]


class TestNonEligibleSkipped:
    """Scenario 1 AC-3: non-RTK-eligible commands not flagged."""

    def test_python_not_flagged(self, tmp_path: Path) -> None:
        _write_md(
            tmp_path,
            """\
            ```bash
            python -m pytest
            ```
            """,
        )
        violations = find_violations([tmp_path])
        assert violations == []

    def test_echo_not_flagged(self, tmp_path: Path) -> None:
        _write_md(
            tmp_path,
            """\
            ```bash
            echo "hello"
            ```
            """,
        )
        violations = find_violations([tmp_path])
        assert violations == []

    def test_cd_not_flagged(self, tmp_path: Path) -> None:
        _write_md(
            tmp_path,
            """\
            ```bash
            cd src/
            ```
            """,
        )
        violations = find_violations([tmp_path])
        assert violations == []


class TestSuppression:
    """Scenario 1 AC-4: rtk:skip suppression."""

    def test_skip_suppresses_next_block(self, tmp_path: Path) -> None:
        _write_md(
            tmp_path,
            """\
            <!-- rtk:skip -->
            ```bash
            git status
            ```
            """,
        )
        violations = find_violations([tmp_path])
        assert violations == []

    def test_skip_only_affects_next_block(self, tmp_path: Path) -> None:
        _write_md(
            tmp_path,
            """\
            <!-- rtk:skip -->
            ```bash
            git status
            ```

            ```bash
            git log -10
            ```
            """,
        )
        violations = find_violations([tmp_path])
        assert len(violations) == 1
        assert "git log" in violations[0][2]


class TestNonShellBlocks:
    """Non-shell code blocks should be ignored."""

    def test_python_block_ignored(self, tmp_path: Path) -> None:
        _write_md(
            tmp_path,
            """\
            ```python
            git = "something"
            ```
            """,
        )
        violations = find_violations([tmp_path])
        assert violations == []

    def test_json_block_ignored(self, tmp_path: Path) -> None:
        _write_md(
            tmp_path,
            """\
            ```json
            {"git": "value"}
            ```
            """,
        )
        violations = find_violations([tmp_path])
        assert violations == []

    def test_yaml_block_ignored(self, tmp_path: Path) -> None:
        _write_md(
            tmp_path,
            """\
            ```yaml
            git: status
            ```
            """,
        )
        violations = find_violations([tmp_path])
        assert violations == []

    def test_untagged_block_with_shell_command(self, tmp_path: Path) -> None:
        """Untagged blocks containing shell-like commands should be checked."""
        _write_md(
            tmp_path,
            """\
            ```
            git status
            ```
            """,
        )
        violations = find_violations([tmp_path])
        assert len(violations) == 1


class TestCommentAndBlankLines:
    """Comments and blank lines inside code blocks should be skipped."""

    def test_comment_lines_skipped(self, tmp_path: Path) -> None:
        _write_md(
            tmp_path,
            """\
            ```bash
            # This is a comment
            rtk git status
            ```
            """,
        )
        violations = find_violations([tmp_path])
        assert violations == []

    def test_blank_lines_skipped(self, tmp_path: Path) -> None:
        _write_md(
            tmp_path,
            """\
            ```bash

            rtk git status

            ```
            """,
        )
        violations = find_violations([tmp_path])
        assert violations == []


class TestEdgeCases:
    """Edge cases for robustness."""

    def test_empty_file(self, tmp_path: Path) -> None:
        md = tmp_path / "empty.md"
        md.write_text("", encoding="utf-8")
        violations = find_violations([tmp_path])
        assert violations == []

    def test_no_code_blocks(self, tmp_path: Path) -> None:
        _write_md(
            tmp_path,
            """\
            # Just prose
            No code blocks here.
            """,
        )
        violations = find_violations([tmp_path])
        assert violations == []

    def test_nonexistent_dir(self, tmp_path: Path) -> None:
        violations = find_violations([tmp_path / "nonexistent"])
        assert violations == []

    def test_rtk_meta_commands_not_flagged(self, tmp_path: Path) -> None:
        """rtk meta commands (gain, discover, proxy) should not be flagged."""
        _write_md(
            tmp_path,
            """\
            ```bash
            rtk gain
            rtk discover
            rtk proxy git status
            ```
            """,
        )
        violations = find_violations([tmp_path])
        assert violations == []

    def test_prek_eligible(self, tmp_path: Path) -> None:
        _write_md(
            tmp_path,
            """\
            ```bash
            prek run
            ```
            """,
        )
        violations = find_violations([tmp_path])
        assert len(violations) == 1
        assert "rtk prek" in violations[0][3]

    def test_qmd_files_scanned(self, tmp_path: Path) -> None:
        qmd = tmp_path / "test.qmd"
        qmd.write_text("```bash\ngit status\n```\n", encoding="utf-8")
        violations = find_violations([tmp_path])
        assert len(violations) == 1
