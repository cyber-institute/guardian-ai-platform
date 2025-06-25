"""
Draggable Floating Chat Component for GUARDIAN
Uses Streamlit components to create a properly working draggable chat bubble
"""

import streamlit as st
import streamlit.components.v1 as components
import uuid

def render_draggable_chat():
    """Render a draggable floating chat bubble that actually works."""
    
    # Initialize chat state
    if 'chat_open' not in st.session_state:
        st.session_state.chat_open = False
    if 'chat_session_id' not in st.session_state:
        st.session_state.chat_session_id = str(uuid.uuid4())
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []

    # Create the draggable floating chat component
    chat_html = f"""
    <div id="floating-chat-container">
        <div id="chat-bubble" class="chat-bubble" draggable="false">
            <div class="bubble-content">
                <div class="bubble-lines">
                    <div class="line"></div>
                    <div class="line"></div>
                    <div class="line"></div>
                </div>
            </div>
        </div>
        
        <div id="chat-window" class="chat-window" style="display: none;">
            <div class="chat-header">
                <span>ARIA Chat</span>
                <button id="close-chat" class="close-btn">&times;</button>
            </div>
            <div class="chat-body">
                <div id="chat-messages"></div>
                <div class="chat-input-area">
                    <input type="text" id="chat-input" placeholder="Ask ARIA about GUARDIAN...">
                    <button id="send-btn">Send</button>
                </div>
            </div>
        </div>
    </div>

    <style>
    #floating-chat-container {{
        position: fixed !important;
        bottom: 20px !important;
        right: 20px !important;
        z-index: 99999 !important;
        font-family: 'Inter', sans-serif;
        pointer-events: auto !important;
    }}
    
    .chat-bubble {{
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%);
        border-radius: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: move;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4);
        transition: all 0.3s ease;
        user-select: none;
        border: 3px solid #1E40AF;
        position: relative;
    }}
    
    .chat-bubble:before {{
        content: "";
        position: absolute;
        bottom: -12px;
        left: 15px;
        width: 0;
        height: 0;
        border-left: 12px solid transparent;
        border-right: 0px solid transparent;
        border-top: 12px solid #1E40AF;
        transform: rotate(15deg);
    }}
    
    .chat-bubble:hover {{
        transform: scale(1.1);
        box-shadow: 0 6px 30px rgba(59, 130, 246, 0.6);
    }}
    
    .bubble-lines {{
        display: flex;
        flex-direction: column;
        gap: 3px;
        align-items: center;
    }}
    
    .line {{
        width: 20px;
        height: 2px;
        background: white;
        border-radius: 1px;
    }}
    
    .line:nth-child(2) {{
        width: 16px;
    }}
    
    .line:nth-child(3) {{
        width: 24px;
    }}
    
    .chat-window {{
        position: absolute;
        bottom: 80px;
        right: 0;
        width: 300px;
        height: 400px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
        border: 1px solid #e2e8f0;
        overflow: hidden;
    }}
    
    .chat-header {{
        background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%);
        color: white;
        padding: 12px 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-weight: 600;
    }}
    
    .close-btn {{
        background: none;
        border: none;
        color: white;
        font-size: 20px;
        cursor: pointer;
        padding: 0;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    
    .chat-body {{
        height: calc(100% - 48px);
        display: flex;
        flex-direction: column;
    }}
    
    #chat-messages {{
        flex: 1;
        padding: 16px;
        overflow-y: auto;
        font-size: 14px;
    }}
    
    .chat-input-area {{
        padding: 16px;
        border-top: 1px solid #e2e8f0;
        display: flex;
        gap: 8px;
    }}
    
    #chat-input {{
        flex: 1;
        padding: 8px 12px;
        border: 1px solid #d1d5db;
        border-radius: 6px;
        font-size: 14px;
    }}
    
    #send-btn {{
        background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%);
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 6px;
        cursor: pointer;
        font-size: 14px;
    }}
    
    .message {{
        margin: 8px 0;
        padding: 8px 12px;
        border-radius: 8px;
        max-width: 85%;
    }}
    
    .user-message {{
        background: #3B82F6;
        color: white;
        margin-left: auto;
        text-align: right;
    }}
    
    .bot-message {{
        background: #f1f5f9;
        color: #334155;
        margin-right: auto;
    }}
    </style>

    <script>
    (function() {{
        let isDragging = false;
        let dragOffset = {{ x: 0, y: 0 }};
        let chatOpen = false;
        
        const container = document.getElementById('floating-chat-container');
        const bubble = document.getElementById('chat-bubble');
        const chatWindow = document.getElementById('chat-window');
        const closeBtn = document.getElementById('close-chat');
        const sendBtn = document.getElementById('send-btn');
        const chatInput = document.getElementById('chat-input');
        const messagesDiv = document.getElementById('chat-messages');
        
        // Make draggable
        bubble.addEventListener('mousedown', startDrag);
        document.addEventListener('mousemove', drag);
        document.addEventListener('mouseup', stopDrag);
        
        function startDrag(e) {{
            e.preventDefault();
            isDragging = true;
            const rect = container.getBoundingClientRect();
            dragOffset.x = e.clientX - rect.left;
            dragOffset.y = e.clientY - rect.top;
            bubble.style.cursor = 'grabbing';
        }}
        
        function drag(e) {{
            if (!isDragging) return;
            e.preventDefault();
            
            const x = e.clientX - dragOffset.x;
            const y = e.clientY - dragOffset.y;
            
            // Keep within viewport
            const maxX = window.innerWidth - container.offsetWidth;
            const maxY = window.innerHeight - container.offsetHeight;
            
            const clampedX = Math.max(0, Math.min(x, maxX));
            const clampedY = Math.max(0, Math.min(y, maxY));
            
            container.style.left = clampedX + 'px';
            container.style.top = clampedY + 'px';
            container.style.right = 'auto';
            container.style.bottom = 'auto';
        }}
        
        function stopDrag() {{
            isDragging = false;
            bubble.style.cursor = 'move';
        }}
        
        // Chat functionality
        bubble.addEventListener('click', function(e) {{
            if (!isDragging) {{
                toggleChat();
            }}
        }});
        
        closeBtn.addEventListener('click', function() {{
            toggleChat();
        }});
        
        function toggleChat() {{
            chatOpen = !chatOpen;
            chatWindow.style.display = chatOpen ? 'block' : 'none';
            
            if (chatOpen && messagesDiv.children.length === 0) {{
                addMessage('bot', 'Hello! I\\'m ARIA, your Advanced Risk Intelligence Assistant. How can I help you with GUARDIAN today?');
            }}
        }}
        
        function addMessage(type, text) {{
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${{type}}-message`;
            messageDiv.textContent = text;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }}
        
        function sendMessage() {{
            const input = chatInput.value.trim();
            if (!input) return;
            
            addMessage('user', input);
            chatInput.value = '';
            
            // Simple bot responses
            setTimeout(() => {{
                let response = generateResponse(input);
                addMessage('bot', response);
            }}, 500);
        }}
        
        function generateResponse(input) {{
            const lower = input.toLowerCase();
            
            if (lower.includes('score') || lower.includes('scoring')) {{
                return 'GUARDIAN uses AI Cybersecurity (0-100), Quantum Readiness (Tier 1-5), and AI Ethics scoring. Click any score badge for detailed analysis!';
            }} else if (lower.includes('upload') || lower.includes('document')) {{
                return 'You can upload documents via the file uploader in All Documents tab, or enter URLs for web scraping. Supported formats: PDF, TXT, DOCX.';
            }} else if (lower.includes('gap') || lower.includes('policy')) {{
                return 'GUARDIAN identifies policy gaps by comparing your documents against NIST frameworks and quantum readiness standards.';
            }} else if (lower.includes('help') || lower.includes('how')) {{
                return 'Navigate using the tabs: All Documents shows your repository, About explains the system. Need help with a specific feature?';
            }} else {{
                return `I understand you\\'re asking about "${{input}}". I can help with document scoring, uploads, policy analysis, and navigation. What specifically would you like to know?`;
            }}
        }}
        
        sendBtn.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', function(e) {{
            if (e.key === 'Enter') {{
                sendMessage();
            }}
        }});
        
        // Debug logging
        console.log('Chat bubble initialized');
        
        // Return value to Streamlit (required for components)
        window.parent.postMessage({{
            type: 'streamlit:setComponentValue',
            value: {{ initialized: true }}
        }}, '*');
    }})();
    </script>
    """
    
    # Render the component with proper height
    result = components.html(chat_html, height=100)
    
    return result