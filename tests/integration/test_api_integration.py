import os
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health_endpoint():
    """Verifica se health check funciona"""
    response = client.get("/health")
    assert response.status_code == 200


def test_root_endpoint():
    """Testa endpoint raiz"""
    response = client.get("/")
    assert response.status_code == 200


def test_for_invalid_route():
    """Testa rota inexistente"""
    response = client.get("/rota-invalida")
    assert response.status_code == 404


def test_wrong_http_method():
    """Testa método HTTP incorreto"""
    response = client.get("/chat")
    assert response.status_code == 405