"""Tests for sonar_scan.functions.

Covers _normalise_url, ensure_available, fetch_metrics, fetch_issues,
group_issues, and current_branch.
"""

import json
from unittest.mock import MagicMock, patch

import pytest
from sonar_scan import (
    DEFAULT_METRICS,
    SonarIssue,
    SonarQubeUnavailableError,
    SonarScanError,
    current_branch,
    ensure_available,
    fetch_issues,
    fetch_metrics,
    group_issues,
)
from sonar_scan.functions import _normalise_url

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _urlopen_mock(data: dict | list) -> MagicMock:
    """Return a context-manager mock that yields the given data as JSON bytes."""
    mock = MagicMock()
    mock.read.return_value = json.dumps(data).encode()
    mock.__enter__ = lambda s: s
    mock.__exit__ = MagicMock(return_value=False)
    return mock


# ---------------------------------------------------------------------------
# _normalise_url
# ---------------------------------------------------------------------------


class TestNormaliseUrl:
    def test_rewrites_host_docker_internal(self) -> None:
        assert (
            _normalise_url("http://host.docker.internal:9000")
            == "http://localhost:9000"
        )

    def test_leaves_localhost_unchanged(self) -> None:
        assert _normalise_url("http://localhost:9000") == "http://localhost:9000"

    def test_leaves_arbitrary_host_unchanged(self) -> None:
        assert (
            _normalise_url("http://sonar.example.com:9000")
            == "http://sonar.example.com:9000"
        )


# ---------------------------------------------------------------------------
# ensure_available
# ---------------------------------------------------------------------------


class TestEnsureAvailable:
    def test_returns_up_when_reachable(self) -> None:
        with patch(
            "urllib.request.urlopen", return_value=_urlopen_mock({"status": "UP"})
        ):
            assert ensure_available("http://localhost:9000") == "UP"

    def test_normalises_host_docker_internal(self) -> None:
        with patch(
            "urllib.request.urlopen", return_value=_urlopen_mock({"status": "UP"})
        ) as mock_open:
            ensure_available("http://host.docker.internal:9000")
        probed_url = mock_open.call_args[0][0]
        assert "localhost" in probed_url
        assert "host.docker.internal" not in probed_url

    def test_raises_when_not_up(self) -> None:
        with patch(
            "urllib.request.urlopen", return_value=_urlopen_mock({"status": "STARTING"})
        ):
            with pytest.raises(SonarQubeUnavailableError):
                ensure_available("http://localhost:9000")

    def test_raises_on_connection_error(self) -> None:
        import urllib.error

        with patch(
            "urllib.request.urlopen", side_effect=urllib.error.URLError("refused")
        ):
            with pytest.raises(SonarQubeUnavailableError):
                ensure_available("http://localhost:9000")


# ---------------------------------------------------------------------------
# fetch_metrics
# ---------------------------------------------------------------------------


_MEASURES_RESPONSE = {
    "component": {
        "measures": [
            {"metric": "coverage", "value": "27.1"},
            {"metric": "bugs", "value": "0"},
            {"metric": "complexity", "value": "22"},
            {"metric": "duplicated_lines_density", "value": "0.0"},
            {"metric": "code_smells", "value": "27"},
        ]
    }
}


