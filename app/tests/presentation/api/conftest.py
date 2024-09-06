from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest

from presentation.api.main import create_app
from tests.fixtures import init_dummy_container


@pytest.fixture
def app() -> FastAPI:
    app = create_app(container=init_dummy_container())
    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
