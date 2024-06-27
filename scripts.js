const chatMessages = document.getElementById("chat-messages");
const messageInput = document.getElementById("message-input");

function appendMessage(role, message) {
  const messageElement = document.createElement("div");
  messageElement.classList.add("message", role);
  messageElement.innerText = message;
  chatMessages.appendChild(messageElement);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function sendMessage() {
  const message = messageInput.value.trim();
  if (message) {
    appendMessage("user", message);
    messageInput.value = "";

    // Send message to backend
    fetch("/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    })
      .then((response) => response.json())
      .then((data) => {
        const aiResponse = data.message;
        appendMessage("assistant", aiResponse);
      })
      .catch((error) => console.error("Error sending message:", error));
  }
}

// Initial message to start conversation
document.addEventListener("DOMContentLoaded", function () {
  appendMessage("assistant", "Hi Imani, how may I help you?");
});
