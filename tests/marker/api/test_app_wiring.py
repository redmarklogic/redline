"""Tests for Phase 1 app wiring: auth seam and error envelope handlers."""

from fastapi.testclient import TestClient

from marker.api.main import create_app


class TestAuthSeam:
    def test_rejects_unauthenticated_with_401_and_www_authenticate(self) -> None:
        app = create_app()
        client = TestClient(app, raise_server_exceptions=False)

        response = client.post("/skeletons", json={})

        assert response.status_code == 401
        assert "www-authenticate" in response.headers
        assert response.headers["www-authenticate"] == "Bearer"

    def test_rejects_malformed_token(self) -> None:
        app = create_app()
        client = TestClient(app, raise_server_exceptions=False)

        response = client.post(
            "/skeletons",
            json={},
            headers={"Authorization": "NotBearer xyz"},
        )

        assert response.status_code in (401, 403)


class TestErrorEnvelope:
    def test_422_uses_error_envelope(self) -> None:
        from marker.api.dependencies.auth import require_bearer

        app = create_app()
        app.dependency_overrides[require_bearer] = lambda: "test-token"
        client = TestClient(app, raise_server_exceptions=False)

        response = client.post("/skeletons", json={})

        assert response.status_code == 422
        body = response.json()
        assert "detail" not in body
        assert "code" in body
        assert "message" in body
        assert "trace_id" in body

    def test_validation_handler_returns_envelope(self) -> None:
        from marker.api.dependencies.auth import require_bearer

        app = create_app()
        app.dependency_overrides[require_bearer] = lambda: "test-token"
        client = TestClient(app, raise_server_exceptions=False)

        response = client.post("/skeletons", json={"extra_unknown_field": True})

        body = response.json()
        assert "detail" not in body
        assert "code" in body
        assert "message" in body
        assert "trace_id" in body

    def test_400_for_malformed_json_body(self) -> None:
        app = create_app()
        client = TestClient(app, raise_server_exceptions=False)

        response = client.post(
            "/skeletons",
            content=b"{not json",
            headers={"Content-Type": "application/json", "Authorization": "Bearer tok"},
        )

        assert response.status_code == 400
        body = response.json()
        assert body["code"] == "BAD_REQUEST"

    def test_500_envelope_contains_no_internal_detail(self) -> None:
        from unittest.mock import patch

        from marker.api.dependencies.auth import require_bearer

        app = create_app()
        app.dependency_overrides[require_bearer] = lambda: "test-token"
        client = TestClient(app, raise_server_exceptions=False)

        with patch(
            "marker.api.routes.build_skeleton_bytes",
            side_effect=RuntimeError("boom internal"),
        ):
            response = client.post(
                "/skeletons",
                json={
                    "sections": ["Introduction"],
                    "project_number": "P-001",
                    "client_name": "Acme",
                    "site_address": "123 St",
                    "date": "2026-06-09",
                },
            )

        assert response.status_code == 500
        body = response.json()
        assert body["code"] == "INTERNAL_ERROR"
        message = body["message"]
        assert "/path" not in message
        assert "RuntimeError" not in message
        assert "Traceback" not in message
        assert 'File "' not in message
        assert "boom internal" not in message
