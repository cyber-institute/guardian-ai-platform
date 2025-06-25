"""
Floating Chat Interface for GUARDIAN
Provides a persistent floating chat button and expandable chat window
"""

import streamlit as st
import uuid
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
    """Render the floating chat button."""
    # CSS for floating button
    st.markdown("""
    <style>
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
    </style>
    """, unsafe_allow_html=True)
    
    # Hidden Streamlit button for functionality
    if st.button("", key="aria_chat_btn", help="Open ARIA Chat"):
        st.session_state.chat_open = True
        st.rerun()
    
    # Floating button HTML
    st.markdown("""
    <div class="floating-chat-btn" onclick="document.querySelector('[data-testid*=\"aria_chat_btn\"] button').click()">
        ARIA
    </div>
    """, unsafe_allow_html=True)

def render_sidebar_chat():
    """Render chat interface in sidebar when open."""
    with st.sidebar:
        # Chat header with close button
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("**ARIA** - Advanced Risk Intelligence Assistant")
        with col2:
            if st.button("×", key="close_chat", help="Close chat"):
                st.session_state.chat_open = False
                st.rerun()
        
        st.markdown("---")
        
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
        
        st.info(f"💡 {tips[current_tip_index]}")
        
        # Chat messages with conversation bubbles
        if st.session_state.chat_messages:
            st.markdown("**Recent Conversation:**")
            
            # CSS for conversation bubbles
            st.markdown("""
            <style>
            .user-message {
                background: #3B82F6;
                color: white;
                padding: 8px 12px;
                border-radius: 18px 18px 4px 18px;
                margin: 8px 0 8px 20px;
                text-align: right;
                display: block;
            }
            
            .assistant-message {
                background: #f1f5f9;
                color: #1e293b;
                padding: 8px 12px;
                border-radius: 18px 18px 18px 4px;
                margin: 8px 20px 8px 0;
                border: 1px solid #e2e8f0;
                display: block;
            }
            </style>
            """, unsafe_allow_html=True)
            
            for message in st.session_state.chat_messages[-4:]:
                if message['role'] == 'user':
                    st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="assistant-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown("Start a conversation with ARIA!")
        
        # Chat input
        user_input = st.text_input("Ask ARIA about GUARDIAN:", key="chat_input", placeholder="e.g., How do I upload a policy document?")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("Send Message", key="send_msg", use_container_width=True):
                if user_input:
                    handle_user_message(user_input)
        with col2:
            if st.button("▷", key="send_arrow", help="Send"):
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