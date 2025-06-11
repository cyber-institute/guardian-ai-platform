"""
Streamlit-Compatible Tooltip System for GUARDIAN Onboarding
Uses Streamlit components for better integration
"""

import streamlit as st
from typing import Dict, List, Optional

class StreamlitTooltipSystem:
    """Streamlit-native tooltip system for user onboarding."""
    
    def __init__(self):
        self.initialize_session_state()
        
    def initialize_session_state(self):
        """Initialize session state variables for onboarding."""
        if "guardian_tour_active" not in st.session_state:
            st.session_state.guardian_tour_active = False
        if "guardian_tour_step" not in st.session_state:
            st.session_state.guardian_tour_step = 1
        if "guardian_welcome_shown" not in st.session_state:
            st.session_state.guardian_welcome_shown = False
        if "guardian_tour_completed" not in st.session_state:
            st.session_state.guardian_tour_completed = False
    
    def render_welcome_banner(self):
        """Render welcome banner for new users."""
        if not st.session_state.guardian_welcome_shown and not st.session_state.guardian_tour_completed:
            with st.container():
                st.info("🛡️ **Welcome to GUARDIAN!** AI-powered governance platform for emerging technology risk assessment. Would you like a guided tour?")
                
                col1, col2, col3, col4 = st.columns([1, 1, 1, 3])
                
                with col1:
                    if st.button("Start Tour", type="primary", key="start_tour_btn"):
                        st.session_state.guardian_tour_active = True
                        st.session_state.guardian_tour_step = 1
                        st.session_state.guardian_welcome_shown = True
                        st.rerun()
                
                with col2:
                    if st.button("Skip Tour", key="skip_tour_btn"):
                        st.session_state.guardian_welcome_shown = True
                        st.session_state.guardian_tour_completed = True
                        st.rerun()
                
                with col3:
                    if st.button("Learn More", key="learn_more_btn"):
                        st.session_state.guardian_welcome_shown = True
                        st.session_state.show_help_expanded = True
                        st.rerun()
    
    def render_tour_progress(self):
        """Render tour progress indicator."""
        if st.session_state.guardian_tour_active:
            progress = st.session_state.guardian_tour_step / 5
            st.sidebar.markdown(f"**Tour Progress: Step {st.session_state.guardian_tour_step}/5**")
            st.sidebar.progress(progress)
            
            if st.sidebar.button("End Tour Early", key="end_tour_btn"):
                st.session_state.guardian_tour_active = False
                st.session_state.guardian_tour_completed = True
                st.rerun()
    
    def render_step_guidance(self, step_key: str, step_number: int):
        """Render step-specific guidance."""
        if st.session_state.guardian_tour_active and st.session_state.guardian_tour_step == step_number:
            
            guidance_content = {
                "policy_repository": {
                    "title": "Policy Repository",
                    "content": "Browse analyzed policy documents with comprehensive scores across AI cybersecurity, quantum security, and ethics frameworks.",
                    "action": "Explore the documents below to see scoring details."
                },
                "policy_analyzer": {
                    "title": "Policy Analyzer", 
                    "content": "Upload draft policies to receive comprehensive gap analysis using GUARDIAN patent algorithms.",
                    "action": "Try uploading a policy document using the form above."
                },
                "ai_recommendations": {
                    "title": "AI Recommendations",
                    "content": "Discover intelligent document recommendations based on content similarity and scoring patterns.",
                    "action": "Explore the recommendation features below."
                },
                "repository_admin": {
                    "title": "Repository Admin",
                    "content": "Access administrative functions including system monitoring and patent scoring insights.",
                    "action": "Review the administrative tools and system status."
                }
            }
            
            if step_key in guidance_content:
                info = guidance_content[step_key]
                
                with st.expander(f"🎯 Tour Step {step_number}: {info['title']}", expanded=True):
                    st.write(info['content'])
                    st.info(f"**Try this:** {info['action']}")
                    
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        if step_number < 5 and st.button("Next Step", type="primary", key=f"next_step_{step_number}"):
                            st.session_state.guardian_tour_step += 1
                            st.rerun()
                    
                    with col2:
                        if step_number == 5 and st.button("Complete Tour", type="primary", key="complete_tour"):
                            st.session_state.guardian_tour_active = False
                            st.session_state.guardian_tour_completed = True
                            st.success("Welcome tour completed! You're ready to use GUARDIAN.")
                            st.balloons()
                            st.rerun()
    
    def render_navigation_hint(self, current_tab: str):
        """Render navigation hints."""
        if st.session_state.guardian_tour_active:
            hint_mapping = {
                1: ("policy_repository", "👈 Click 'Policy Repository' to see analyzed documents"),
                2: ("policy_analyzer", "👈 Try 'Policy Analyzer' to upload and analyze a policy"),
                3: ("ai_recommendations", "👈 Explore 'AI Recommendations' for intelligent suggestions"),
                4: ("repository_admin", "👈 Check 'Repository Admin' for system management")
            }
            
            step = st.session_state.guardian_tour_step
            if step in hint_mapping:
                target_tab, hint_text = hint_mapping[step]
                if current_tab != target_tab:
                    st.info(f"**Next Step:** {hint_text}")
    
    def render_contextual_help(self, help_key: str, title: str):
        """Render contextual help buttons."""
        help_content = {
            "scoring_framework": "GUARDIAN uses patent-based algorithms to score documents across four frameworks: AI Cybersecurity (0-100), Quantum Cybersecurity (1-5 tiers), AI Ethics (0-100), and Quantum Ethics (0-100).",
            "gap_analysis": "Gap analysis identifies policy weaknesses with severity levels (Critical, High, Medium, Low) and provides targeted recommendations for improvement using GUARDIAN patent algorithms.",
            "patent_algorithms": "GUARDIAN implements three patent-pending algorithms for dynamic governance, reinforcement learning, and adaptive risk assessment of emerging technologies.",
            "recommendation_engine": "AI-powered recommendations use semantic similarity, content analysis, and scoring patterns to suggest relevant documents and identify policy gaps."
        }
        
        if help_key in help_content:
            with st.expander(f"ℹ️ {title}", expanded=False):
                st.write(help_content[help_key])
    
    def render_feature_overview(self):
        """Render feature overview for new users."""
        if st.session_state.get("show_help_expanded", False):
            with st.expander("🚀 GUARDIAN Key Features", expanded=True):
                st.markdown("""
                **Comprehensive AI Governance Platform:**
                
                **🔍 Policy Analysis**: Upload documents for gap analysis using patent algorithms
                
                **🤖 AI Recommendations**: Intelligent document suggestions based on content similarity
                
                **📊 Multi-Framework Scoring**: Assessment across AI cybersecurity, quantum security, and ethics
                
                **⚡ Real-time Risk Assessment**: Dynamic scoring with Bayesian updates
                
                **🛡️ Compliance Checking**: Automated assessment against major frameworks (NIST, EU AI Act)
                
                **📈 Strategic Insights**: Learning-based recommendations for policy improvement
                """)
                
                if st.button("Start Guided Tour", type="primary", key="start_tour_from_features"):
                    st.session_state.guardian_tour_active = True
                    st.session_state.guardian_tour_step = 1
                    st.session_state.show_help_expanded = False
                    st.rerun()
    
    def render_quick_help_sidebar(self):
        """Render quick help in sidebar."""
        with st.sidebar:
            st.markdown("### Quick Help")
            
            if st.button("🎯 Restart Tour", key="restart_tour_sidebar"):
                st.session_state.guardian_tour_active = True
                st.session_state.guardian_tour_step = 1
                st.rerun()
            
            with st.expander("Scoring Guide", expanded=False):
                st.markdown("""
                **AI Cybersecurity**: 0-100 points
                **Quantum Security**: 1-5 tiers (QCMEA)
                **AI Ethics**: 0-100 points  
                **Quantum Ethics**: 0-100 points
                """)
            
            with st.expander("Gap Analysis", expanded=False):
                st.markdown("""
                **Critical**: Immediate attention required
                **High**: Address within 30 days
                **Medium**: Address within 90 days
                **Low**: Monitor and improve
                """)
    
    def is_tour_active(self) -> bool:
        """Check if tour is currently active."""
        return st.session_state.guardian_tour_active
    
    def get_current_step(self) -> int:
        """Get current tour step."""
        return st.session_state.guardian_tour_step

# Global instance
streamlit_tooltips = StreamlitTooltipSystem()