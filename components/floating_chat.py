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
    """Render floating chat button using Streamlit's HTML component bridge."""
    
    # The proven solution: Use st.components.v1.html with bidirectional communication
    import streamlit.components.v1 as components
    
    # Create the HTML component with embedded JavaScript
    html_code = f"""
    <div id="aria-chat-container">
        <style>
        #aria-chat-container {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 10000;
            pointer-events: none;
        }}
        
        .floating-aria-btn {{
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
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s ease;
            animation: ariaPulse 3s infinite;
            user-select: none;
            pointer-events: auto;
        }}
        
        .floating-aria-btn:hover {{
            transform: scale(1.1);
            box-shadow: 0 6px 30px rgba(59, 130, 246, 0.6);
        }}
        
        .floating-aria-btn:active {{
            transform: scale(0.95);
        }}
        
        @keyframes ariaPulse {{
            0%, 100% {{ box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4); }}
            50% {{ box-shadow: 0 4px 20px rgba(59, 130, 246, 0.8); }}
        }}
        </style>
        
        <button class="floating-aria-btn" onclick="openAriaChat()">
            ARIA
        </button>
        
        <script>
        function openAriaChat() {{
            // Send data back to Streamlit using the component communication method
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: {{ action: 'open_chat', timestamp: Date.now() }}
            }}, '*');
            
            // Visual feedback
            document.querySelector('.floating-aria-btn').style.transform = 'scale(0.9)';
            setTimeout(() => {{
                document.querySelector('.floating-aria-btn').style.transform = '';
            }}, 150);
        }}
        </script>
    </div>
    """
    
    # Use Streamlit's HTML component for reliable communication
    component_value = components.html(html_code, height=80, width=80)
    
    # Check if the component sent back a value
    if component_value and isinstance(component_value, dict):
        if component_value.get('action') == 'open_chat':
            st.session_state.chat_open = True
            st.rerun()

def render_sidebar_chat():
    """Render floating chat bubble using Streamlit components."""
    
    import streamlit.components.v1 as components
    
    # Get current tip and messages
    tips = [
        "Ask me about document scoring to understand the assessment frameworks",
        "Upload documents in PDF, TXT, or URL format for instant analysis", 
        "Click on any score badge to see detailed breakdown and recommendations",
        "Use filters to find documents by region, organization, or document type",
        "Try asking 'What are the critical gaps in my policy?' for targeted insights",
        "I can explain GUARDIAN's patent-protected algorithms and methodologies"
    ]
    current_tip_index = (int(time.time()) // 10) % len(tips)
    
    # Format messages for HTML
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
    
    # Create floating chat bubble HTML
    chat_html = f"""
    <div id="chat-bubble-container">
        <style>
        #chat-bubble-container {{
            position: fixed;
            bottom: 90px;
            right: 20px;
            width: 350px;
            max-height: 500px;
            z-index: 10001;
            pointer-events: auto;
        }}
        
        .chat-bubble-window {{
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
            border: 1px solid #e5e7eb;
            animation: slideUpChat 0.3s ease;
            overflow: hidden;
        }}
        
        @keyframes slideUpChat {{
            from {{ transform: translateY(20px); opacity: 0; }}
            to {{ transform: translateY(0); opacity: 1; }}
        }}
        
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
        
        .chat-bubble-body {{
            padding: 15px;
            max-height: 300px;
            overflow-y: auto;
        }}
        
        .chat-tip {{
            background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
            border: 1px solid #93c5fd;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 15px;
            font-size: 13px;
            color: #1e40af;
        }}
        
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
                <button class="chat-close-btn" onclick="closeChat()">×</button>
            </div>
            
            <div class="chat-bubble-body">
                <div class="chat-tip">💡 {tips[current_tip_index]}</div>
                {messages_html}
            </div>
            
            <div class="chat-bubble-input">
                <input type="text" class="chat-input-field" id="chatInput" placeholder="Ask ARIA about GUARDIAN..." 
                       onkeypress="if(event.key==='Enter') sendMessage()">
                <button class="chat-send-btn" onclick="sendMessage()">▷</button>
            </div>
        </div>
        
        <script>
        function closeChat() {{
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: {{ action: 'close_chat', timestamp: Date.now() }}
            }}, '*');
        }}
        
        function sendMessage() {{
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            if (message) {{
                window.parent.postMessage({{
                    type: 'streamlit:setComponentValue',
                    value: {{ action: 'send_message', message: message, timestamp: Date.now() }}
                }}, '*');
                input.value = '';
            }}
        }}
        </script>
    </div>
    """
    
    # Render the chat bubble component
    component_value = components.html(chat_html, height=500, width=350)
    
    # Handle component responses
    if component_value and isinstance(component_value, dict):
        action = component_value.get('action')
        if action == 'close_chat':
            st.session_state.chat_open = False
            st.rerun()
        elif action == 'send_message':
            message = component_value.get('message')
            if message:
                handle_user_message(message)

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