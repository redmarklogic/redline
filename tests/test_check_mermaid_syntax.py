"""Tests for hooks/check-mermaid-syntax.py."""

import importlib.util
from pathlib import Path

_HOOK = Path(__file__).parent.parent / "hooks" / "check-mermaid-syntax.py"
_spec = importlib.util.spec_from_file_location("check_mermaid_syntax", _HOOK)
_mod = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
_spec.loader.exec_module(_mod)  # type: ignore[union-attr]

_check_file = _mod._check_file
find_violations = _mod.find_violations
fix_file = _mod.fix_file


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write(tmp_path: Path, content: str) -> Path:
    f = tmp_path / "test.md"
    f.write_text(content, encoding="utf-8")
    return f


# ---------------------------------------------------------------------------
# Clean files — no violations expected
# ---------------------------------------------------------------------------


def test_no_mermaid_block_passes(tmp_path: Path) -> None:
    f = _write(tmp_path, "# Just prose\n\nNo diagrams here.\n")
    assert _check_file(f) == []


def test_clean_mermaid_block_passes(tmp_path: Path) -> None:
    f = _write(
        tmp_path,
        "```mermaid\nflowchart TD\n    A[Foundation] --> B[Core Standards]\n```\n",
    )
    assert _check_file(f) == []


def test_hyphen_in_label_passes(tmp_path: Path) -> None:
    f = _write(
        tmp_path,
        "```mermaid\nflowchart TD\n    SK[spec-kit - vendor]\n```\n",
    )
    assert _check_file(f) == []


def test_wildcard_outside_brackets_passes(tmp_path: Path) -> None:
    """A * in a comment line above the block should not be flagged."""
    f = _write(
        tmp_path,
        "Use `eda-*` skills.\n\n```mermaid\nflowchart TD\n    A[eda-codebook]\n```\n",
    )
    assert _check_file(f) == []


# ---------------------------------------------------------------------------
# Em-dash violations
# ---------------------------------------------------------------------------


def test_em_dash_in_subgraph_title_fails(tmp_path: Path) -> None:
    f = _write(
        tmp_path,
        '```mermaid\nflowchart TD\n    subgraph L0["Layer 0 \u2014 Foundation"]\n    end\n```\n',
    )
    violations = _check_file(f)
    assert len(violations) == 1
    assert violations[0][2] == "dash"
    assert "em-dash" in violations[0][3]


def test_em_dash_in_node_label_fails(tmp_path: Path) -> None:
    f = _write(
        tmp_path,
        "```mermaid\nflowchart TD\n    A[spec-kit \u2014 vendor]\n```\n",
    )
    violations = _check_file(f)
    assert len(violations) == 1
    assert violations[0][2] == "dash"
    assert "em-dash" in violations[0][3]


def test_em_dash_outside_mermaid_block_passes(tmp_path: Path) -> None:
    """Em-dash in prose should not be flagged."""
    f = _write(
        tmp_path,
        "This is prose \u2014 with an em-dash.\n\n```mermaid\nflowchart TD\n    A[Clean]\n```\n",
    )
    assert _check_file(f) == []


# ---------------------------------------------------------------------------
# En-dash violations
# ---------------------------------------------------------------------------


def test_en_dash_in_node_label_fails(tmp_path: Path) -> None:
    f = _write(
        tmp_path,
        "```mermaid\nflowchart TD\n    A[step 1 \u2013 step 2]\n```\n",
    )
    violations = _check_file(f)
    assert len(violations) == 1
    assert violations[0][2] == "dash"
    assert "en-dash" in violations[0][3]


# ---------------------------------------------------------------------------
# Wildcard violations
# ---------------------------------------------------------------------------


def test_wildcard_in_node_brackets_fails(tmp_path: Path) -> None:
    f = _write(
        tmp_path,
        "```mermaid\nflowchart TD\n    EDA[eda-* / python-plot-colors]\n```\n",
    )
    violations = _check_file(f)
    assert len(violations) == 1
    assert violations[0][2] == "wildcard"


def test_wildcard_in_quoted_subgraph_title_fails(tmp_path: Path) -> None:
    f = _write(
        tmp_path,
        '```mermaid\nflowchart TD\n    subgraph L5["Applied - eda-*"]\n    end\n```\n',
    )
    violations = _check_file(f)
    assert len(violations) == 1
    assert violations[0][2] == "wildcard"


