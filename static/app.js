const commandInput = document.getElementById("command");
const classifyButton = document.getElementById("classifyButton");
const micButton = document.getElementById("micButton");
const speechStatus = document.getElementById("speechStatus");
const resultPanel = document.getElementById("result");

async function classifyCommand() {
  const text = commandInput.value.trim();
  if (!text) {
    speechStatus.textContent = "Please type or speak a command first.";
    commandInput.focus();
    return;
  }

  classifyButton.disabled = true;
  classifyButton.textContent = "Classifying…";
  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({text})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Prediction failed.");

    document.getElementById("intent").textContent =
      data.intent.replaceAll("_", " ").toUpperCase();
    document.getElementById("message").textContent = data.message;
    const percent = Math.round(data.confidence * 100);
    document.getElementById("confidence").textContent = `${percent}%`;
    document.getElementById("meterFill").style.width = `${percent}%`;
    resultPanel.classList.remove("hidden");
  } catch (error) {
    speechStatus.textContent = error.message;
  } finally {
    classifyButton.disabled = false;
    classifyButton.textContent = "Classify intent";
  }
}

classifyButton.addEventListener("click", classifyCommand);
commandInput.addEventListener("keydown", event => {
  if (event.ctrlKey && event.key === "Enter") classifyCommand();
});

document.querySelectorAll(".chip").forEach(button => {
  button.addEventListener("click", () => {
    commandInput.value = button.dataset.command;
    classifyCommand();
  });
});

// SpeechRecognition is supported in Chromium-based browsers. Text input
// remains available when the browser does not support microphone recognition.
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
if (SpeechRecognition) {
  const recognition = new SpeechRecognition();
  recognition.lang = "en-IN";
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  micButton.addEventListener("click", () => {
    speechStatus.textContent = "Listening… Please speak now.";
    recognition.start();
  });
  recognition.onresult = event => {
    commandInput.value = event.results[0][0].transcript;
    speechStatus.textContent = "Speech captured. Classifying your command…";
    classifyCommand();
  };
  recognition.onerror = event => {
    speechStatus.textContent = `Microphone error: ${event.error}. You can type instead.`;
  };
  recognition.onend = () => {
    if (speechStatus.textContent === "Listening… Please speak now.") {
      speechStatus.textContent = "Listening stopped.";
    }
  };
} else {
  micButton.disabled = true;
  micButton.title = "Speech recognition is not supported by this browser.";
  speechStatus.textContent =
    "Speech recognition is not available in this browser. You can still type commands.";
}
