from fastapi import FastAPI

from marker.api.main import create_app


class TestCreateApp:
    def test_create_app_returns_fastapi_instance(self) -> None:
        app = create_app()

        assert isinstance(app, FastAPI)
