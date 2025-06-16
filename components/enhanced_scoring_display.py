"""
Enhanced Scoring Display Component for GUARDIAN
Provides visual indicators, color-coded buttons, and detailed analysis popups for risk scores
"""

import streamlit as st
from typing import Dict, Any, Tuple

class EnhancedScoringDisplay:
    """Enhanced visual scoring system with color-coded indicators and analysis popups"""
    
    def __init__(self):
        self.score_colors = {
            'excellent': {'bg': '#28a745', 'border': '#28a745', 'text': '#ffffff', 'icon': '🟢'},  # Green
            'warning': {'bg': '#fd7e14', 'border': '#fd7e14', 'text': '#ffffff', 'icon': '🟠'},    # Orange  
            'danger': {'bg': '#dc3545', 'border': '#dc3545', 'text': '#ffffff', 'icon': '🔴'},     # Red
            'na': {'bg': '#6c757d', 'border': '#6c757d', 'text': '#ffffff', 'icon': '❓'}          # Gray
        }
    
    def get_score_category(self, score: Any, framework_type: str = 'standard') -> str:
        """Determine score category based on value and framework type"""
        if score == 'N/A' or score is None:
            return 'na'
        
        # Handle tier-based scoring (Tier 1, Tier 2, etc.)
        if isinstance(score, str) and 'tier' in score.lower():
            try:
                tier_num = int(''.join(filter(str.isdigit, score)))
                if tier_num >= 4:
                    return 'excellent'  # Green for Tier 4 or 5
                elif tier_num == 3:
                    return 'warning'    # Orange for Tier 3
                else:
                    return 'danger'     # Red for Tier 1 or 2
            except (ValueError, TypeError):
                return 'na'
        
        try:
            score_val = float(score)
        except (ValueError, TypeError):
            return 'na'
        
        # For 100-point scale scoring
        if score_val >= 75:
            return 'excellent'  # Green for 75-100
        elif score_val >= 50:
            return 'warning'    # Orange for 50-74
        else:
            return 'danger'     # Red for below 50
    
    def render_enhanced_score_button(self, score: Any, label: str, framework_type: str, 
                                   unique_id: str, help_text: str, on_click_data: Dict[str, Any]) -> bool:
        """Render an enhanced score button with visual indicators"""
        category = self.get_score_category(score, framework_type)
        colors = self.score_colors[category]
        
        # Format display value based on framework type
        if framework_type == 'quantum_cybersecurity':
            display_value = f"Tier {score}/5" if score != 'N/A' else "N/A"
        else:
            display_value = f"{score}/100" if score != 'N/A' else "N/A"
        
        # Add ultra-compact CSS styling to eliminate all spacing
        button_css = f"""
        <style>
        .stButton > button,
        button[kind="secondary"],
        button[kind="primary"],
        [data-testid*="button"] {{
            height: 22px !important;
            padding: 1px 4px !important;
            font-size: 8px !important;
            font-family: inherit !important;
            line-height: 1.0 !important;
            margin: 0px !important;
            border-radius: 0px !important;
            font-weight: 500 !important;
            min-height: 22px !important;
            background: {colors['bg']} !important;
            border: 1px solid {colors['border']} !important;
            color: {colors['text']} !important;
            width: 100% !important;
        }}
        .stButton > button:hover,
        button[kind="secondary"]:hover,
        button[kind="primary"]:hover,
        [data-testid*="button"]:hover {{
            background: {colors['border']}30 !important;
            transform: none !important;
            box-shadow: none !important;
        }}
        .stButton {{
            margin: 0px !important;
            padding: 0px !important;
        }}
        div[data-testid="column"] {{
            padding: 0px !important;
            margin: 0px !important;
            gap: 0px !important;
        }}
        div[data-testid="stVerticalBlock"] {{
            gap: 0px !important;
            margin: 0px !important;
            padding: 0px !important;
        }}
        .element-container {{
            margin: 0px !important;
            padding: 0px !important;
        }}
        [data-testid="stVerticalBlock"] > div {{
            margin: 0px !important;
            padding: 0px !important;
        }}
        </style>
        """
        st.markdown(button_css, unsafe_allow_html=True)
        
        # Generate unique CSS ID for this specific button
        button_id = f"btn_{framework_type}_{unique_id}_{hash(label)}"
        
        # Add button-specific CSS styling
        st.markdown(f"""
        <style>
        #{button_id} {{
            background-color: {colors['bg']} !important;
            color: {colors['text']} !important;
            border: 1px solid {colors['border']} !important;
            background-image: none !important;
        }}
        </style>
        """, unsafe_allow_html=True)
        
        # Create HTML div with button styling that matches Streamlit buttons
        button_html = f"""
        <div class="stButton" style="width: 100%; margin: 0px; padding: 0px;">
            <button id="{button_id}" 
                    style="
                        background-color: {colors['bg']} !important;
                        color: {colors['text']} !important;
                        border: 1px solid {colors['border']} !important;
                        background-image: none !important;
                        height: 18px !important;
                        padding: 2px 4px !important;
                        font-size: 8px !important;
                        font-weight: bold !important;
                        font-family: inherit !important;
                        line-height: 1.0 !important;
                        margin: 0px !important;
                        border-radius: 0px !important;
                        width: 100% !important;
                        cursor: pointer;
                        transition: opacity 0.2s ease;
                    " 
                    onclick="
                        // Trigger the hidden Streamlit button
                        const hiddenBtn = document.querySelector('button[data-testid*=\\'{framework_type}_{unique_id}\\']');
                        if (hiddenBtn) hiddenBtn.click();
                        // Store click state
                        window.streamlitButtonClicked = '{framework_type}_{unique_id}';
                    "
                    onmouseover="this.style.opacity='0.8'" 
                    onmouseout="this.style.opacity='1'"
                    title="{help_text}">
                {colors['icon']} {label}: {display_value}
            </button>
        </div>
        """
        
        st.markdown(button_html, unsafe_allow_html=True)
        
        # Hidden Streamlit button for state management
        if st.button("", key=f"{framework_type}_{unique_id}", help="", type="secondary"):
            button_clicked = True
        else:
            button_clicked = False
            
        # Check for JavaScript click trigger
        if 'streamlitButtonClicked' in st.session_state and st.session_state.get('streamlitButtonClicked') == f"{framework_type}_{unique_id}":
            button_clicked = True
            del st.session_state['streamlitButtonClicked']
        
        # Hide the Streamlit button completely
        st.markdown(f"""
        <style>
        button[data-testid*="{framework_type}_{unique_id}"] {{
            display: none !important;
            visibility: hidden !important;
            position: absolute !important;
            left: -9999px !important;
        }}
        </style>
        """, unsafe_allow_html=True)
        
        if button_clicked:
            # Store data for modal popup
            st.session_state[f"modal_doc_data_{unique_id}"] = on_click_data
            st.session_state[f"show_analysis_{unique_id}"] = framework_type
            return True
        
        return False
    
    def render_score_grid(self, scores: Dict[str, Any], document_data: Dict[str, Any], 
                         unique_id: str, help_tooltips=None) -> None:
        """Render a complete grid of enhanced score buttons"""
        
        # Create two-column layout for scores
        col1, col2 = st.columns(2)
        
        with col1:
            # AI Cybersecurity Score
            clicked = self.render_enhanced_score_button(
                score=scores.get('ai_cybersecurity', 'N/A'),
                label="AI Cyber",
                framework_type="ai_cybersecurity",
                unique_id=unique_id,
                help_text="AI Cybersecurity Framework Assessment - Click for detailed analysis",
                on_click_data=document_data
            )
            if clicked:
                st.rerun()
            
            # AI Ethics Score
            clicked = self.render_enhanced_score_button(
                score=scores.get('ai_ethics', 'N/A'),
                label="AI Ethics",
                framework_type="ai_ethics",
                unique_id=unique_id,
                help_text="AI Ethics Evaluation Framework - Click for detailed analysis",
                on_click_data=document_data
            )
            if clicked:
                st.rerun()
        
        with col2:
            # Quantum Cybersecurity Score
            clicked = self.render_enhanced_score_button(
                score=scores.get('quantum_cybersecurity', 'N/A'),
                label="Q Cyber",
                framework_type="quantum_cybersecurity",
                unique_id=unique_id,
                help_text="Quantum Cybersecurity Maturity Assessment - Click for detailed analysis",
                on_click_data=document_data
            )
            if clicked:
                st.rerun()
            
            # Quantum Ethics Score
            clicked = self.render_enhanced_score_button(
                score=scores.get('quantum_ethics', 'N/A'),
                label="Q Ethics",
                framework_type="quantum_ethics",
                unique_id=unique_id,
                help_text="Quantum Ethics Framework Assessment - Click for detailed analysis",
                on_click_data=document_data
            )
            if clicked:
                st.rerun()
    
    def render_analysis_popup(self, unique_id: str) -> None:
        """Render detailed analysis popup when score button is clicked"""
        
        # Check if modal should be shown
        if f"show_analysis_{unique_id}" in st.session_state:
            analysis_type = st.session_state[f"show_analysis_{unique_id}"]
            doc_data = st.session_state.get(f"modal_doc_data_{unique_id}", {})
            
            if doc_data:
                self._render_detailed_analysis_modal(analysis_type, doc_data, unique_id)
    
    def _render_detailed_analysis_modal(self, analysis_type: str, doc_data: Dict[str, Any], 
                                      unique_id: str) -> None:
        """Render the detailed analysis modal content"""
        
        title = doc_data.get('title', 'Unknown Document')
        scores = doc_data.get('scores', {})
        content = doc_data.get('content', '')
        
        # Create modal-style container
        with st.container():
            st.markdown("---")
            st.markdown(f"### 🔍 {self._get_framework_title(analysis_type)} Analysis")
            st.markdown(f"**Document:** {title}")
            
            # Display score with visual indicator
            score = scores.get(analysis_type, 'N/A')
            category = self.get_score_category(score, analysis_type)
            colors = self.score_colors[category]
            
            st.markdown(f"""
                <div style="
                    background: {colors['bg']};
                    border: 2px solid {colors['border']};
                    border-radius: 8px;
                    padding: 12px;
                    margin: 8px 0;
                    text-align: center;
                ">
                    <span style="color: {colors['text']}; font-size: 18px; font-weight: 600;">
                        {colors['icon']} Score: {score if analysis_type != 'quantum_cybersecurity' else f'Tier {score}/5' if score != 'N/A' else 'N/A'}
                    </span>
                </div>
            """, unsafe_allow_html=True)
            
            # Provide framework-specific analysis
            self._render_framework_analysis(analysis_type, score, content)
            
            # Close button
            if st.button("Close Analysis", key=f"close_{unique_id}"):
                if f"show_analysis_{unique_id}" in st.session_state:
                    del st.session_state[f"show_analysis_{unique_id}"]
                if f"modal_doc_data_{unique_id}" in st.session_state:
                    del st.session_state[f"modal_doc_data_{unique_id}"]
                st.rerun()
    
    def _get_framework_title(self, analysis_type: str) -> str:
        """Get human-readable framework title"""
        titles = {
            'ai_cybersecurity': 'AI Cybersecurity Framework',
            'ai_ethics': 'AI Ethics Framework',
            'quantum_cybersecurity': 'Quantum Cybersecurity Maturity',
            'quantum_ethics': 'Quantum Ethics Framework'
        }
        return titles.get(analysis_type, 'Framework Analysis')
    
    def _render_framework_analysis(self, framework_type: str, score: Any, content: str) -> None:
        """Render detailed framework-specific analysis"""
        
        if framework_type == 'ai_cybersecurity':
            self._render_ai_cybersecurity_analysis(score, content)
        elif framework_type == 'ai_ethics':
            self._render_ai_ethics_analysis(score, content)
        elif framework_type == 'quantum_cybersecurity':
            self._render_quantum_cybersecurity_analysis(score, content)
        elif framework_type == 'quantum_ethics':
            self._render_quantum_ethics_analysis(score, content)
    
    def _render_ai_cybersecurity_analysis(self, score: Any, content: str) -> None:
        """Render AI cybersecurity specific analysis"""
        st.markdown("#### 🔒 AI Cybersecurity Assessment")
        
        if score == 'N/A':
            st.info("This document does not sufficiently contain AI content to be evaluated under the AI cybersecurity framework.")
            return
        
        try:
            score_val = float(score)
        except (ValueError, TypeError):
            st.warning("Unable to parse score value for detailed analysis.")
            return
        
        # Score interpretation
        if score_val >= 85:
            st.success("**Excellent AI Cybersecurity Posture**")
            st.markdown("- Comprehensive threat modeling and risk assessment")
            st.markdown("- Advanced adversarial robustness measures")
            st.markdown("- Strong data governance and privacy protection")
            st.markdown("- Robust model security and monitoring")
        elif score_val >= 70:
            st.warning("**Good AI Cybersecurity Foundation**")
            st.markdown("- Basic security frameworks in place")
            st.markdown("- Some adversarial protection measures")
            st.markdown("- Areas for improvement in threat detection")
            st.markdown("- Consider enhanced monitoring capabilities")
        elif score_val >= 50:
            st.warning("**Moderate AI Security Concerns**")
            st.markdown("- Limited security framework coverage")
            st.markdown("- Vulnerability to adversarial attacks")
            st.markdown("- Insufficient data protection measures")
            st.markdown("- Requires significant security enhancements")
        else:
            st.error("**Critical AI Security Gaps**")
            st.markdown("- Minimal security framework implementation")
            st.markdown("- High vulnerability to cyber threats")
            st.markdown("- Urgent need for comprehensive security overhaul")
            st.markdown("- Immediate action required for risk mitigation")
        
        # Key findings from content analysis
        st.markdown("#### 📊 Key Security Elements Identified")
        
        security_terms = ['encryption', 'authentication', 'authorization', 'monitoring', 'threat detection', 
                         'adversarial', 'privacy', 'data protection', 'security framework']
        found_terms = [term for term in security_terms if term.lower() in content.lower()]
        
        if found_terms:
            st.markdown("**Security concepts mentioned:**")
            for term in found_terms[:5]:  # Show top 5
                st.markdown(f"- {term.title()}")
        else:
            st.info("Limited security terminology found in document content.")
    
    def _render_ai_ethics_analysis(self, score: Any, content: str) -> None:
        """Render AI ethics specific analysis"""
        st.markdown("#### 🧠 AI Ethics Assessment")
        
        if score == 'N/A':
            st.info("This document does not sufficiently contain AI content to be evaluated under the AI ethics framework.")
            return
        
        try:
            score_val = float(score)
        except (ValueError, TypeError):
            st.warning("Unable to parse score value for detailed analysis.")
            return
        
        # Score interpretation
        if score_val >= 85:
            st.success("**Excellent Ethical AI Implementation**")
            st.markdown("- Comprehensive bias detection and mitigation")
            st.markdown("- Strong algorithmic accountability measures")
            st.markdown("- Transparent decision-making processes")
            st.markdown("- Robust fairness and equity frameworks")
        elif score_val >= 70:
            st.warning("**Good Ethical Foundation**")
            st.markdown("- Basic fairness considerations addressed")
            st.markdown("- Some bias mitigation measures in place")
            st.markdown("- Opportunities for enhanced transparency")
            st.markdown("- Consider strengthening accountability mechanisms")
        elif score_val >= 50:
            st.warning("**Moderate Ethical Concerns**")
            st.markdown("- Limited bias detection capabilities")
            st.markdown("- Insufficient transparency measures")
            st.markdown("- Weak accountability frameworks")
            st.markdown("- Requires significant ethical enhancements")
        else:
            st.error("**Critical Ethical Gaps**")
            st.markdown("- Minimal ethical framework implementation")
            st.markdown("- High risk of biased or unfair outcomes")
            st.markdown("- Lack of transparency and accountability")
            st.markdown("- Urgent ethical framework development needed")
        
        # Key ethical concepts identified
        st.markdown("#### ⚖️ Ethical Principles Identified")
        
        ethics_terms = ['fairness', 'bias', 'transparency', 'accountability', 'privacy', 
                       'equity', 'inclusion', 'explainability', 'human oversight']
        found_terms = [term for term in ethics_terms if term.lower() in content.lower()]
        
        if found_terms:
            st.markdown("**Ethical concepts mentioned:**")
            for term in found_terms[:5]:
                st.markdown(f"- {term.title()}")
        else:
            st.info("Limited ethical terminology found in document content.")
    
    def _render_quantum_cybersecurity_analysis(self, score: Any, content: str) -> None:
        """Render quantum cybersecurity specific analysis"""
        st.markdown("#### ⚡ Quantum Cybersecurity Maturity")
        
        if score == 'N/A':
            st.info("This document does not sufficiently contain quantum content to be evaluated under the quantum cybersecurity framework.")
            return
        
        try:
            score_val = float(score)
        except (ValueError, TypeError):
            st.warning("Unable to parse score value for detailed analysis.")
            return
        
        # Tier-based interpretation
        if score_val >= 4:
            st.success("**Tier 4-5: Advanced Quantum Security**")
            st.markdown("- Comprehensive post-quantum cryptography implementation")
            st.markdown("- Advanced quantum key distribution capabilities")
            st.markdown("- Dynamic quantum threat response systems")
            st.markdown("- Continuous quantum security adaptation")
        elif score_val >= 3:
            st.warning("**Tier 3: Developing Quantum Security**")
            st.markdown("- Scalable quantum-safe solutions in progress")
            st.markdown("- Active post-quantum cryptography deployment")
            st.markdown("- Growing quantum threat awareness")
            st.markdown("- Consider accelerating quantum security measures")
        elif score_val >= 2:
            st.warning("**Tier 2: Basic Quantum Preparation**")
            st.markdown("- Foundational quantum security planning")
            st.markdown("- Limited post-quantum cryptography adoption")
            st.markdown("- Initial quantum threat assessment")
            st.markdown("- Significant quantum security development needed")
        else:
            st.error("**Tier 1: Minimal Quantum Readiness**")
            st.markdown("- Basic quantum threat awareness only")
            st.markdown("- No substantial quantum security measures")
            st.markdown("- Vulnerable to quantum computing attacks")
            st.markdown("- Urgent quantum security strategy required")
        
        # Quantum security concepts
        st.markdown("#### 🔐 Quantum Security Elements")
        
        quantum_terms = ['post-quantum', 'quantum cryptography', 'quantum key distribution', 
                        'quantum-safe', 'lattice-based', 'quantum resistant', 'qkd']
        found_terms = [term for term in quantum_terms if term.lower() in content.lower()]
        
        if found_terms:
            st.markdown("**Quantum security concepts mentioned:**")
            for term in found_terms[:5]:
                st.markdown(f"- {term.title()}")
        else:
            st.info("Limited quantum security terminology found in document content.")
    
    def _render_quantum_ethics_analysis(self, score: Any, content: str) -> None:
        """Render quantum ethics specific analysis"""
        st.markdown("#### 🌐 Quantum Ethics Assessment")
        
        if score == 'N/A':
            st.info("This document does not sufficiently contain quantum content to be evaluated under the quantum ethics framework.")
            return
        
        try:
            score_val = float(score)
        except (ValueError, TypeError):
            st.warning("Unable to parse score value for detailed analysis.")
            return
        
        # Score interpretation
        if score_val >= 85:
            st.success("**Excellent Quantum Ethics Framework**")
            st.markdown("- Comprehensive quantum technology ethics")
            st.markdown("- Strong equitable access considerations")
            st.markdown("- Robust quantum research ethics protocols")
            st.markdown("- Thoughtful societal impact assessment")
        elif score_val >= 70:
            st.warning("**Good Quantum Ethics Foundation**")
            st.markdown("- Basic quantum ethics considerations")
            st.markdown("- Some access equity measures in place")
            st.markdown("- Opportunities for enhanced ethical frameworks")
            st.markdown("- Consider expanding societal impact analysis")
        elif score_val >= 50:
            st.warning("**Moderate Quantum Ethics Concerns**")
            st.markdown("- Limited quantum ethics framework")
            st.markdown("- Insufficient access equity measures")
            st.markdown("- Weak societal impact consideration")
            st.markdown("- Requires enhanced quantum ethics development")
        else:
            st.error("**Critical Quantum Ethics Gaps**")
            st.markdown("- Minimal quantum ethics consideration")
            st.markdown("- Risk of inequitable quantum technology access")
            st.markdown("- Lack of societal impact assessment")
            st.markdown("- Urgent quantum ethics framework needed")
        
        # Quantum ethics concepts
        st.markdown("#### 🤝 Quantum Ethics Principles")
        
        quantum_ethics_terms = ['quantum ethics', 'quantum equity', 'quantum access', 
                               'quantum responsibility', 'quantum governance', 'quantum society']
        found_terms = [term for term in quantum_ethics_terms if term.lower() in content.lower()]
        
        if found_terms:
            st.markdown("**Quantum ethics concepts mentioned:**")
            for term in found_terms[:5]:
                st.markdown(f"- {term.title()}")
        else:
            st.info("Limited quantum ethics terminology found in document content.")