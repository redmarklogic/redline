"""Tests for the addin Flask server (issue #190, Scenario 1).

These exercise routing and body via Flask's test client. The HTTPS/ssl_context
binding is not testable here (the test client does not perform a TLS handshake);
it is verified by the live ``curl`` acceptance check in the plan.
"""

from addin.server import app


def test_taskpane_returns_200():
    """GET /taskpane.html returns HTTP 200."""
    response = app.test_client().get("/taskpane.html")
    assert response.status_code == 200


def test_taskpane_body_contains_hello_world_marker():
    """The served page contains the hello-world marker text (FR-005, SC-002)."""
    response = app.test_client().get("/taskpane.html")
    assert b"hello" in response.data.lower()


def test_unknown_path_returns_404():
    """An unknown path returns 404, not a crash (edge case)."""
    response = app.test_client().get("/no-such-page.html")
    assert response.status_code == 404


def test_taskpane_sends_no_cache_headers():
    """The page is served uncacheable so the web view never shows a stale edit.

    The embedded WebView2 caches the taskpane; ``Cache-Control: no-store`` plus
    ``Pragma: no-cache`` force a fresh fetch on every reload (FR-001, FR-002,
    SC-001 — issue #192).
    """
    response = app.test_client().get("/taskpane.html")
    assert "no-store" in response.headers.get("Cache-Control", "")
    assert response.headers.get("Pragma") == "no-cache"
