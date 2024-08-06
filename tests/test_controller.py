from tests.conftest import client, get_test_user
from fastapi.testclient import TestClient
from httpx import Response


def test_login(client: TestClient, get_test_user: dict[str, str]):
    etalon_practice_name: str = 'practice_main'
    response: Response = client.post("/login", json=get_test_user)
    response_text: dict[str, str] = response.json()
    assert response.status_code == 200
    assert response_text.get('practice_name') == etalon_practice_name


def test_logout_failed(client: TestClient):
    response: Response = client.post("/logout")
    assert response.status_code == 401


def test_logout_successful(client: TestClient, get_test_user: dict[str, str]):
    etalon_message: str = 'Пользователь успешно вышел из системы.'
    client.post("/login", json=get_test_user)
    response: Response = client.post("/logout")
    response_text: dict[str, str] = response.json()
    assert response.status_code == 200
    assert response_text.get('message') == etalon_message


def test_get_appsec_correct_appsec(client: TestClient, get_test_user: dict[str, str]):
    etalon_practice_name: str = 'practice_sast'
    client.post("/login", json=get_test_user)
    response: Response = client.get("/appsec?key=practice_sast")
    response_text: dict[str, str] = response.json()
    assert response.status_code == 200
    assert response_text.get('practice_name') == etalon_practice_name


def test_get_appsec_incorrect_appsec(client: TestClient, get_test_user: dict[str, str]):
    etalon_message: str = 'Указана неверная практика разработки.'
    client.post("/login", json=get_test_user)
    response: Response = client.get("/appsec?key=practice")
    response_text: dict[str, str] = response.json()
    assert response.status_code == 404
    assert response_text.get('message') == etalon_message
