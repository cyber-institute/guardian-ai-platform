"""
Floating Chat Interface for GUARDIAN
Provides a persistent floating chat button and expandable chat window
"""

import streamlit as st
import uuid
import time
from utils.dialogflow_chatbot import chatbot

def render_floating_chat():
    """Render floating chat that works properly in Streamlit."""
    
    # Initialize chat state
    if 'chat_open' not in st.session_state:
        st.session_state.chat_open = False
    if 'chat_session_id' not in st.session_state:
        st.session_state.chat_session_id = str(uuid.uuid4())
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []

    # Render chat in sidebar when open, button when closed
    if st.session_state.chat_open:
        render_sidebar_chat()
    else:
        render_floating_button()

def render_floating_button():
    """Render floating chat button with working HTML onclick."""
    
    # Initialize click counter for reliable state tracking
    if 'aria_click_count' not in st.session_state:
        st.session_state.aria_click_count = 0
    
    # Create the floating button and chat bubble HTML
    st.markdown(f"""
    <style>
    /* Floating chat button */
    .floating-chat-btn {{
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
        animation: chatPulse 3s infinite;
        user-select: none;
    }}
    
    .floating-chat-btn:hover {{
        transform: scale(1.1);
        box-shadow: 0 6px 30px rgba(59, 130, 246, 0.6);
    }}
    
    .floating-chat-btn:active {{
        transform: scale(0.95);
    }}
    
    @keyframes chatPulse {{
        0%, 100% {{ box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4); }}
        50% {{ box-shadow: 0 4px 20px rgba(59, 130, 246, 0.8); }}
    }}
    
    /* Hidden form for Streamlit communication */
    .hidden-form {{
        display: none;
    }}
    </style>
    
    <!-- Hidden form method for reliable Streamlit communication -->
    <form class="hidden-form" id="ariaForm">
        <input type="text" id="ariaClickInput" value="{st.session_state.aria_click_count}">
        <button type="submit" id="ariaSubmit">Submit</button>
    </form>
    
    <!-- Floating chat button -->
    <div class="floating-chat-btn" id="ariaChatBtn">
        ARIA
    </div>
    
    <script>
    // Reliable HTML to Streamlit communication using form submission
    (function() {{
        const chatBtn = document.getElementById('ariaChatBtn');
        const clickInput = document.getElementById('ariaClickInput');
        const form = document.getElementById('ariaForm');
        
        if (chatBtn && clickInput && form && !chatBtn.hasStreamlitHandler) {{
            chatBtn.hasStreamlitHandler = true;
            
            chatBtn.addEventListener('click', function(e) {{
                e.preventDefault();
                
                // Method 1: Update hidden input and trigger change
                const currentCount = parseInt(clickInput.value) || 0;
                clickInput.value = currentCount + 1;
                
                // Trigger input change event
                clickInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                clickInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                
                // Method 2: Find and trigger Streamlit number input
                setTimeout(() => {{
                    const stInputs = document.querySelectorAll('input[type="number"]');
                    stInputs.forEach(input => {{
                        if (input.step === '1' && input.min === '0') {{
                            input.value = currentCount + 1;
                            input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                            input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                        }}
                    }});
                }}, 10);
                
                // Method 3: URL hash change detection
                window.location.hash = '#aria-clicked-' + (currentCount + 1);
                
                // Visual feedback
                chatBtn.style.transform = 'scale(0.9)';
                setTimeout(() => {{
                    chatBtn.style.transform = '';
                }}, 150);
            }});
        }}
    }})();
    </script>
    """, unsafe_allow_html=True)
    
    # Hidden number input for click detection
    click_count = st.number_input("", min_value=0, step=1, value=st.session_state.aria_click_count, key="aria_click_detector", label_visibility="collapsed")
    
    # Check if click count changed
    if click_count > st.session_state.aria_click_count:
        st.session_state.aria_click_count = click_count
        st.session_state.chat_open = True
        st.rerun()
    
    # Check URL hash for click detection
    hash_value = st.query_params.get("aria_clicked", None)
    if hash_value and hash_value != st.session_state.get("last_hash", ""):
        st.session_state.last_hash = hash_value
        st.session_state.chat_open = True
        st.rerun()

