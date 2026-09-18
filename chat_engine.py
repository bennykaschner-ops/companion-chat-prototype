"""
Core chat engine for the companion prototype.

Design goal: the engine works out of the box with zero API keys (so anyone
cloning the repo can run it immediately), but transparently upgrades to a
real LLM (Anthropic's Claude) the moment an ANTHROPIC_API_KEY is present.
That "mock-first, real-when-available" pattern is deliberate: it's a small
product decision (frictionless demo > forcing a setup step) baked into the
code, not just a coding exercise.
"""

import json
import os
import random
from pathlib import Path

PERSONAS_PATH = Path(__file__).parent / "personas.json"


def load_personas() -> dict:
    with open(PERSONAS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _mock_reply(persona: dict, message: str) -> str:
    """Deterministic-ish fallback so the app is fully functional with no API key."""
    bank = persona["fallback_bank"]
    # light "personalization": pick based on message length so replies vary
    # instead of being purely random, and stay stable for repeated inputs.
    index = len(message) % len(bank)
    return bank[index]


def _llm_reply(persona: dict, message: str, history: list) -> str:
    """Real LLM call via Anthropic's API. Only used when ANTHROPIC_API_KEY is set."""
    import anthropic

    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    messages = history + [{"role": "user", "content": message}]
    response = client.messages.create(
        model="claude-3-5-haiku-latest",
        max_tokens=200,
        system=persona["system_prompt"],
        messages=messages,
    )
    return response.content[0].text


def generate_reply(persona_key: str, message: str, history: list | None = None) -> dict:
    """
    Returns {"reply": str, "mode": "llm" | "mock"}.
    Raises KeyError if persona_key is unknown.
    """
    personas = load_personas()
    persona = personas[persona_key]  # KeyError on purpose: fail loudly on bad input
    history = history or []

    if os.environ.get("ANTHROPIC_API_KEY"):
        try:
            return {"reply": _llm_reply(persona, message, history), "mode": "llm"}
        except Exception:
            # Never let a flaky API call break the demo experience.
            return {"reply": _mock_reply(persona, message), "mode": "mock-fallback"}

    return {"reply": _mock_reply(persona, message), "mode": "mock"}
