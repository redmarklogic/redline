"""Tests for the GET /health endpoint (US1 — Infrastructure Probe)."""

from fastapi.testclient import TestClient

from marker.api.main import create_app


class TestHealthEndpoint:
    def test_health_returns_200_no_auth(self) -> None:
        """Bare TestClient, no auth override — unauthenticated request must return 200."""
        app = create_app()
        client = TestClient(app)

        response = client.get("/health")

        assert response.status_code == 200

    def test_health_returns_200_with_invalid_auth(self) -> None:
        """Invalid Bearer token must NOT cause 401 — auth is ignored on /health."""
        app = create_app()
        client = TestClient(app)

        response = client.get("/health", headers={"Authorization": "Bearer invalid"})

        assert response.status_code == 200

    def test_health_response_body_shape(self) -> None:
        """Response body must be exactly {"status": "healthy"} — no extra fields."""
        app = create_app()
        client = TestClient(app)

        response = client.get("/health")
        body = response.json()

        assert set(body.keys()) == {"status"}
        assert body["status"] == "healthy"
