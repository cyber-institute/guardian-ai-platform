"""
Interactive Chatbot Widget for GUARDIAN
Provides floating chat interface and intelligent tooltips
"""

import streamlit as st
import uuid
from utils.dialogflow_chatbot import chatbot

def render_chatbot_widget():
    """Render chatbot widget with Dialogflow CX integration."""
    
    # Initialize chat session
    if 'chat_session_id' not in st.session_state:
        st.session_state.chat_session_id = str(uuid.uuid4())
    
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    
    # Always show chatbot in sidebar
    with st.sidebar:
        st.markdown("### GUARDIAN Assistant")
        
        # Onboarding and Quick Help
        from components.streamlit_tooltips import streamlit_tooltips
        
        # Welcome message for new users
        if not st.session_state.get("guardian_welcome_shown", False):
            st.info("Welcome to GUARDIAN! Start a guided tour?")
            if st.button("Start Tour", key="start_tour_chat", use_container_width=True):
                st.session_state.guardian_tour_active = True
                st.session_state.guardian_tour_step = 1
                st.session_state.guardian_welcome_shown = True
                handle_quick_question("Start guided tour")
                st.rerun()
        
        # Tour progress
        if st.session_state.get("guardian_tour_active", False):
            progress = st.session_state.get("guardian_tour_step", 1) / 4
            st.progress(progress, text=f"Tour Step {st.session_state.get('guardian_tour_step', 1)}/4")
            if st.button("End Tour", key="end_tour_chat"):
                st.session_state.guardian_tour_active = False
                st.session_state.guardian_tour_completed = True
                st.rerun()
        
        st.markdown("**Quick Help:**")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Navigation Guide", key="quick_nav", help="Learn how to navigate GUARDIAN"):
                handle_quick_question("How do I navigate the Policy Repository?")
            if st.button("Document Upload", key="quick_upload", help="How to upload documents"):
                handle_quick_question("How do I upload and analyze a policy document?")
        with col2:
            if st.button("Scoring Guide", key="quick_scoring", help="Understanding scores"):
                handle_quick_question("How does GUARDIAN scoring work?")
            if st.button("Gap Analysis", key="quick_gaps", help="Policy gap analysis"):
                handle_quick_question("What is policy gap analysis?")
        
        # Chat input
        user_input = st.text_input("Ask me anything about GUARDIAN:", key="chat_input", placeholder="e.g., How do I upload a policy?")
        
        if st.button("Send", key="send_message", use_container_width=True) and user_input:
            handle_user_message(user_input)
        
        # Display recent chat messages
        if st.session_state.chat_messages:
            st.markdown("---")
            st.markdown("**Recent Conversation:**")
            # Show last 2 exchanges
            recent_messages = st.session_state.chat_messages[-4:] if len(st.session_state.chat_messages) > 4 else st.session_state.chat_messages
            for message in recent_messages:
                if message['role'] == 'user':
                    st.markdown(f"**You:** {message['content']}")
                else:
                    st.markdown(f"**Assistant:** {message['content'][:200]}{'...' if len(message['content']) > 200 else ''}")
        
        # Clear chat button
        if st.session_state.chat_messages and st.button("Clear Chat", key="clear_chat"):
            st.session_state.chat_messages = []
            st.rerun()
    
    # CSS for floating chatbot
    st.markdown("""
    <style>
    .chatbot-container {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 1000;
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
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .chat-toggle-btn:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.6);
    }
    
    .chat-window {
        position: absolute;
        bottom: 80px;
        right: 0;
        width: 350px;
        height: 450px;
        background: white;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
        border: 1px solid #e5e7eb;
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }
    
    .chat-header {
        background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%);
        color: white;
        padding: 16px;
        font-weight: 600;
        font-size: 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .chat-messages {
        flex: 1;
        padding: 16px;
        overflow-y: auto;
        background: #f9fafb;
    }
    
    .message {
        margin-bottom: 12px;
        padding: 8px 12px;
        border-radius: 8px;
        max-width: 85%;
        word-wrap: break-word;
    }
    
    .user-message {
        background: #3B82F6;
        color: white;
        margin-left: auto;
        text-align: right;
    }
    
    .bot-message {
        background: white;
        color: #374151;
        border: 1px solid #e5e7eb;
    }
    
    .chat-input-area {
        padding: 16px;
        border-top: 1px solid #e5e7eb;
        background: white;
    }
    
    .tooltip-trigger {
        display: inline-block;
        position: relative;
        cursor: help;
        border-bottom: 1px dotted #3B82F6;
        color: #3B82F6;
    }
    
    .tooltip-content {
        visibility: hidden;
        position: absolute;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        background: #1f2937;
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 12px;
        white-space: nowrap;
        z-index: 1001;
        opacity: 0;
        transition: opacity 0.3s;
        max-width: 250px;
        white-space: normal;
    }
    
    .tooltip-trigger:hover .tooltip-content {
        visibility: visible;
        opacity: 1;
    }
    
    .quick-help-buttons {
        display: flex;
        flex-wrap: wrap;
        gap: 4px;
        margin-bottom: 12px;
    }
    
    .quick-help-btn {
        background: #f3f4f6;
        border: 1px solid #d1d5db;
        color: #374151;
        padding: 4px 8px;
        border-radius: 16px;
        font-size: 11px;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .quick-help-btn:hover {
        background: #3B82F6;
        color: white;
        border-color: #3B82F6;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Remove old floating chat logic - now using sidebar only

def render_chat_button():
    """Render the floating chat toggle button."""
    st.markdown("""
    <div class="chatbot-container">
        <div class="chat-toggle-btn" onclick="openChat()">
            💬
        </div>
    </div>
    
    <script>
    function openChat() {
        // Use Streamlit's component communication
        window.parent.postMessage({type: 'open_chat'}, '*');
    }
    </script>
    """, unsafe_allow_html=True)
    
    # Handle chat opening
    if st.button("", key="invisible_chat_opener", help="Open GUARDIAN Assistant"):
        st.session_state.chat_open = True
        st.rerun()

def render_chat_window():
    """Render the full chat window interface."""
    
    # Chat window container
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("### 🤖 GUARDIAN Assistant")
            
            # Quick help buttons
            st.markdown("**Quick Help:**")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                if st.button("AI Cybersecurity", key="quick_ai_cyber"):
                    handle_quick_question("What is AI Cybersecurity Maturity?")
            with col_b:
                if st.button("Quantum Security", key="quick_quantum"):
                    handle_quick_question("Explain Quantum Cybersecurity")
            with col_c:
                if st.button("Scoring Help", key="quick_scoring"):
                    handle_quick_question("How does GUARDIAN scoring work?")
            
            col_d, col_e = st.columns(2)
            with col_d:
                if st.button("Document Types", key="quick_docs"):
                    handle_quick_question("What are the document types?")
            with col_e:
                if st.button("Interface Help", key="quick_interface"):
                    handle_quick_question("How do I use the filters?")
            
            st.markdown("---")
            
            # Display chat messages
            if st.session_state.chat_messages:
                st.markdown("**Conversation:**")
                for message in st.session_state.chat_messages[-5:]:  # Show last 5 messages
                    if message['role'] == 'user':
                        st.markdown(f"**You:** {message['content']}")
                    else:
                        st.markdown(f"**Assistant:** {message['content']}")
                st.markdown("---")
            
            # Chat input
            user_input = st.text_input("Ask about GUARDIAN features, scoring, or navigation:", key="chat_input")
            
            col_send, col_close = st.columns([1, 1])
            with col_send:
                if st.button("Send", key="send_message") and user_input:
                    handle_user_message(user_input)
            with col_close:
                if st.button("Close Chat", key="close_chat"):
                    st.session_state.chat_open = False
                    st.rerun()

def handle_user_message(message: str):
    """Process user message and get chatbot response."""
    # Add user message to chat history
    st.session_state.chat_messages.append({
        'role': 'user',
        'content': message
    })
    
    # Get response from Dialogflow CX chatbot
    response = chatbot.detect_intent(message, st.session_state.chat_session_id)
    
    if response:
        bot_response = response.get('response_text', 'I apologize, but I cannot provide a response right now.')
        
        # Add bot response to chat history
        st.session_state.chat_messages.append({
            'role': 'assistant', 
            'content': bot_response
        })
    
    # Clear input and refresh
    st.session_state.chat_input = ""
    st.rerun()

def handle_quick_question(question: str):
    """Handle predefined quick help questions."""
    # Handle tour-specific responses
    if "Start guided tour" in question:
        response = """Welcome to GUARDIAN! Let me guide you through the system:

**Step 1: Policy Repository**
- Navigate to 'Policy Repository' → 'Document Repository' to browse analyzed documents
- View comprehensive scores across AI cybersecurity, quantum security, and ethics frameworks
- Use filters to find specific document types and organizations

**Step 2: Policy Analyzer**
- Go to 'Policy Repository' → 'Policy Analyzer' to upload new policies
- Get comprehensive gap analysis using GUARDIAN patent algorithms
- Receive targeted recommendations for policy improvement

**Step 3: Repository Insights**
- Check 'Policy Repository' → 'Repository Insights' for intelligent suggestions
- Discover similar documents and identify best practices
- Access AI-powered insights based on content analysis

Ready to explore? Ask me about any specific feature!"""
        
        st.session_state.chat_messages.append({
            'role': 'user',
            'content': question
        })
        st.session_state.chat_messages.append({
            'role': 'assistant',
            'content': response
        })
        st.rerun()
    elif "How do I navigate the Policy Repository" in question:
        response = """**GUARDIAN Navigation Guide:**

**Main Tabs:**
- **Policy Repository**: All document and analysis features
- **Repository Admin**: System management and monitoring
- **About GUARDIAN**: System information and patent technology

**Policy Repository Subtabs:**
1. **Repository**: Browse and filter analyzed policies
2. **Policy Analyzer**: Upload and analyze new documents
3. **Repository Insights**: AI-powered learning and suggestions

**Key Features:**
- Filter by organization, document type, or scoring framework
- View detailed scoring breakdowns and gap analysis
- Access patent-based algorithms for comprehensive assessment

Navigate using the tabs at the top. Need help with a specific section?"""
        
        st.session_state.chat_messages.append({
            'role': 'user',
            'content': question
        })
        st.session_state.chat_messages.append({
            'role': 'assistant',
            'content': response
        })
        st.rerun()
    elif "How does GUARDIAN scoring work" in question:
        response = """**GUARDIAN Scoring Framework:**

**Four Assessment Areas:**
1. **AI Cybersecurity**: 0-100 points measuring AI security maturity
2. **Quantum Cybersecurity**: 1-5 tier QCMEA framework assessment
3. **AI Ethics**: 0-100 points evaluating ethical AI practices
4. **Quantum Ethics**: 0-100 points assessing quantum ethics compliance

**Patent-Based Algorithms:**
- Dynamic governance using reinforcement learning
- Bayesian updates for real-time risk assessment
- Adaptive scoring based on emerging threats

**Color-Coded Results:**
- Green (High): Strong compliance and maturity
- Yellow (Medium): Areas needing attention
- Red (Low): Critical gaps requiring immediate action

Each score includes detailed breakdowns and improvement recommendations."""
        
        st.session_state.chat_messages.append({
            'role': 'user',
            'content': question
        })
        st.session_state.chat_messages.append({
            'role': 'assistant',
            'content': response
        })
        st.rerun()
    elif "upload and analyze a policy document" in question:
        response = """**Document Upload & Analysis:**

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

**Step 5: Save & Track**
- Documents are automatically saved to repository
- Track progress over time
- Compare with similar organizational policies

Upload takes 30-60 seconds depending on document size."""
        
        st.session_state.chat_messages.append({
            'role': 'user',
            'content': question
        })
        st.session_state.chat_messages.append({
            'role': 'assistant',
            'content': response
        })
        st.rerun()
    elif "What is policy gap analysis" in question:
        response = """**Policy Gap Analysis:**

**GUARDIAN Patent Algorithm:**
Uses reinforcement learning to identify policy weaknesses and provide targeted recommendations.

**Gap Severity Levels:**
- **Critical**: Immediate attention required (security vulnerabilities)
- **High**: Address within 30 days (compliance issues)
- **Medium**: Address within 90 days (best practice improvements)
- **Low**: Monitor and improve (optimization opportunities)

**Analysis Areas:**
- Regulatory compliance gaps
- Security framework deficiencies
- Ethics policy weaknesses
- Implementation inconsistencies

**Strategic Recommendations:**
- Specific policy language suggestions
- Regulatory alignment guidance
- Best practice implementation steps
- Timeline for addressing gaps

**Benefits:**
- Proactive risk identification
- Compliance assurance
- Continuous improvement tracking
- Evidence-based policy development

Gap analysis helps organizations strengthen their AI and quantum governance before issues arise."""
        
        st.session_state.chat_messages.append({
            'role': 'user',
            'content': question
        })
        st.session_state.chat_messages.append({
            'role': 'assistant',
            'content': response
        })
        st.rerun()
    else:
        handle_user_message(question)

def create_tooltip(text: str, tooltip_text: str, element_type: str = "general", element_name: str = "") -> str:
    """Create HTML tooltip for any text element."""
    if element_type and element_name:
        tooltip_content = chatbot.get_tooltip_response(element_type, element_name)
    else:
        tooltip_content = tooltip_text
    
    return f"""
    <span class="tooltip-trigger">
        {text}
        <span class="tooltip-content">{tooltip_content}</span>
    </span>
    """

def render_help_tooltip(label: str, help_text: str) -> str:
    """Render a help tooltip for form elements."""
    return f"""
    <div style="display: inline-flex; align-items: center; gap: 4px;">
        <span>{label}</span>
        <span class="tooltip-trigger" style="color: #3B82F6; cursor: help;">
            ℹ️
            <span class="tooltip-content">{help_text}</span>
        </span>
    </div>
    """

def inject_chatbot_css():
    """Inject global CSS for chatbot functionality."""
    st.markdown("""
    <style>
    /* Global tooltip styles */
    .tooltip-help {
        position: relative;
        display: inline-block;
        cursor: help;
        color: #3B82F6;
        margin-left: 4px;
    }
    
    .tooltip-help:hover::after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        background: #1f2937;
        color: white;
        padding: 6px 10px;
        border-radius: 4px;
        font-size: 12px;
        white-space: nowrap;
        z-index: 1000;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    
    /* Score badge tooltips */
    .score-badge {
        position: relative;
        cursor: help;
    }
    
    .score-badge:hover::after {
        content: attr(data-explanation);
        position: absolute;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        background: #1f2937;
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 11px;
        white-space: normal;
        max-width: 200px;
        z-index: 1001;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)