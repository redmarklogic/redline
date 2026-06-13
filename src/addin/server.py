"""Flask dev server for the Word taskpane spike (issue #190, Scenario 1).

Serves a single static hello-world page at ``/taskpane.html`` over HTTPS, using
the certificate produced by :mod:`addin.make_cert`. Adapted from the Masterjx9
Outlook-Addin-TaskPane-python template's ``app.py`` (see ``README.md``).

Run::

    python -m addin.server

Generate the certificate first with ``python -m addin.make_cert``.
"""

from pathlib import Path

from flask import Flask

# Resolve paths relative to the package directory, not the process working
# directory, so the server starts from any cwd (plan risk register).
HERE = Path(__file__).resolve().parent
CERT = HERE / "certs" / "cert.pem"
KEY = HERE / "certs" / "key.pem"
TASKPANE = HERE / "static" / "taskpane.html"

PORT = 3000  # Office add-in convention; single documented value (FR-006, plan D6).

app = Flask(__name__, static_folder="static", static_url_path="")


@app.route("/taskpane.html", methods=["GET"])
def taskpane():
    """Serve the static hello-world taskpane page (FR-001).

    The page is read eagerly into the response rather than streamed via a lazy
    file handle, so no dangling file descriptor is finalized after the request
    (which trips ``filterwarnings=error`` under pytest).
    """
    return TASKPANE.read_text(encoding="utf-8"), 200, {"Content-Type": "text/html"}


def main() -> None:
    """Start the HTTPS dev server on the documented port.

    Binds with ``ssl_context=(cert, key)`` so the page is served over HTTPS as
    Microsoft Word add-ins require (FR-002). Fails loudly if the port is in use
    or the certificate is missing (run ``python -m addin.make_cert`` first).
    """
    if not CERT.exists() or not KEY.exists():
        raise SystemExit(
            f"Certificate not found at {CERT} / {KEY}. "
            "Run `python -m addin.make_cert` first."
        )
    app.run(host="localhost", port=PORT, ssl_context=(str(CERT), str(KEY)))


if __name__ == "__main__":
    main()
