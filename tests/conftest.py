import pytest
from fastapi.testclient import TestClient

from config import settings
from main import app


@pytest.fixture(scope="function")
def client() -> TestClient:
    with TestClient(app, base_url="http://127.0.0.1:6080") as client:
        yield client


@pytest.fixture(scope="function")
def get_test_user() -> dict[str, str]:
    return {"login": settings.auth.login, "password": settings.auth.login}