class TestFetchMetrics:
    def test_returns_float_dict(self) -> None:
        with patch(
            "urllib.request.urlopen",
            side_effect=[
                _urlopen_mock({"status": "UP"}),
                _urlopen_mock(_MEASURES_RESPONSE),
            ],
        ):
            result = fetch_metrics(
                "http://localhost:9000", project="redline", branch="main", token="tok"
            )

        assert result["coverage"] == pytest.approx(27.1)
        assert result["bugs"] == 0.0
        assert result["complexity"] == 22.0
        assert result["duplicated_lines_density"] == 0.0
        assert result["code_smells"] == 27.0

    def test_normalises_url(self) -> None:
        with patch(
            "urllib.request.urlopen",
            side_effect=[
                _urlopen_mock({"status": "UP"}),
                _urlopen_mock(_MEASURES_RESPONSE),
            ],
        ) as mock_open:
            fetch_metrics(
                "http://host.docker.internal:9000", project="p", branch="b", token="t"
            )

        for c in mock_open.call_args_list:
            raw = c[0][0]
            url_str = raw.full_url if hasattr(raw, "full_url") else str(raw)
            assert "host.docker.internal" not in url_str

    def test_omits_metrics_without_value(self) -> None:
        response = {
            "component": {
                "measures": [
                    {"metric": "coverage", "value": "50.0"},
                    {"metric": "security_hotspots"},  # no "value" key
                ]
            }
        }
        with patch(
            "urllib.request.urlopen",
            side_effect=[_urlopen_mock({"status": "UP"}), _urlopen_mock(response)],
        ):
            result = fetch_metrics(
                "http://localhost:9000", project="p", branch="b", token="t"
            )

        assert "coverage" in result
        assert "security_hotspots" not in result

    def test_raises_when_unavailable(self) -> None:
        import urllib.error

        with patch(
            "urllib.request.urlopen", side_effect=urllib.error.URLError("refused")
        ):
            with pytest.raises(SonarQubeUnavailableError):
                fetch_metrics(
                    "http://localhost:9000", project="p", branch="b", token="t"
                )

    def test_raises_on_bad_json(self) -> None:
        bad = MagicMock()
        bad.read.return_value = b"not-json"
        bad.__enter__ = lambda s: s
        bad.__exit__ = MagicMock(return_value=False)
        with patch(
            "urllib.request.urlopen",
            side_effect=[_urlopen_mock({"status": "UP"}), bad],
        ):
            with pytest.raises(SonarScanError):
                fetch_metrics(
                    "http://localhost:9000", project="p", branch="b", token="t"
                )

    def test_default_metrics_constant_is_tuple(self) -> None:
        assert isinstance(DEFAULT_METRICS, tuple)
        assert "coverage" in DEFAULT_METRICS
        assert "bugs" in DEFAULT_METRICS


# ---------------------------------------------------------------------------
# fetch_issues
# ---------------------------------------------------------------------------


_ISSUES_RESPONSE = {
    "issues": [
        {
            "key": "AY-1",
            "rule": "python:S1192",
            "severity": "MINOR",
            "component": "redline:src/rl/foo.py",
            "line": 12,
            "message": "Define a constant instead of duplicating this literal.",
            "status": "OPEN",
        },
        {
            "key": "AY-2",
            "rule": "python:S100",
            "severity": "MAJOR",
            "component": "redline:src/rl/bar.py",
            "message": "Rename this function.",  # no "line" -> file-level issue
            "status": "OPEN",
        },
    ]
}


