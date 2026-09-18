"""
Lightweight engagement/retention layer.

This is the "product" part of the prototype: a companion app's business
model lives or dies on repeat usage, so the engine tracks a simple
per-session engagement signal and surfaces a *nudge* at defined moments,
the same way a homepage recommendation slot or a push notification would.

Kept deliberately simple (in-memory dict, no DB) since the point here is to
demonstrate the pattern end-to-end, not to build production infra.
"""

from dataclasses import dataclass, field

NUDGE_AT_MESSAGE_COUNTS = {3, 7}

NUDGES = {
    3: "By the way, I'm here most days if you want to check back in — want me to remind you tomorrow?",
    7: "We've talked for a bit now — want to save this conversation so we can pick it back up later?",
}


@dataclass
class SessionState:
    message_count: int = 0
    history: list = field(default_factory=list)

    def register_turn(self, user_message: str, reply: str) -> None:
        self.message_count += 1
        self.history.append({"role": "user", "content": user_message})
        self.history.append({"role": "assistant", "content": reply})

    def pending_nudge(self) -> str | None:
        return NUDGES.get(self.message_count)


class SessionStore:
    """In-memory store keyed by session_id. Fine for a demo; would be Redis in prod."""

    def __init__(self):
        self._sessions: dict[str, SessionState] = {}

    def get(self, session_id: str) -> SessionState:
        if session_id not in self._sessions:
            self._sessions[session_id] = SessionState()
        return self._sessions[session_id]
