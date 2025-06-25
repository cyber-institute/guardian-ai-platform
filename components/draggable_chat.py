"""
Draggable Floating Chat Component for GUARDIAN
Uses Streamlit components to create a properly working draggable chat bubble
"""

import streamlit as st
import streamlit.components.v1 as components
import uuid

def render_draggable_chat():
    """Render a draggable floating chat bubble that actually works."""
    
    # Initialize chat state
    if 'chat_open' not in st.session_state:
        st.session_state.chat_open = False
    if 'chat_session_id' not in st.session_state:
        st.session_state.chat_session_id = str(uuid.uuid4())
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []

    # Create a simpler floating chat that works with Streamlit
    chat_html = """
    <div id="floating-chat-system">
        <div id="chat-bubble" class="speech-bubble">
            <div class="bubble-lines">
                <div class="line"></div>
                <div class="line"></div>
                <div class="line"></div>
            </div>
        </div>
    </div>

    <style>
    #floating-chat-system {
        position: fixed !important;
        bottom: 20px !important;
        right: 20px !important;
        z-index: 99999 !important;
        pointer-events: auto !important;
    }
    
    .speech-bubble {
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #3B82F6 0%, #1E40AF 100%);
        border-radius: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4);
        transition: all 0.3s ease;
        user-select: none;
        border: 3px solid #1E40AF;
        position: relative;
        animation: pulse 3s infinite;
    }
    
    .speech-bubble:before {
        content: "";
        position: absolute;
        bottom: -12px;
        left: 15px;
        width: 0;
        height: 0;
        border-left: 12px solid transparent;
        border-right: 0px solid transparent;
        border-top: 12px solid #1E40AF;
        transform: rotate(15deg);
    }
    
    .speech-bubble:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 30px rgba(59, 130, 246, 0.6);
    }
    
    @keyframes pulse {
        0%, 100% { 
            box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4);
        }
        50% { 
            box-shadow: 0 4px 20px rgba(59, 130, 246, 0.8);
        }
    }
    
    .bubble-lines {
        display: flex;
        flex-direction: column;
        gap: 3px;
        align-items: center;
    }
    
    .line {
        width: 20px;
        height: 2px;
        background: white;
        border-radius: 1px;
    }
    
    .line:nth-child(2) {
        width: 16px;
    }
    
    .line:nth-child(3) {
        width: 24px;
    }
    </style>

    <script>
    document.addEventListener('DOMContentLoaded', function() {
        const bubble = document.getElementById('chat-bubble');
        
        if (bubble) {
            console.log('Speech bubble found and ready');
            
            bubble.addEventListener('click', function() {
                console.log('Speech bubble clicked');
                // Post message to parent to trigger sidebar chat
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: { action: 'open_chat', timestamp: Date.now() }
                }, '*');
            });
            
            // Add drag functionality
            let isDragging = false;
            let startX, startY, offsetX, offsetY;
            
            bubble.addEventListener('mousedown', function(e) {
                isDragging = true;
                const rect = bubble.getBoundingClientRect();
                startX = e.clientX - rect.left;
                startY = e.clientY - rect.top;
                bubble.style.cursor = 'grabbing';
                e.preventDefault();
            });
            
            document.addEventListener('mousemove', function(e) {
                if (!isDragging) return;
                
                const container = document.getElementById('floating-chat-system');
                const newX = e.clientX - startX;
                const newY = e.clientY - startY;
                
                // Keep within viewport bounds
                const maxX = window.innerWidth - 80;
                const maxY = window.innerHeight - 80;
                
                const clampedX = Math.max(0, Math.min(newX, maxX));
                const clampedY = Math.max(0, Math.min(newY, maxY));
                
                container.style.left = clampedX + 'px';
                container.style.top = clampedY + 'px';
                container.style.right = 'auto';
                container.style.bottom = 'auto';
            });
            
            document.addEventListener('mouseup', function() {
                isDragging = false;
                bubble.style.cursor = 'pointer';
            });
        }
    });
    </script>
    """
    
    # Render the component with proper height
    result = components.html(chat_html, height=80)
    
    # Check if chat was opened via the bubble click
    if result and isinstance(result, dict) and result.get('action') == 'open_chat':
        st.session_state.chat_open = True
        st.rerun()
    
    return result