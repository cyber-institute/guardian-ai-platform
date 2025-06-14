"""
Scoring Explanation System
Interactive pop-up modals explaining framework scores, evaluation criteria, and improvement recommendations
"""

import streamlit as st

def get_ai_cybersecurity_explanation(score, content="", title=""):
    """Generate detailed explanation for AI Cybersecurity score"""
    
    # Analyze content for specific factors
    content_lower = (content + " " + title).lower()
    
    factors_found = []
    factors_missing = []
    
    # AI Security factors
    ai_factors = {
        'security frameworks': ['security framework', 'cybersecurity framework', 'security model'],
        'threat assessment': ['threat', 'risk assessment', 'vulnerability', 'attack'],
        'data protection': ['data protection', 'privacy', 'encryption', 'secure data'],
        'model security': ['model security', 'ai model protection', 'adversarial', 'poisoning'],
        'governance': ['governance', 'oversight', 'compliance', 'audit'],
        'incident response': ['incident response', 'security incident', 'breach response'],
        'access controls': ['access control', 'authentication', 'authorization', 'identity'],
        'monitoring': ['monitoring', 'detection', 'logging', 'surveillance']
    }
    
    for factor, keywords in ai_factors.items():
        if any(keyword in content_lower for keyword in keywords):
            factors_found.append(factor)
        else:
            factors_missing.append(factor)
    
    # Score interpretation
    if score >= 80:
        performance = "Excellent"
        color = "#2e7d32"
        interpretation = "Document demonstrates comprehensive AI cybersecurity practices with robust security measures."
    elif score >= 60:
        performance = "Good"
        color = "#f57c00"
        interpretation = "Document shows solid AI cybersecurity foundation with room for enhancement."
    elif score >= 40:
        performance = "Moderate"
        color = "#ed6c02"
        interpretation = "Document addresses basic AI cybersecurity but lacks comprehensive coverage."
    elif score >= 20:
        performance = "Limited"
        color = "#d32f2f"
        interpretation = "Document provides minimal AI cybersecurity guidance."
    else:
        performance = "Insufficient"
        color = "#d32f2f"
        interpretation = "Document lacks adequate AI cybersecurity considerations."
    
    return {
        'title': 'AI Cybersecurity Maturity Assessment',
        'score': score,
        'performance': performance,
        'color': color,
        'interpretation': interpretation,
        'what_evaluated': [
            'AI system security architecture and frameworks',
            'Threat modeling and risk assessment procedures',
            'Data protection and privacy measures',
            'AI model security and integrity protection',
            'Governance and compliance structures',
            'Incident response and recovery capabilities',
            'Access controls and identity management',
            'Continuous monitoring and detection systems'
        ],
        'factors_found': factors_found,
        'factors_missing': factors_missing[:3],  # Top 3 missing
        'improvements': [
            'Implement comprehensive AI threat modeling',
            'Establish robust model validation procedures',
            'Develop AI-specific incident response plans',
            'Create continuous monitoring frameworks',
            'Enhance data governance for AI systems'
        ]
    }

