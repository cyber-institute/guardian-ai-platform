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
        width: 60px;
        height: 60px;
    }
    
    .fixed-chat-window {
        position: fixed;
        top: 20px;
        right: 20px;
        width: 350px;
        max-height: 500px;
        z-index: 9998;
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        border: 1px solid #e5e7eb;
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

    # Create a fixed position container for the chat button
    if not st.session_state.chat_open:
        # Show floating chat button
        st.markdown('<div class="fixed-chat-button">', unsafe_allow_html=True)
        if st.button("💬", key="floating_chat_toggle", help="Open GUARDIAN Assistant"):
            st.session_state.chat_open = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Render chat window if open
    if st.session_state.chat_open:
        render_chat_window()

def render_chat_window():
    """Render the floating chat window as a sidebar expander."""
    
    # Use an expander in the main content area for the chat window
    with st.expander("🤖 GUARDIAN Assistant", expanded=True):
        st.markdown("**Quick Help:**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Scoring Guide", key="floating_scoring", help="Understanding scores"):
                handle_quick_question("How does GUARDIAN scoring work?")
            if st.button("Navigation", key="floating_nav", help="Learn navigation"):
                handle_quick_question("How do I navigate the Policy Repository?")
        with col2:
            if st.button("Upload Help", key="floating_upload", help="Document upload"):
                handle_quick_question("How do I upload and analyze a policy document?")
            if st.button("Gap Analysis", key="floating_gaps", help="Policy gaps"):
                handle_quick_question("What is policy gap analysis?")
        
        # Chat messages
        if st.session_state.chat_messages:
            st.markdown("---")
            st.markdown("**Recent Conversation:**")
            for message in st.session_state.chat_messages[-3:]:  # Show last 3 messages
                if message['role'] == 'user':
                    st.markdown(f"**You:** {message['content']}")
                else:
                    st.markdown(f"**Assistant:** {message['content'][:200]}{'...' if len(message['content']) > 200 else ''}")
        
        # Chat input
        user_input = st.text_input("Ask me anything about GUARDIAN:", key="floating_chat_input", placeholder="e.g., How do I upload a policy?")
        
        col_send, col_close = st.columns([2, 1])
        with col_send:
            if st.button("Send", key="floating_send", use_container_width=True) and user_input:
                handle_user_message(user_input)
        with col_close:
            if st.button("Close Chat", key="close_floating_chat", use_container_width=True):
                st.session_state.chat_open = False
                st.rerun()

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
        "How does GUARDIAN scoring work?": """**GUARDIAN Scoring System:**

**Four Assessment Frameworks:**
1. **AI Cybersecurity**: 0-100 points using NIST AI RMF
2. **Quantum Cybersecurity**: 1-5 tier QCMEA framework 
3. **AI Ethics**: 0-100 points evaluating ethical practices
4. **Quantum Ethics**: 0-100 points assessing compliance

**Patent-Based Algorithms:**
- Dynamic governance using reinforcement learning
- Bayesian updates for real-time risk assessment
- Adaptive scoring based on emerging threats

**Color-Coded Results:**
- Green (High): Strong compliance and maturity
- Yellow (Medium): Areas needing attention  
- Red (Low): Critical gaps requiring immediate action""",

        "How do I navigate the Policy Repository?": """**Policy Repository Navigation:**

**Main Sections:**
- **Policy Repository**: Browse all analyzed documents
- **Policy Analyzer**: Upload new documents for analysis
- **Patent Technology**: View GUARDIAN's technical details
- **About GUARDIAN**: System overview and capabilities

**Filtering & Search:**
- Use filters by region, organization, document type
- Search by keywords in content or metadata
- Sort by scores, date, or relevance

**Document Actions:**
- Click scores to see detailed analysis
- Use Content Preview for quick summary
- Translation available for international documents

**Tips:**
- Hover over elements for helpful tooltips
- Use quick filters for common searches
- Check score explanations for improvement guidance""",

        "How do I upload and analyze a policy document?": """**Document Upload & Analysis:**

**Step 1: Access Policy Analyzer**
- Go to 'Policy Repository' → 'Policy Analyzer'
- Use the document upload section

**Step 2: Upload Document**  
- Supports PDF, TXT, and URL formats
- Drag & drop or click to browse files
- Add organization name and document type

**Step 3: Analysis Process**
- GUARDIAN extracts and processes content
- Applies patent-based scoring algorithms
- Generates comprehensive gap analysis

**Step 4: Review Results**
- View detailed scoring across all frameworks
- Check gap analysis with severity levels
- Access strategic recommendations for improvement

Upload takes 30-60 seconds depending on document size.""",

        "What is policy gap analysis?": """**Policy Gap Analysis:**

**GUARDIAN Patent Algorithm:**
Uses reinforcement learning to identify policy weaknesses and provide targeted recommendations.

**Gap Severity Levels:**
- **Critical**: Immediate attention required
- **High**: Address within 30 days  
- **Medium**: Address within 90 days
- **Low**: Monitor and improve

**Analysis Areas:**
- Regulatory compliance gaps
- Security framework deficiencies
- Ethics policy weaknesses
- Implementation inconsistencies

**Benefits:**
- Proactive risk identification
- Compliance assurance
- Continuous improvement tracking
- Evidence-based policy development"""
    }
    
    response = responses.get(question, "I can help with GUARDIAN navigation, scoring, document upload, and policy analysis. What would you like to know?")
    
    st.session_state.chat_messages.append({
        'role': 'user',
        'content': question
    })
    st.session_state.chat_messages.append({
        'role': 'assistant', 
        'content': response
    })
    st.rerun()