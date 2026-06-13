"""Test settings: real settings with the database swapped for in-memory SQLite.

pytest must never depend on (or touch) the docker-compose Postgres service.
An in-memory SQLite database is created per test run and vanishes with the
process — no server, no cleanup, no risk to real data. Wired via the pytest
``--ds=web.settings_test`` option in pyproject.toml.
"""

from web.settings import *  # noqa: F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