def get_quantum_cybersecurity_explanation(score, content="", title=""):
    """Generate detailed explanation for Quantum Cybersecurity score"""
    
    content_lower = (content + " " + title).lower()
    
    factors_found = []
    factors_missing = []
    
    # Quantum Security factors
    quantum_factors = {
        'post-quantum cryptography': ['post-quantum', 'quantum-safe', 'quantum-resistant'],
        'quantum key distribution': ['qkd', 'quantum key', 'quantum communication'],
        'quantum threat assessment': ['quantum threat', 'quantum attack', 'quantum computing threat'],
        'cryptographic agility': ['crypto agility', 'algorithm agility', 'cryptographic transition'],
        'quantum readiness': ['quantum readiness', 'quantum preparedness', 'quantum migration'],
        'quantum standards': ['quantum standard', 'nist quantum', 'quantum compliance'],
        'hybrid security': ['hybrid quantum', 'classical-quantum', 'quantum-classical'],
        'quantum risk management': ['quantum risk', 'quantum vulnerability', 'quantum impact']
    }
    
    for factor, keywords in quantum_factors.items():
        if any(keyword in content_lower for keyword in keywords):
            factors_found.append(factor)
        else:
            factors_missing.append(factor)
    
    # Score interpretation (Tier-based for quantum)
    if score >= 80:
        tier = "Tier 5 - Advanced"
        color = "#1976d2"
        interpretation = "Organization demonstrates advanced quantum cybersecurity readiness with comprehensive post-quantum strategies."
    elif score >= 60:
        tier = "Tier 4 - Proficient"
        color = "#1976d2"
        interpretation = "Strong quantum cybersecurity foundation with active post-quantum planning."
    elif score >= 40:
        tier = "Tier 3 - Developing"
        color = "#f57c00"
        interpretation = "Basic quantum awareness with initial post-quantum considerations."
    elif score >= 20:
        tier = "Tier 2 - Emerging"
        color = "#ed6c02"
        interpretation = "Limited quantum cybersecurity awareness and preparation."
    else:
        tier = "Tier 1 - Baseline"
        color = "#d32f2f"
        interpretation = "Minimal quantum cybersecurity considerations."
    
    return {
        'title': 'Quantum Cybersecurity Maturity Assessment',
        'score': score,
        'performance': tier,
        'color': color,
        'interpretation': interpretation,
        'what_evaluated': [
            'Post-quantum cryptography adoption and planning',
            'Quantum key distribution implementation',
            'Quantum threat assessment and risk analysis',
            'Cryptographic agility and migration strategies',
            'Quantum-safe standards compliance',
            'Hybrid classical-quantum security approaches',
            'Quantum risk management frameworks',
            'Organizational quantum readiness'
        ],
        'factors_found': factors_found,
        'factors_missing': factors_missing[:3],
        'improvements': [
            'Develop post-quantum cryptography migration plan',
            'Implement quantum threat assessment procedures',
            'Establish cryptographic agility frameworks',
            'Create quantum risk management policies',
            'Plan for NIST post-quantum standards adoption'
        ]
    }

def get_ai_ethics_explanation(score, content="", title=""):
    """Generate detailed explanation for AI Ethics score"""
    
    content_lower = (content + " " + title).lower()
    
    factors_found = []
    factors_missing = []
    
    # AI Ethics factors
    ethics_factors = {
        'bias mitigation': ['bias', 'fairness', 'discrimination', 'bias mitigation'],
        'transparency': ['transparency', 'explainable', 'interpretable', 'explainability'],
        'accountability': ['accountability', 'responsibility', 'oversight', 'audit'],
        'privacy protection': ['privacy', 'data protection', 'personal data', 'consent'],
        'human oversight': ['human oversight', 'human control', 'human-in-the-loop'],
        'social impact': ['social impact', 'societal', 'community', 'social good'],
        'ethical guidelines': ['ethical', 'ethics', 'moral', 'values'],
        'stakeholder engagement': ['stakeholder', 'community input', 'public engagement']
    }
    
    for factor, keywords in ethics_factors.items():
        if any(keyword in content_lower for keyword in keywords):
            factors_found.append(factor)
        else:
            factors_missing.append(factor)
    
    # Score interpretation
    if score >= 80:
        performance = "Exemplary"
        color = "#2e7d32"
        interpretation = "Document demonstrates comprehensive AI ethics framework with strong emphasis on responsible AI."
    elif score >= 60:
        performance = "Proficient"
        color = "#f57c00"
        interpretation = "Good AI ethics foundation with most key principles addressed."
    elif score >= 40:
        performance = "Developing"
        color = "#ed6c02"
        interpretation = "Basic AI ethics considerations with room for significant improvement."
    elif score >= 20:
        performance = "Emerging"
        color = "#d32f2f"
        interpretation = "Limited AI ethics awareness and implementation."
    else:
        performance = "Insufficient"
        color = "#d32f2f"
        interpretation = "Inadequate attention to AI ethics principles."
    
    return {
        'title': 'AI Ethics Assessment',
        'score': score,
        'performance': performance,
        'color': color,
        'interpretation': interpretation,
        'what_evaluated': [
            'Bias detection and mitigation strategies',
            'Transparency and explainability measures',
            'Accountability and governance structures',
            'Privacy protection and data rights',
            'Human oversight and control mechanisms',
            'Social impact assessment and management',
            'Ethical guidelines and principles',
            'Stakeholder engagement and participation'
        ],
        'factors_found': factors_found,
        'factors_missing': factors_missing[:3],
        'improvements': [
            'Implement comprehensive bias testing procedures',
            'Develop explainable AI capabilities',
            'Establish ethical review boards',
            'Create stakeholder engagement processes',
            'Enhance privacy-preserving techniques'
        ]
    }

