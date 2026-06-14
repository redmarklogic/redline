"""Throwaway htmx demonstration views (#162).

Proves the vendored htmx round trip: a page whose button POSTs to the action
view and swaps the returned HTML fragment into the page in place. Isolated in
its own module and URL namespace so #171 can delete it cleanly when the real
auth-gated button page lands (D4, FR-006). No database, session, or auth.
"""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def htmx_demo(request: HttpRequest) -> HttpResponse:
    """Render the demo page that loads htmx and hosts the round-trip button.

    Args:
        request: The incoming HTTP request (method-blind; GET in practice).

    Returns:
        A 200 text/html response rendering ``web/demo/htmx_demo.html``.
    """
    return render(request, "web/demo/htmx_demo.html")


def htmx_demo_action(request: HttpRequest) -> HttpResponse:
    """Return the server-rendered fragment htmx swaps into the page.

    Args:
        request: The incoming HTTP request (POST; CSRF-protected by middleware).

    Returns:
        A 200 text/html response rendering the static ``_clicked.html`` fragment.
    """
    return render(request, "web/demo/_clicked.html")
