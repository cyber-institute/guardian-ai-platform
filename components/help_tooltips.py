"""
Contextual Help Tooltips for GUARDIAN Risk Calculation Terms
Provides interactive help bubbles for complex cybersecurity and ethics terminology
"""

import streamlit as st

class HelpTooltips:
    """Centralized help tooltip system for GUARDIAN risk assessment terms"""
    
    def __init__(self):
        self.tooltip_definitions = {
            # AI Cybersecurity Terms
            'ai_cybersecurity_score': {
                'title': 'AI Cybersecurity Score',
                'definition': 'Comprehensive assessment of artificial intelligence security measures and threat resilience',
                'calculation': 'Based on NIST AI Risk Management Framework factors including adversarial robustness, model security, data protection, and threat detection capabilities',
                'range': '0-100 (Higher scores indicate better AI security posture)',
                'factors': ['Adversarial ML Protection', 'Model Validation', 'Data Security', 'AI Threat Detection', 'Incident Response']
            },
            'adversarial_robustness': {
                'title': 'Adversarial Robustness', 
                'definition': 'System resistance to malicious inputs designed to manipulate AI model behavior',
                'calculation': 'Measures protection against adversarial attacks, input validation strength, and model stability under attack conditions',
                'importance': 'Critical for preventing AI system manipulation and ensuring reliable decision-making',
                'examples': ['Input sanitization', 'Adversarial training', 'Model ensemble defenses']
            },
            'model_security': {
                'title': 'Model Security',
                'definition': 'Protection of AI/ML models from theft, tampering, and unauthorized access',
                'calculation': 'Evaluates model encryption, access controls, versioning security, and intellectual property protection',
                'importance': 'Prevents model theft and maintains competitive advantage while ensuring model integrity',
                'examples': ['Model encryption', 'Access control systems', 'Secure model deployment']
            },
            
            # Quantum Cybersecurity Terms
            'quantum_cybersecurity_score': {
                'title': 'Quantum Cybersecurity Score',
                'definition': 'Assessment of organizational readiness for quantum computing threats and post-quantum security',
                'calculation': 'Based on post-quantum cryptography adoption, quantum threat assessment, and cryptographic agility measures',
                'range': '0-100 (Higher scores indicate better quantum threat preparedness)',
                'factors': ['Post-Quantum Cryptography', 'Quantum Key Distribution', 'Cryptographic Agility', 'Quantum Threat Assessment']
            },
            'post_quantum_cryptography': {
                'title': 'Post-Quantum Cryptography',
                'definition': 'Cryptographic algorithms designed to resist attacks from quantum computers',
                'calculation': 'Measures adoption of quantum-resistant algorithms and migration planning from current cryptographic systems',
                'importance': 'Essential for maintaining data security when quantum computers become capable of breaking current encryption',
                'examples': ['Lattice-based cryptography', 'Hash-based signatures', 'NIST standardized algorithms']
            },
            'quantum_key_distribution': {
                'title': 'Quantum Key Distribution (QKD)',
                'definition': 'Quantum mechanical method for secure communication key exchange',
                'calculation': 'Evaluates implementation of quantum secure communication channels and key management systems',
                'importance': 'Provides theoretically unbreakable key exchange using quantum physics principles',
                'examples': ['BB84 protocol', 'Quantum entanglement', 'Photonic quantum networks']
            },
            'cryptographic_agility': {
                'title': 'Cryptographic Agility',
                'definition': 'Ability to rapidly transition between cryptographic algorithms and protocols',
                'calculation': 'Measures flexibility in cryptographic implementations and readiness for algorithm updates',
                'importance': 'Critical for responding to cryptographic vulnerabilities and quantum threats',
                'examples': ['Modular crypto systems', 'Algorithm abstraction layers', 'Automated key rotation']
            },
            
            # AI Ethics Terms
            'ai_ethics_score': {
                'title': 'AI Ethics Score',
                'definition': 'Comprehensive evaluation of ethical AI practices and responsible development principles',
                'calculation': 'Based on bias mitigation, transparency, accountability, privacy protection, and human oversight measures',
                'range': '0-100 (Higher scores indicate stronger ethical AI implementation)',
                'factors': ['Bias Mitigation', 'Transparency', 'Accountability', 'Privacy Protection', 'Human Oversight']
            },
            'bias_mitigation': {
                'title': 'Bias Mitigation',
                'definition': 'Systematic approaches to identify, measure, and reduce unfair bias in AI systems',
                'calculation': 'Evaluates bias testing procedures, fairness metrics implementation, and diverse dataset usage',
                'importance': 'Ensures AI systems treat all groups fairly and avoid discriminatory outcomes',
                'examples': ['Fairness audits', 'Diverse training data', 'Algorithmic impact assessments']
            },
            'transparency': {
                'title': 'AI Transparency',
                'definition': 'Clarity and understandability of AI system decisions and operational processes',
                'calculation': 'Measures explainability features, decision documentation, and stakeholder communication',
                'importance': 'Enables trust, accountability, and regulatory compliance in AI systems',
                'examples': ['Explainable AI (XAI)', 'Decision audit trails', 'Model interpretability tools']
            },
            'accountability': {
                'title': 'AI Accountability',
                'definition': 'Clear responsibility assignment and oversight mechanisms for AI system outcomes',
                'calculation': 'Evaluates governance structures, oversight processes, and responsibility frameworks',
                'importance': 'Ensures responsible parties can be identified and held accountable for AI decisions',
                'examples': ['Governance committees', 'Audit procedures', 'Impact assessments']
            },
            
            # Quantum Ethics Terms
            'quantum_ethics_score': {
                'title': 'Quantum Ethics Score',
                'definition': 'Assessment of ethical considerations in quantum technology development and deployment',
                'calculation': 'Based on quantum security implications, equitable access, research ethics, and societal impact',
                'range': '0-100 (Higher scores indicate stronger quantum ethics implementation)',
                'factors': ['Quantum Security Ethics', 'Access Equity', 'Research Ethics', 'Societal Impact']
            },
            'quantum_advantage': {
                'title': 'Quantum Advantage',
                'definition': 'Situations where quantum computers outperform classical computers for specific problems',
                'calculation': 'Measures understanding and ethical implications of quantum computational superiority',
                'importance': 'Critical for assessing societal and security impacts of quantum technology advancement',
                'examples': ['Quantum supremacy', 'Computational complexity', 'Algorithm optimization']
            },
            'quantum_security_ethics': {
                'title': 'Quantum Security Ethics',
                'definition': 'Ethical considerations around quantum technologies impact on privacy and security',
                'calculation': 'Evaluates responsible disclosure practices and security transition planning',
                'importance': 'Ensures quantum advances dont compromise existing security without proper safeguards',
                'examples': ['Responsible disclosure', 'Migration timelines', 'Stakeholder protection']
            },
            
            # General Assessment Terms
            'confidence_score': {
                'title': 'Confidence Score',
                'definition': 'Statistical measure of assessment reliability and evidence quality',
                'calculation': 'Based on document completeness, evidence strength, and assessment consistency',
                'range': '0-100% (Higher values indicate more reliable assessments)',
                'factors': ['Evidence Quality', 'Document Completeness', 'Assessment Consistency']
            },
            'maturity_level': {
                'title': 'Maturity Level',
                'definition': 'Organizational capability and sophistication in implementing security or ethics practices',
                'calculation': 'Tiered assessment from baseline to advanced based on practice comprehensiveness and effectiveness',
                'levels': ['Baseline', 'Emerging', 'Developing', 'Proficient', 'Advanced'],
                'importance': 'Provides roadmap for capability improvement and benchmarking'
            },
            'risk_assessment': {
                'title': 'Risk Assessment',
                'definition': 'Systematic evaluation of potential threats, vulnerabilities, and impact scenarios',
                'calculation': 'Combines likelihood estimates with potential impact severity across multiple threat vectors',
                'methodology': 'Based on industry frameworks including NIST, ISO 27001, and sector-specific guidelines',
                'output': 'Risk ratings and prioritized mitigation recommendations'
            }
        }
    
    def render_help_icon(self, term_key, size="small"):
        """Render a help icon with tooltip for a specific term"""
        if term_key not in self.tooltip_definitions:
            return
        
        term_data = self.tooltip_definitions[term_key]
        
        # Create detailed help text
        help_text = f"**{term_data['title']}**\n\n"
        help_text += f"{term_data['definition']}\n\n"
        
        if 'calculation' in term_data:
            help_text += f"**Calculation Method:**\n{term_data['calculation']}\n\n"
        
        if 'range' in term_data:
            help_text += f"**Score Range:** {term_data['range']}\n\n"
        
        if 'factors' in term_data:
            help_text += f"**Key Factors:** {', '.join(term_data['factors'])}\n\n"
        
        if 'importance' in term_data:
            help_text += f"**Why It Matters:** {term_data['importance']}\n\n"
        
        if 'examples' in term_data:
            help_text += f"**Examples:** {', '.join(term_data['examples'])}"
        
        # Size configurations
        icon_sizes = {
            'small': '16px',
            'medium': '20px', 
            'large': '24px'
        }
        
        icon_size = icon_sizes.get(size, '16px')
        
        # Render help icon with tooltip
        st.markdown(
            f"""
            <span style="position: relative; display: inline-block;">
                <span style="
                    display: inline-block;
                    width: {icon_size};
                    height: {icon_size};
                    background: #1976d2;
                    color: white;
                    border-radius: 50%;
                    text-align: center;
                    line-height: {icon_size};
                    font-size: 12px;
                    font-weight: bold;
                    cursor: help;
                    margin-left: 5px;
                    vertical-align: top;
                " title="{help_text.replace(chr(10), ' ').replace('**', '')}">?</span>
            </span>
            """,
            unsafe_allow_html=True
        )
    
    def render_expandable_help(self, term_key, expanded=False):
        """Render an expandable help section for detailed explanations"""
        if term_key not in self.tooltip_definitions:
            return
        
        term_data = self.tooltip_definitions[term_key]
        
        with st.expander(f"ℹ️ About {term_data['title']}", expanded=expanded):
            st.markdown(f"**Definition:** {term_data['definition']}")
            
            if 'calculation' in term_data:
                st.markdown(f"**How It's Calculated:** {term_data['calculation']}")
            
            if 'range' in term_data:
                st.markdown(f"**Score Range:** {term_data['range']}")
            
            if 'factors' in term_data:
                st.markdown("**Key Assessment Factors:**")
                for factor in term_data['factors']:
                    st.markdown(f"• {factor}")
            
            if 'importance' in term_data:
                st.markdown(f"**Why This Matters:** {term_data['importance']}")
            
            if 'examples' in term_data:
                st.markdown("**Examples:**")
                for example in term_data['examples']:
                    st.markdown(f"• {example}")
            
            if 'levels' in term_data:
                st.markdown("**Maturity Levels:**")
                for i, level in enumerate(term_data['levels'], 1):
                    st.markdown(f"{i}. {level}")
    
    def render_contextual_help_panel(self, visible_terms):
        """Render a sidebar panel with help for currently visible terms"""
        st.sidebar.markdown("### 📚 Help & Definitions")
        st.sidebar.markdown("Click on any term below for detailed explanations:")
        
        for term_key in visible_terms:
            if term_key in self.tooltip_definitions:
                term_data = self.tooltip_definitions[term_key]
                
                with st.sidebar.expander(f"❓ {term_data['title']}", expanded=False):
                    st.markdown(term_data['definition'])
                    
                    if 'range' in term_data:
                        st.markdown(f"**Range:** {term_data['range']}")
                    
                    if 'importance' in term_data:
                        st.markdown(f"**Key Point:** {term_data['importance']}")
    
    def get_help_text(self, term_key):
        """Get the help text for a specific term"""
        if term_key in self.tooltip_definitions:
            return self.tooltip_definitions[term_key]['definition']
        return "No help available for this term."
    
    def add_custom_css(self):
        """Add custom CSS for enhanced tooltip styling"""
        st.markdown("""
        <style>
        .help-tooltip {
            position: relative;
            display: inline-block;
            cursor: help;
        }
        
        .help-tooltip .tooltip-text {
            visibility: hidden;
            width: 300px;
            background-color: #333;
            color: #fff;
            text-align: left;
            border-radius: 6px;
            padding: 10px;
            position: absolute;
            z-index: 1000;
            bottom: 125%;
            left: 50%;
            margin-left: -150px;
            opacity: 0;
            transition: opacity 0.3s;
            font-size: 12px;
            line-height: 1.4;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        }
        
        .help-tooltip .tooltip-text::after {
            content: "";
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -5px;
            border-width: 5px;
            border-style: solid;
            border-color: #333 transparent transparent transparent;
        }
        
        .help-tooltip:hover .tooltip-text {
            visibility: visible;
            opacity: 1;
        }
        
        .help-icon {
            display: inline-block;
            width: 18px;
            height: 18px;
            background: linear-gradient(135deg, #1976d2, #42a5f5);
            color: white;
            border-radius: 50%;
            text-align: center;
            line-height: 18px;
            font-size: 12px;
            font-weight: bold;
            margin-left: 6px;
            cursor: help;
            transition: transform 0.2s ease;
        }
        
        .help-icon:hover {
            transform: scale(1.1);
            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }
        
        .score-explanation {
            background: #f8f9fa;
            border-left: 4px solid #1976d2;
            padding: 12px;
            margin: 8px 0;
            border-radius: 4px;
            font-size: 14px;
        }
        
        .maturity-badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
            margin: 2px;
        }
        </style>
        """, unsafe_allow_html=True)

# Global instance for easy access
help_tooltips = HelpTooltips()