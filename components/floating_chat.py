"""
Floating Chat Interface for GUARDIAN
Provides a persistent floating chat button and expandable chat window
"""

import streamlit as st
import uuid
from utils.dialogflow_chatbot import chatbot

def render_floating_chat():
    """Render a simple floating chat interface using Streamlit components."""
    
    # Initialize chat state
    if 'chat_open' not in st.session_state:
        st.session_state.chat_open = False
    if 'chat_session_id' not in st.session_state:
        st.session_state.chat_session_id = str(uuid.uuid4())
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []

    # Simple CSS for positioned elements
    st.markdown("""
    <style>
    .fixed-chat-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 9999;
        width: 70px;
        height: 40px;
    }
    
    .fixed-chat-window {
        position: fixed;
        top: 20px;
        right: 20px;
        width: 350px;
        max-height: 500px;
        z-index: 9998;
        background: white;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
        overflow: hidden;
    }
    
    /* Simple button styling */
    .stButton > button {
        background-color: #f8f9fa !important;
        color: #374151 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-size: 12px !important;
        padding: 8px 12px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton > button:hover {
        background-color: #e5e7eb !important;
        border-color: #9ca3af !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15) !important;
    }
    
    /* Special styling for send button */
    .stButton[data-testid*="floating_send"] > button {
        width: 40px !important;
        height: 40px !important;
        border-radius: 50% !important;
        padding: 0 !important;
        font-size: 16px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Create a simple floating chat button
    if not st.session_state.chat_open:
        st.markdown('<div class="fixed-chat-button">', unsafe_allow_html=True)
        if st.button("ARIA", key="floating_chat_toggle", help="ARIA - Advanced Risk Intelligence Assistant"):
            st.session_state.chat_open = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Render chat window if open
    if st.session_state.chat_open:
        render_chat_window()

def render_chat_window():
    """Render the floating chat window as a sidebar expander."""
    
    # Use an expander in the main content area for the chat window
    with st.expander("ARIA - Advanced Risk Intelligence Assistant", expanded=True):
        
        # Display rotating tip
        tips = [
            "💡 Tip: Ask me about document scoring to understand the assessment frameworks",
            "💡 Tip: Upload documents in PDF, TXT, or URL format for instant analysis", 
            "💡 Tip: Click on any score badge to see detailed breakdown and recommendations",
            "💡 Tip: Use filters to find documents by region, organization, or document type",
            "💡 Tip: Try asking 'What are the critical gaps in my policy?' for targeted insights",
            "💡 Tip: I can explain GUARDIAN's patent-protected algorithms and methodologies"
        ]
        
        # Initialize tip index if not exists
        if 'aria_tip_index' not in st.session_state:
            st.session_state.aria_tip_index = 0
        
        # Show current tip and rotate every 5 seconds (simulated by user interaction)
        import time
        current_time = int(time.time())
        tip_rotation_interval = 10  # Change tip every 10 seconds
        current_tip_index = (current_time // tip_rotation_interval) % len(tips)
        
        st.info(tips[current_tip_index])
        
        # Chat messages
        if st.session_state.chat_messages:
            st.markdown("**Recent Conversation:**")
            for message in st.session_state.chat_messages[-3:]:  # Show last 3 messages
                if message['role'] == 'user':
                    st.markdown(f"**You:** {message['content']}")
                else:
                    st.markdown(f"**ARIA:** {message['content'][:200]}{'...' if len(message['content']) > 200 else ''}")
        
        # Chat input with paper airplane send
        user_input = st.text_input("Ask ARIA about GUARDIAN:", key="floating_chat_input", placeholder="e.g., How do I upload a policy document?")
        
        # Single send button with paper airplane
        if st.button("✈️", key="floating_send", help="Send message") and user_input:
            handle_user_message(user_input)

def handle_user_message(message: str):
    """Handle user chat messages."""
    try:
        # Use chatbot for response
        response = chatbot.get_response(message, st.session_state.chat_session_id)
        
        # Add to chat history
        st.session_state.chat_messages.append({
            'role': 'user',
            'content': message
        })
        st.session_state.chat_messages.append({
            'role': 'assistant',
            'content': response
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