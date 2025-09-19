document.getElementById('send-btn').addEventListener('click', sendMessage);
document.getElementById('user-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (userInput.trim() === "") return;

    // Add user message to chat box
    const chatBox = document.getElementById('chat-box');
    const userMessage = document.createElement('div');
    userMessage.className = 'user-message';
    userMessage.textContent = userInput;
    chatBox.appendChild(userMessage);

    // Clear input
    document.getElementById('user-input').value = '';

    // Scroll to bottom
    chatBox.scrollTop = chatBox.scrollHeight;

    // Send message to backend
    fetch(`/get-response/?message=${encodeURIComponent(userInput)}`, {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        // Add bot response to chat box
        const botMessage = document.createElement('div');
        botMessage.className = 'bot-message';
        botMessage.textContent = data.response;
        chatBox.appendChild(botMessage);

        // Scroll to bottom
        chatBox.scrollTop = chatBox.scrollHeight;

        // Speak the bot's response
        speak(data.response);
    })
    .catch(error => console.error('Error:', error));
}

// Function to speak text using the Web Speech API
function speak(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.voice = speechSynthesis.getVoices().find(voice => voice.name === 'Google US English'); // Optional: Set a specific voice
        speechSynthesis.speak(utterance);
    } else {
        console.error('Web Speech API is not supported in this browser.');
    }
}
const utterance = new SpeechSynthesisUtterance("Hello, this is a test.");
speechSynthesis.speak(utterance);