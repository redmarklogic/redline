"""Tests for POST /skeletons route — success path, validation, and auth edge cases."""

import pytest
from fastapi.testclient import TestClient


VALID_BODY = {
    "sections": ["Introduction", "Site Description", "Conclusions"],
    "project_number": "GIR-001",
    "client_name": "Acme Corp",
    "site_address": "123 Example Street",
    "date": "2026-06-09",
}

DOCX_MEDIA_TYPE = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)


class TestSkeletonsRoute:
    def test_returns_docx_bytes_with_correct_headers(
        self, client: TestClient, mocker
    ) -> None:
        mock_bytes = b"PK\x03\x04" + b"\x00" * 100
        mocker.patch(
            "marker.api.routes.build_skeleton_bytes",
            return_value=mock_bytes,
        )

        response = client.post("/skeletons", json=VALID_BODY)

        assert response.status_code == 200
        assert DOCX_MEDIA_TYPE in response.headers["content-type"]
        assert response.headers["content-type"] != "text/event-stream"
        assert "attachment" in response.headers["content-disposition"]
        assert ".docx" in response.headers["content-disposition"]
        assert response.content[:4] == b"PK\x03\x04"

    def test_rejects_missing_required_field(self, client: TestClient) -> None:
        body = {k: v for k, v in VALID_BODY.items() if k != "project_number"}

        response = client.post("/skeletons", json=body)

        assert response.status_code == 422

    def test_rejects_extra_fields(self, client: TestClient) -> None:
        body = {**VALID_BODY, "unexpected_field": "value"}

        response = client.post("/skeletons", json=body)

        assert response.status_code == 422

    def test_domain_invalid_sections_returns_422_empty(
        self, client: TestClient
    ) -> None:
        body = {**VALID_BODY, "sections": []}

        response = client.post("/skeletons", json=body)

        assert response.status_code == 422

    def test_domain_invalid_sections_returns_422_duplicates(
        self, client: TestClient
    ) -> None:
        body = {**VALID_BODY, "sections": ["Introduction", "Introduction"]}

        response = client.post("/skeletons", json=body)

        assert response.status_code == 422

    def test_domain_invalid_sections_returns_422_blank_heading(
        self, client: TestClient
    ) -> None:
        body = {**VALID_BODY, "sections": ["   "]}

        response = client.post("/skeletons", json=body)

        assert response.status_code == 422

    def test_skeletons_route_registered_plural_unversioned(
        self, app
    ) -> None:
        routes = [r.path for r in app.routes]  # type: ignore[attr-defined]
        assert any(r == "/skeletons" for r in routes)
        assert not any("/v1" in r for r in routes)

    def test_rejects_malformed_token(self) -> None:
        from marker.api.main import create_app

        app = create_app()
        client = TestClient(app, raise_server_exceptions=False)

        response = client.post(
            "/skeletons",
            json=VALID_BODY,
            headers={"Authorization": "NotBearer xyz"},
        )

        assert response.status_code in (401, 403)
