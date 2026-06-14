"""Tests for the addin Word manifest build (issue #191, Phase 0).

These exercise the pure ``build_manifest_xml(config_path, template_path)`` function:
it reads the ``addin`` surface from a config fixture and renders the committed
template, so the taskpane URL can never drift from what the #190 server binds
(spec FR-002). The trusted-catalog sideload itself is a human-verified Office side
effect (Phase 1) and is not asserted here, matching the boundary #190 drew.
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from addin.build_manifest import build_manifest_xml

REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = REPO_ROOT / "config" / "dev-endpoints.json"
TEMPLATE_PATH = REPO_ROOT / "src" / "addin" / "manifest.template.xml"


@pytest.fixture
def rendered() -> str:
    """The manifest XML rendered from the committed config and template."""
    return build_manifest_xml(CONFIG_PATH, TEMPLATE_PATH)


@pytest.fixture
def addin_port() -> int:
    """The addin surface port from the same config the build reads (no-drift)."""
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return config["surfaces"]["addin"]["port"]


def test_output_is_well_formed_xml(rendered: str):
    """The rendered manifest parses as well-formed XML (FR-001)."""
    ET.fromstring(rendered)  # raises ParseError if malformed


def test_source_location_url_derives_from_config(rendered: str, addin_port: int):
    """SourceLocation equals https://localhost:<port>/taskpane.html from config (FR-002)."""
    root = ET.fromstring(rendered)
    source = root.find(".//{*}SourceLocation")
    assert source is not None, "SourceLocation element missing"
    assert source.get("DefaultValue") == f"https://localhost:{addin_port}/taskpane.html"


def test_app_domain_equals_rendered_base_url(rendered: str, addin_port: int):
    """AppDomain equals the rendered base URL (no path) (FR-002)."""
    root = ET.fromstring(rendered)
    app_domain = root.find(".//{*}AppDomains/{*}AppDomain")
    assert app_domain is not None, "AppDomain element missing"
    assert app_domain.text == f"https://localhost:{addin_port}"


def test_word_host_is_present(rendered: str):
    """A Word host (Host Name='Document') is declared (FR-003)."""
    root = ET.fromstring(rendered)
    hosts = [h.get("Name") for h in root.findall(".//{*}Hosts/{*}Host")]
    assert "Document" in hosts


def test_wordapi_min_version_floor(rendered: str):
    """The WordApi Set declares MinVersion 1.3 per ADR-028 D1 (FR-009)."""
    root = ET.fromstring(rendered)
    sets = root.findall(".//{*}Requirements/{*}Sets/{*}Set")
    wordapi = [s for s in sets if s.get("Name") == "WordApi"]
    assert wordapi, "WordApi Set missing"
    assert wordapi[0].get("MinVersion") == "1.3"


def test_token_does_not_survive(rendered: str):
    """The __ADDIN_BASE_URL__ template token is fully substituted (FR-002)."""
    assert "__ADDIN_BASE_URL__" not in rendered
