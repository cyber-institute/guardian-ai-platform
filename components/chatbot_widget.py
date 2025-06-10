"""
Interactive Chatbot Widget for GUARDIAN
Provides floating chat interface and intelligent tooltips
"""

import streamlit as st
import uuid
from utils.dialogflow_chatbot import chatbot

def render_chatbot_widget():
    """Render floating chatbot widget with Dialogflow CX integration."""
    
    # Initialize chat session
    if 'chat_session_id' not in st.session_state:
        st.session_state.chat_session_id = str(uuid.uuid4())
    
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    
    if 'chat_open' not in st.session_state:
        st.session_state.chat_open = False
    
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
    
    # Chatbot toggle button and window
    if st.session_state.chat_open:
        render_chat_window()
    else:
        render_chat_button()

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