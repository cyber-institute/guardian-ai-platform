"""
Intuitive User Journey Onboarding Tooltip System for GUARDIAN
Provides guided tour and contextual help for new users
"""

import streamlit as st
from typing import Dict, List, Optional
import json

class OnboardingTooltipSystem:
    """Manages onboarding tooltips and user journey guidance for GUARDIAN."""
    
    def __init__(self):
        self.tooltip_definitions = self._initialize_tooltips()
        self.user_progress_key = "guardian_onboarding_progress"
        self.tour_active_key = "guardian_tour_active"
        
    def _initialize_tooltips(self) -> Dict[str, Dict]:
        """Initialize tooltip definitions for different features."""
        return {
            "welcome": {
                "title": "Welcome to GUARDIAN",
                "content": "GUARDIAN provides AI-powered governance and risk assessment for emerging technologies. Let's take a quick tour!",
                "position": "center",
                "step": 1,
                "next_step": "policy_repository"
            },
            
            "policy_repository": {
                "title": "Policy Repository",
                "content": "Browse and search through analyzed policy documents. Each document has comprehensive scores across AI cybersecurity, quantum security, and ethics frameworks.",
                "position": "top",
                "step": 2,
                "next_step": "policy_analyzer"
            },
            
            "policy_analyzer": {
                "title": "Policy Analyzer",
                "content": "Upload draft policies to receive comprehensive gap analysis using GUARDIAN patent algorithms. Get strategic recommendations and compliance assessments.",
                "position": "top",
                "step": 3,
                "next_step": "ai_recommendations"
            },
            
            "ai_recommendations": {
                "title": "AI Recommendations",
                "content": "Discover intelligent document recommendations based on content similarity, scoring patterns, and contextual analysis.",
                "position": "top",
                "step": 4,
                "next_step": "repository_admin"
            },
            
            "repository_admin": {
                "title": "Repository Admin",
                "content": "Access administrative functions including system monitoring, patent scoring insights, and database management.",
                "position": "top",
                "step": 5,
                "next_step": "complete"
            },
            
            "scoring_framework": {
                "title": "Scoring Framework",
                "content": "GUARDIAN uses patent-based algorithms to score documents across four frameworks: AI Cybersecurity (0-100), Quantum Cybersecurity (1-5 tiers), AI Ethics (0-100), and Quantum Ethics (0-100).",
                "position": "right",
                "step": "contextual"
            },
            
            "gap_analysis": {
                "title": "Gap Analysis",
                "content": "Identify policy gaps with severity levels (Critical, High, Medium, Low) and receive targeted recommendations for improvement.",
                "position": "left",
                "step": "contextual"
            },
            
            "patent_algorithms": {
                "title": "Patent Algorithms",
                "content": "GUARDIAN implements three patent-pending algorithms for dynamic governance, reinforcement learning, and adaptive risk assessment.",
                "position": "bottom",
                "step": "contextual"
            }
        }
    
    def is_tour_active(self) -> bool:
        """Check if onboarding tour is currently active."""
        return st.session_state.get(self.tour_active_key, False)
    
    def start_tour(self):
        """Start the onboarding tour."""
        st.session_state[self.tour_active_key] = True
        st.session_state[self.user_progress_key] = {
            "current_step": 1,
            "completed_steps": [],
            "tour_started": True
        }
    
    def end_tour(self):
        """End the onboarding tour."""
        st.session_state[self.tour_active_key] = False
        progress = st.session_state.get(self.user_progress_key, {})
        progress["tour_completed"] = True
        st.session_state[self.user_progress_key] = progress
    
    def get_current_step(self) -> int:
        """Get the current tour step."""
        progress = st.session_state.get(self.user_progress_key, {})
        return progress.get("current_step", 1)
    
    def advance_step(self):
        """Advance to the next tour step."""
        progress = st.session_state.get(self.user_progress_key, {})
        current_step = progress.get("current_step", 1)
        progress["current_step"] = current_step + 1
        progress["completed_steps"] = progress.get("completed_steps", []) + [current_step]
        st.session_state[self.user_progress_key] = progress
    
    def render_welcome_modal(self):
        """Render the welcome modal for new users."""
        if not st.session_state.get("guardian_welcome_shown", False):
            with st.container():
                st.markdown("""
                <div style="
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background-color: rgba(0, 0, 0, 0.5);
                    z-index: 1000;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                ">
                    <div style="
                        background: white;
                        padding: 2rem;
                        border-radius: 8px;
                        max-width: 500px;
                        text-align: center;
                        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
                    ">
                        <h2>🛡️ Welcome to GUARDIAN</h2>
                        <p>AI-powered governance platform for emerging technology risk assessment</p>
                        <p>Would you like a guided tour of the features?</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col1:
                    if st.button("Start Tour", type="primary"):
                        self.start_tour()
                        st.session_state["guardian_welcome_shown"] = True
                        st.rerun()
                
                with col2:
                    if st.button("Skip Tour"):
                        st.session_state["guardian_welcome_shown"] = True
                        st.rerun()
                
                with col3:
                    if st.button("Learn More"):
                        st.session_state["guardian_welcome_shown"] = True
                        st.session_state["show_help"] = True
                        st.rerun()
    
    def render_step_tooltip(self, step_key: str, target_element_id: Optional[str] = None):
        """Render a tooltip for a specific step."""
        if not self.is_tour_active():
            return
        
        tooltip = self.tooltip_definitions.get(step_key)
        if not tooltip:
            return
        
        current_step = self.get_current_step()
        if tooltip.get("step") != current_step and tooltip.get("step") != "contextual":
            return
        
        # Render tooltip with arrow and positioning
        st.markdown(f"""
        <div class="onboarding-tooltip" style="
            position: relative;
            background: #1f77b4;
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            animation: fadeIn 0.3s ease-in-out;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <strong>{tooltip['title']}</strong>
                <span style="background: rgba(255,255,255,0.2); padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.8rem;">
                    Step {current_step}/5
                </span>
            </div>
            <p style="margin: 0; line-height: 1.4;">{tooltip['content']}</p>
            <div style="margin-top: 1rem; display: flex; justify-content: space-between;">
                <button onclick="window.location.reload()" style="
                    background: rgba(255,255,255,0.2);
                    border: none;
                    color: white;
                    padding: 0.5rem 1rem;
                    border-radius: 4px;
                    cursor: pointer;
                ">Skip Tour</button>
                <button onclick="window.location.reload()" style="
                    background: white;
                    border: none;
                    color: #1f77b4;
                    padding: 0.5rem 1rem;
                    border-radius: 4px;
                    cursor: pointer;
                    font-weight: bold;
                ">Next</button>
            </div>
        </div>
        
        <style>
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(-10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        </style>
        """, unsafe_allow_html=True)
    
    def render_contextual_help(self, help_key: str, trigger_text: str = "?"):
        """Render contextual help tooltip."""
        tooltip = self.tooltip_definitions.get(help_key)
        if not tooltip:
            return
        
        help_col1, help_col2 = st.columns([10, 1])
        
        with help_col2:
            if st.button(trigger_text, key=f"help_{help_key}", help="Click for help"):
                st.session_state[f"show_help_{help_key}"] = not st.session_state.get(f"show_help_{help_key}", False)
        
        if st.session_state.get(f"show_help_{help_key}", False):
            st.info(f"**{tooltip['title']}**: {tooltip['content']}")
    
    def render_progress_indicator(self):
        """Render tour progress indicator."""
        if not self.is_tour_active():
            return
        
        current_step = self.get_current_step()
        total_steps = 5
        
        progress = current_step / total_steps
        
        st.markdown(f"""
        <div style="
            position: fixed;
            top: 10px;
            right: 10px;
            background: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            z-index: 999;
            border: 1px solid #e0e0e0;
        ">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 0.8rem; color: #666;">Tour Progress</span>
                <div style="
                    width: 100px;
                    height: 6px;
                    background: #e0e0e0;
                    border-radius: 3px;
                    overflow: hidden;
                ">
                    <div style="
                        width: {progress * 100}%;
                        height: 100%;
                        background: #1f77b4;
                        transition: width 0.3s ease;
                    "></div>
                </div>
                <span style="font-size: 0.8rem; color: #666;">{current_step}/{total_steps}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def render_navigation_hints(self, current_tab: str):
        """Render navigation hints based on current tab."""
        if not self.is_tour_active():
            return
        
        current_step = self.get_current_step()
        
        hint_mapping = {
            1: ("policy_repository", "Click on 'Policy Repository' to see analyzed documents"),
            2: ("policy_analyzer", "Try 'Policy Analyzer' to upload and analyze a policy"),
            3: ("ai_recommendations", "Explore 'AI Recommendations' for intelligent suggestions"),
            4: ("repository_admin", "Check 'Repository Admin' for system management"),
        }
        
        if current_step in hint_mapping:
            target_tab, hint_text = hint_mapping[current_step]
            if current_tab != target_tab:
                st.info(f"💡 **Next**: {hint_text}")
    
    def render_feature_highlights(self):
        """Render feature highlights for new users."""
        with st.expander("🚀 Key Features", expanded=False):
            st.markdown("""
            **GUARDIAN provides comprehensive AI governance capabilities:**
            
            🔍 **Policy Analysis**: Upload documents for gap analysis using patent algorithms
            
            🤖 **AI Recommendations**: Intelligent document suggestions based on content similarity
            
            📊 **Multi-Framework Scoring**: Assessment across AI cybersecurity, quantum security, and ethics
            
            ⚡ **Real-time Risk Assessment**: Dynamic scoring with Bayesian updates
            
            🛡️ **Compliance Checking**: Automated assessment against major frameworks (NIST, EU AI Act)
            
            📈 **Strategic Insights**: Learning-based recommendations for policy improvement
            """)
    
    def check_user_needs_onboarding(self) -> bool:
        """Check if user needs onboarding based on usage patterns."""
        # Check if this is a new user
        progress = st.session_state.get(self.user_progress_key, {})
        welcome_shown = st.session_state.get("guardian_welcome_shown", False)
        
        return not welcome_shown and not progress.get("tour_completed", False)

# Global instance for use across the application
onboarding_system = OnboardingTooltipSystem()