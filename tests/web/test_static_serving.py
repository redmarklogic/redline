"""Tests for production static delivery via WhiteNoise (#162, Phase 1, FR-004).

Proves the vendored htmx file is delivered when the app runs as in the cloud
(DEBUG off, after collectstatic): the middleware is wired in the right slot, the
base settings use the compressed-manifest backend, and collectstatic produces a
hashed file plus a manifest entry for the vendored asset.
"""

import importlib
import json
from pathlib import Path

from django.core.management import call_command
from django.test import override_settings


def test_whitenoise_middleware_installed_after_security():
    # FR-004: WhiteNoiseMiddleware must sit immediately after SecurityMiddleware
    # so it serves static files before later middleware run.
    from django.conf import settings

    middleware = list(settings.MIDDLEWARE)
    security = "django.middleware.security.SecurityMiddleware"
    whitenoise = "whitenoise.middleware.WhiteNoiseMiddleware"

    assert whitenoise in middleware
    assert middleware.index(whitenoise) == middleware.index(security) + 1


def test_staticfiles_storage_is_manifest_in_base_settings():
    # D2: the BASE settings (web.settings) use the compressed-manifest backend.
    # Read the module directly so the D6 test-settings override does not mask it.
    base = importlib.import_module("web.settings")

    assert (
        base.STORAGES["staticfiles"]["BACKEND"]
        == "whitenoise.storage.CompressedManifestStaticFilesStorage"
    )


def test_collectstatic_collects_htmx_and_manifest_serves_it(tmp_path):
    # FR-004: collectstatic gathers the vendored file into STATIC_ROOT under the
    # manifest backend, producing a hashed file and a staticfiles.json entry.
    static_root = tmp_path / "staticfiles"
    with override_settings(
        STATIC_ROOT=str(static_root),
        STORAGES={
            **__import__("django.conf", fromlist=["settings"]).settings.STORAGES,
            "staticfiles": {
                "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
            },
        },
    ):
        call_command("collectstatic", "--noinput", verbosity=0)

        manifest = static_root / "staticfiles.json"
        assert manifest.exists()
        entries = json.loads(manifest.read_text())["paths"]
        assert "web/vendor/htmx.min.js" in entries

        hashed = static_root / entries["web/vendor/htmx.min.js"]
        assert hashed.exists()
        assert Path(entries["web/vendor/htmx.min.js"]).name != "htmx.min.js"
