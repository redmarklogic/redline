"""Views for the Django web shell (#159).

Volatile per Constitution XIII — the root placeholder is replaced by the
auth-gated button page in #171. No database, session, or template access.
"""

from django.http import HttpResponse, JsonResponse


def root(request):
    """Return a minimal HTTP 200 placeholder page (contract: root-page.md).

    Args:
        request: The incoming HTTP request (unused; method-blind by contract).

    Returns:
        A 200 text/html response with non-contractual placeholder content.
    """
    return HttpResponse("<!doctype html><title>Redline</title><p>Redline web shell.</p>")


def health(request):
    """Return a JSON liveness signal (contract: health-endpoint.md, FR-007).

    Args:
        request: The incoming HTTP request (unused; no auth, DB, or session).

    Returns:
        A 200 application/json response with body {"status": "healthy"}.
    """
    return JsonResponse({"status": "healthy"})
