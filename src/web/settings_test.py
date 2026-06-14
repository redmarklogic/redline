"""Test settings: real settings with the database swapped for in-memory SQLite.

pytest must never depend on (or touch) the docker-compose Postgres service.
An in-memory SQLite database is created per test run and vanishes with the
process — no server, no cleanup, no risk to real data. Wired via the pytest
``--ds=web.settings_test`` option in pyproject.toml.

The os.environ.setdefault calls below bootstrap the required environment
variables BEFORE ``from web.settings import *`` imports the module and
instantiates Settings() at module load time. Without this bootstrap, pytest
collection crashes for the whole repo with a ValidationError (#161 D3).
setdefault does NOT override variables already exported by the developer's
shell, so a real environment takes precedence over these fixture values.
"""

import os

os.environ.setdefault(  # hook: allow -- test fixture (ADR-021 escape hatch)
    "DJANGO_SECRET_KEY",
    "test-fixture-key-not-the-burned-literal-redline-web-abc987",
)
os.environ.setdefault(  # hook: allow -- test fixture (ADR-021 escape hatch)
    "DJANGO_ALLOWED_HOSTS",
    "testserver,localhost",
)
os.environ.setdefault(  # hook: allow -- test fixture (ADR-021 escape hatch)
    "POSTGRES_DB",
    "testdb",
)
os.environ.setdefault(  # hook: allow -- test fixture (ADR-021 escape hatch)
    "POSTGRES_USER",
    "testuser",
)
os.environ.setdefault(  # hook: allow -- test fixture (ADR-021 escape hatch)
    "POSTGRES_PASSWORD",
    "testpass",
)
os.environ.setdefault(  # hook: allow -- test fixture (ADR-021 escape hatch)
    "POSTGRES_HOST",
    "127.0.0.1",
)
os.environ.setdefault(  # hook: allow -- test fixture (ADR-021 escape hatch)
    "POSTGRES_PORT",
    "5432",
)

from web.settings import *  # noqa: F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# The compressed-manifest staticfiles backend (web.settings, D2) raises
# "Missing staticfiles manifest entry" when a {% static %} tag renders before
# collectstatic runs; with filterwarnings=["error"] that breaks template tests.
# Swap in the non-manifest backend so template tests render {% static %} without
# collectstatic. The manifest/production path is covered by test_static_serving
# (#161 D6 pattern; #162 D6).
STORAGES = {
    **STORAGES,  # noqa: F405
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# WhiteNoiseMiddleware scans STATIC_ROOT at init; in tests collectstatic has not
# run, so that directory is absent and WhiteNoise emits a "No directory at"
# UserWarning that filterwarnings=["error"] turns fatal. AUTOREFRESH=True is
# WhiteNoise's documented test setting: it skips the start-up scan and serves
# lazily, leaving middleware behaviour otherwise unchanged.
WHITENOISE_AUTOREFRESH = True