def test_wildcard_outside_brackets_in_block_passes(tmp_path: Path) -> None:
    """A * on an edge-label line not inside [...] should not be flagged."""
    f = _write(
        tmp_path,
        "```mermaid\nflowchart TD\n    A -->|select *| B\n```\n",
    )
    assert _check_file(f) == []


def test_state_diagram_start_end_state_passes(tmp_path: Path) -> None:
    """[*] is the valid stateDiagram start/end token and must not be flagged."""
    f = _write(
        tmp_path,
        "```mermaid\nstateDiagram-v2\n    [*] --> Empty\n    Empty --> [*]\n```\n",
    )
    assert _check_file(f) == []


# ---------------------------------------------------------------------------
# Suppression
# ---------------------------------------------------------------------------


def test_suppression_skips_em_dash_line(tmp_path: Path) -> None:
    f = _write(
        tmp_path,
        "```mermaid\nflowchart TD\n    A[spec-kit \u2014 vendor] <!-- mermaid: allow -->\n```\n",
    )
    assert _check_file(f) == []


def test_suppression_skips_wildcard_line(tmp_path: Path) -> None:
    f = _write(
        tmp_path,
        "```mermaid\nflowchart TD\n    EDA[eda-*] <!-- mermaid: allow -->\n```\n",
    )
    assert _check_file(f) == []


# ---------------------------------------------------------------------------
# Multiple violations in one file
# ---------------------------------------------------------------------------


def test_multiple_violations_reported(tmp_path: Path) -> None:
    f = _write(
        tmp_path,
        "```mermaid\nflowchart TD\n"
        '    subgraph L0["Layer 0 \u2014 Foundation"]\n'
        "    SK[spec-kit \u2013 vendor]\n"
        "    EDA[eda-*]\n"
        "    end\n```\n",
    )
    violations = _check_file(f)
    assert len(violations) == 3


# ---------------------------------------------------------------------------
# .qmd files are scanned
# ---------------------------------------------------------------------------


def test_qmd_file_is_checked(tmp_path: Path) -> None:
    f = tmp_path / "report.qmd"
    f.write_text(
        "```mermaid\nflowchart TD\n    A[step \u2014 one]\n```\n", encoding="utf-8"
    )
    violations = find_violations([tmp_path])
    assert len(violations) == 1
    assert (
        violations[0][3] == "dash"
    )  # vtype is at index 3 in (file, lineno, line, vtype, reason)


# ---------------------------------------------------------------------------
# --fix: auto-repair em/en-dashes
# ---------------------------------------------------------------------------


def test_fix_replaces_em_dash_in_mermaid_block(tmp_path: Path) -> None:
    f = _write(
        tmp_path,
        '```mermaid\nflowchart TD\n    subgraph L0["Layer 0 \u2014 Foundation"]\n    end\n```\n',
    )
    fixed = fix_file(f)
    assert fixed is True
    assert "\u2014" not in f.read_text(encoding="utf-8")
    assert "Layer 0 - Foundation" in f.read_text(encoding="utf-8")


def test_fix_replaces_en_dash_in_mermaid_block(tmp_path: Path) -> None:
    f = _write(tmp_path, "```mermaid\nflowchart TD\n    A[step \u2013 two]\n```\n")
    fixed = fix_file(f)
    assert fixed is True
    assert "\u2013" not in f.read_text(encoding="utf-8")
    assert "step - two" in f.read_text(encoding="utf-8")


def test_fix_does_not_touch_dash_outside_mermaid_block(tmp_path: Path) -> None:
    content = (
        "Prose with em\u2014dash.\n\n```mermaid\nflowchart TD\n    A[Clean]\n```\n"
    )
    f = _write(tmp_path, content)
    fixed = fix_file(f)
    assert fixed is False
    assert "\u2014" in f.read_text(encoding="utf-8")  # prose unchanged


def test_fix_leaves_wildcard_unfixed(tmp_path: Path) -> None:
    f = _write(tmp_path, "```mermaid\nflowchart TD\n    EDA[eda-*]\n```\n")
    fixed = fix_file(f)
    assert fixed is False
    violations = _check_file(f)
    assert len(violations) == 1  # wildcard still reported


def test_fix_returns_false_when_nothing_to_fix(tmp_path: Path) -> None:
    f = _write(tmp_path, "```mermaid\nflowchart TD\n    A[Clean]\n```\n")
    assert fix_file(f) is False


def test_fix_clears_violations_for_dashes(tmp_path: Path) -> None:
    f = _write(tmp_path, "```mermaid\nflowchart TD\n    A[x \u2014 y]\n```\n")
    fix_file(f)
    assert _check_file(f) == []
