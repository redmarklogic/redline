"""Build the Word add-in manifest for trusted-catalog sideload (issue #191).

This is **build-time tooling**, run from the sideload runbook or the launcher — not
runtime app source. It reads ``config/dev-endpoints.json`` (the committed single
source of truth for local ports) and substitutes the ``__ADDIN_BASE_URL__`` token
in the committed ``manifest.template.xml``, so the taskpane address can never drift
from the address the #190 server actually binds (spec FR-002).

Reading the config here does not violate ADR-021: that rule targets the deployed
Django/marker app source, not dev generators — exactly as ``tasks/run-app.ps1``
already reads the same file. The config ``_comment`` explicitly blesses this
"#191 manifest build" to read it.

Standard library only (no Node.js toolchain, no new dependency).

Run::

    python -m addin.build_manifest

This writes ``src/addin/catalog/manifest.xml`` and prints the catalog folder path
to register under Word's Trusted Add-in Catalogs.
"""

import json
from pathlib import Path

# The token the template carries everywhere the live base URL must appear; the
# build fails to leave it behind, so a stale hard-coded port cannot survive (D3).
BASE_URL_TOKEN = "__ADDIN_BASE_URL__"

# Resolve repo-relative paths from the package directory, not the process working
# directory, so the build runs from any cwd (mirrors server.py).
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
DEFAULT_CONFIG = REPO_ROOT / "config" / "dev-endpoints.json"
DEFAULT_TEMPLATE = HERE / "manifest.template.xml"
CATALOG_DIR = HERE / "catalog"
OUTPUT = CATALOG_DIR / "manifest.xml"


def _addin_base_url(config_path: Path) -> str:
    """Compute ``https://localhost:<port>`` from the ``addin`` surface in config.

    The host is fixed to ``localhost`` (what the #190 server binds, server.py),
    not the config ``host`` field (``127.0.0.1``, used only by the launcher's
    health probe). The port is the one value that varies, so it is the only value
    derived from config (D2).
    """
    config = json.loads(config_path.read_text(encoding="utf-8"))
    addin = config["surfaces"]["addin"]
    return f"{addin['scheme']}://localhost:{addin['port']}"


def build_manifest_xml(config_path: Path, template_path: Path) -> str:
    """Render the manifest XML string from the template and config.

    Pure function (no filesystem writes) so it is testable without touching the
    real catalog layout. Substitutes every ``__ADDIN_BASE_URL__`` occurrence in
    the template with the base URL derived from ``config_path``.
    """
    base_url = _addin_base_url(config_path)
    template = template_path.read_text(encoding="utf-8")
    return template.replace(BASE_URL_TOKEN, base_url)


def main() -> None:
    """Render the manifest and write it into the local catalog folder.

    Creates ``src/addin/catalog/`` (gitignored, mirroring ``certs/``) if needed
    and prints the absolute folder path to register under Word's Trusted Add-in
    Catalogs (Trust Center).
    """
    xml = build_manifest_xml(DEFAULT_CONFIG, DEFAULT_TEMPLATE)
    CATALOG_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(xml, encoding="utf-8")
    print(f"Wrote manifest: {OUTPUT}")
    print(f"Register this folder in Word's Trusted Add-in Catalogs: {CATALOG_DIR}")


if __name__ == "__main__":
    main()
