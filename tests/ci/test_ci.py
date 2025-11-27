from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data


def test_for_invalid_route():
    response = client.get("/rota-invalida")
    assert response.status_code == 404


def test_wrong_http_method():
    response = client.get("/chat")
    assert response.status_code == 405


def test_docs_endpoint():
    response = client.get("/docs")
    assert response.status_code == 200


def test_chat_endpoint_with_message():
    response = client.post("/chat", params={"message": "Olá, tudo bem?"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
