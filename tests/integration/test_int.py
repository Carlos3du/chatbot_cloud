import httpx

STAGING_URL = "http://localhost:8000/chat"
client = httpx.Client(base_url=STAGING_URL, timeout=60.0)


def test_chat_message():
    response = client.post("/chat", params={"message": "Olá, responda apenas 'oi"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert len(data["response"]) > 0


def test_chat_special_characters():
    response = client.post(
        "/chat", params={"message": "Olá! Como está? 😊 #teste @user"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
