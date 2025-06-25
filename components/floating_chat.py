"""
Floating Chat Interface for GUARDIAN
Provides a persistent floating chat button and expandable chat window
"""

import streamlit as st
import uuid
from utils.dialogflow_chatbot import chatbot

def render_floating_chat():
    """Render a floating chat bubble interface within Streamlit."""
    
    # Initialize chat state
    if 'chat_open' not in st.session_state:
        st.session_state.chat_open = False
    if 'chat_session_id' not in st.session_state:
        st.session_state.chat_session_id = str(uuid.uuid4())
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []

    # CSS for floating chat interface
    st.markdown("""
    <style>
    /* Position the container to hold chat elements */
    .floating-chat-container {
        position: fixed !important;
        bottom: 20px !important;
        right: 20px !important;
        z-index: 10000 !important;
        pointer-events: none !important;
    }
    
    .floating-chat-container * {
        pointer-events: auto !important;
    }
    
    /* Floating chat button styling */
    .floating-chat-container .stButton > button {
        width: 60px !important;
        height: 60px !important;
        border-radius: 50% !important;
        background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 12px !important;
        box-shadow: 0 6px 25px rgba(59, 130, 246, 0.4) !important;
        transition: all 0.3s ease !important;
        animation: chatPulse 3s infinite !important;
    }
    
    .floating-chat-container .stButton > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 8px 35px rgba(59, 130, 246, 0.6) !important;
    }
    
    @keyframes chatPulse {
        0%, 100% { box-shadow: 0 6px 25px rgba(59, 130, 246, 0.4); }
        50% { box-shadow: 0 6px 25px rgba(59, 130, 246, 0.8); }
    }
    
    /* Chat bubble positioning */
    .chat-bubble-container {
        position: fixed !important;
        bottom: 90px !important;
        right: 20px !important;
        width: 350px !important;
        z-index: 10001 !important;
        pointer-events: auto !important;
    }
    
    /* Chat bubble styling */
    .chat-bubble-container .stContainer {
        background: white !important;
        border-radius: 15px !important;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15) !important;
        border: 1px solid #e5e7eb !important;
        padding: 0 !important;
        animation: slideUpBubble 0.3s ease !important;
    }
    
    @keyframes slideUpBubble {
        from { transform: translateY(20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    /* Chat header styling */
    .chat-header {
        background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%) !important;
        color: white !important;
        padding: 15px 20px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        border-radius: 15px 15px 0 0 !important;
        margin: 0 !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
    }
    
    /* Chat body styling */
    .chat-body {
        padding: 15px !important;
        max-height: 350px !important;
        overflow-y: auto !important;
    }
    
    /* Message bubble styling */
    .message-bubble {
        margin-bottom: 12px;
        padding: 8px 12px;
        border-radius: 18px;
        max-width: 80%;
        word-wrap: break-word;
    }
    
    .message-bubble.user {
        background: #3B82F6;
        color: white;
        margin-left: auto;
        text-align: right;
    }
    
    .message-bubble.assistant {
        background: #f1f5f9;
        color: #1e293b;
        margin-right: auto;
        border: 1px solid #e2e8f0;
    }
    
    /* Tip bubble styling */
    .tip-bubble {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border: 1px solid #93c5fd;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 15px;
        font-size: 13px;
        color: #1e40af;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
    }
    
    /* Input area styling */
    .chat-input-section {
        padding: 15px;
        border-top: 1px solid #e5e7eb;
        background: #fafafa;
        border-radius: 0 0 15px 15px;
    }
    
    .chat-input-section .stTextInput > div > div > input {
        border-radius: 20px !important;
        border: 1px solid #d1d5db !important;
        padding: 10px 15px !important;
        font-size: 14px !important;
    }
    
    .chat-input-section .stTextInput > div > div > input:focus {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* Send button styling */
    .chat-input-section .stButton > button {
        width: 40px !important;
        height: 40px !important;
        border-radius: 50% !important;
        background-color: #3B82F6 !important;
        color: white !important;
        border: none !important;
        font-size: 16px !important;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3) !important;
        transition: all 0.2s ease !important;
    }
    
    .chat-input-section .stButton > button:hover {
        background-color: #1E40AF !important;
        transform: scale(1.05) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* Close button styling */
    .close-btn-section .stButton > button {
        background: rgba(255, 255, 255, 0.2) !important;
        color: white !important;
        border: none !important;
        width: 30px !important;
        height: 30px !important;
        border-radius: 50% !important;
        font-size: 18px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Render the floating chat interface
    if not st.session_state.chat_open:
        render_floating_button()
    else:
        render_chat_bubble()

def render_floating_button():
    """Render the floating chat button using Streamlit container."""
    # Create a positioned container for the floating button
    st.markdown('<div class="floating-chat-container">', unsafe_allow_html=True)
    
    if st.button("ARIA", key="floating_chat_toggle", help="ARIA - Advanced Risk Intelligence Assistant"):
        st.session_state.chat_open = True
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_chat_bubble():
    """Render the chat bubble window using Streamlit components."""
    
    # Position the chat bubble container
    st.markdown('<div class="chat-bubble-container">', unsafe_allow_html=True)
    
    with st.container():
        # Chat header with close button
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown('<div class="chat-header">ARIA - Advanced Risk Intelligence Assistant</div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="close-btn-section">', unsafe_allow_html=True)
            if st.button("×", key="floating_close", help="Close chat"):
                st.session_state.chat_open = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat body
        st.markdown('<div class="chat-body">', unsafe_allow_html=True)
        
        # Display rotating tip
        tips = [
            "Ask me about document scoring to understand the assessment frameworks",
            "Upload documents in PDF, TXT, or URL format for instant analysis", 
            "Click on any score badge to see detailed breakdown and recommendations",
            "Use filters to find documents by region, organization, or document type",
            "Try asking 'What are the critical gaps in my policy?' for targeted insights",
            "I can explain GUARDIAN's patent-protected algorithms and methodologies"
        ]
        
        import time
        current_time = int(time.time())
        current_tip_index = (current_time // 10) % len(tips)
        
        st.markdown(f'<div class="tip-bubble">💡 {tips[current_tip_index]}</div>', unsafe_allow_html=True)
        
        # Chat messages with bubble styling
        if st.session_state.chat_messages:
            for message in st.session_state.chat_messages[-3:]:
                if message['role'] == 'user':
                    st.markdown(f'<div class="message-bubble user">{message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="message-bubble assistant">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align: center; color: #64748b; padding: 20px; font-style: italic;">Start a conversation with ARIA!</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Chat input section
        st.markdown('<div class="chat-input-section">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([4, 1])
        with col1:
            user_input = st.text_input("", key="floating_chat_input", placeholder="Ask ARIA about GUARDIAN...", label_visibility="collapsed")
        with col2:
            if st.button("▷", key="floating_send", help="Send message"):
                if user_input:
                    handle_user_message(user_input)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

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