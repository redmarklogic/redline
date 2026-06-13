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

from web.settings import *  # noqa: E402, F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
