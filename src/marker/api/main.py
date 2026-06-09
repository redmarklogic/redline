"""FastAPI application factory for the Marker API."""

from fastapi import FastAPI

from marker.api import routes
from marker.api.exception_handlers import register_exception_handlers


def create_app() -> FastAPI:
    """Create and configure the Marker FastAPI application.

    Returns:
        Configured FastAPI application instance.
    """
    app = FastAPI(title="Marker API", version="0.1.0")
    register_exception_handlers(app)
    app.include_router(routes.router)
    return app
