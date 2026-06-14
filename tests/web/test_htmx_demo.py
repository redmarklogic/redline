"""Tests for the htmx demo round trip (#162, Phase 0). All DB-free.

Proves the vendored htmx capability end to end: the static file is findable,
the demo page references it, the POST action returns a server-rendered fragment,
and Django's CSRF protection rejects an unauthenticated state-changing request.
The root/health regression (FR-007) is pinned by test_skeleton.py — not here.
"""

from django.contrib.staticfiles import finders
from django.templatetags.static import static
from django.test import Client


def test_htmx_static_file_is_findable():
    # FR-001/FR-005: the vendored htmx file resolves through the staticfiles
    # finder, proving STATICFILES_DIRS points at src/web/static.
    # RED until the file + STATICFILES_DIRS land.
    assert finders.find("web/vendor/htmx.min.js") is not None


def test_demo_page_returns_200_and_references_htmx():
    # FR-002/FR-003: GET /htmx-demo/ is a 200 text/html page whose body loads
    # htmx via {% static %} (proves the tag resolves to the vendored URL).
    response = Client().get("/htmx-demo/")

    assert response.status_code == 200
    assert response["Content-Type"].startswith("text/html")
    assert static("web/vendor/htmx.min.js") in response.content.decode()


def test_demo_action_post_returns_fragment():
    # FR-006: a CSRF-valid POST /htmx-demo/action/ returns 200 and the fragment
    # markup htmx swaps into #result.
    client = Client(enforce_csrf_checks=True)
    # Prime the CSRF cookie/token from the demo page, then echo it back.
    client.get("/htmx-demo/")
    token = client.cookies["csrftoken"].value
    response = client.post("/htmx-demo/action/", HTTP_X_CSRFTOKEN=token)

    assert response.status_code == 200
    assert "Clicked" in response.content.decode()


def test_demo_action_post_without_csrf_is_forbidden():
    # FR-006: the state-changing action is CSRF-protected. A token-less POST
    # against a CSRF-enforcing client is rejected with 403.
    response = Client(enforce_csrf_checks=True).post("/htmx-demo/action/")

    assert response.status_code == 403
