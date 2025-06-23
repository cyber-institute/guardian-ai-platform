"""
Floating Chat Interface for GUARDIAN
Provides a persistent floating chat button and expandable chat window
"""

import streamlit as st
import uuid
from utils.dialogflow_chatbot import chatbot

def render_floating_chat():
    """Render a floating chat bubble interface using component state."""
    
    # Initialize chat state
    if 'chat_open' not in st.session_state:
        st.session_state.chat_open = False
    if 'chat_session_id' not in st.session_state:
        st.session_state.chat_session_id = str(uuid.uuid4())
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []

    # CSS for floating chat bubble
    st.markdown("""
    <style>
    /* Floating chat button */
    .floating-chat-btn {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%);
        color: white;
        border: none;
        font-weight: 600;
        font-size: 12px;
        cursor: pointer;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4);
        z-index: 10000;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
        animation: pulse 3s infinite;
    }
    
    .floating-chat-btn:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 30px rgba(59, 130, 246, 0.6);
    }
    
    @keyframes pulse {
        0%, 100% { box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4); }
        50% { box-shadow: 0 4px 20px rgba(59, 130, 246, 0.8); }
    }
    
    /* Chat bubble window */
    .chat-bubble {
        position: fixed;
        bottom: 90px;
        right: 20px;
        width: 350px;
        max-height: 500px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
        border: 1px solid #e5e7eb;
        z-index: 10001;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        animation: slideUp 0.3s ease;
    }
    
    @keyframes slideUp {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    /* Chat header */
    .chat-header {
        background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%);
        color: white;
        padding: 15px 20px;
        font-weight: 600;
        font-size: 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .chat-close-btn {
        background: none;
        border: none;
        color: white;
        font-size: 18px;
        cursor: pointer;
        padding: 0;
        width: 20px;
        height: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Chat body */
    .chat-body {
        flex: 1;
        padding: 15px;
        max-height: 350px;
        overflow-y: auto;
    }
    
    /* Chat input area */
    .chat-input-area {
        padding: 15px;
        border-top: 1px solid #e5e7eb;
        background: #fafafa;
        display: flex;
        gap: 10px;
        align-items: flex-end;
    }
    
    .chat-input {
        flex: 1;
        border: 1px solid #d1d5db;
        border-radius: 20px;
        padding: 10px 15px;
        font-size: 14px;
        outline: none;
        resize: none;
        max-height: 100px;
        min-height: 40px;
    }
    
    .chat-input:focus {
        border-color: #3B82F6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Send button */
    .chat-send-btn {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: #3B82F6;
        color: white;
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        transition: all 0.2s ease;
        flex-shrink: 0;
    }
    
    .chat-send-btn:hover {
        background-color: #1E40AF;
        transform: scale(1.05);
    }
    
    .chat-send-btn:disabled {
        background-color: #9CA3AF;
        cursor: not-allowed;
        transform: none;
    }
    
    /* Message styling */
    .chat-message {
        margin-bottom: 12px;
        line-height: 1.4;
    }
    
    .chat-message.user {
        text-align: right;
    }
    
    .chat-message.assistant {
        background: #f3f4f6;
        padding: 10px;
        border-radius: 10px;
        margin-right: 20px;
    }
    
    /* Tip styling */
    .chat-tip {
        background: #dbeafe;
        border: 1px solid #93c5fd;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 15px;
        font-size: 13px;
        color: #1e40af;
    }
    
    /* Hide streamlit elements in chat */
    .chat-bubble .stTextInput > div > div > input {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
    }
    
    .chat-bubble .stButton > button {
        background: none !important;
        border: none !important;
        padding: 0 !important;
        width: 100% !important;
        height: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Render floating button or chat
    if not st.session_state.chat_open:
        render_floating_button()
    else:
        render_chat_window()

def render_floating_button():
    """Render the floating chat button."""
    # Use a session state key to trigger reopening
    if st.button("", key="chat_trigger", help="Open ARIA Chat"):
        st.session_state.chat_open = True
        st.rerun()
    
    # HTML floating button overlay
    st.markdown("""
    <div class="floating-chat-btn" id="chatBtn">
        ARIA
    </div>
    
    <script>
    // Pure CSS/HTML approach - no onClick handlers
    document.addEventListener('DOMContentLoaded', function() {
        const chatBtn = document.getElementById('chatBtn');
        if (chatBtn) {
            chatBtn.addEventListener('click', function() {
                // Find and click the hidden Streamlit button
                const hiddenBtn = document.querySelector('button[kind="secondary"][data-testid*="chat_trigger"]');
                if (hiddenBtn) {
                    hiddenBtn.click();
                }
            });
        }
    });
    </script>
    """, unsafe_allow_html=True)

def render_chat_window():
    """Render the chat bubble window."""
    
    # Hidden close button
    if st.button("", key="chat_close_trigger", help="Close chat"):
        st.session_state.chat_open = False
        st.rerun()
    
    # Hidden send button  
    user_input = st.text_input("", key="chat_input_hidden", label_visibility="collapsed")
    if st.button("", key="chat_send_trigger", help="Send"):
        if user_input:
            handle_user_message(user_input)
    
    # Chat bubble HTML
    tips = [
        "Tip: Ask me about document scoring to understand the assessment frameworks",
        "Tip: Upload documents in PDF, TXT, or URL format for instant analysis", 
        "Tip: Click on any score badge to see detailed breakdown and recommendations",
        "Tip: Use filters to find documents by region, organization, or document type",
        "Tip: Try asking 'What are the critical gaps in my policy?' for targeted insights",
        "Tip: I can explain GUARDIAN's patent-protected algorithms and methodologies"
    ]
    
    import time
    current_time = int(time.time())
    current_tip_index = (current_time // 10) % len(tips)
    
    # Format chat messages
    messages_html = ""
    if st.session_state.chat_messages:
        for message in st.session_state.chat_messages[-3:]:
            if message['role'] == 'user':
                messages_html += f'<div class="chat-message user"><strong>You:</strong> {message["content"]}</div>'
            else:
                messages_html += f'<div class="chat-message assistant"><strong>ARIA:</strong> {message["content"]}</div>'
    
    st.markdown(f"""
    <div class="chat-bubble" id="chatBubble">
        <div class="chat-header">
            <span>ARIA - Advanced Risk Intelligence Assistant</span>
            <button class="chat-close-btn" id="closeBtn">×</button>
        </div>
        
        <div class="chat-body">
            <div class="chat-tip">{tips[current_tip_index]}</div>
            
            {messages_html if messages_html else '<div style="text-align: center; color: #6b7280; padding: 20px;">Start a conversation with ARIA!</div>'}
        </div>
        
        <div class="chat-input-area">
            <textarea class="chat-input" id="chatInput" placeholder="Ask ARIA about GUARDIAN..." rows="1"></textarea>
            <button class="chat-send-btn" id="sendBtn">▷</button>
        </div>
    </div>
    
    <script>
    document.addEventListener('DOMContentLoaded', function() {{
        // Close button functionality
        const closeBtn = document.getElementById('closeBtn');
        if (closeBtn) {{
            closeBtn.addEventListener('click', function() {{
                const hiddenCloseBtn = document.querySelector('button[data-testid*="chat_close_trigger"]');
                if (hiddenCloseBtn) hiddenCloseBtn.click();
            }});
        }}
        
        // Send button functionality
        const sendBtn = document.getElementById('sendBtn');
        const chatInput = document.getElementById('chatInput');
        const hiddenInput = document.querySelector('input[data-testid*="chat_input_hidden"]');
        
        if (sendBtn && chatInput && hiddenInput) {{
            sendBtn.addEventListener('click', function() {{
                if (chatInput.value.trim()) {{
                    hiddenInput.value = chatInput.value;
                    hiddenInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    
                    setTimeout(() => {{
                        const hiddenSendBtn = document.querySelector('button[data-testid*="chat_send_trigger"]');
                        if (hiddenSendBtn) {{
                            hiddenSendBtn.click();
                            chatInput.value = '';
                        }}
                    }}, 100);
                }}
            }});
            
            // Enter key to send
            chatInput.addEventListener('keypress', function(e) {{
                if (e.key === 'Enter' && !e.shiftKey) {{
                    e.preventDefault();
                    sendBtn.click();
                }}
            }});
        }}
    }});
    </script>
    """, unsafe_allow_html=True)

def handle_user_message(message: str):
    """Handle user chat messages."""
    try:
        # Use chatbot for response with correct method
        response = chatbot.detect_intent(message, st.session_state.chat_session_id)
        response_text = response.get('response_text', 'I understand your question. Let me help you with GUARDIAN.')
        
        # Add to chat history
        st.session_state.chat_messages.append({
            'role': 'user',
            'content': message
        })
        st.session_state.chat_messages.append({
            'role': 'assistant',
            'content': response_text
        })
        
        # Keep only last 10 messages for performance
        if len(st.session_state.chat_messages) > 10:
            st.session_state.chat_messages = st.session_state.chat_messages[-10:]
        
        st.rerun()
    except Exception as e:
        st.error(f"Chat error: {e}")

def handle_quick_question(question: str):
    """Handle predefined quick questions."""
    responses = {
        "How does GUARDIAN scoring work?": """**ARIA Analysis: GUARDIAN Scoring System**

**Four Assessment Frameworks:**
1. **AI Cybersecurity**: 0-100 points using NIST AI RMF
2. **Quantum Cybersecurity**: 1-5 tier QCMEA framework 
3. **AI Ethics**: 0-100 points evaluating ethical practices
4. **Quantum Ethics**: 0-100 points assessing compliance

**Patent-Based Algorithms:**
- Dynamic governance using reinforcement learning
- Bayesian updates for real-time risk assessment
- Adaptive scoring based on emerging threats

**Color-Coded Intelligence:**
- Green (High): Strong compliance and maturity
- Yellow (Medium): Areas needing attention  
- Red (Low): Critical gaps requiring immediate action""",

        "How do I navigate the Policy Repository?": """**ARIA Navigation Guide: Policy Repository**

**Main Sections:**
- **Policy Repository**: Browse all analyzed documents
- **Policy Analyzer**: Upload new documents for analysis
- **Patent Technology**: View GUARDIAN's technical details
- **About GUARDIAN**: System overview and capabilities

**Intelligent Filtering:**
- Use filters by region, organization, document type
- Search by keywords in content or metadata
- Sort by scores, date, or relevance

**Document Actions:**
- Click scores to see detailed analysis
- Use Content Preview for quick summary
- Translation available for international documents

**ARIA Tips:**
- Hover over elements for contextual help
- Use quick filters for common searches
- Check score explanations for improvement guidance""",

        "How do I upload and analyze a policy document?": """**ARIA Guide: Document Upload & Analysis**

**Step 1: Access Policy Analyzer**
- Go to 'Policy Repository' → 'Policy Analyzer'
- Use the document upload section

**Step 2: Upload Document**  
- Supports PDF, TXT, and URL formats
- Drag & drop or click to browse files
- Add organization name and document type

**Step 3: AI Analysis Process**
- GUARDIAN extracts and processes content
- Applies patent-based scoring algorithms
- Generates comprehensive gap analysis

**Step 4: Review Intelligence**
- View detailed scoring across all frameworks
- Check gap analysis with severity levels
- Access strategic recommendations for improvement

Analysis takes 30-60 seconds depending on document size.""",

        "What is policy gap analysis?": """**ARIA Intelligence: Policy Gap Analysis**

**GUARDIAN Patent Algorithm:**
Uses reinforcement learning to identify policy weaknesses and provide targeted recommendations.

**Gap Severity Intelligence:**
- **Critical**: Immediate attention required
- **High**: Address within 30 days  
- **Medium**: Address within 90 days
- **Low**: Monitor and improve

**Analysis Areas:**
- Regulatory compliance gaps
- Security framework deficiencies
- Ethics policy weaknesses
- Implementation inconsistencies

**ARIA Benefits:**
- Proactive risk identification
- Compliance assurance
- Continuous improvement tracking
- Evidence-based policy development"""
    }
    
    response = responses.get(question, "I'm ARIA, your Advanced Risk Intelligence Assistant. I can help with GUARDIAN navigation, scoring, document upload, and policy analysis. What would you like to know?")
    
    st.session_state.chat_messages.append({
        'role': 'user',
        'content': question
    })
    st.session_state.chat_messages.append({
        'role': 'assistant', 
        'content': response
    })
    st.rerun()