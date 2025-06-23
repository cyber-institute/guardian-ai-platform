"""
Floating Chat Interface for GUARDIAN
Provides a persistent floating chat button and expandable chat window
"""

import streamlit as st
import uuid
from utils.dialogflow_chatbot import chatbot

def render_floating_chat():
    """Render a floating chat bubble interface."""
    
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
    }
    
    .floating-chat-btn:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 30px rgba(59, 130, 246, 0.6);
    }
    
    /* Floating chat window overlay */
    .chat-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background: rgba(0, 0, 0, 0.1);
        z-index: 9999;
        backdrop-filter: blur(1px);
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
    }
    
    /* Chat header */
    .chat-header {
        background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%);
        color: white;
        padding: 15px 20px;
        font-weight: 600;
        font-size: 14px;
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
        align-items: center;
    }
    
    /* Send button styling */
    .chat-send-btn {
        width: 40px;
        height: 40px;
        border-radius: 8px;
        background-color: #6b7280;
        color: white;
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        transition: all 0.2s ease;
    }
    
    .chat-send-btn:hover {
        background-color: #4b5563;
        transform: translateY(-1px);
    }
    
    /* Hide default streamlit button styling for chat */
    .chat-container .stButton > button {
        background: none !important;
        border: none !important;
        padding: 0 !important;
        width: 100% !important;
        height: 100% !important;
    }
    </style>
    
    <script>
    // Close chat when clicking overlay
    function closeChatOverlay() {
        const overlay = document.querySelector('.chat-overlay');
        if (overlay) {
            overlay.addEventListener('click', function(e) {
                if (e.target === overlay) {
                    // Send message to Streamlit to close chat
                    window.parent.postMessage({type: 'close_chat'}, '*');
                }
            });
        }
    }
    
    // Initialize overlay click handler
    setTimeout(closeChatOverlay, 100);
    </script>
    """, unsafe_allow_html=True)

    # Floating chat button
    if not st.session_state.chat_open:
        st.markdown("""
        <div class="floating-chat-btn" onclick="window.parent.postMessage({type: 'open_chat'}, '*')">
            ARIA
        </div>
        """, unsafe_allow_html=True)
        
        # Hidden button for Streamlit interaction
        if st.button("", key="floating_chat_toggle", help="ARIA - Advanced Risk Intelligence Assistant"):
            st.session_state.chat_open = True
            st.rerun()
    
    # Chat bubble overlay
    if st.session_state.chat_open:
        render_chat_bubble()

def render_chat_bubble():
    """Render the floating chat bubble with overlay."""
    
    # Chat overlay (closes chat when clicked)
    st.markdown('<div class="chat-overlay"></div>', unsafe_allow_html=True)
    
    # Chat bubble
    st.markdown('<div class="chat-bubble">', unsafe_allow_html=True)
    
    # Chat header
    st.markdown('<div class="chat-header">ARIA - Advanced Risk Intelligence Assistant</div>', unsafe_allow_html=True)
    
    # Chat body with container
    with st.container():
        st.markdown('<div class="chat-body">', unsafe_allow_html=True)
        
        # Display rotating tip
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
        tip_rotation_interval = 10
        current_tip_index = (current_time // tip_rotation_interval) % len(tips)
        
        st.info(tips[current_tip_index])
        
        # Chat messages
        if st.session_state.chat_messages:
            st.markdown("**Recent Conversation:**")
            for message in st.session_state.chat_messages[-3:]:
                if message['role'] == 'user':
                    st.markdown(f"**You:** {message['content']}")
                else:
                    st.markdown(f"**ARIA:** {message['content']}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input area
    st.markdown('<div class="chat-input-area">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([4, 1])
    with col1:
        user_input = st.text_input("Ask ARIA about GUARDIAN:", key="floating_chat_input", placeholder="e.g., How do I upload a policy document?", label_visibility="collapsed")
    
    with col2:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        if st.button("▷", key="floating_send", help="Send message"):
            if user_input:
                handle_user_message(user_input)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle overlay clicks to close chat
    if st.button("", key="close_chat_overlay", help="Close chat"):
        st.session_state.chat_open = False
        st.rerun()

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