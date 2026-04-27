from pathlib import Path

import pytest

collect_ignore_glob = []
pytest_plugins = []


@pytest.fixture(scope="session", name="repo_root")
def repo_root_fixture() -> Path:
    """Return the repository root for test fixtures."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session", name="tools_dir")
def tools_dir_fixture(repo_root: Path) -> Path:
    """Return the library tools directory."""
    return repo_root / ".agents" / "tools" / "library"


@pytest.fixture(scope="session", name="pdf_assets_dir")
def pdf_assets_dir_fixture() -> Path:
    """Return the synthetic PDF asset directory."""
    return Path(__file__).parent / "assets" / "pdfs"
