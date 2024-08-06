import pytest
from fastapi.testclient import TestClient

from main import app
from t1_company.src.shema import User


@pytest.fixture(scope="function")
def client() -> TestClient:
    with TestClient(app, base_url="http://127.0.0.1:6080") as client:
        yield client


@pytest.fixture(scope="function")
def get_test_user() -> dict[str, str]:
    return {"login": "admin", "password": "admin"}
