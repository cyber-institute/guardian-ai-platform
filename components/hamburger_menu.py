"""
Hamburger Menu Component for GUARDIAN
Provides expandable menu with chatbot and navigation options
"""

import streamlit as st
from utils.dialogflow_chatbot import chatbot

def render_hamburger_menu():
    """Render hamburger menu with chatbot integration."""
    
    # Initialize menu state
    if 'menu_open' not in st.session_state:
        st.session_state.menu_open = False
    
    if 'chat_session_id' not in st.session_state:
        st.session_state.chat_session_id = str(__import__('uuid').uuid4())
    
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    
    # CSS for hamburger menu
    st.markdown("""
    <style>
    .hamburger-menu {
        position: fixed;
        top: 20px;
        left: 20px;
        z-index: 1000;
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        font-family: 'Inter', sans-serif;
    }
    
    .hamburger-button {
        width: 48px;
        height: 48px;
        background: white;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        gap: 3px;
        transition: all 0.3s ease;
    }
    
    .hamburger-button:hover {
        background: #f3f4f6;
        border-color: #9ca3af;
    }
    
    .hamburger-line {
        width: 20px;
        height: 2px;
        background: #374151;
        border-radius: 1px;
        transition: all 0.3s ease;
    }
    
    .menu-panel {
        position: absolute;
        top: 56px;
        left: 0;
        width: 320px;
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        padding: 20px;
        max-height: 600px;
        overflow-y: auto;
    }
    
    .menu-section {
        margin-bottom: 20px;
        padding-bottom: 16px;
        border-bottom: 1px solid #f3f4f6;
    }
    
    .menu-section:last-child {
        border-bottom: none;
        margin-bottom: 0;
    }
    
    .menu-title {
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 12px;
        font-size: 14px;
    }
    
    .quick-action-btn {
        display: block;
        width: 100%;
        padding: 8px 12px;
        margin-bottom: 6px;
        background: #f9fafb;
        border: 1px solid #e5e7eb;
        border-radius: 6px;
        color: #374151;
        text-decoration: none;
        font-size: 13px;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .quick-action-btn:hover {
        background: #3b82f6;
        color: white;
        border-color: #3b82f6;
    }
    
    .chat-input {
        width: 100%;
        padding: 8px 12px;
        border: 1px solid #d1d5db;
        border-radius: 6px;
        font-size: 13px;
        margin-bottom: 8px;
    }
    
    .chat-message {
        padding: 8px 12px;
        margin-bottom: 8px;
        border-radius: 6px;
        font-size: 12px;
        line-height: 1.4;
    }
    
    .user-message {
        background: #eff6ff;
        color: #1e40af;
        text-align: right;
    }
    
    .bot-message {
        background: #f3f4f6;
        color: #374151;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Hamburger button
    hamburger_html = f"""
    <div class="hamburger-menu">
        <div class="hamburger-button" onclick="toggleMenu()">
            <div class="hamburger-line"></div>
            <div class="hamburger-line"></div>
            <div class="hamburger-line"></div>
        </div>
        {render_menu_panel() if st.session_state.menu_open else ''}
    </div>
    
    <script>
    function toggleMenu() {{
        window.parent.postMessage({{type: 'toggle_menu'}}, '*');
    }}
    </script>
    """
    
    st.markdown(hamburger_html, unsafe_allow_html=True)
    
    # Handle menu toggle with invisible button
    col1, col2, col3 = st.columns([1, 10, 1])
    with col1:
        if st.button("", key="menu_toggle", help="Toggle menu"):
            st.session_state.menu_open = not st.session_state.menu_open
            st.rerun()

def render_menu_panel():
    """Render the expandable menu panel content."""
    
    menu_content = f"""
    <div class="menu-panel">
        <div class="menu-section">
            <div class="menu-title">GUARDIAN Assistant</div>
            {render_quick_actions()}
        </div>
        
        <div class="menu-section">
            <div class="menu-title">Quick Help</div>
            {render_chat_interface()}
        </div>
        
        <div class="menu-section">
            <div class="menu-title">Navigation</div>
            {render_navigation_links()}
        </div>
    </div>
    """
    
    return menu_content

def render_quick_actions():
    """Render quick action buttons."""
    actions = [
        ("AI Security Info", "What is AI Cybersecurity Maturity?"),
        ("Quantum Security Info", "Explain Quantum Cybersecurity"),
        ("Document Upload Help", "How do I upload a document?"),
        ("Interface Guide", "How do I use the filters?"),
        ("Scoring Explanation", "How does GUARDIAN scoring work?")
    ]
    
    action_html = ""
    for label, question in actions:
        action_html += f'<div class="quick-action-btn" onclick="askQuestion(\'{question}\')">{label}</div>'
    
    return action_html

def render_chat_interface():
    """Render chat interface within menu."""
    chat_html = """
    <input type="text" class="chat-input" placeholder="Ask about GUARDIAN..." id="chatInput">
    <div class="quick-action-btn" onclick="sendChatMessage()">Send Message</div>
    """
    
    # Add recent messages if any
    if st.session_state.chat_messages:
        chat_html += "<div style='max-height: 200px; overflow-y: auto; margin-top: 12px;'>"
        recent_messages = st.session_state.chat_messages[-4:]
        for msg in recent_messages:
            msg_class = "user-message" if msg['role'] == 'user' else "bot-message"
            content = msg['content'][:100] + "..." if len(msg['content']) > 100 else msg['content']
            chat_html += f'<div class="chat-message {msg_class}">{content}</div>'
        chat_html += "</div>"
    
    return chat_html

def render_navigation_links():
    """Render navigation shortcuts."""
    nav_html = """
    <div class="quick-action-btn" onclick="scrollToSection('documents')">All Documents</div>
    <div class="quick-action-btn" onclick="scrollToSection('patents')">Patent Technology</div>
    <div class="quick-action-btn" onclick="scrollToSection('admin')">Repository Admin</div>
    <div class="quick-action-btn" onclick="scrollToSection('about')">About GUARDIAN</div>
    """
    
    return nav_html

def handle_menu_chat_message(message: str):
    """Handle chat messages from hamburger menu."""
    if not message.strip():
        return
    
    # Add user message
    st.session_state.chat_messages.append({
        'role': 'user',
        'content': message
    })
    
    # Get chatbot response
    response = chatbot.detect_intent(message, st.session_state.chat_session_id)
    
    if response:
        bot_response = response.get('response_text', 'I apologize, but I cannot provide a response right now.')
        st.session_state.chat_messages.append({
            'role': 'assistant',
            'content': bot_response
        })
    
    st.rerun()

def add_menu_interactions():
    """Add JavaScript for menu interactions."""
    st.markdown("""
    <script>
    function askQuestion(question) {
        // Send predefined question
        window.parent.postMessage({type: 'chat_message', message: question}, '*');
    }
    
    function sendChatMessage() {
        const input = document.getElementById('chatInput');
        if (input && input.value.trim()) {
            window.parent.postMessage({type: 'chat_message', message: input.value}, '*');
            input.value = '';
        }
    }
    
    function scrollToSection(section) {
        // Scroll to section (would need to be implemented based on page structure)
        window.parent.postMessage({type: 'navigate', section: section}, '*');
    }
    
    // Handle Enter key in chat input
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && e.target.id === 'chatInput') {
            sendChatMessage();
        }
    });
    </script>
    """, unsafe_allow_html=True)

# Simple version for immediate implementation
def render_simple_hamburger_menu():
    """Render simplified hamburger menu using Streamlit components."""
    
    # Initialize state
    if 'menu_open' not in st.session_state:
        st.session_state.menu_open = False
    
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    
    # Create hamburger button in top-left
    col1, col2 = st.columns([1, 20])
    
    with col1:
        if st.button("≡", key="hamburger_btn", help="Open menu", use_container_width=True):
            st.session_state.menu_open = not st.session_state.menu_open
            st.rerun()
    
    # Show menu panel if open
    if st.session_state.menu_open:
        with st.expander("GUARDIAN Menu", expanded=True):
            # Quick Actions
            st.markdown("**Quick Help:**")
            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button("AI Security", key="menu_ai"):
                    handle_menu_message("What is AI Cybersecurity Maturity?")
                if st.button("Document Upload", key="menu_upload"):
                    handle_menu_message("How do I upload a document?")
            
            with col_b:
                if st.button("Quantum Security", key="menu_quantum"):
                    handle_menu_message("Explain Quantum Cybersecurity")
                if st.button("Interface Help", key="menu_help"):
                    handle_menu_message("How do I use the filters?")
            
            st.markdown("---")
            
            # Chat Interface
            st.markdown("**Ask GUARDIAN:**")
            user_input = st.text_input("", placeholder="Ask about GUARDIAN features...", key="menu_chat")
            
            if st.button("Send", key="menu_send") and user_input:
                handle_menu_message(user_input)
            
            # Recent messages
            if st.session_state.chat_messages:
                st.markdown("**Recent:**")
                for msg in st.session_state.chat_messages[-2:]:
                    if msg['role'] == 'user':
                        st.caption(f"You: {msg['content']}")
                    else:
                        st.caption(f"Assistant: {msg['content'][:100]}...")
            
            if st.button("Close Menu", key="close_menu"):
                st.session_state.menu_open = False
                st.rerun()

def handle_menu_message(message: str):
    """Handle messages from menu interface."""
    st.session_state.chat_messages.append({'role': 'user', 'content': message})
    
    response = chatbot.detect_intent(message)
    if response:
        st.session_state.chat_messages.append({
            'role': 'assistant', 
            'content': response.get('response_text', 'No response available')
        })
    
    st.rerun()