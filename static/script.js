const messagesEl = document.getElementById("messages");
const formEl = document.getElementById("chat-form");
const inputEl = document.getElementById("chat-input");
const personaSelect = document.getElementById("persona-select");
const nudgeEl = document.getElementById("nudge");
const modeEl = document.getElementById("mode-indicator");

const sessionId = crypto.randomUUID();
let personas = [];

function addMessage(role, text) {
  const div = document.createElement("div");
  div.className = `msg ${role}`;
  div.textContent = text;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

async function loadPersonas() {
  const res = await fetch("/api/personas");
  personas = await res.json();
  personaSelect.innerHTML = personas
    .map((p) => `<option value="${p.key}">${p.display_name}</option>`)
    .join("");
  showOpeningLine();
}

function showOpeningLine() {
  messagesEl.innerHTML = "";
  const current = personas.find((p) => p.key === personaSelect.value) || personas[0];
  if (current) addMessage("assistant", current.opening_line);
}

personaSelect.addEventListener("change", showOpeningLine);

formEl.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = inputEl.value.trim();
  if (!message) return;

  addMessage("user", message);
  inputEl.value = "";

  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, persona: personaSelect.value, session_id: sessionId }),
  });
  const data = await res.json();

  if (data.error) {
    addMessage("assistant", `(error: ${data.error})`);
    return;
  }

  addMessage("assistant", data.reply);
  modeEl.textContent = data.mode;

  if (data.nudge) {
    nudgeEl.textContent = data.nudge;
    nudgeEl.classList.remove("hidden");
  }
});

loadPersonas();
