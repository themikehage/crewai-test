import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from agent.crew import analyze_random_fact, chat_with_agent

app = FastAPI()

class ChatMessage(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CrewAI Chat - Analista de Datos Curiosos</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            
            body {
                font-family: 'Inter', system-ui, -apple-system, sans-serif;
                background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            
            .chat-container {
                width: 100%;
                max-width: 600px;
                height: 80vh;
                max-height: 700px;
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(20px);
                border-radius: 24px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                display: flex;
                flex-direction: column;
                overflow: hidden;
                box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            }
            
            .chat-header {
                padding: 20px 24px;
                background: rgba(255, 255, 255, 0.03);
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
                display: flex;
                align-items: center;
                gap: 12px;
            }
            
            .avatar {
                width: 44px;
                height: 44px;
                border-radius: 50%;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 20px;
            }
            
            .header-info h1 {
                font-size: 16px;
                font-weight: 600;
                color: #fff;
            }
            
            .header-info p {
                font-size: 12px;
                color: rgba(255, 255, 255, 0.5);
                margin-top: 2px;
            }
            
            .status-dot {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: #22c55e;
                margin-left: auto;
                animation: pulse 2s infinite;
            }
            
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
            
            .chat-messages {
                flex: 1;
                overflow-y: auto;
                padding: 24px;
                display: flex;
                flex-direction: column;
                gap: 16px;
            }
            
            .chat-messages::-webkit-scrollbar {
                width: 6px;
            }
            
            .chat-messages::-webkit-scrollbar-track {
                background: transparent;
            }
            
            .chat-messages::-webkit-scrollbar-thumb {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 3px;
            }
            
            .message {
                display: flex;
                gap: 12px;
                max-width: 85%;
                animation: fadeIn 0.3s ease;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .message.user {
                align-self: flex-end;
                flex-direction: row-reverse;
            }
            
            .message-avatar {
                width: 32px;
                height: 32px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 14px;
                flex-shrink: 0;
            }
            
            .message.bot .message-avatar {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            
            .message.user .message-avatar {
                background: rgba(255, 255, 255, 0.15);
            }
            
            .message-content {
                padding: 12px 16px;
                border-radius: 18px;
                font-size: 14px;
                line-height: 1.5;
            }
            
            .message.bot .message-content {
                background: rgba(255, 255, 255, 0.08);
                color: #fff;
                border-bottom-left-radius: 4px;
            }
            
            .message.user .message-content {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #fff;
                border-bottom-right-radius: 4px;
            }
            
            .typing-indicator {
                display: flex;
                gap: 4px;
                padding: 8px 0;
            }
            
            .typing-indicator span {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.4);
                animation: typing 1.4s infinite;
            }
            
            .typing-indicator span:nth-child(2) { animation-delay: 0.2s; }
            .typing-indicator span:nth-child(3) { animation-delay: 0.4s; }
            
            @keyframes typing {
                0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
                30% { transform: translateY(-8px); opacity: 1; }
            }
            
            .chat-input {
                padding: 16px 20px;
                background: rgba(255, 255, 255, 0.03);
                border-top: 1px solid rgba(255, 255, 255, 0.08);
                display: flex;
                gap: 12px;
                align-items: center;
            }
            
            .chat-input input {
                flex: 1;
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 14px 18px;
                font-size: 14px;
                color: #fff;
                outline: none;
                transition: all 0.2s;
            }
            
            .chat-input input::placeholder {
                color: rgba(255, 255, 255, 0.4);
            }
            
            .chat-input input:focus {
                border-color: rgba(102, 126, 234, 0.5);
                background: rgba(255, 255, 255, 0.1);
            }
            
            .chat-input button {
                width: 44px;
                height: 44px;
                border-radius: 12px;
                border: none;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #fff;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.2s;
            }
            
            .chat-input button:hover {
                transform: scale(1.05);
            }
            
            .chat-input button:disabled {
                opacity: 0.5;
                cursor: not-allowed;
                transform: none;
            }
            
            .chat-input button svg {
                width: 20px;
                height: 20px;
            }
            
            .quick-actions {
                display: flex;
                gap: 8px;
                padding: 0 20px 16px;
                flex-wrap: wrap;
            }
            
            .quick-action {
                padding: 8px 14px;
                background: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 20px;
                font-size: 12px;
                color: rgba(255, 255, 255, 0.7);
                cursor: pointer;
                transition: all 0.2s;
            }
            
            .quick-action:hover {
                background: rgba(255, 255, 255, 0.1);
                color: #fff;
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div class="chat-header">
                <div class="avatar">🧠</div>
                <div class="header-info">
                    <h1>Analista de Datos Curiosos</h1>
                    <p>Powered by CrewAI + Groq</p>
                </div>
                <div class="status-dot"></div>
            </div>
            
            <div class="chat-messages" id="messages">
                <div class="message bot">
                    <div class="message-avatar">🧠</div>
                    <div class="message-content">
                        ¡Hola! Soy tu analista de datos curiosos. Puedo contarte hechos aleatorios y analizar si son útiles o inútiles. ¿Qué te gustaría saber?
                    </div>
                </div>
            </div>
            
            <div class="quick-actions">
                <div class="quick-action" onclick="sendQuick('Cuéntame un dato curioso')">🎲 Dato curioso</div>
                <div class="quick-action" onclick="sendQuick('¿Qué puedes hacer?')">❓ Ayuda</div>
            </div>
            
            <div class="chat-input">
                <input 
                    type="text" 
                    id="messageInput" 
                    placeholder="Escribe un mensaje..."
                    onkeypress="if(event.key === 'Enter') sendMessage()"
                >
                <button onclick="sendMessage()" id="sendBtn">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M22 2L11 13M22 2L15 22L11 13M22 2L2 9L11 13"/>
                    </svg>
                </button>
            </div>
        </div>

        <script>
            const messagesDiv = document.getElementById('messages');
            const input = document.getElementById('messageInput');
            const sendBtn = document.getElementById('sendBtn');
            
            function addMessage(content, isUser = false) {
                const msg = document.createElement('div');
                msg.className = `message ${isUser ? 'user' : 'bot'}`;
                msg.innerHTML = `
                    <div class="message-avatar">${isUser ? '👤' : '🧠'}</div>
                    <div class="message-content">${content}</div>
                `;
                messagesDiv.appendChild(msg);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }
            
            function addTypingIndicator() {
                const msg = document.createElement('div');
                msg.className = 'message bot';
                msg.id = 'typing';
                msg.innerHTML = `
                    <div class="message-avatar">🧠</div>
                    <div class="message-content">
                        <div class="typing-indicator">
                            <span></span><span></span><span></span>
                        </div>
                    </div>
                `;
                messagesDiv.appendChild(msg);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }
            
            function removeTypingIndicator() {
                const typing = document.getElementById('typing');
                if (typing) typing.remove();
            }
            
            async function sendMessage() {
                const message = input.value.trim();
                if (!message) return;
                
                addMessage(message, true);
                input.value = '';
                sendBtn.disabled = true;
                addTypingIndicator();
                
                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message })
                    });
                    
                    const data = await response.json();
                    removeTypingIndicator();
                    
                    if (data.success) {
                        addMessage(data.result);
                    } else {
                        addMessage('Error: ' + data.error);
                    }
                } catch (error) {
                    removeTypingIndicator();
                    addMessage('Error de conexión: ' + error.message);
                }
                
                sendBtn.disabled = false;
                input.focus();
            }
            
            function sendQuick(text) {
                input.value = text;
                sendMessage();
            }
            
            input.focus();
        </script>
    </body>
    </html>
    """

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/agent")
async def run_agent():
    try:
        result = analyze_random_fact()
        return {
            "success": True,
            "result": str(result)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/chat")
async def chat(chat_message: ChatMessage):
    try:
        result = chat_with_agent(chat_message.message)
        return {
            "success": True,
            "result": str(result)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