def get_quantum_ethics_explanation(score, content="", title=""):
    """Generate detailed explanation for Quantum Ethics score"""
    
    content_lower = (content + " " + title).lower()
    
    factors_found = []
    factors_missing = []
    
    # Quantum Ethics factors
    quantum_ethics_factors = {
        'quantum advantage equity': ['quantum advantage', 'quantum supremacy', 'equitable access'],
        'quantum privacy': ['quantum privacy', 'quantum encryption', 'quantum security'],
        'quantum governance': ['quantum governance', 'quantum regulation', 'quantum policy'],
        'societal impact': ['societal impact', 'social implications', 'public benefit'],
        'quantum education': ['quantum education', 'quantum literacy', 'public understanding'],
        'quantum responsibility': ['quantum responsibility', 'responsible quantum', 'ethical quantum'],
        'quantum justice': ['quantum justice', 'quantum equity', 'quantum fairness'],
        'future implications': ['future implications', 'long-term impact', 'generational effect']
    }
    
    for factor, keywords in quantum_ethics_factors.items():
        if any(keyword in content_lower for keyword in keywords):
            factors_found.append(factor)
        else:
            factors_missing.append(factor)
    
    # Score interpretation
    if score >= 80:
        performance = "Advanced"
        color = "#2e7d32"
        interpretation = "Document shows sophisticated understanding of quantum ethics with comprehensive consideration of societal implications."
    elif score >= 60:
        performance = "Developed"
        color = "#f57c00"
        interpretation = "Good quantum ethics awareness with attention to key societal considerations."
    elif score >= 40:
        performance = "Emerging"
        color = "#ed6c02"
        interpretation = "Basic quantum ethics considerations with limited depth."
    elif score >= 20:
        performance = "Initial"
        color = "#d32f2f"
        interpretation = "Minimal quantum ethics awareness."
    else:
        performance = "Absent"
        color = "#d32f2f"
        interpretation = "No significant quantum ethics considerations identified."
    
    return {
        'title': 'Quantum Ethics Assessment',
        'score': score,
        'performance': performance,
        'color': color,
        'interpretation': interpretation,
        'what_evaluated': [
            'Equitable access to quantum advantages',
            'Quantum privacy and security implications',
            'Quantum technology governance frameworks',
            'Societal impact and public benefit considerations',
            'Quantum education and public understanding',
            'Responsible quantum development practices',
            'Quantum justice and fairness principles',
            'Long-term implications for future generations'
        ],
        'factors_found': factors_found,
        'factors_missing': factors_missing[:3],
        'improvements': [
            'Develop quantum equity frameworks',
            'Address quantum digital divide concerns',
            'Create quantum ethics guidelines',
            'Establish quantum governance structures',
            'Promote quantum literacy initiatives'
        ]
    }

