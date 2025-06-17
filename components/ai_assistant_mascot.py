"""
Floating AI Assistant Mascot Component
Provides contextual guidance and help throughout the GUARDIAN interface
"""

import streamlit as st
import random
from datetime import datetime

class AIAssistantMascot:
    def __init__(self):
        self.name = "ARIA"  # AI Risk Assessment Intelligence Assistant
        self.personality_traits = [
            "helpful", "knowledgeable", "encouraging", "professional"
        ]
        self.current_context = None
        
    def initialize_session_state(self):
        """Initialize session state variables for the assistant"""
        if 'assistant_visible' not in st.session_state:
            st.session_state.assistant_visible = True
        if 'assistant_context' not in st.session_state:
            st.session_state.assistant_context = 'welcome'
        if 'assistant_tips_shown' not in st.session_state:
            st.session_state.assistant_tips_shown = set()
        if 'assistant_interactions' not in st.session_state:
            st.session_state.assistant_interactions = 0

    def get_contextual_message(self, context, user_action=None):
        """Generate contextual messages based on current page/action"""
        
        messages = {
            'welcome': [
                "Welcome to GUARDIAN! I'm ARIA, your AI Risk Assessment assistant. Click on any document to see detailed scoring analysis.",
                "Hello! I'm here to help you navigate GUARDIAN's comprehensive AI and quantum security assessment tools.",
                "Welcome! Use the search and filter options to find specific documents by topic, organization, or scoring criteria."
            ],
            
            'documents_view': [
                "💡 Tip: Color-coded scores help you quickly identify document maturity levels - green for advanced, orange for developing, red for foundational.",
                "🔍 Pro tip: Use the search bar to filter documents by keywords, organizations, or specific frameworks.",
                "📊 Notice the different scoring systems: AI frameworks use 0-100 scales, while Quantum uses tier levels 1-5.",
                "⚡ Quick help: Click any score badge to see detailed analysis and recommendations for that framework."
            ],
            
            'analysis_modal': [
                "📋 This analysis breaks down how the document addresses specific security and ethics criteria.",
                "🎯 Focus areas show where the document excels and where improvements could be made.",
                "📈 Scoring considers implementation guidance, framework alignment, and practical applicability.",
                "💼 Use these insights to identify best practices and potential gaps in your organization's approach."
            ],
            
            'patent_technology': [
                "🔬 Our patent-protected Convergence AI system provides bias detection and anti-poisoning capabilities.",
                "⚙️ This section showcases the mathematical frameworks and quantum orchestration behind GUARDIAN's scoring.",
                "🛡️ The bias detection algorithms help ensure fair and accurate assessments across different document types.",
                "🧬 Quantum integration enhances pattern recognition and reduces computational bias in the analysis."
            ],
            
            'recommendations': [
                "📝 Recommendations are generated based on document gaps and industry best practices.",
                "🎯 Priority levels help you focus on the most impactful improvements first.",
                "📊 Implementation timelines provide realistic planning guidance for your organization.",
                "🔄 Regular assessment updates help track progress and identify emerging requirements."
            ],
            
            'error_recovery': [
                "⚠️ If you encounter any issues, try refreshing the page or clearing your browser cache.",
                "🔧 For scoring problems, the system automatically provides fallback analysis when needed.",
                "📞 Complex technical issues can be reported through the help documentation.",
                "💪 GUARDIAN is designed to be resilient - temporary glitches won't affect your data integrity."
            ]
        }
        
        context_messages = messages.get(context, messages['welcome'])
        return random.choice(context_messages)

    def render_floating_assistant(self):
        """Render the floating assistant mascot"""
        self.initialize_session_state()
        
        if not st.session_state.assistant_visible:
            return
            
        # Get current context
        current_page = st.session_state.get('current_page', 'documents')
        message = self.get_contextual_message(st.session_state.assistant_context)
        
        # Floating assistant CSS and HTML
        assistant_html = f"""
        <div id="ai-assistant-mascot" style="
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 320px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            padding: 15px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            z-index: 1000;
            color: white;
            font-family: Arial, sans-serif;
            animation: float 3s ease-in-out infinite;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        ">
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <div style="
                    width: 40px;
                    height: 40px;
                    background: linear-gradient(45deg, #ff6b6b, #feca57);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    margin-right: 12px;
                    font-size: 20px;
                    animation: pulse 2s infinite;
                ">
                    🤖
                </div>
                <div>
                    <div style="font-weight: bold; font-size: 14px;">ARIA Assistant</div>
                    <div style="font-size: 11px; opacity: 0.8;">AI Risk Assessment Guide</div>
                </div>
                <button onclick="toggleAssistant()" style="
                    background: none;
                    border: none;
                    color: white;
                    font-size: 18px;
                    margin-left: auto;
                    cursor: pointer;
                    opacity: 0.7;
                    padding: 5px;
                    border-radius: 50%;
                    width: 30px;
                    height: 30px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                ">×</button>
            </div>
            
            <div style="
                font-size: 13px;
                line-height: 1.4;
                margin-bottom: 12px;
                padding: 10px;
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
                border-left: 3px solid #feca57;
            ">
                {message}
            </div>
            
            <div style="display: flex; gap: 8px; justify-content: space-between;">
                <button onclick="getNewTip()" style="
                    background: rgba(255,255,255,0.2);
                    border: none;
                    color: white;
                    padding: 6px 12px;
                    border-radius: 15px;
                    font-size: 11px;
                    cursor: pointer;
                    flex: 1;
                    transition: all 0.3s ease;
                ">💡 New Tip</button>
                <button onclick="showHelp()" style="
                    background: rgba(255,255,255,0.2);
                    border: none;
                    color: white;
                    padding: 6px 12px;
                    border-radius: 15px;
                    font-size: 11px;
                    cursor: pointer;
                    flex: 1;
                    transition: all 0.3s ease;
                ">❓ Help</button>
            </div>
        </div>
        
        <style>
        @keyframes float {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-10px); }}
        }}
        
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.1); }}
        }}
        
        #ai-assistant-mascot button:hover {{
            background: rgba(255,255,255,0.3) !important;
            transform: scale(1.05);
        }}
        
        @media (max-width: 768px) {{
            #ai-assistant-mascot {{
                width: 280px;
                bottom: 10px;
                right: 10px;
                font-size: 12px;
            }}
        }}
        </style>
        
        <script>
        function toggleAssistant() {{
            const assistant = document.getElementById('ai-assistant-mascot');
            if (assistant) {{
                assistant.style.display = 'none';
            }}
        }}
        
        function getNewTip() {{
            // Trigger Streamlit rerun to get new tip
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue',
                value: 'new_tip_' + Date.now()
            }}, '*');
        }}
        
        function showHelp() {{
            window.parent.postMessage({{
                type: 'streamlit:setComponentValue', 
                value: 'show_help_' + Date.now()
            }}, '*');
        }}
        </script>
        """
        
        st.markdown(assistant_html, unsafe_allow_html=True)

    def update_context(self, new_context, user_action=None):
        """Update the assistant's context for more relevant guidance"""
        st.session_state.assistant_context = new_context
        if user_action:
            st.session_state.assistant_interactions += 1

    def show_help_modal(self):
        """Show comprehensive help modal when requested"""
        with st.sidebar:
            st.markdown("### 🤖 ARIA Assistant Help")
            st.markdown("""
            **What I can do:**
            - Provide contextual tips based on your current page
            - Explain scoring systems and color coding
            - Guide you through document analysis features
            - Offer navigation help and shortcuts
            
            **Quick Tips:**
            - **Green scores (75+)**: Advanced implementation
            - **Orange scores (50-74)**: Developing practices  
            - **Red scores (<50)**: Foundational level
            - **Gray scores**: Not applicable to document type
            
            **Keyboard Shortcuts:**
            - Press **Ctrl+F** to search documents
            - Click score badges for detailed analysis
            - Use filters to narrow down results
            
            **Getting Started:**
            1. Browse the Policy Repository tab for document analysis
            2. Check Patent Technology for technical details
            3. View Recommendations for improvement suggestions
            4. Explore LLM Enhancement for advanced features
            """)

    def provide_contextual_guidance(self, page_name, element_type=None):
        """Provide specific guidance based on current page and element"""
        
        guidance_map = {
            'documents': {
                'page_load': 'documents_view',
                'score_click': 'analysis_modal',
                'search': 'documents_view',
                'filter': 'documents_view'
            },
            'patent': {
                'page_load': 'patent_technology',
                'mathematical': 'patent_technology',
                'convergence': 'patent_technology'
            },
            'recommendations': {
                'page_load': 'recommendations',
                'priority': 'recommendations'
            },
            'about': {
                'page_load': 'welcome'
            }
        }
        
        context = guidance_map.get(page_name, {}).get(element_type, 'welcome')
        self.update_context(context, element_type)

def render_ai_assistant():
    """Convenience function to render the AI assistant"""
    assistant = AIAssistantMascot()
    assistant.render_floating_assistant()
    return assistant