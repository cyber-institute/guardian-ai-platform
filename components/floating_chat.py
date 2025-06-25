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

def render_sidebar_chat():
    """Render chat interface in an expander when open."""
    # Create a floating chat window using expander
    with st.expander("💬 ARIA - Advanced Risk Intelligence Assistant", expanded=True):
        # Close button
        if st.button("Close Chat", key="aria_close_chat", use_container_width=True):
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
        
        current_time = int(time.time())
        current_tip_index = (current_time // 10) % len(tips)
        
        st.info(f"💡 {tips[current_tip_index]}")
        
        # Chat messages with conversation bubbles
        if st.session_state.chat_messages:
            st.markdown("**Recent Conversation:**")
            
            # CSS for conversation bubbles
            st.markdown("""
            <style>
            .user-bubble {
                background: #3B82F6;
                color: white;
                padding: 10px 15px;
                border-radius: 20px 20px 5px 20px;
                margin: 8px 0 8px 40px;
                display: inline-block;
                max-width: 80%;
                word-wrap: break-word;
                float: right;
                clear: both;
            }
            
            .assistant-bubble {
                background: #f8fafc;
                color: #334155;
                padding: 10px 15px;
                border-radius: 20px 20px 20px 5px;
                margin: 8px 40px 8px 0;
                border: 1px solid #e2e8f0;
                display: inline-block;
                max-width: 80%;
                word-wrap: break-word;
                float: left;
                clear: both;
            }
            
            .chat-container::after {
                content: "";
                display: table;
                clear: both;
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for message in st.session_state.chat_messages[-4:]:
                if message['role'] == 'user':
                    st.markdown(f'<div class="user-bubble">{message["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="assistant-bubble">{message["content"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("*Start a conversation with ARIA by typing below!*")
        
        # Chat input
        user_input = st.text_input("Type your message:", key="aria_chat_input", placeholder="Ask ARIA about GUARDIAN features...")
        
        col1, col2 = st.columns([4, 1])
        with col1:
            if st.button("Send Message", key="aria_send_full", use_container_width=True):
                if user_input:
                    handle_user_message(user_input)
        with col2:
            if st.button("▷", key="aria_send_arrow", help="Send"):
                if user_input:
                    handle_user_message(user_input)

def handle_user_message(user_input):
    """Handle user message and generate response."""
    if user_input.strip():
        # Add user message to chat history
        st.session_state.chat_messages.append({
            'role': 'user',
            'content': user_input
        })
        
        # Generate response using the chatbot
        try:
            response = chatbot(user_input, st.session_state.chat_session_id)
            st.session_state.chat_messages.append({
                'role': 'assistant',
                'content': response
            })
        except Exception as e:
            st.session_state.chat_messages.append({
                'role': 'assistant',
                'content': f"I'm having trouble processing your request right now. Please try asking about GUARDIAN's features, document scoring, or navigation help."
            })
        
        # Clear the input and rerun
        st.rerun()