"""
Floating Chat Interface for GUARDIAN
Provides a persistent floating chat button and expandable chat window
"""

import streamlit as st
import uuid
from utils.dialogflow_chatbot import chatbot

def render_floating_chat():
    """Render a floating chat button that opens a chat interface."""
    
    # Initialize chat state
    if 'chat_open' not in st.session_state:
        st.session_state.chat_open = False
    if 'chat_session_id' not in st.session_state:
        st.session_state.chat_session_id = str(uuid.uuid4())
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []

    # CSS for floating chat
    st.markdown("""
    <style>
    .floating-chat-container {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 9999;
        font-family: 'Inter', sans-serif;
    }
    
    .chat-toggle-btn {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%);
        border: none;
        color: white;
        font-size: 24px;
        cursor: pointer;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4);
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
        animation: pulse 2s infinite;
    }
    
    .chat-toggle-btn:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 30px rgba(59, 130, 246, 0.6);
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4); }
        50% { box-shadow: 0 4px 20px rgba(59, 130, 246, 0.8); }
        100% { box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4); }
    }
    
    .chat-window {
        position: fixed;
        bottom: 90px;
        right: 20px;
        width: 350px;
        height: 500px;
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
        border: 1px solid #e5e7eb;
        z-index: 9998;
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }
    
    .chat-header {
        background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%);
        color: white;
        padding: 15px;
        font-weight: 600;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .chat-close {
        background: none;
        border: none;
        color: white;
        font-size: 18px;
        cursor: pointer;
        padding: 0;
        width: 20px;
        height: 20px;
    }
    
    .chat-body {
        flex: 1;
        padding: 15px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    
    .chat-message {
        padding: 10px;
        border-radius: 10px;
        max-width: 85%;
        word-wrap: break-word;
    }
    
    .user-message {
        background: #3B82F6;
        color: white;
        align-self: flex-end;
        margin-left: auto;
    }
    
    .assistant-message {
        background: #f3f4f6;
        color: #374151;
        align-self: flex-start;
    }
    
    .quick-buttons {
        display: flex;
        flex-wrap: wrap;
        gap: 5px;
        margin-bottom: 10px;
    }
    
    .quick-btn {
        background: #f3f4f6;
        border: 1px solid #d1d5db;
        color: #374151;
        padding: 5px 8px;
        border-radius: 15px;
        font-size: 11px;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .quick-btn:hover {
        background: #3B82F6;
        color: white;
        border-color: #3B82F6;
    }
    
    .chat-input-area {
        padding: 15px;
        border-top: 1px solid #e5e7eb;
        background: #fafafa;
    }
    </style>
    """, unsafe_allow_html=True)

    # Render floating chat button
    chat_button_html = f"""
    <div class="floating-chat-container">
        <div class="chat-toggle-btn" onclick="toggleChat()" title="Chat with GUARDIAN Assistant">
            💬
        </div>
    </div>
    
    <script>
    function toggleChat() {{
        // Send message to Streamlit to toggle chat
        window.parent.postMessage({{type: 'toggle_chat'}}, '*');
    }}
    </script>
    """
    
    st.markdown(chat_button_html, unsafe_allow_html=True)

    # Chat toggle logic
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        if st.button("💬", key="floating_chat_toggle", help="Open GUARDIAN Assistant"):
            st.session_state.chat_open = not st.session_state.chat_open
            st.rerun()

    # Render chat window if open
    if st.session_state.chat_open:
        render_chat_window()

def render_chat_window():
    """Render the floating chat window."""
    
    # Chat window HTML structure
    chat_window_html = """
    <div class="chat-window">
        <div class="chat-header">
            <span>🤖 GUARDIAN Assistant</span>
            <button class="chat-close" onclick="closeChat()">×</button>
        </div>
    </div>
    
    <script>
    function closeChat() {
        window.parent.postMessage({type: 'close_chat'}, '*');
    }
    </script>
    """
    
    # Use container for chat content
    with st.container():
        st.markdown("### 🤖 GUARDIAN Assistant")
        
        # Quick help buttons
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
            for message in st.session_state.chat_messages[-3:]:  # Show last 3 messages
                if message['role'] == 'user':
                    st.markdown(f"**You:** {message['content']}")
                else:
                    st.markdown(f"**Assistant:** {message['content'][:150]}{'...' if len(message['content']) > 150 else ''}")
        
        # Chat input
        user_input = st.text_input("Ask me anything about GUARDIAN:", key="floating_chat_input", placeholder="e.g., How do I upload a policy?")
        
        if st.button("Send", key="floating_send", use_container_width=True) and user_input:
            handle_user_message(user_input)
        
        # Close button
        if st.button("Close Chat", key="close_floating_chat"):
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