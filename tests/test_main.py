from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Testa o endpoint raiz"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data


def test_chat_endpoint_missing_message():
    response = client.post("/chat", params={"message": ""})
    assert response.status_code == 500


def test_chat_endpoint_with_message():
    response = client.post("/chat", params={"message": "Me fale algo sobre panquecas"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
