"""
GUARDIAN Patent Interactive Web Application
Nonprovisional Utility Patent Application: "System for Real-Time Dynamic Governance of Emerging Technologies"
"""

import streamlit as st
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import io
import base64

def render():
    """Render the interactive patent web application."""
    
    # Patent header - clean version without blue background or icons
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem; border-left: 4px solid #B91C2C;">
        <h2 style="color: #B91C2C; margin-bottom: 0.8rem; font-size: 1.6rem;">GUARDIAN Patent Application Overview</h2>
        <p style="font-size: 1rem; line-height: 1.5; color: #374151; margin: 0;">
            System for Real-Time Dynamic Governance of Emerging Technologies - Nonprovisional Utility Patent Application for Advanced AI Risk Assessment Framework
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    patent_sections = [
        "System Overview",
        "Mathematical Formulations", 
        "Risk Calculator",
        "Process Flow",
        "Patent Claims",
        "Innovation Summary"
    ]
    
    selected_section = st.selectbox("Navigate Patent Sections:", patent_sections)
    
    if selected_section == "System Overview":
        render_system_overview()
    elif selected_section == "Mathematical Formulations":
        render_mathematical_formulations()
    elif selected_section == "Risk Calculator":
        render_risk_calculator()
    elif selected_section == "Process Flow":
        render_process_flow()
    elif selected_section == "Patent Claims":
        render_claims()
    elif selected_section == "Innovation Summary":
        render_innovation_summary()

def render_system_overview():
    """Render the system overview section."""
    
    # Compact overview section
    st.markdown("""
    <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; margin-bottom: 1.5rem;">
    <h4 style="color: #B91C2C; margin-bottom: 0.5rem;">Patent System Overview</h4>
    <p style="font-size: 0.95rem; line-height: 1.5; color: #374151; margin: 0;">
    AI-driven governance technology providing real-time assessment and mitigation of complex risks across cybersecurity, ethics, and policy domains.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Three-column layout for patent capabilities
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: #fef2f2; padding: 1rem; border-radius: 6px; height: 280px;">
        <h5 style="color: #B91C2C; margin-bottom: 0.8rem;">Core Capabilities</h5>
        <div style="font-size: 0.85rem; line-height: 1.4;">
        <strong>Real-time Risk Assessment</strong><br>
        Continuous monitoring and evaluation<br><br>
        <strong>Multi-modal Analysis</strong><br>
        Text, policy, regulatory content processing<br><br>
        <strong>Adaptive Learning</strong><br>
        Self-improving assessment algorithms<br><br>
        <strong>Cross-domain Integration</strong><br>
        Unified cybersecurity and ethics evaluation
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; height: 280px;">
        <h5 style="color: #B91C2C; margin-bottom: 0.8rem;">Technical Innovation</h5>
        <div style="font-size: 0.85rem; line-height: 1.4;">
        <strong>Patent-based Scoring</strong><br>
        Proprietary assessment frameworks<br><br>
        <strong>LLM Integration</strong><br>
        Advanced natural language understanding<br><br>
        <strong>Dynamic Governance</strong><br>
        Adaptive policy recommendations<br><br>
        <strong>Scalable Architecture</strong><br>
        Cloud-native deployment ready
        </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div style="background: #f0fdf4; padding: 1rem; border-radius: 6px; height: 280px;">
        <h5 style="color: #B91C2C; margin-bottom: 0.8rem;">Patent Features</h5>
        <div style="font-size: 0.85rem; line-height: 1.4;">
        <strong>Conversational AI Interface</strong><br>
        Natural language processing capabilities<br><br>
        <strong>Policy Repository Integration</strong><br>
        UN, NIST, OECD framework alignment<br><br>
        <strong>Scoring Engines</strong><br>
        Dual-modality risk evaluation<br><br>
        <strong>Feedback Integration</strong><br>
        Real-time recommendation generation
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Compact system flow section
    st.markdown("""
    <div style="background: #fffbeb; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
    <h5 style="color: #B91C2C; margin-bottom: 0.8rem; text-align: center;">Patent System Flow</h5>
    </div>
    """, unsafe_allow_html=True)
    
    # Compact flow visualization using HTML cards
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(6, 1fr); gap: 0.5rem; margin: 0.5rem 0;">
        <div style="background: #3B82F6; color: white; padding: 0.8rem; border-radius: 6px; text-align: center; font-size: 0.8rem; font-weight: 600;">
            User Query
        </div>
        <div style="background: #10B981; color: white; padding: 0.8rem; border-radius: 6px; text-align: center; font-size: 0.8rem; font-weight: 600;">
            NLP Engine
        </div>
        <div style="background: #F59E0B; color: white; padding: 0.8rem; border-radius: 6px; text-align: center; font-size: 0.8rem; font-weight: 600;">
            Policy Repository
        </div>
        <div style="background: #EF4444; color: white; padding: 0.8rem; border-radius: 6px; text-align: center; font-size: 0.8rem; font-weight: 600;">
            AI Scoring
        </div>
        <div style="background: #8B5CF6; color: white; padding: 0.8rem; border-radius: 6px; text-align: center; font-size: 0.8rem; font-weight: 600;">
            Risk Evaluation
        </div>
        <div style="background: #059669; color: white; padding: 0.8rem; border-radius: 6px; text-align: center; font-size: 0.8rem; font-weight: 600;">
            Recommendations
        </div>
    </div>
    <div style="text-align: center; margin: 0.5rem 0; font-size: 0.8rem; color: #666;">
        Patent Figure 1: GUARDIAN System Architecture Flow
    </div>
    """, unsafe_allow_html=True)

