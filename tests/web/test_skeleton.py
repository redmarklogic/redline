"""Smoke tests for the Django web skeleton (#159). All DB-free (research.md D5)."""

from django.core.management import call_command
from django.test import Client


def test_root_url_returns_200():
    # done-when 1 (contracts/root-page.md): GET / serves a 200 text/html placeholder.
    # RED until src/web/views.root + the path("", ...) route land — startproject's
    # urlconf serves only admin/, so this returns 404 first.
    response = Client().get("/")

    assert response.status_code == 200
    assert response["Content-Type"].startswith("text/html")


def test_system_check_clean():
    # done-when 2 regression pin (NOT a Red test — passes already): the system check
    # reports zero issues headlessly. call_command raises SystemCheckError on failure.
    call_command("check")


def test_health_returns_200():
    # FR-007 (contracts/health-endpoint.md): GET /health/ returns 200 application/json
    # with JSON body {"status": "healthy"}. RED until views.health + the route land.
    # JSON-equality, never byte-equality (JsonResponse serialiser whitespace may vary).
    response = Client().get("/health/")

    assert response.status_code == 200
    assert response["Content-Type"] == "application/json"
    assert response.json() == {"status": "healthy"}
