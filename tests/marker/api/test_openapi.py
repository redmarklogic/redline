"""Tests for OpenAPI schema validity."""

from fastapi import status
from fastapi.testclient import TestClient
from openapi_spec_validator import validate


class TestOpenAPISchema:
    def test_openapi_schema_is_valid(self, app) -> None:
        app.docs_url = "/docs"
        client = TestClient(app)

        response = client.get("/openapi.json")

        assert response.status_code == status.HTTP_200_OK
        validate(response.json())
