import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_personas_endpoint(client):
    res = client.get("/api/personas")
    assert res.status_code == 200
    data = res.get_json()
    assert any(p["key"] == "nova" for p in data)


def test_chat_endpoint_requires_message(client):
    res = client.post("/api/chat", json={"persona": "nova", "message": ""})
    assert res.status_code == 400


def test_chat_endpoint_happy_path(client):
    res = client.post(
        "/api/chat",
        json={"persona": "nova", "message": "hi", "session_id": "test-session"},
    )
    assert res.status_code == 200
    data = res.get_json()
    assert "reply" in data
    assert data["message_count"] == 1


def test_chat_endpoint_unknown_persona(client):
    res = client.post(
        "/api/chat",
        json={"persona": "ghost", "message": "hi", "session_id": "test-session-2"},
    )
    assert res.status_code == 404
