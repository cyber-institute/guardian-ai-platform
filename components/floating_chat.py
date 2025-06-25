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

    # Always render the floating button (fake speech bubble)
    render_floating_button()
    
    # Render chat in sidebar when open
    if st.session_state.chat_open:
        render_sidebar_chat()

def render_floating_button():
    """Render a fake working chat bubble with speech bubble shape."""
    
    # CSS for the speech bubble shaped chat button
    st.markdown("""
    <style>
    .speech-bubble {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 80px;
        height: 60px;
        background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%);
        border-radius: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4);
        z-index: 10000;
        transition: all 0.3s ease;
        animation: bubblePulse 3s infinite;
        user-select: none;
        border: 3px solid #1E40AF;
    }
    
    .speech-bubble:before {
        content: "";
        position: absolute;
        bottom: -15px;
        left: 20px;
        width: 0;
        height: 0;
        border-left: 15px solid transparent;
        border-right: 0px solid transparent;
        border-top: 15px solid #1E40AF;
        transform: rotate(15deg);
    }
    
    .speech-bubble:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 30px rgba(59, 130, 246, 0.6);
    }
    
    .speech-bubble:active {
        transform: scale(0.95);
    }
    
    .bubble-lines {
        display: flex;
        flex-direction: column;
        gap: 4px;
        align-items: center;
    }
    
    .bubble-line {
        width: 30px;
        height: 3px;
        background: white;
        border-radius: 2px;
    }
    
    .bubble-line:nth-child(2) {
        width: 25px;
    }
    
    .bubble-line:nth-child(3) {
        width: 35px;
    }
    
    @keyframes bubblePulse {
        0%, 100% { box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4); }
        50% { box-shadow: 0 4px 20px rgba(59, 130, 246, 0.8); }
    }
    
    /* Hide the real Streamlit button */
    .hidden-aria-btn {
        position: fixed;
        bottom: -100px;
        right: -100px;
        opacity: 0;
        pointer-events: none;
        z-index: -1;
    }
    </style>
    
    <div class="speech-bubble" onclick="
        const hiddenBtn = document.querySelector('.hidden-aria-btn button');
        if (hiddenBtn) hiddenBtn.click();
    ">
        <div class="bubble-lines">
            <div class="bubble-line"></div>
            <div class="bubble-line"></div>
            <div class="bubble-line"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hidden Streamlit button that actually works
    st.markdown('<div class="hidden-aria-btn">', unsafe_allow_html=True)
    if st.button("Open ARIA Chat", key="hidden_aria_button", help="Hidden ARIA button"):
        st.session_state.chat_open = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Always show test button in sidebar for now
    with st.sidebar:
        st.markdown("---")
        st.markdown("**Test Chat Interface**")
        
        # Blue button styling for test button
        st.markdown("""
        <style>
        /* Test button styling */
        .stButton > button[data-testid="baseButton-secondary"] {
            background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            padding: 12px 24px !important;
            box-shadow: 0 3px 10px rgba(59, 130, 246, 0.4) !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button[data-testid="baseButton-secondary"]:hover {
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
            box-shadow: 0 5px 15px rgba(59, 130, 246, 0.6) !important;
            transform: translateY(-2px) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        if st.button("Test ARIA Chat", key="test_aria_chat"):
            st.session_state.chat_open = True
            st.rerun()

def render_sidebar_chat():
    """Render chat interface in sidebar when open."""
    with st.sidebar:
        st.markdown("### 💬 ARIA Chat")
        st.markdown("*Advanced Risk Intelligence Assistant*")
        
        # Custom CSS for blue button styling
        st.markdown("""
        <style>
        /* Blue button styling for ARIA chat */
        .stButton > button {
            background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            padding: 10px 20px !important;
            box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3) !important;
            transition: all 0.3s ease !important;
            width: auto !important;
            max-width: 200px !important;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.5) !important;
            transform: translateY(-1px) !important;
        }
        
        .stButton > button:active {
            transform: translateY(0px) !important;
        }
        
        /* Adjust text input styling */
        .stTextInput > div > div > input {
            font-size: 14px !important;
            padding: 8px 12px !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Close button
        if st.button("Close Chat", key="aria_close_chat"):
            st.session_state.chat_open = False
            st.rerun()
        
        st.markdown("---")
        
        # Display rotating tip
        tips = [
            "Ask me about document scoring frameworks",
            "Upload documents for instant analysis", 
            "Click score badges for detailed breakdowns",
            "Use filters to find documents by criteria",
            "Ask about critical policy gaps",
            "Learn about GUARDIAN's algorithms"
        ]
        
        current_time = int(time.time())
        current_tip_index = (current_time // 10) % len(tips)
        
        st.info(f"💡 {tips[current_tip_index]}")
        
        # Chat messages container
        chat_container = st.container()
        
        with chat_container:
            if st.session_state.chat_messages:
                st.markdown("**Conversation:**")
                
                # Display messages in simple format for sidebar
                for i, message in enumerate(st.session_state.chat_messages[-5:]):
                    if message['role'] == 'user':
                        st.markdown(f"**You:** {message['content']}")
                    else:
                        st.markdown(f"**ARIA:** {message['content']}")
                    
                    if i < len(st.session_state.chat_messages[-5:]) - 1:
                        st.markdown("---")
            else:
                st.markdown("*Start chatting with ARIA below!*")
        
        st.markdown("---")
        
        # Chat input section
        user_input = st.text_input(
            "Type your message:", 
            key="aria_chat_input_real", 
            placeholder="Ask ARIA about GUARDIAN features...",
            label_visibility="visible"
        )
        
        col1, col2 = st.columns([2, 1])
        with col1:
            send_clicked = st.button("Send Message", key="aria_send_btn")
        with col2:
            clear_clicked = st.button("Clear", key="aria_clear_btn")
        
        # Handle button clicks
        if send_clicked and user_input.strip():
            handle_user_message(user_input.strip())
            
        if clear_clicked:
            st.session_state.chat_messages = []
            st.rerun()

def handle_user_message(user_input):
    """Handle user message and generate ARIA response."""
    # Add user message to chat history
    st.session_state.chat_messages.append({
        'role': 'user',
        'content': user_input
    })
    
    # Generate intelligent response based on GUARDIAN context
    response = generate_aria_response(user_input)
    
    st.session_state.chat_messages.append({
        'role': 'assistant',
        'content': response
    })
    
    # Rerun to update display
    st.rerun()

def generate_aria_response(user_input):
    """Generate contextual ARIA responses about GUARDIAN."""
    user_input_lower = user_input.lower()
    
    # Document scoring questions
    if any(word in user_input_lower for word in ['score', 'scoring', 'assessment', 'evaluate']):
        return "GUARDIAN uses a multi-tier scoring system: AI Cybersecurity (0-100), Quantum Readiness (Tier 1-5), and AI Ethics evaluation. Each score reflects comprehensive content analysis using our patent-protected algorithms. Click any score badge for detailed breakdowns!"
    
    # Upload questions
    elif any(word in user_input_lower for word in ['upload', 'add', 'document', 'file']):
        return "You can upload documents in multiple ways: 1) Use the file uploader in All Documents tab, 2) Enter URLs for web scraping, 3) Bulk upload via CSV. Supported formats: PDF, TXT, DOCX, and web URLs. Each document gets automatically analyzed and scored."
    
    # Gap analysis questions
    elif any(word in user_input_lower for word in ['gap', 'missing', 'policy', 'recommendation']):
        return "GUARDIAN's Policy Gap Analysis identifies critical security gaps by comparing your documents against NIST frameworks, quantum readiness standards, and AI ethics benchmarks. Check the Policy Analyzer for specific recommendations based on your document portfolio."
    
    # Framework questions
    elif any(word in user_input_lower for word in ['nist', 'framework', 'standard', 'cybersecurity']):
        return "GUARDIAN aligns with NIST AI Risk Management Framework, NIST Cybersecurity Framework, and emerging quantum security standards. Our scoring reflects compliance levels with these frameworks and identifies areas needing attention."
    
    # Convergence AI questions
    elif any(word in user_input_lower for word in ['convergence', 'multi-llm', 'bias', 'ensemble']):
        return "Convergence AI is GUARDIAN's patent-protected multi-LLM system that prevents bias and poisoning attacks. It uses quantum-enhanced routing to synthesize insights from multiple AI models, ensuring more accurate and unbiased document analysis."
    
    # Navigation help
    elif any(word in user_input_lower for word in ['help', 'how', 'navigate', 'use', 'tutorial']):
        return "Navigate GUARDIAN easily: All Documents tab shows your repository, About tab explains the system, Convergence AI shows our technology. Use filters to find documents, click score badges for details, and upload new content anytime. Need specific help with any feature?"
    
    # Quantum questions
    elif any(word in user_input_lower for word in ['quantum', 'tier', 'readiness']):
        return "Quantum scoring uses our 5-tier system: Tier 1 (Basic awareness) to Tier 5 (Post-quantum ready). This evaluates quantum security preparedness, cryptographic resilience, and quantum computing integration readiness in your documents."
    
    # General greeting
    elif any(word in user_input_lower for word in ['hello', 'hi', 'help', 'start']):
        return "Hello! I'm ARIA, your Advanced Risk Intelligence Assistant. I can help you understand GUARDIAN's scoring systems, document management, policy gap analysis, and navigation. What would you like to know about?"
    
    # Default response
    else:
        return f"I understand you're asking about '{user_input}'. As GUARDIAN's AI assistant, I can help with document scoring, upload processes, policy gap analysis, framework compliance, and system navigation. Could you be more specific about what you'd like to know?"