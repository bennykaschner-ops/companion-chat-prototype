# Companion Chat Prototype

A small, functional AI companion chat app: persona-based conversation,
optional real LLM integration (Anthropic Claude), and a simple retention
nudge system inspired by recommendation/engagement patterns I work with as
a product manager.

Built end-to-end with AI-assisted coding (Claude) as a hands-on exercise —
this repo's commit history shows the incremental build, not a single dump.

## Why this exists

My day-to-day product work involves prototyping (Figma/no-code) to brief
UX and engineering, not personally shipping code. I built this specific
project to get real, first-hand experience with AI-assisted development —
writing/modifying code, running tests, and using Git — end to end.

## What it does

- Chat with one of two personas (Nova, Sage), each with a distinct tone.
- Works immediately with **no API key** (deterministic mock replies), and
  transparently upgrades to real Claude responses if `ANTHROPIC_API_KEY`
  is set — a small product decision (zero-friction demo first) reflected
  directly in the code (`chat_engine.py`).
- Tracks a lightweight engagement signal per session and surfaces a
  **retention nudge** after 3 and 7 messages (`engagement.py`) — the same
  pattern behind a homepage recommendation slot or a re-engagement push,
  just simplified into an in-memory demo.

## Architecture

```
static/          chat UI (HTML/CSS/vanilla JS)
app.py           Flask routes: /, /api/personas, /api/chat
chat_engine.py   persona loading + LLM call / mock fallback
engagement.py    per-session message count + nudge logic
personas.json    persona definitions (tone, system prompt, fallback replies)
tests/           pytest coverage for engine, engagement, and API
```

## Running it

```bash
pip install -r requirements.txt
python app.py
# open http://localhost:5000
```

To use real Claude responses instead of the mock fallback:

```bash
export ANTHROPIC_API_KEY=sk-...
python app.py
```

## Tests

```bash
pytest
```

## What I'd build next

- Persist sessions (Redis) instead of an in-memory dict.
- A/B test nudge copy and timing against a real retention metric (D1/D7
  return rate) rather than a fixed message-count trigger.
- Add guardrails/content moderation hooks around the LLM call.
