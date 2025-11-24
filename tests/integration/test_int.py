import os, httpx


STAGING_URL = os.getenv("STAGING_URL")
client = httpx.Client(base_url=STAGING_URL)


def test_chat_message():
    response = client.post("/chat", params={"message": "Olá, responda apenas 'oi"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert len(data["response"]) > 0


def test_chat_long_message():
    long_message = "Explique " + "detalhadamente " * 50 + "sobre IA"
    response = client.post("/chat", params={"message": long_message})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data


def test_chat_special_characters():
    response = client.post(
        "/chat", params={"message": "Olá! Como está? 😊 #teste @user"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
