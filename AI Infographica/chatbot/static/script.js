async function sendMessage() {
  let input = document.getElementById("user-input");
  let message = input.value.trim();
  if (!message) return;

  let langSelect = document.getElementById("language-select");
  let language = langSelect.value;

  let chatBox = document.getElementById("chat-box");
  chatBox.innerHTML += `<div class='user-msg'>You: ${message}</div>`;
  input.value = "";

  let response = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, language })
  });

  let data = await response.json();
  chatBox.innerHTML += `<div class='bot-msg'>Bot: ${data.reply}</div>`;
  chatBox.scrollTop = chatBox.scrollHeight;
}