class TestFetchIssues:
    def test_returns_typed_issues(self) -> None:
        with patch(
            "urllib.request.urlopen",
            side_effect=[
                _urlopen_mock({"status": "UP"}),
                _urlopen_mock(_ISSUES_RESPONSE),
            ],
        ):
            issues = fetch_issues(
                "http://localhost:9000", project="redline", branch="main", token="tok"
            )

        assert [i.key for i in issues] == ["AY-1", "AY-2"]
        assert issues[0].severity == "MINOR"
        assert issues[0].file_path == "src/rl/foo.py"
        assert issues[0].line == 12
        assert issues[1].line is None

    def test_sends_bearer_token(self) -> None:
        with patch(
            "urllib.request.urlopen",
            side_effect=[
                _urlopen_mock({"status": "UP"}),
                _urlopen_mock(_ISSUES_RESPONSE),
            ],
        ) as mock_open:
            fetch_issues(
                "http://localhost:9000", project="p", branch="b", token="secret"
            )

        request = mock_open.call_args_list[1][0][0]
        assert request.get_header("Authorization") == "Bearer secret"

    def test_normalises_url(self) -> None:
        with patch(
            "urllib.request.urlopen",
            side_effect=[
                _urlopen_mock({"status": "UP"}),
                _urlopen_mock(_ISSUES_RESPONSE),
            ],
        ) as mock_open:
            fetch_issues(
                "http://host.docker.internal:9000", project="p", branch="b", token="t"
            )

        for c in mock_open.call_args_list:
            raw = c[0][0]
            url_str = raw.full_url if hasattr(raw, "full_url") else str(raw)
            assert "host.docker.internal" not in url_str

    def test_raises_when_unavailable(self) -> None:
        import urllib.error

        with patch(
            "urllib.request.urlopen", side_effect=urllib.error.URLError("refused")
        ):
            with pytest.raises(SonarQubeUnavailableError):
                fetch_issues(
                    "http://localhost:9000", project="p", branch="b", token="t"
                )

    def test_raises_on_bad_json(self) -> None:
        bad = MagicMock()
        bad.read.return_value = b"not-json"
        bad.__enter__ = lambda s: s
        bad.__exit__ = MagicMock(return_value=False)
        with patch(
            "urllib.request.urlopen", side_effect=[_urlopen_mock({"status": "UP"}), bad]
        ):
            with pytest.raises(SonarScanError):
                fetch_issues(
                    "http://localhost:9000", project="p", branch="b", token="t"
                )


# ---------------------------------------------------------------------------
# group_issues
# ---------------------------------------------------------------------------


def _issue(component: str, severity: str = "MINOR") -> SonarIssue:
    """Build a SonarIssue for grouping tests."""
    return SonarIssue(
        key="k",
        rule="python:S1",
        severity=severity,
        component=component,
        line=1,
        message="m",
        status="OPEN",
    )


class TestGroupIssues:
    def test_groups_by_file(self) -> None:
        issues = [
            _issue("redline:src/a.py"),
            _issue("redline:src/a.py"),
            _issue("redline:src/b.py"),
        ]
        grouped = group_issues(issues, by="file")
        assert set(grouped) == {"src/a.py", "src/b.py"}
        assert len(grouped["src/a.py"]) == 2

    def test_groups_by_severity(self) -> None:
        issues = [
            _issue("redline:src/a.py", "MINOR"),
            _issue("redline:src/b.py", "BLOCKER"),
        ]
        grouped = group_issues(issues, by="severity")
        assert set(grouped) == {"MINOR", "BLOCKER"}

    def test_defaults_to_file(self) -> None:
        grouped = group_issues([_issue("redline:src/a.py")])
        assert "src/a.py" in grouped

    def test_raises_on_unknown_grouping(self) -> None:
        with pytest.raises(SonarScanError):
            group_issues([], by="rule")


# ---------------------------------------------------------------------------
# current_branch
# ---------------------------------------------------------------------------


def _completed(stdout: str, returncode: int = 0, stderr: str = "") -> MagicMock:
    """Build a subprocess.CompletedProcess-like mock."""
    result = MagicMock()
    result.stdout = stdout
    result.stderr = stderr
    result.returncode = returncode
    return result


class TestCurrentBranch:
    def test_returns_branch_name(self) -> None:
        with patch("subprocess.run", return_value=_completed("feature/x\n")):
            assert current_branch() == "feature/x"

    def test_raises_on_detached_head(self) -> None:
        with patch("subprocess.run", return_value=_completed("HEAD\n")):
            with pytest.raises(SonarScanError):
                current_branch()

    def test_raises_on_git_error(self) -> None:
        with patch(
            "subprocess.run",
            return_value=_completed("", returncode=128, stderr="fatal"),
        ):
            with pytest.raises(SonarScanError):
                current_branch()

    def test_raises_on_empty_output(self) -> None:
        with patch("subprocess.run", return_value=_completed("\n")):
            with pytest.raises(SonarScanError):
                current_branch()
