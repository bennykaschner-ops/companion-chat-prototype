import os

import pytest

from chat_engine import generate_reply, load_personas


def test_load_personas_has_expected_keys():
    personas = load_personas()
    assert "nova" in personas
    assert "sage" in personas
    assert "system_prompt" in personas["nova"]


def test_generate_reply_mock_mode_when_no_api_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    result = generate_reply("nova", "hello there")
    assert result["mode"] == "mock"
    assert isinstance(result["reply"], str) and len(result["reply"]) > 0


def test_generate_reply_unknown_persona_raises_keyerror():
    with pytest.raises(KeyError):
        generate_reply("does-not-exist", "hi")


def test_generate_reply_is_deterministic_for_same_message_length(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    r1 = generate_reply("nova", "abc")
    r2 = generate_reply("nova", "xyz")  # same length, different content
    assert r1["reply"] == r2["reply"]
