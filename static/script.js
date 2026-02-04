document.addEventListener('DOMContentLoaded', () => {
    const inputField = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const chatHistory = document.getElementById('chat-history');

    // Auto-focus input
    inputField.focus();

    // Event Listeners
    sendBtn.addEventListener('click', sendMessage);
    inputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    async function sendMessage() {
        const text = inputField.value.trim();
        if (!text) return;

        // Add User Message
        addMessage(text, 'user');
        inputField.value = '';

        // Show Typing Indicator (simulated)
        const loadingId = addLoadingIndicator();
        scrollToBottom();

        try {
            // Send to Backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: text }),
            });

            const data = await response.json();

            // Remove loading and add System Message
            removeMessage(loadingId);
            addMessage(data.response, 'system');

        } catch (error) {
            console.error('Error:', error);
            removeMessage(loadingId);
            addMessage("System Error: Connection to Core Failed.", 'system');
        }

        scrollToBottom();
    }

    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;

        const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        // Icon based on sender
        const icon = sender === 'system' ? 'fa-robot' : 'fa-user';

        messageDiv.innerHTML = `
            <div class="avatar"><i class="fas ${icon}"></i></div>
            <div class="content">
                <p>${text}</p>
                <span class="timestamp">${timestamp}</span>
            </div>
        `;

        chatHistory.appendChild(messageDiv);
        return messageDiv; // Return for manipulation if needed
    }

    function addLoadingIndicator() {
        const id = 'loading-' + Date.now();
        const messageDiv = document.createElement('div');
        messageDiv.className = `message system-message`;
        messageDiv.id = id;

        messageDiv.innerHTML = `
            <div class="avatar"><i class="fas fa-atom fa-spin"></i></div>
            <div class="content">
                <p>Processing Neural Pathways...</p>
            </div>
        `;

        chatHistory.appendChild(messageDiv);
        return id;
    }

    function removeMessage(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    function scrollToBottom() {
        chatHistory.scrollTop = chatHistory.scrollHeight;
    }
});
