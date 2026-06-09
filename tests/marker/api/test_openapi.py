"""Tests for OpenAPI schema validity."""

from fastapi import status
from fastapi.testclient import TestClient
from openapi_spec_validator import validate

from marker.api.main import create_app


class TestOpenAPISchema:
    def test_openapi_schema_is_valid(self, app) -> None:
        client = TestClient(app)

        response = client.get("/openapi.json")

        assert response.status_code == status.HTTP_200_OK
        validate(response.json())

    def test_health_not_in_openapi_schema(self) -> None:
        """GET /health must be absent from the OpenAPI schema paths (FR-003)."""
        app = create_app()

        paths = app.openapi().get("paths", {})

        assert "/health" not in paths
