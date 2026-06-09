"""FastAPI application factory for the Marker API."""

from fastapi import FastAPI


def create_app() -> FastAPI:
    """Create and configure the Marker FastAPI application.

    Returns:
        Configured FastAPI application instance.
    """
    app = FastAPI(docs_url=None, redoc_url=None)
    return app
