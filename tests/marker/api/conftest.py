"""Shared fixtures for marker.api tests."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from marker.api.main import create_app


@pytest.fixture
def app() -> FastAPI:
    """Return a configured app instance; clear dependency overrides on teardown."""
    application = create_app()
    yield application
    application.dependency_overrides.clear()


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    """Return a TestClient with auth bypassed via dependency override."""
    from marker.api.dependencies.auth import require_bearer

    app.dependency_overrides[require_bearer] = lambda: "test-token"
    return TestClient(app, raise_server_exceptions=True)


@pytest.fixture
def client_raises_off(app: FastAPI) -> TestClient:
    """Return a TestClient with raise_server_exceptions=False for 500-path tests."""
    from marker.api.dependencies.auth import require_bearer

    app.dependency_overrides[require_bearer] = lambda: "test-token"
    return TestClient(app, raise_server_exceptions=False)