def render_score_explanation_modal(framework_type, score, content="", title="", doc_id=None):
    """Render interactive modal with score explanation"""
    
    modal_key = f"score_modal_{framework_type}_{doc_id}"
    
    if st.session_state.get(modal_key, False):
        # Get explanation based on framework type
        if framework_type == 'ai_cybersecurity':
            explanation = get_ai_cybersecurity_explanation(score, content, title)
        elif framework_type == 'quantum_cybersecurity':
            explanation = get_quantum_cybersecurity_explanation(score, content, title)
        elif framework_type == 'ai_ethics':
            explanation = get_ai_ethics_explanation(score, content, title)
        elif framework_type == 'quantum_ethics':
            explanation = get_quantum_ethics_explanation(score, content, title)
        else:
            return
        
        # Create modal overlay
        st.markdown(f"""
        <div style="position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.7); z-index: 999; display: flex; align-items: center; justify-content: center;">
            <div style="background: white; border-radius: 12px; max-width: 600px; max-height: 80vh; overflow-y: auto; box-shadow: 0 10px 30px rgba(0,0,0,0.3); margin: 20px;">
                <div style="padding: 24px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; border-bottom: 2px solid #f0f0f0; padding-bottom: 16px;">
                        <h3 style="margin: 0; color: {explanation['color']}; font-size: 1.3rem;">{explanation['title']}</h3>
                        <button onclick="document.querySelector('[data-testid=\\"stMarkdownContainer\\"]').innerHTML=''" style="background: none; border: none; font-size: 1.5rem; cursor: pointer; color: #666;">✕</button>
                    </div>
                    
                    <div style="margin-bottom: 20px;">
                        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
                            <div style="background: {explanation['color']}; color: white; padding: 8px 16px; border-radius: 20px; font-weight: bold; font-size: 1.1rem;">
                                {score if score != 'N/A' else 'N/A'}
                            </div>
                            <div style="font-weight: bold; color: {explanation['color']}; font-size: 1.1rem;">
                                {explanation['performance']}
                            </div>
                        </div>
                        <p style="margin: 0; color: #555; line-height: 1.5; font-size: 0.95rem;">
                            {explanation['interpretation']}
                        </p>
                    </div>
                    
                    <div style="margin-bottom: 20px;">
                        <h4 style="color: #333; margin-bottom: 8px; font-size: 1rem;">📊 Evaluation Criteria</h4>
                        <ul style="margin: 0; padding-left: 20px; color: #555; font-size: 0.9rem;">
                            {''.join([f'<li style="margin-bottom: 4px;">{item}</li>' for item in explanation['what_evaluated']])}
                        </ul>
                    </div>
                    
                    {f'''
                    <div style="margin-bottom: 20px;">
                        <h4 style="color: #2e7d32; margin-bottom: 8px; font-size: 1rem;">✅ Strengths Identified</h4>
                        <ul style="margin: 0; padding-left: 20px; color: #555; font-size: 0.9rem;">
                            {''.join([f'<li style="margin-bottom: 4px; text-transform: capitalize;">{factor}</li>' for factor in explanation['factors_found']]) if explanation['factors_found'] else '<li style="color: #999;">No specific strengths identified in content analysis</li>'}
                        </ul>
                    </div>
                    ''' if explanation['factors_found'] or score == 'N/A' else ''}
                    
                    <div style="margin-bottom: 20px;">
                        <h4 style="color: #f57c00; margin-bottom: 8px; font-size: 1rem;">🎯 Improvement Opportunities</h4>
                        <ul style="margin: 0; padding-left: 20px; color: #555; font-size: 0.9rem;">
                            {''.join([f'<li style="margin-bottom: 4px;">{improvement}</li>' for improvement in explanation['improvements'][:5]])}
                        </ul>
                    </div>
                    
                    <div style="background: #f8f9fa; padding: 16px; border-radius: 8px; border-left: 4px solid {explanation['color']};">
                        <p style="margin: 0; font-size: 0.85rem; color: #666; line-height: 1.4;">
                            <strong>Note:</strong> Scores are calculated using GUARDIAN's multi-LLM ensemble analysis engine, evaluating content against established frameworks including NIST AI RMF, CISA guidelines, and quantum security standards.
                        </p>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Close button functionality
        if st.button("Close", key=f"close_{modal_key}", type="secondary"):
            st.session_state[modal_key] = False
            st.rerun()

def create_clickable_score_badge(framework_type, score, doc_id, content="", title=""):
    """Create clickable score badge that opens explanation modal"""
    
    modal_key = f"score_modal_{framework_type}_{doc_id}"
    
    # Color coding based on score
    if score == 'N/A':
        color = '#9e9e9e'
        bg_color = '#f5f5f5'
    elif isinstance(score, (int, float)):
        if score >= 80:
            color = '#2e7d32'
            bg_color = '#e8f5e8'
        elif score >= 60:
            color = '#f57c00'
            bg_color = '#fff3e0'
        elif score >= 40:
            color = '#ed6c02'
            bg_color = '#fff3e0'
        else:
            color = '#d32f2f'
            bg_color = '#ffebee'
    else:
        color = '#9e9e9e'
        bg_color = '#f5f5f5'
    
    # Framework labels
    labels = {
        'ai_cybersecurity': 'AI Cyber',
        'quantum_cybersecurity': 'Q Cyber',
        'ai_ethics': 'AI Ethics',
        'quantum_ethics': 'Q Ethics'
    }
    
    label = labels.get(framework_type, framework_type)
    
    # Create clickable badge
    if st.button(
        f"{label}: {score}",
        key=f"score_btn_{framework_type}_{doc_id}",
        help="Click for detailed scoring explanation",
        type="secondary"
    ):
        st.session_state[modal_key] = True
        st.rerun()
    
    # Render modal if active
    render_score_explanation_modal(framework_type, score, content, title, doc_id)

    return f"""
    <span style='background:{bg_color};padding:4px 12px;border-radius:10px;color:{color};font-weight:600;cursor:pointer;transition:all 0.2s ease;' 
          onclick='alert("Click the button version for detailed explanation")' 
          title='Click for detailed scoring explanation'>{score}</span>
    """