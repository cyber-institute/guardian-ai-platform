"""
Smart Context-Aware Help Bubbles for GUARDIAN
Provides intelligent, adaptive help based on user context, document content, and interaction patterns
"""

import streamlit as st
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import re

class SmartHelpBubbles:
    """Smart context-aware help system that adapts to user behavior and content context"""
    
    def __init__(self):
        # Initialize user interaction tracking
        if 'help_interactions' not in st.session_state:
            st.session_state.help_interactions = {}
        if 'user_help_preferences' not in st.session_state:
            st.session_state.user_help_preferences = {
                'detail_level': 'medium',  # basic, medium, detailed
                'shown_helps': set(),
                'dismissed_helps': set(),
                'preferred_formats': ['tooltip', 'expandable']
            }
        
        self.context_definitions = {
            # Document-specific help
            'document_scoring': {
                'context_triggers': ['score', 'assessment', 'rating'],
                'basic': 'Document scores show how well policies address cybersecurity and ethics.',
                'medium': 'Scores range 0-100 for most frameworks, 1-5 for Quantum Cybersecurity. Higher scores indicate better coverage.',
                'detailed': 'GUARDIAN uses multi-LLM analysis against NIST AI RMF, quantum security standards, and ethics frameworks. Scores reflect comprehensiveness, implementation guidance, and risk mitigation coverage.'
            },
            'quantum_cybersecurity': {
                'context_triggers': ['quantum', 'post-quantum', 'cryptography'],
                'basic': 'Quantum cybersecurity protects against quantum computing threats.',
                'medium': 'Assesses post-quantum cryptography readiness and quantum-safe practices on 1-5 tier scale.',
                'detailed': 'Evaluates quantum key distribution, post-quantum algorithms, quantum-resistant protocols, and transition planning. Tier 1 = Basic awareness, Tier 5 = Comprehensive quantum security.'
            },
            'ai_cybersecurity': {
                'context_triggers': ['ai', 'artificial intelligence', 'machine learning'],
                'basic': 'AI cybersecurity focuses on securing AI systems and using AI for security.',
                'medium': 'Measures AI threat detection, model protection, data security, and adversarial robustness (0-100 scale).',
                'detailed': 'Comprehensive assessment including adversarial ML protection, model validation, AI-powered threat detection, bias mitigation, and AI system governance based on NIST AI RMF.'
            },
            'policy_gaps': {
                'context_triggers': ['gap', 'missing', 'recommendation'],
                'basic': 'Policy gaps show areas needing improvement.',
                'medium': 'Identified weaknesses with severity levels and targeted recommendations.',
                'detailed': 'AI-powered gap analysis using patent algorithms to identify policy weaknesses, assess impact severity (Critical/High/Medium/Low), and generate specific improvement recommendations.'
            },
            'filter_usage': {
                'context_triggers': ['filter', 'search', 'organization'],
                'basic': 'Filters help find specific documents.',
                'medium': 'Filter by document type, organization, year, region, or AI/Quantum focus.',
                'detailed': 'Smart filtering with auto-complete, topic detection, and regional classification. Hover over filter labels for detailed explanations of each category.'
            }
        }
        
        # Adaptive help based on user journey
        self.journey_stages = {
            'newcomer': {
                'triggers': lambda: len(st.session_state.get('help_interactions', {})) < 3,
                'help_style': 'proactive',
                'detail_level': 'medium'
            },
            'explorer': {
                'triggers': lambda: 3 <= len(st.session_state.get('help_interactions', {})) < 10,
                'help_style': 'contextual',
                'detail_level': 'detailed'
            },
            'expert': {
                'triggers': lambda: len(st.session_state.get('help_interactions', {})) >= 10,
                'help_style': 'minimal',
                'detail_level': 'basic'
            }
        }
    
    def detect_user_stage(self) -> str:
        """Detect current user stage based on interaction patterns"""
        for stage, config in self.journey_stages.items():
            if config['triggers']():
                return stage
        return 'newcomer'
    
    def analyze_content_context(self, content: str, title: str = "") -> List[str]:
        """Analyze content to determine relevant help topics"""
        combined_text = (content + " " + title).lower()
        relevant_contexts = []
        
        for context_key, context_data in self.context_definitions.items():
            for trigger in context_data['context_triggers']:
                if trigger in combined_text:
                    relevant_contexts.append(context_key)
                    break
        
        return relevant_contexts
    
    def should_show_help(self, help_key: str, force: bool = False) -> bool:
        """Determine if help should be shown based on user preferences and history"""
        if force:
            return True
        
        # Initialize user help preferences if not present
        if 'user_help_preferences' not in st.session_state:
            st.session_state.user_help_preferences = {
                'dismissed_helps': [],
                'shown_helps': [],
                'interaction_count': 0,
                'first_visit': True
            }
        
        prefs = st.session_state.user_help_preferences
        
        # Don't show if user dismissed this help
        if help_key in prefs['dismissed_helps']:
            return False
        
        # Show based on user stage
        user_stage = self.detect_user_stage()
        stage_config = self.journey_stages[user_stage]
        
        if stage_config['help_style'] == 'minimal':
            return help_key not in prefs['shown_helps']
        elif stage_config['help_style'] == 'proactive':
            return True
        else:  # contextual
            return help_key not in prefs['shown_helps'] or len(prefs['shown_helps']) < 5
    
    def get_help_content(self, context_key: str, custom_detail_level: str = None) -> str:
        """Get appropriate help content based on user preferences"""
        if context_key not in self.context_definitions:
            return ""
        
        prefs = st.session_state.user_help_preferences
        detail_level = custom_detail_level or prefs['detail_level']
        
        return self.context_definitions[context_key].get(detail_level, 
               self.context_definitions[context_key]['medium'])
    
    def render_smart_tooltip(self, text: str, context_key: str, 
                           position: str = "top", style: str = "bubble") -> str:
        """Render smart tooltip with context-aware content"""
        if not self.should_show_help(context_key):
            return text
        
        help_content = self.get_help_content(context_key)
        
        # Track interaction
        self._track_help_interaction(context_key, 'tooltip_shown')
        
        if style == "bubble":
            return f"""
            <div class="smart-tooltip-container" style="position: relative; display: inline-block;">
                <span class="tooltip-trigger" style="
                    border-bottom: 1px dotted #3B82F6;
                    cursor: help;
                    color: #3B82F6;
                ">{text}</span>
                <div class="smart-tooltip bubble-style" style="
                    visibility: hidden;
                    opacity: 0;
                    position: absolute;
                    z-index: 1000;
                    background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
                    color: white;
                    padding: 12px 16px;
                    border-radius: 12px;
                    font-size: 14px;
                    line-height: 1.4;
                    max-width: 300px;
                    box-shadow: 0 8px 32px rgba(59, 130, 246, 0.3);
                    transform: translateY(-10px);
                    transition: all 0.3s ease;
                    {self._get_position_styles(position)}
                ">{help_content}</div>
            </div>
            <style>
            .smart-tooltip-container:hover .smart-tooltip {{
                visibility: visible;
                opacity: 1;
                transform: translateY(0);
            }}
            </style>
            """
        else:  # minimal style
            return f'<span title="{help_content}" style="border-bottom: 1px dotted #6B7280; cursor: help;">{text}</span>'
    
    def render_contextual_help_panel(self, document_content: str = "", 
                                   document_title: str = "", show_all: bool = False):
        """Render adaptive help panel based on current context"""
        if not document_content and not show_all:
            return
        
        relevant_contexts = self.analyze_content_context(document_content, document_title) if document_content else []
        user_stage = self.detect_user_stage()
        
        # Show different help based on user stage
        if user_stage == 'newcomer' or show_all:
            with st.expander("💡 Smart Help - Getting Started", expanded=user_stage == 'newcomer'):
                self._render_newcomer_help(relevant_contexts)
        elif user_stage == 'explorer':
            if relevant_contexts:
                with st.expander("🔍 Context-Aware Help", expanded=False):
                    self._render_contextual_help(relevant_contexts)
        # Expert users get minimal help unless explicitly requested
    
    def render_interactive_help_bubble(self, help_key: str, text: str, 
                                     bubble_type: str = "info") -> None:
        """Render interactive help bubble with actions"""
        if not self.should_show_help(help_key):
            return
        
        help_content = self.get_help_content(help_key)
        
        bubble_colors = {
            'info': '#3B82F6',
            'tip': '#10B981', 
            'warning': '#F59E0B',
            'important': '#EF4444'
        }
        
        color = bubble_colors.get(bubble_type, '#3B82F6')
        
        col1, col2, col3 = st.columns([6, 1, 1])
        
        with col1:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, {color}15 0%, {color}25 100%);
                border-left: 4px solid {color};
                padding: 12px 16px;
                border-radius: 8px;
                margin: 8px 0;
            ">
                <div style="color: {color}; font-weight: 600; margin-bottom: 4px;">{text}</div>
                <div style="color: #374151; font-size: 14px;">{help_content}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.button("📚", key=f"more_{help_key}", help="More details"):
                self._show_detailed_help(help_key)
        
        with col3:
            if st.button("✕", key=f"dismiss_{help_key}", help="Dismiss"):
                self._dismiss_help(help_key)
    
    def render_progress_aware_help(self, current_section: str):
        """Render help that adapts to user's current section and progress"""
        section_helps = {
            'policy_repository': {
                'newcomer': "Welcome! Start by exploring documents using the filters above. Click on any document card to see detailed analysis.",
                'explorer': "Pro tip: Use the View Mode options (Cards, Compact, Table) to customize how you browse documents.",
                'expert': ""
            },
            'patent_technology': {
                'newcomer': "This section showcases GUARDIAN's patent-pending algorithms for AI governance and risk assessment.",
                'explorer': "Explore the mathematical formulas and implementation details behind GUARDIAN's scoring systems.",
                'expert': ""
            },
            'recommendations': {
                'newcomer': "Get AI-powered recommendations for improving your cybersecurity and ethics policies.",
                'explorer': "Use advanced filters to get targeted recommendations for specific frameworks or document types.",
                'expert': ""
            }
        }
        
        user_stage = self.detect_user_stage()
        help_text = section_helps.get(current_section, {}).get(user_stage, "")
        
        if help_text and self.should_show_help(f"section_{current_section}"):
            st.info(help_text)
    
    def _get_position_styles(self, position: str) -> str:
        """Get CSS styles for tooltip positioning"""
        positions = {
            'top': 'bottom: 100%; left: 50%; transform: translateX(-50%); margin-bottom: 8px;',
            'bottom': 'top: 100%; left: 50%; transform: translateX(-50%); margin-top: 8px;',
            'left': 'right: 100%; top: 50%; transform: translateY(-50%); margin-right: 8px;',
            'right': 'left: 100%; top: 50%; transform: translateY(-50%); margin-left: 8px;'
        }
        return positions.get(position, positions['top'])
    
    def _render_newcomer_help(self, relevant_contexts: List[str]):
        """Render comprehensive help for new users"""
        st.markdown("**Welcome to GUARDIAN!** Here's what you need to know:")
        
        cols = st.columns(2)
        
        with cols[0]:
            st.markdown("""
            **🔍 Exploring Documents:**
            - Use filters to find specific documents
            - Click document cards for detailed analysis
            - Switch between view modes for different layouts
            """)
            
            st.markdown("""
            **📊 Understanding Scores:**
            - Green (75+): Excellent coverage
            - Orange (50-74): Good but improvable  
            - Red (<50): Needs attention
            - Gray: Not applicable to this document
            """)
        
        with cols[1]:
            st.markdown("""
            **🎯 Key Features:**
            - Policy gap analysis with recommendations
            - Multi-framework scoring (AI, Quantum, Ethics)
            - Smart search and filtering
            - Export capabilities
            """)
            
            if relevant_contexts:
                st.markdown("**📋 Relevant to this document:**")
                for context in relevant_contexts[:3]:
                    help_text = self.get_help_content(context, 'basic')
                    st.markdown(f"• {help_text}")
    
    def _render_contextual_help(self, relevant_contexts: List[str]):
        """Render help relevant to current document context"""
        st.markdown("**Context-aware guidance for this document:**")
        
        for context in relevant_contexts:
            help_content = self.get_help_content(context, 'detailed')
            with st.expander(f"📖 {context.replace('_', ' ').title()}", expanded=False):
                st.markdown(help_content)
    
    def _show_detailed_help(self, help_key: str):
        """Show detailed help in a modal or expander"""
        st.session_state[f"show_detailed_{help_key}"] = True
        self._track_help_interaction(help_key, 'detailed_requested')
    
    def _dismiss_help(self, help_key: str):
        """Dismiss help and remember user preference"""
        prefs = st.session_state.user_help_preferences
        prefs['dismissed_helps'].add(help_key)
        self._track_help_interaction(help_key, 'dismissed')
        st.rerun()
    
    def _track_help_interaction(self, help_key: str, action: str):
        """Track user interactions with help system"""
        interactions = st.session_state.help_interactions
        if help_key not in interactions:
            interactions[help_key] = []
        
        interactions[help_key].append({
            'action': action,
            'timestamp': datetime.now().isoformat()
        })
        
        # Mark as shown
        if action in ['tooltip_shown', 'bubble_shown']:
            st.session_state.user_help_preferences['shown_helps'].add(help_key)
    
    def render_help_settings(self):
        """Render help system preferences"""
        with st.expander("⚙️ Help Settings", expanded=False):
            prefs = st.session_state.user_help_preferences
            
            col1, col2 = st.columns(2)
            
            with col1:
                detail_level = st.selectbox(
                    "Help Detail Level",
                    ['basic', 'medium', 'detailed'],
                    index=['basic', 'medium', 'detailed'].index(prefs['detail_level'])
                )
                prefs['detail_level'] = detail_level
            
            with col2:
                if st.button("Reset Help History"):
                    prefs['shown_helps'] = set()
                    prefs['dismissed_helps'] = set()
                    st.session_state.help_interactions = {}
                    st.success("Help history reset!")
                    st.rerun()
            
            # Show help statistics
            st.markdown("**📊 Your Help Usage:**")
            interactions = st.session_state.help_interactions
            if interactions:
                total_interactions = sum(len(events) for events in interactions.values())
                st.write(f"Total help interactions: {total_interactions}")
                st.write(f"Help topics accessed: {len(interactions)}")
                st.write(f"Current user stage: {self.detect_user_stage().title()}")
            else:
                st.write("No help interactions yet")

# Global instance
smart_help = SmartHelpBubbles()