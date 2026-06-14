"""Regression tests for the github_projects invocation contract.

These lock the three friction points that cost a standup session repeated
failed calls (retro 2026-06-14):

1. The canonical import is ``from github_projects import ...`` (``.agents/tools``
   is on ``pythonpath`` per pyproject). The unimportable ``agents.tools.github_projects``
   form must never reappear in skill/runbook docs.
2. ``TaskRecord.issue_number`` exists — the reasonable guess is now correct, so
   callers never hand-parse ``issue_url``.
3. ``count_tasks`` returns the authoritative board total in Python, so the
   standup completeness assert never needs a hand-rolled ``gh api graphql``
   string (whose ``$var`` syntax collides with PowerShell interpolation).
"""

import re
from pathlib import Path
from unittest.mock import patch

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[4]
_DOC_FILES = (
    _REPO_ROOT / ".agents" / "skills" / "github-projects" / "SKILL.md",
    _REPO_ROOT / ".agents" / "tools" / "github_projects" / "bootstrap-runbook.md",
)
# Match an actual import statement using the unimportable path — not prose that
# names the wrong form to warn against it.
_BROKEN_IMPORT_STMT = re.compile(
    r"^\s*(?:from|import)\s+agents\.tools\.github_projects", re.MULTILINE
)


# ---------------------------------------------------------------------------
# Fix 1 — import path
# ---------------------------------------------------------------------------


class TestImportContract:
    def test_canonical_import_works(self) -> None:
        """The documented import resolves with .agents/tools on the path."""
        from github_projects import list_tasks, resolve_project_config

        assert callable(list_tasks)
        assert callable(resolve_project_config)

    @pytest.mark.parametrize("doc", _DOC_FILES, ids=lambda p: p.name)
    def test_docs_do_not_use_broken_import(self, doc: Path) -> None:
        """No doc may instruct the unimportable agents.tools.github_projects form."""
        assert doc.exists(), f"doc not found: {doc}"
        text = doc.read_text(encoding="utf-8")
        match = _BROKEN_IMPORT_STMT.search(text)
        assert match is None, (
            f"{doc.name} documents the unimportable import '{match.group().strip()}'; "
            "use 'from github_projects import ...' (pythonpath = .agents/tools)."
        )


# ---------------------------------------------------------------------------
# Fix 2 — TaskRecord.issue_number
# ---------------------------------------------------------------------------


class TestIssueNumber:
    def _record(self, url: str):
        from github_projects import TaskRecord

        return TaskRecord(item_id="PVTI_x", issue_url=url, title="t", status="Backlog")

    def test_extracts_trailing_number(self) -> None:
        rec = self._record("https://github.com/redmarklogic/redline/issues/197")
        assert rec.issue_number == 197

    def test_handles_trailing_slash(self) -> None:
        rec = self._record("https://github.com/redmarklogic/redline/issues/64/")
        assert rec.issue_number == 64

    def test_none_when_no_number(self) -> None:
        rec = self._record("")
        assert rec.issue_number is None


# ---------------------------------------------------------------------------
# Fix 3 — count_tasks (no PowerShell GraphQL)
# ---------------------------------------------------------------------------


class TestCountTasks:
    @pytest.fixture(name="config")
    def _config(self):
        from github_projects import ProjectConfig

        cfg_path = (
            _REPO_ROOT / ".agents" / "tools" / "github_projects" / "project_config.json"
        )
        return ProjectConfig.model_validate_json(cfg_path.read_text(encoding="utf-8"))

    def test_returns_total_count_single_page(self, config) -> None:
        from github_projects import count_tasks

        items = [{"id": f"i{n}"} for n in range(12)]
        with patch(
            "github_projects.functions._run_gh",
            return_value=(0, {"items": items, "totalCount": 12}, ""),
        ):
            assert count_tasks(config) == 12

    def test_refetches_when_first_page_truncated(self, config) -> None:
        from github_projects import count_tasks

        page1 = [{"id": f"i{n}"} for n in range(500)]
        page2 = [{"id": f"i{n}"} for n in range(600)]
        with patch(
            "github_projects.functions._run_gh",
            side_effect=[
                (0, {"items": page1, "totalCount": 600}, ""),
                (0, {"items": page2, "totalCount": 600}, ""),
            ],
        ):
            assert count_tasks(config) == 600

    def test_matches_list_tasks_length(self, config) -> None:
        """len(list_tasks) == count_tasks by construction (both complete)."""
        from github_projects import count_tasks, list_tasks

        items = [
            {
                "id": f"PVTI_{n}",
                "content": {"url": f"https://github.com/o/r/issues/{n}"},
                "title": f"t{n}",
                "status": "Backlog",
            }
            for n in range(7)
        ]
        with patch(
            "github_projects.functions._run_gh",
            return_value=(0, {"items": items, "totalCount": 7}, ""),
        ):
            assert count_tasks(config) == len(list_tasks(config)) == 7