def render_mathematical_formulations():
    """Render the mathematical formulations from the patent."""
    
    # Compact overview section
    st.markdown("""
    <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; margin-bottom: 1.5rem;">
    <h4 style="color: #B91C2C; margin-bottom: 0.5rem;">Mathematical Formulations</h4>
    <p style="font-size: 0.95rem; line-height: 1.5; color: #374151; margin: 0;">
    Sophisticated mathematical models for multi-dimensional risk assessment and policy evaluation across AI and quantum domains.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Primary risk formula section
    st.markdown("""
    <div style="background: #fef2f2; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
    <h5 style="color: #B91C2C; margin-bottom: 0.8rem;">Primary Risk Assessment Formula</h5>
    <p style="font-size: 0.9rem; margin: 0; color: #374151;">Core risk calculation integrating multiple assessment dimensions:</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.latex(r'''
    R_{total} = \sum_{i=1}^{n} w_i \cdot \frac{V_i \cdot C_i \cdot P_i}{T_i}
    ''')
    
    # Variable definitions in compact grid
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem; margin: 1rem 0; font-size: 0.85rem;">
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>R<sub>total</sub></strong> = Total risk score</div>
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>w<sub>i</sub></strong> = Weight factor</div>
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>V<sub>i</sub></strong> = Vulnerability score</div>
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>C<sub>i</sub></strong> = Criticality factor</div>
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>P<sub>i</sub></strong> = Probability of occurrence</div>
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>T<sub>i</sub></strong> = Time sensitivity factor</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Framework integration header
    st.markdown("""
    <div style="background: #fffbeb; padding: 1rem; border-radius: 6px; margin: 1rem 0;">
    <h5 style="color: #B91C2C; margin-bottom: 0.5rem; text-align: center;">Multi-Framework Scoring Integration</h5>
    <p style="font-size: 0.9rem; margin: 0; color: #374151; text-align: center;">Four distinct patent-based scoring frameworks</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Two-column formula layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #fef2f2; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
        <h6 style="color: #B91C2C; margin-bottom: 0.5rem;">AI Cybersecurity Maturity (0-100 scale)</h6>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r'''
        S_{AI-Cyber} = \alpha \cdot E + \beta \cdot A + \gamma \cdot T + \delta \cdot I
        ''')
        
        st.markdown("""
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; margin: 1rem 0;">
        <h6 style="color: #B91C2C; margin-bottom: 0.5rem;">Quantum Cybersecurity Maturity (1-5 scale)</h6>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r'''
        S_{Q-Cyber} = \lceil \frac{Q_{awareness} + Q_{implementation} + Q_{integration}}{3} \rceil
        ''')
    
    with col2:
        st.markdown("""
        <div style="background: #f0fdf4; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
        <h6 style="color: #B91C2C; margin-bottom: 0.5rem;">AI Ethics Assessment (0-100 scale)</h6>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r'''
        S_{AI-Ethics} = \sum_{j=1}^{4} \omega_j \cdot F_j
        ''')
        
        st.markdown("""
        <div style="background: #fffbeb; padding: 1rem; border-radius: 6px; margin: 1rem 0;">
        <h6 style="color: #B91C2C; margin-bottom: 0.5rem;">Quantum Ethics Assessment (0-100 scale)</h6>
        </div>
        """, unsafe_allow_html=True)
        st.latex(r'''
        S_{Q-Ethics} = \frac{\sum_{k=1}^{m} \phi_k \cdot E_k}{\sum_{k=1}^{m} \phi_k} \cdot 100
        ''')

def render_risk_calculator():
    """Interactive risk calculator based on patent formulations."""
    
    st.markdown("""
    ## Interactive Risk Calculator
    
    Experience the patent's risk assessment algorithms in real-time.
    """)
    
    # Create tabs for different calculators
    tab1, tab2, tab3 = st.tabs(["Cybersecurity Risk", "Ethics Risk", "Combined Assessment"])
    
    with tab1:
        render_cyber_calculator()
    
    with tab2:
        render_ethics_calculator()
    
    with tab3:
        render_combined_calculator()

def render_cyber_calculator():
    """Cybersecurity risk calculator."""
    
    st.markdown("### Cybersecurity Risk Assessment")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("**Risk Parameters:**")
        
        # Input parameters
        auth_weakness = st.slider("Authentication Weakness (0-5)", 0, 5, 2)
        encryption_gaps = st.slider("Encryption Gaps (0-5)", 0, 5, 1)
        access_control = st.slider("Access Control Issues (0-5)", 0, 5, 1)
        monitoring_gaps = st.slider("Monitoring Gaps (0-5)", 0, 5, 2)
        
        # Store vulnerabilities for calculation
        vulnerabilities = [
            (0.3, auth_weakness, 0.8),
            (0.25, encryption_gaps, 0.9),
            (0.25, access_control, 0.7),
            (0.2, monitoring_gaps, 0.6)
        ]
    
    with col2:
        # Calculate risk
        total_risk = sum(w * v * c for w, v, c in vulnerabilities)
        
        st.markdown("**Risk Assessment Results:**")
        
        # Risk gauge using speedometer from about_tab
        from about_tab import create_speedometer_dial
        risk_percentage = min(100, (total_risk / 5) * 100)
        risk_dial = create_speedometer_dial(int(risk_percentage))
        st.markdown("**Cybersecurity Risk Score**")
        st.markdown(risk_dial, unsafe_allow_html=True)
        st.markdown(f"**Score:** {total_risk:.2f}/5")
        
        # Risk interpretation
        if total_risk < 1:
            risk_level = "Low Risk"
            color = "green"
        elif total_risk < 2.5:
            risk_level = "Moderate Risk"
            color = "orange"
        else:
            risk_level = "High Risk"
            color = "red"
        
        st.markdown(f"**Risk Level:** :{color}[{risk_level}]")

def render_ethics_calculator():
    """Ethics risk calculator."""
    
    st.markdown("### AI Ethics Assessment")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("**Ethics Parameters:**")
        
        fairness = st.slider("Fairness & Bias Mitigation (0-25)", 0, 25, 15)
        transparency = st.slider("Transparency & Explainability (0-25)", 0, 25, 18)
        accountability = st.slider("Accountability Mechanisms (0-25)", 0, 25, 12)
        privacy = st.slider("Privacy Protection (0-25)", 0, 25, 20)
    
    with col2:
        # Calculate ethics score
        total_ethics = fairness + transparency + accountability + privacy
        
        st.markdown("**Ethics Assessment Results:**")
        
        # Ethics gauge
        from about_tab import create_speedometer_dial
        ethics_dial = create_speedometer_dial(total_ethics)
        st.markdown("**AI Ethics Score**")
        st.markdown(ethics_dial, unsafe_allow_html=True)
        st.markdown(f"**Score:** {total_ethics}/100")
        
        # Ethics interpretation
        if total_ethics >= 75:
            ethics_level = "Excellent Ethics"
            color = "green"
        elif total_ethics >= 50:
            ethics_level = "Good Ethics"
            color = "blue"
        elif total_ethics >= 25:
            ethics_level = "Developing Ethics"
            color = "orange"
        else:
            ethics_level = "Requires Attention"
            color = "red"
        
        st.markdown(f"**Ethics Level:** :{color}[{ethics_level}]")

def render_combined_calculator():
    """Combined risk assessment."""
    
    st.markdown("### Comprehensive Risk Assessment")
    
    # Sample combined scores
    ai_cyber_score = 72
    quantum_cyber_score = 3
    ai_ethics_score = 68
    quantum_ethics_score = 75
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Current Assessment Scores:**")
        
        # Display all four gauges
        from about_tab import create_speedometer_dial
        
        st.markdown("**AI Cybersecurity Maturity**")
        dial1 = create_speedometer_dial(ai_cyber_score)
        st.markdown(dial1, unsafe_allow_html=True)
        
        st.markdown("**Quantum Cybersecurity Maturity**")
        dial2 = create_speedometer_dial((quantum_cyber_score / 5) * 100)
        st.markdown(dial2, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Ethics Assessment Scores:**")
        
        st.markdown("**AI Ethics Assessment**")
        dial3 = create_speedometer_dial(ai_ethics_score)
        st.markdown(dial3, unsafe_allow_html=True)
        
        st.markdown("**Quantum Ethics Assessment**")
        dial4 = create_speedometer_dial(quantum_ethics_score)
        st.markdown(dial4, unsafe_allow_html=True)
    
    # Combined risk calculation
    combined_score = (ai_cyber_score + (quantum_cyber_score * 20) + ai_ethics_score + quantum_ethics_score) / 4
    
    st.markdown("---")
    st.markdown("### Overall Risk Profile")
    
    combined_dial = create_speedometer_dial(int(combined_score))
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("**Combined Maturity Score**")
        st.markdown(combined_dial, unsafe_allow_html=True)
        st.markdown(f"**Overall Score:** {combined_score:.1f}/100")

def render_process_flow():
    """Process flow demonstration."""
    
    st.markdown("""
    ## Patent Process Flow
    
    This section demonstrates the step-by-step process flow outlined in the patent application.
    """)
    
    # Process steps
    process_steps = [
        {
            "step": "1. Document Ingestion",
            "description": "System receives policy documents, regulations, or technical specifications",
            "technical": "Multi-format parsing with NLP preprocessing"
        },
        {
            "step": "2. Content Analysis", 
            "description": "Advanced NLP engines extract key concepts and risk indicators",
            "technical": "Transformer-based language models with domain-specific fine-tuning"
        },
        {
            "step": "3. Risk Classification",
            "description": "Content is classified across cybersecurity and ethics dimensions",
            "technical": "Multi-label classification with confidence scoring"
        },
        {
            "step": "4. Scoring Application",
            "description": "Patent-based scoring frameworks generate quantitative assessments",
            "technical": "Weighted scoring algorithms with adaptive thresholds"
        },
        {
            "step": "5. Risk Aggregation",
            "description": "Individual scores are combined into comprehensive risk profiles",
            "technical": "Multi-dimensional risk modeling with uncertainty quantification"
        },
        {
            "step": "6. Recommendation Generation",
            "description": "System provides actionable recommendations for risk mitigation",
            "technical": "Rule-based expert system with continuous learning capabilities"
        }
    ]
    
    for i, step_info in enumerate(process_steps):
        with st.expander(step_info["step"], expanded=i==0):
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"**Description:** {step_info['description']}")
                st.markdown(f"**Technical Implementation:** {step_info['technical']}")
            with col2:
                # Show progress indicator
                progress = (i + 1) / len(process_steps)
                st.progress(progress)
                st.markdown(f"Step {i+1} of {len(process_steps)}")

def render_claims():
    """Patent claims and technical features."""
    
    # Compact overview section
    st.markdown("""
    <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; margin-bottom: 1.5rem;">
    <h4 style="color: #B91C2C; margin-bottom: 0.5rem;">Patent Claims & Technical Features</h4>
    <p style="font-size: 0.95rem; line-height: 1.5; color: #374151; margin: 0;">
    Key technical innovations and claims from the GUARDIAN patent application demonstrating novel governance methodologies.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Three-column claims layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: #fef2f2; padding: 1rem; border-radius: 6px; height: 320px;">
        <h5 style="color: #B91C2C; margin-bottom: 0.8rem;">Primary Claim 1</h5>
        <h6 style="color: #374151; margin-bottom: 0.5rem;">Real-time Dynamic Risk Assessment</h6>
        <div style="font-size: 0.85rem; line-height: 1.4;">
        <strong>• Continuous Monitoring</strong><br>
        AI and quantum technology evaluation<br><br>
        <strong>• Adaptive Algorithms</strong><br>
        Machine learning-enhanced scoring<br><br>
        <strong>• Multi-modal Processing</strong><br>
        Text, policy, technical specifications<br><br>
        <strong>• Real-time Updates</strong><br>
        Dynamic assessment capabilities
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; height: 320px;">
        <h5 style="color: #B91C2C; margin-bottom: 0.8rem;">Primary Claim 2</h5>
        <h6 style="color: #374151; margin-bottom: 0.5rem;">Integrated Scoring Framework</h6>
        <div style="font-size: 0.85rem; line-height: 1.4;">
        <strong>• Four Assessment Dimensions</strong><br>
        Patent-protected algorithms<br><br>
        <strong>• Cross-domain Correlation</strong><br>
        Risk aggregation methodology<br><br>
        <strong>• Scalable Architecture</strong><br>
        Enterprise deployment ready<br><br>
        <strong>• Unified Evaluation</strong><br>
        Comprehensive risk assessment
        </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div style="background: #f0fdf4; padding: 1rem; border-radius: 6px; height: 320px;">
        <h5 style="color: #B91C2C; margin-bottom: 0.8rem;">Primary Claim 3</h5>
        <h6 style="color: #374151; margin-bottom: 0.5rem;">Automated Governance Recommendations</h6>
        <div style="font-size: 0.85rem; line-height: 1.4;">
        <strong>• Policy Gap Identification</strong><br>
        Automated remediation suggestions<br><br>
        <strong>• Compliance Monitoring</strong><br>
        Regulatory reporting capabilities<br><br>
        <strong>• Strategy Generation</strong><br>
        Risk mitigation recommendations<br><br>
        <strong>• Decision Support</strong><br>
        Actionable governance insights
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Technical innovations header
    st.markdown("""
    <div style="background: #fffbeb; padding: 1rem; border-radius: 6px; margin: 1rem 0;">
    <h5 style="color: #B91C2C; margin-bottom: 0.5rem; text-align: center;">Technical Innovations</h5>
    <p style="font-size: 0.9rem; margin: 0; color: #374151; text-align: center;">Patent-protected technical advances in AI governance</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Compact innovations grid
    innovations = [
        ("Natural Language Processing Engine", "Advanced NLP with domain-specific training for policy and technical document analysis"),
        ("Multi-dimensional Risk Modeling", "Sophisticated mathematical models for risk assessment across cybersecurity and ethics domains"),
        ("Adaptive Learning Architecture", "Self-improving algorithms that enhance assessment accuracy over time"),
        ("Cross-domain Integration", "Unified framework for evaluating both AI and quantum technology risks"),
        ("Real-time Processing Pipeline", "High-performance architecture for continuous risk monitoring and assessment")
    ]
    
    # Display innovations in compact cards
    cols = st.columns(2)
    for i, (innovation, description) in enumerate(innovations):
        with cols[i % 2]:
            st.markdown(f"""
            <div style="background: #f9fafb; padding: 0.8rem; border-radius: 4px; margin-bottom: 0.5rem; border-left: 3px solid #B91C2C;">
            <h6 style="color: #B91C2C; margin-bottom: 0.3rem; font-size: 0.9rem;">{innovation}</h6>
            <p style="font-size: 0.8rem; line-height: 1.3; color: #374151; margin: 0;">{description}</p>
            </div>
            """, unsafe_allow_html=True)

def render_innovation_summary():
    """Innovation summary and commercial applications."""
    
    # Compact overview section
    st.markdown("""
    <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; margin-bottom: 1.5rem;">
    <h4 style="color: #B91C2C; margin-bottom: 0.5rem;">Innovation Summary & Commercial Applications</h4>
    <p style="font-size: 0.95rem; line-height: 1.5; color: #374151; margin: 0;">
    Significant advancement in AI governance technology with broad commercial applications across government, enterprise, and research sectors.
    </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Four-column market applications layout
    st.markdown("""
    <div style="background: #fffbeb; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
    <h5 style="color: #B91C2C; margin-bottom: 0.8rem; text-align: center;">Market Applications</h5>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: #fef2f2; padding: 1rem; border-radius: 6px; height: 240px;">
        <h6 style="color: #B91C2C; margin-bottom: 0.8rem;">Government & Regulatory</h6>
        <div style="font-size: 0.85rem; line-height: 1.4;">
        <strong>• Federal AI Compliance</strong><br>
        Agency monitoring systems<br><br>
        <strong>• Framework Development</strong><br>
        Regulatory testing platforms<br><br>
        <strong>• Policy Harmonization</strong><br>
        Cross-agency coordination<br><br>
        <strong>• Standards Implementation</strong><br>
        Compliance automation
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; height: 240px;">
        <h6 style="color: #B91C2C; margin-bottom: 0.8rem;">Enterprise</h6>
        <div style="font-size: 0.85rem; line-height: 1.4;">
        <strong>• Risk Governance</strong><br>
        Corporate AI management<br><br>
        <strong>• Compliance Automation</strong><br>
        Regulatory adherence tools<br><br>
        <strong>• Due Diligence</strong><br>
        Risk assessment platforms<br><br>
        <strong>• Strategic Planning</strong><br>
        Technology governance
        </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div style="background: #f0fdf4; padding: 1rem; border-radius: 6px; height: 240px;">
        <h6 style="color: #B91C2C; margin-bottom: 0.8rem;">Academic & Research</h6>
        <div style="font-size: 0.85rem; line-height: 1.4;">
        <strong>• Policy Analysis</strong><br>
        Academic research tools<br><br>
        <strong>• Educational Platforms</strong><br>
        Governance training systems<br><br>
        <strong>• Simulation Testing</strong><br>
        Policy stress testing<br><br>
        <strong>• Research Support</strong><br>
        Analysis frameworks
        </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
        <div style="background: #faf5ff; padding: 1rem; border-radius: 6px; height: 240px;">
        <h6 style="color: #B91C2C; margin-bottom: 0.8rem;">Consulting & Advisory</h6>
        <div style="font-size: 0.85rem; line-height: 1.4;">
        <strong>• Risk Assessment Services</strong><br>
        Professional evaluation tools<br><br>
        <strong>• Compliance Consulting</strong><br>
        Automated advisory systems<br><br>
        <strong>• Policy Development</strong><br>
        Strategic support platforms<br><br>
        <strong>• Implementation Support</strong><br>
        Deployment assistance
        </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Competitive advantages in two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #fef2f2; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
        <h5 style="color: #B91C2C; margin-bottom: 0.8rem;">Competitive Advantages</h5>
        <div style="font-size: 0.9rem; line-height: 1.4;">
        <strong>First-to-Market Innovation</strong><br>
        Novel AI and quantum risk integration<br><br>
        <strong>Comprehensive Patent Protection</strong><br>
        Core algorithms and methods coverage<br><br>
        <strong>Scalable Cloud Architecture</strong><br>
        Enterprise-ready deployment design
        </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
        <h5 style="color: #B91C2C; margin-bottom: 0.8rem;">Technical Differentiators</h5>
        <div style="font-size: 0.9rem; line-height: 1.4;">
        <strong>Advanced NLP Processing</strong><br>
        Policy-tuned language models<br><br>
        <strong>Multi-framework Integration</strong><br>
        Four distinct assessment methods<br><br>
        <strong>Real-time Analysis Pipeline</strong><br>
        Continuous monitoring capabilities
        </div>
        </div>
        """, unsafe_allow_html=True)