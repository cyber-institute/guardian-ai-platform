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
    """Render the floating chat button using HTML with proper Streamlit integration."""
    
    # Initialize session state trigger
    if 'aria_clicked' not in st.session_state:
        st.session_state.aria_clicked = False
    
    # CSS and HTML for floating button
    st.markdown("""
    <style>
    .floating-aria-btn {
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
        animation: ariaPulse 3s infinite;
        user-select: none;
    }
    
    .floating-aria-btn:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 30px rgba(59, 130, 246, 0.6);
    }
    
    .floating-aria-btn:active {
        transform: scale(0.95);
    }
    
    @keyframes ariaPulse {
        0%, 100% { box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4); }
        50% { box-shadow: 0 4px 20px rgba(59, 130, 246, 0.8); }
    }
    </style>
    
    <div class="floating-aria-btn" id="ariaBtn">
        ARIA
    </div>
    
    <script>
    // Use session state approach to trigger Streamlit rerun
    (function() {
        const ariaBtn = document.getElementById('ariaBtn');
        if (ariaBtn && !ariaBtn.hasEventListener) {
            ariaBtn.hasEventListener = true;
            ariaBtn.addEventListener('click', function() {
                // Set a flag in localStorage that Streamlit can check
                localStorage.setItem('aria_chat_trigger', Date.now().toString());
                
                // Trigger a Streamlit rerun by dispatching a custom event
                window.dispatchEvent(new CustomEvent('ariaButtonClicked'));
                
                // Also try to trigger Streamlit's built-in event system
                if (window.parent && window.parent.postMessage) {
                    window.parent.postMessage({
                        type: 'streamlit:setComponentValue',
                        value: { clicked: true, timestamp: Date.now() }
                    }, '*');
                }
            });
        }
    })();
    </script>
    """, unsafe_allow_html=True)
    
    # Check for click trigger using timestamp
    current_timestamp = int(time.time())
    stored_trigger = st.session_state.get('last_aria_trigger', '0')
    
    # Use a polling approach with session state
    if st.button("", key="aria_trigger_check", help="Hidden trigger"):
        st.session_state.chat_open = True
        st.rerun()
    
    # JavaScript-based trigger detection
    st.markdown(f"""
    <script>
    // Check localStorage for trigger
    const trigger = localStorage.getItem('aria_chat_trigger');
    if (trigger && trigger !== '{stored_trigger}') {{
        localStorage.setItem('aria_chat_trigger', '');
        // Find and click the hidden Streamlit button
        setTimeout(() => {{
            const hiddenBtn = document.querySelector('[data-testid*="aria_trigger_check"] button');
            if (hiddenBtn) {{
                hiddenBtn.click();
            }}
        }}, 50);
    }}
    </script>
    """, unsafe_allow_html=True)
    
    # Alternative approach: Use query parameters
    query_params = st.query_params
    if 'aria_open' in query_params:
        st.session_state.chat_open = True
        # Clear the query parameter
        new_params = {k: v for k, v in query_params.items() if k != 'aria_open'}
        st.query_params.clear()
        for k, v in new_params.items():
            st.query_params[k] = v
        st.rerun()
    
    # Fallback: Check for click state changes
    if 'aria_last_check' not in st.session_state:
        st.session_state.aria_last_check = current_timestamp
    
    # Simple polling mechanism - check every few seconds
    if current_timestamp - st.session_state.aria_last_check > 2:
        st.session_state.aria_last_check = current_timestamp
        # This causes a rerun that can detect state changes
        st.rerun()

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