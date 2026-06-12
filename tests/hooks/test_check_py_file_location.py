"""Tests for the check-py-file-location git hook.

The hook is a standalone script under hooks/ (not an importable package), so it
is loaded by path. Covers the manage.py exact-path exemption (specs/159,
ADR-024) and proves the exemption is exact-match, not prefix/substring.
"""

import importlib.util
from pathlib import Path

_HOOK_PATH = Path(__file__).resolve().parents[2] / "hooks" / "check-py-file-location.py"
_spec = importlib.util.spec_from_file_location("check_py_file_location", _HOOK_PATH)
assert _spec is not None
assert _spec.loader is not None
hook = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hook)


def test_root_manage_py_is_allowed() -> None:
    """The framework-mandated root entrypoint is not a location violation."""
    assert hook.find_location_violations(["manage.py"]) == []


def test_exemption_is_exact_match_not_prefix() -> None:
    """Decoys sharing the manage.py prefix/substring are still violations."""
    decoys = ["manage.py/foo.py", "submanage.py"]
    assert hook.find_location_violations(decoys) == decoys


def test_src_and_tests_still_allowed() -> None:
    """Regression: the existing prefix allow-list is unaffected."""
    assert (
        hook.find_location_violations(["src/web/views.py", "tests/web/test_x.py"]) == []
    )


def test_stray_root_module_still_rejected() -> None:
    """A non-exempt root .py file remains a violation."""
    assert hook.find_location_violations(["random.py"]) == ["random.py"]