def render_sidebar_chat():
    """Render floating chat bubble window."""
    
    # Get current tip
    tips = [
        "Ask me about document scoring to understand the assessment frameworks",
        "Upload documents in PDF, TXT, or URL format for instant analysis", 
        "Click on any score badge to see detailed breakdown and recommendations",
        "Use filters to find documents by region, organization, or document type",
        "Try asking 'What are the critical gaps in my policy?' for targeted insights",
        "I can explain GUARDIAN's patent-protected algorithms and methodologies"
    ]
    current_tip_index = (int(time.time()) // 10) % len(tips)
    
    # Format chat messages for display
    messages_html = ""
    if st.session_state.chat_messages:
        for message in st.session_state.chat_messages[-4:]:
            if message['role'] == 'user':
                messages_html += f'''
                <div class="user-message">
                    <div class="message-content">{message["content"]}</div>
                </div>'''
            else:
                messages_html += f'''
                <div class="assistant-message">
                    <div class="message-content">{message["content"]}</div>
                </div>'''
    else:
        messages_html = '<div class="empty-chat">Start a conversation with ARIA!</div>'
    
    # Render floating chat bubble
    st.markdown(f"""
    <style>
    /* Floating chat bubble window */
    .chat-bubble-window {{
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
        animation: slideUpChat 0.3s ease;
        overflow: hidden;
    }}
    
    @keyframes slideUpChat {{
        from {{ transform: translateY(20px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
    }}
    
    /* Chat header */
    .chat-bubble-header {{
        background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%);
        color: white;
        padding: 15px 20px;
        font-weight: 600;
        font-size: 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    
    .chat-close-btn {{
        background: rgba(255, 255, 255, 0.2);
        border: none;
        color: white;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        cursor: pointer;
        font-size: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
    }}
    
    .chat-close-btn:hover {{
        background: rgba(255, 255, 255, 0.3);
    }}
    
    /* Chat body */
    .chat-bubble-body {{
        padding: 15px;
        max-height: 300px;
        overflow-y: auto;
    }}
    
    /* Tip styling */
    .chat-tip {{
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border: 1px solid #93c5fd;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 15px;
        font-size: 13px;
        color: #1e40af;
    }}
    
    /* Message bubbles */
    .user-message {{
        display: flex;
        justify-content: flex-end;
        margin-bottom: 10px;
    }}
    
    .user-message .message-content {{
        background: #3B82F6;
        color: white;
        padding: 10px 15px;
        border-radius: 18px 18px 4px 18px;
        max-width: 80%;
        word-wrap: break-word;
    }}
    
    .assistant-message {{
        display: flex;
        justify-content: flex-start;
        margin-bottom: 10px;
    }}
    
    .assistant-message .message-content {{
        background: #f8fafc;
        color: #334155;
        padding: 10px 15px;
        border-radius: 18px 18px 18px 4px;
        border: 1px solid #e2e8f0;
        max-width: 80%;
        word-wrap: break-word;
    }}
    
    .empty-chat {{
        text-align: center;
        color: #64748b;
        font-style: italic;
        padding: 20px;
    }}
    
    /* Chat input area */
    .chat-bubble-input {{
        padding: 15px;
        border-top: 1px solid #e5e7eb;
        background: #fafafa;
        display: flex;
        gap: 10px;
        align-items: center;
    }}
    
    .chat-input-field {{
        flex: 1;
        border: 1px solid #d1d5db;
        border-radius: 20px;
        padding: 10px 15px;
        font-size: 14px;
        outline: none;
    }}
    
    .chat-input-field:focus {{
        border-color: #3B82F6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }}
    
    .chat-send-btn {{
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #3B82F6;
        color: white;
        border: none;
        cursor: pointer;
        font-size: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s ease;
    }}
    
    .chat-send-btn:hover {{
        background: #1E40AF;
        transform: scale(1.05);
    }}
    </style>
    
    <div class="chat-bubble-window">
        <div class="chat-bubble-header">
            <span>ARIA - Advanced Risk Intelligence Assistant</span>
            <button class="chat-close-btn" onclick="document.getElementById('closeChatTrigger').click()">×</button>
        </div>
        
        <div class="chat-bubble-body">
            <div class="chat-tip">💡 {tips[current_tip_index]}</div>
            {messages_html}
        </div>
        
        <div class="chat-bubble-input">
            <input type="text" class="chat-input-field" id="chatInput" placeholder="Ask ARIA about GUARDIAN..." 
                   onkeypress="if(event.key==='Enter') document.getElementById('sendChatBtn').click()">
            <button class="chat-send-btn" id="sendChatBtn" onclick="sendChatMessage()">▷</button>
        </div>
    </div>
    
    <script>
    function sendChatMessage() {{
        const input = document.getElementById('chatInput');
        const message = input.value.trim();
        if (message) {{
            // Set message in hidden Streamlit input
            const hiddenInput = document.getElementById('hiddenChatInput');
            if (hiddenInput) {{
                hiddenInput.value = message;
                hiddenInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                hiddenInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
            
            // Trigger send button
            setTimeout(() => {{
                document.getElementById('sendMessageTrigger').click();
                input.value = '';
            }}, 100);
        }}
    }}
    </script>
    """, unsafe_allow_html=True)
    
    # Hidden Streamlit components for functionality
    if st.button("", key="closeChatTrigger", help="Close chat"):
        st.session_state.chat_open = False
        st.rerun()
    
    user_input = st.text_input("", key="hiddenChatInput", label_visibility="collapsed")
    
    if st.button("", key="sendMessageTrigger", help="Send"):
        if user_input:
            handle_user_message(user_input)

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