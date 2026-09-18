from engagement import SessionStore


def test_new_session_has_zero_messages():
    store = SessionStore()
    session = store.get("abc")
    assert session.message_count == 0
    assert session.pending_nudge() is None


def test_nudge_fires_at_message_three():
    store = SessionStore()
    session = store.get("abc")
    for i in range(3):
        session.register_turn(f"msg {i}", f"reply {i}")
    assert session.message_count == 3
    assert session.pending_nudge() is not None


def test_nudge_does_not_fire_outside_configured_counts():
    store = SessionStore()
    session = store.get("abc")
    for i in range(2):
        session.register_turn(f"msg {i}", f"reply {i}")
    assert session.pending_nudge() is None


def test_sessions_are_isolated_by_id():
    store = SessionStore()
    a = store.get("a")
    b = store.get("b")
    a.register_turn("hi", "hello")
    assert a.message_count == 1
    assert b.message_count == 0
