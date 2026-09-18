from flask import Flask, jsonify, request, send_from_directory

from chat_engine import generate_reply, load_personas
from engagement import SessionStore

app = Flask(__name__, static_folder="static")
sessions = SessionStore()


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/api/personas")
def personas():
    personas = load_personas()
    return jsonify(
        [
            {"key": key, "display_name": p["display_name"], "opening_line": p["opening_line"]}
            for key, p in personas.items()
        ]
    )


@app.post("/api/chat")
def chat():
    data = request.get_json(force=True)
    persona_key = data.get("persona", "nova")
    message = (data.get("message") or "").strip()
    session_id = data.get("session_id", "default")

    if not message:
        return jsonify({"error": "message is required"}), 400

    try:
        session = sessions.get(session_id)
        result = generate_reply(persona_key, message, history=session.history)
        session.register_turn(message, result["reply"])
        nudge = session.pending_nudge()

        return jsonify(
            {
                "reply": result["reply"],
                "mode": result["mode"],
                "message_count": session.message_count,
                "nudge": nudge,
            }
        )
    except KeyError:
        return jsonify({"error": f"unknown persona '{persona_key}'"}), 404


if __name__ == "__main__":
    app.run(debug=True, port=5000)
