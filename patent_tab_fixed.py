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
            System for Real-Time Dynamic Governance of Emerging Technologies based on three patent pending technologies:
        </p>
        <ul style="font-size: 0.95rem; line-height: 1.4; color: #4b5563; margin: 0.8rem 0 0 1.2rem; padding-left: 0;">
            <li><strong>AI-Powered Policy Evaluation and Ethical Compliance System</strong> (Patent Application 19/045,526): Provides comprehensive gap analysis and reinforcement learning algorithms for policy evaluation that enable continuous improvement of governance frameworks through machine learning feedback loops.</li>
            <li><strong>Quantum Cybersecurity Framework for Policy Assessment and Maturity Evaluation</strong> (Patent Application 19/004,435): Delivers quantum-specific risk assessment capabilities through a 5-tier scoring system that addresses the unique security challenges posed by quantum computing technologies.</li>
            <li><strong>System for Real-Time Dynamic Governance of Emerging Technologies</strong> (Patent Application 19/204,583): Implements real-time adaptive risk calculations using Bayesian inference and mathematical formulations that automatically adjust governance recommendations based on emerging threat landscapes.</li>
        </ul>
        <p style="font-size: 0.9rem; line-height: 1.4; color: #6b7280; margin: 0.8rem 0 0 0; font-style: italic;">
            This integrated approach creates the first comprehensive governance platform capable of dynamically adapting to emerging technology risks in real-time, filling a critical gap in existing regulatory frameworks.
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
    
    # Comprehensive patent formulations organized by category
    
    # 1. Bayesian Inference & Dynamic Maturity Updates
    st.markdown("""
    <div style="background: #fef2f2; padding: 1rem; border-radius: 6px; margin: 1rem 0;">
    <h5 style="color: #B91C2C; margin-bottom: 0.8rem;">Bayesian Inference for Dynamic Maturity Updates</h5>
    <p style="font-size: 0.9rem; margin: 0; color: #374151;">Dynamically updates maturity levels as new data is received</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.latex(r'''
    P(M|D) = \frac{P(D|M)P(M)}{P(D)}
    ''')
    
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem; margin: 1rem 0; font-size: 0.85rem;">
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>M</strong> = Maturity level (Initial, Basic, etc.)</div>
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>D</strong> = Observed data (queries, outcomes, policy adoption rates)</div>
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>P(M|D)</strong> = Posterior probability of maturity given data</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 2. Reinforcement Learning for Policy Optimization
    st.markdown("""
    <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; margin: 1rem 0;">
    <h5 style="color: #B91C2C; margin-bottom: 0.8rem;">Reinforcement Learning Policy Optimization</h5>
    <p style="font-size: 0.9rem; margin: 0; color: #374151;">Continuously refines policy recommendations using Q-learning</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Q-Learning Formula:**")
        st.latex(r'''
        Q(s,a) = R + \gamma \max Q(s',a')
        ''')
        
        st.markdown("**Policy Optimization Formula:**")
        st.latex(r'''
        Q(s,a) = Q(s,a) + \alpha[R(s,a) + \gamma \max Q(s',a') - Q(s,a)]
        ''')
    
    with col2:
        st.markdown("""
        <div style="display: grid; grid-template-columns: 1fr; gap: 0.3rem; font-size: 0.8rem;">
            <div style="background: #f9fafb; padding: 0.3rem; border-radius: 3px;"><strong>Q(s,a)</strong> = Value of taking action in state s</div>
            <div style="background: #f9fafb; padding: 0.3rem; border-radius: 3px;"><strong>R</strong> = Immediate reward (reduced vulnerabilities)</div>
            <div style="background: #f9fafb; padding: 0.3rem; border-radius: 3px;"><strong>γ</strong> = Discount factor for future rewards</div>
            <div style="background: #f9fafb; padding: 0.3rem; border-radius: 3px;"><strong>α</strong> = Learning rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 3. Cybersecurity Risk Assessment
    st.markdown("""
    <div style="background: #f0fdf4; padding: 1rem; border-radius: 6px; margin: 1rem 0;">
    <h5 style="color: #B91C2C; margin-bottom: 0.8rem;">Cybersecurity Risk Assessment</h5>
    <p style="font-size: 0.9rem; margin: 0; color: #374151;">Compliance metrics using NIST RMF, ISO 27001, and GDPR frameworks</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.latex(r'''
    Risk_{cyber} = \sum_{i=1}^{n} (W_i \times V_i \times C_i)
    ''')
    
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem; margin: 1rem 0; font-size: 0.85rem;">
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>W<sub>i</sub></strong> = Weight for vulnerability type</div>
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>V<sub>i</sub></strong> = Estimated likelihood of exploitability</div>
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>C<sub>i</sub></strong> = Consequence or impact severity</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 4. Ethics Risk Assessment
    st.markdown("""
    <div style="background: #fffbeb; padding: 1rem; border-radius: 6px; margin: 1rem 0;">
    <h5 style="color: #B91C2C; margin-bottom: 0.8rem;">Ethics Risk Assessment</h5>
    <p style="font-size: 0.9rem; margin: 0; color: #374151;">Bias, fairness, transparency, and human autonomy evaluation</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.latex(r'''
    Risk_{ethics} = (1 - T) \times B \times A
    ''')
    
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem; margin: 1rem 0; font-size: 0.85rem;">
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>T</strong> = Transparency score (0-1)</div>
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>B</strong> = Assessed bias factor</div>
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>A</strong> = Autonomy or control risk index</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 5. Cybersecurity Threat Simulation
    st.markdown("""
    <div style="background: #fef2f2; padding: 1rem; border-radius: 6px; margin: 1rem 0;">
    <h5 style="color: #B91C2C; margin-bottom: 0.8rem;">Cybersecurity Threat Simulation</h5>
    <p style="font-size: 0.9rem; margin: 0; color: #374151;">Built-in simulator modeling attack vectors and testing policies</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.latex(r'''
    Risk_{cyber} = \sum_{i=1}^{n} (W_i \times V_i \times C_i)
    ''')
    
    # 6. Similarity Detection for Model Drift
    st.markdown("""
    <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; margin: 1rem 0;">
    <h5 style="color: #B91C2C; margin-bottom: 0.8rem;">Similarity Detection for Model Drift</h5>
    <p style="font-size: 0.9rem; margin: 0; color: #374151;">Cosine similarity for detecting semantic drift in policy vectors</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.latex(r'''
    Similarity = \frac{A \cdot B}{||A|| ||B||}
    ''')
    
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.5rem; margin: 1rem 0; font-size: 0.85rem;">
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>A, B</strong> = Vectorized user interaction representations</div>
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>||A||, ||B||</strong> = Euclidean norms (magnitudes)</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 7. Gap Score Computation
    st.markdown("""
    <div style="background: #f0fdf4; padding: 1rem; border-radius: 6px; margin: 1rem 0;">
    <h5 style="color: #B91C2C; margin-bottom: 0.8rem;">Policy Gap Score Computation</h5>
    <p style="font-size: 0.9rem; margin: 0; color: #374151;">Comprehensive compliance gap analysis and reporting</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.latex(r'''
    G_{policy} = 1 - \frac{C_{match} + E_{match}}{C_{total} + E_{total}}
    ''')
    
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.5rem; margin: 1rem 0; font-size: 0.85rem;">
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>C<sub>match</sub></strong> = Cybersecurity provisions found</div>
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>E<sub>match</sub></strong> = Ethics provisions found</div>
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>C<sub>total</sub></strong> = Expected cybersecurity provisions</div>
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>E<sub>total</sub></strong> = Expected ethical provisions</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 8. AI Policy Effectiveness Score
    st.markdown("""
    <div style="background: #fffbeb; padding: 1rem; border-radius: 6px; margin: 1rem 0;">
    <h5 style="color: #B91C2C; margin-bottom: 0.8rem;">AI Policy Effectiveness Score</h5>
    <p style="font-size: 0.9rem; margin: 0; color: #374151;">Probabilistic reinforcement learning for policy synthesis</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.latex(r'''
    E_{policy} = P_{success} \times R_f \times E_c
    ''')
    
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem; margin: 1rem 0; font-size: 0.85rem;">
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>P<sub>success</sub></strong> = Probability of policy adoption</div>
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>R<sub>f</sub></strong> = Regulatory influence factor</div>
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>E<sub>c</sub></strong> = Ethical compliance coefficient</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 9. Probability-Based Policy Optimization
    st.markdown("""
    <div style="background: #fef2f2; padding: 1rem; border-radius: 6px; margin: 1rem 0;">
    <h5 style="color: #B91C2C; margin-bottom: 0.8rem;">Novel Probability-Based Policy Optimization</h5>
    <p style="font-size: 0.9rem; margin: 0; color: #374151;">Success probability calculation for policy adoption</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.latex(r'''
    P_{success} = \sum_{i=1}^{n} w_i \times S_i
    ''')
    
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.5rem; margin: 1rem 0; font-size: 0.85rem;">
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>P<sub>success</sub></strong> = Likelihood of successful adoption</div>
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>S<sub>i</sub></strong> = Success score of each component</div>
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>w<sub>i</sub></strong> = Weight based on constraints</div>
    </div>
    """, unsafe_allow_html=True)
    
    # 10. Stress-Testing Scoring Formula
    st.markdown("""
    <div style="background: #f0f9ff; padding: 1rem; border-radius: 6px; margin: 1rem 0;">
    <h5 style="color: #B91C2C; margin-bottom: 0.8rem;">AI Policy Sandbox Stress-Testing Score</h5>
    <p style="font-size: 0.9rem; margin: 0; color: #374151;">Four-criteria assessment: Ethical Compliance, Adaptability, Legal Alignment, Implementation Feasibility</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.latex(r'''
    S_{final} = \frac{ECS + AS + LAS + IFS}{4}
    ''')
    
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.5rem; margin: 1rem 0; font-size: 0.85rem;">
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>ECS</strong> = Ethical Compliance Score</div>
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>AS</strong> = Adaptability Score</div>
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>LAS</strong> = Legal Alignment Score</div>
        <div style="background: #f9fafb; padding: 0.5rem; border-radius: 4px;"><strong>IFS</strong> = Implementation Feasibility Score</div>
    </div>
    """, unsafe_allow_html=True)

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
    ## GUARDIAN Patent System Flow
    
    Comprehensive visual diagram showing how the three patent pending technologies interact within the complete GUARDIAN ecosystem.
    """)
    
    # Create comprehensive system flow diagram
    st.markdown("""
    <div style="background: #f8fafc; padding: 2rem; border-radius: 12px; margin: 1.5rem 0;">
        <h3 style="color: #B91C2C; text-align: center; margin-bottom: 2rem;">GUARDIAN Three-Patent Integration Flow</h3>
        
        <!-- Data Ingestion Layer -->
        <div style="background: #e0f2fe; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;">
            <h4 style="color: #0277bd; text-align: center; margin-bottom: 1rem;">📥 Data Ingestion Layer</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem;">
                <div style="background: white; padding: 1rem; border-radius: 6px; text-align: center;">
                    <strong>Backend Scraping</strong><br>
                    <small>• Web APIs<br>• RSS Feeds<br>• Government Portals</small>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 6px; text-align: center;">
                    <strong>Frontend Uploads</strong><br>
                    <small>• PDF Documents<br>• Policy Files<br>• Manual Entry</small>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 6px; text-align: center;">
                    <strong>URL Processing</strong><br>
                    <small>• Direct Links<br>• Content Extraction<br>• Real-time Monitoring</small>
                </div>
            </div>
        </div>
        
        <!-- Repository & Analysis Layer -->
        <div style="background: #f3e5f5; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;">
            <h4 style="color: #7b1fa2; text-align: center; margin-bottom: 1rem;">🗄️ Central Repository & Analysis Engine</h4>
            <div style="display: grid; grid-template-columns: 1fr 2fr 1fr; gap: 1rem; align-items: center;">
                <div style="background: white; padding: 1rem; border-radius: 6px; text-align: center;">
                    <strong>Document Storage</strong><br>
                    <small>PostgreSQL Database<br>Metadata Extraction<br>Thumbnail Generation</small>
                </div>
                <div style="background: #fff3e0; padding: 1rem; border-radius: 6px; text-align: center; border: 2px dashed #ff9800;">
                    <strong>Patent Integration Hub</strong><br>
                    <div style="font-size: 0.8rem; margin-top: 0.5rem;">
                        <div style="margin: 0.3rem 0;"><strong>Patent 19/045,526:</strong> AI Policy Analysis</div>
                        <div style="margin: 0.3rem 0;"><strong>Patent 19/004,435:</strong> Quantum Cybersecurity</div>
                        <div style="margin: 0.3rem 0;"><strong>Patent 19/204,583:</strong> Dynamic Risk Scoring</div>
                    </div>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 6px; text-align: center;">
                    <strong>Content Processing</strong><br>
                    <small>NLP Analysis<br>Feature Extraction<br>Classification</small>
                </div>
            </div>
        </div>
        
        <!-- Scoring Engine Layer -->
        <div style="background: #e8f5e8; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;">
            <h4 style="color: #2e7d32; text-align: center; margin-bottom: 1rem;">⚖️ Patent-Based Scoring Engines</h4>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem;">
                <div style="background: white; padding: 1rem; border-radius: 6px; text-align: center;">
                    <strong>AI Cybersecurity</strong><br>
                    <small>Formula: Σ(w<sub>i</sub> × v<sub>i</sub> × c<sub>i</sub>)<br>Risk = 0-100 Scale</small>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 6px; text-align: center;">
                    <strong>Quantum Cybersecurity</strong><br>
                    <small>QCMEA: 5-Tier System<br>Initial → Optimized</small>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 6px; text-align: center;">
                    <strong>AI Ethics</strong><br>
                    <small>Ethics = F + T + A + P<br>Range: 0-100 Points</small>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 6px; text-align: center;">
                    <strong>Quantum Ethics</strong><br>
                    <small>Multi-dimensional<br>Ethical Framework</small>
                </div>
            </div>
        </div>
        
        <!-- Continuous Learning Layer -->
        <div style="background: #fff3e0; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;">
            <h4 style="color: #ef6c00; text-align: center; margin-bottom: 1rem;">🧠 Continuous Learning & Reinforcement</h4>
            <div style="display: grid; grid-template-columns: 1fr 2fr 1fr; gap: 1rem;">
                <div style="background: white; padding: 1rem; border-radius: 6px; text-align: center;">
                    <strong>Bayesian Updates</strong><br>
                    <small>P(M|D) = P(D|M)P(M)/P(D)<br>Dynamic Maturity</small>
                </div>
                <div style="background: #f3e5f5; padding: 1rem; border-radius: 6px; text-align: center; border: 2px solid #7b1fa2;">
                    <strong>Reinforcement Learning Loop</strong><br>
                    <small>Q(s,a) = R + γ max Q(s',a')<br>Policy Optimization<br>Feedback Integration</small>
                    <div style="margin-top: 0.5rem; font-size: 0.75rem;">
                        Repository Data → LLM Training → Improved Scoring → Better Insights
                    </div>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 6px; text-align: center;">
                    <strong>Model Updates</strong><br>
                    <small>Adaptive Thresholds<br>Learning Rate Adjustment</small>
                </div>
            </div>
        </div>
        
        <!-- User Interface Layer -->
        <div style="background: #e1f5fe; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;">
            <h4 style="color: #0277bd; text-align: center; margin-bottom: 1rem;">👥 User Interface & Guidance System</h4>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
                <div style="background: white; padding: 1rem; border-radius: 6px; text-align: center;">
                    <strong>Policy Analyzer</strong><br>
                    <small>Individual Document Analysis<br>Gap Assessment<br>Recommendations</small>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 6px; text-align: center;">
                    <strong>Repository Insights</strong><br>
                    <small>Strategic Analysis<br>Trend Discovery<br>Learning Patterns</small>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 6px; text-align: center;">
                    <strong>AI Chatbot Guide</strong><br>
                    <small>Skill-to-Novice Support<br>Interactive Help<br>System Navigation</small>
                </div>
            </div>
        </div>
        
        <!-- Output & Feedback Layer -->
        <div style="background: #fce4ec; padding: 1rem; border-radius: 8px;">
            <h4 style="color: #c2185b; text-align: center; margin-bottom: 1rem;">📊 Output & Continuous Improvement</h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div style="background: white; padding: 1rem; border-radius: 6px;">
                    <strong>Immediate Outputs:</strong><br>
                    <small>• Risk Scores & Badges<br>• Gap Analysis Reports<br>• Policy Recommendations<br>• Compliance Assessments</small>
                </div>
                <div style="background: white; padding: 1rem; border-radius: 6px;">
                    <strong>Feedback Loop:</strong><br>
                    <small>• User Interactions → Learning Data<br>• Score Accuracy → Model Updates<br>• Usage Patterns → UI Improvements<br>• Policy Outcomes → Algorithm Refinement</small>
                </div>
            </div>
        </div>
        
        <!-- Mathematical Formulas Applied -->
        <div style="background: #f5f5f5; padding: 1rem; border-radius: 8px; margin-top: 1.5rem; border-left: 4px solid #B91C2C;">
            <h5 style="color: #B91C2C; margin-bottom: 1rem;">Key Mathematical Formulations Applied</h5>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; font-size: 0.85rem;">
                <div>
                    <strong>Bayesian Inference:</strong> P(M|D) = P(D|M)P(M)/P(D)<br>
                    <strong>Reinforcement Learning:</strong> Q(s,a) = R + γ max Q(s',a')<br>
                    <strong>Risk Calculation:</strong> Risk = Σ(w<sub>i</sub> × v<sub>i</sub> × c<sub>i</sub>)
                </div>
                <div>
                    <strong>Ethics Score:</strong> E = F + T + A + P (0-100)<br>
                    <strong>QCMEA Tiers:</strong> Initial → Basic → Intermediate → Advanced → Optimized<br>
                    <strong>Confidence Scoring:</strong> C = exp(-uncertainty) × reliability
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Interactive flow visualization
    st.markdown("### Interactive Flow Demonstration")
    
    flow_step = st.selectbox(
        "Explore System Flow Components:",
        [
            "Data Ingestion Process",
            "Patent Integration Analysis", 
            "Scoring Engine Application",
            "Continuous Learning Loop",
            "User Guidance System",
            "Feedback & Improvement Cycle"
        ]
    )
    
    if flow_step == "Data Ingestion Process":
        st.markdown("""
        **Multi-Source Data Collection:**
        - **Backend Scraping:** Automated collection from government APIs, policy databases, and regulatory feeds
        - **Frontend Uploads:** User-initiated document uploads with PDF processing and metadata extraction
        - **URL Processing:** Real-time web content analysis and monitoring for policy changes
        
        **Technical Implementation:**
        - Trafilatura for web content extraction
        - PDF2Image and PyPDF for document processing
        - SQLAlchemy for database operations
        - Celery for background task processing
        """)
        
    elif flow_step == "Patent Integration Analysis":
        st.markdown("""
        **Three-Patent Synergy:**
        - **AI Policy Patent (19/045,526):** Provides gap analysis algorithms and reinforcement learning frameworks
        - **Quantum Cybersecurity Patent (19/004,435):** Delivers quantum-specific risk assessment through QCMEA 5-tier system
        - **Dynamic Risk Patent (19/204,583):** Implements real-time adaptive scoring using Bayesian inference
        
        **Integration Points:**
        - Shared feature extraction pipeline
        - Cross-patent scoring validation
        - Unified recommendation engine
        """)
        
    elif flow_step == "Scoring Engine Application":
        st.markdown("""
        **Four Scoring Frameworks Applied:**
        
        1. **AI Cybersecurity:** Risk = Σ(w_i × v_i × c_i) where w=weight, v=vulnerability, c=criticality
        2. **Quantum Cybersecurity:** 5-tier QCMEA system from Initial to Optimized maturity levels
        3. **AI Ethics:** E = Fairness + Transparency + Accountability + Privacy (0-100 scale)
        4. **Quantum Ethics:** Multi-dimensional ethical framework for quantum computing governance
        
        **Formula Application Points:**
        - Document ingestion → Feature extraction
        - Content analysis → Risk classification  
        - Score calculation → Confidence assessment
        """)
        
    elif flow_step == "Continuous Learning Loop":
        st.markdown("""
        **Reinforcement Learning Implementation:**
        - **Q-Learning Formula:** Q(s,a) = Q(s,a) + α[R(s,a) + γ max Q(s',a') - Q(s,a)]
        - **Bayesian Updates:** P(M|D) = P(D|M)P(M)/P(D) for dynamic maturity assessment
        - **Policy Optimization:** Continuous refinement based on user interactions and outcomes
        
        **Learning Data Sources:**
        - User scoring feedback
        - Policy implementation outcomes
        - System usage patterns
        - External validation metrics
        """)
        
    elif flow_step == "User Guidance System":
        st.markdown("""
        **Skill-to-Novice User Support:**
        - **AI Chatbot Integration:** Google Dialogflow CX with domain-specific training
        - **Progressive Disclosure:** Interface complexity adapts to user expertise level
        - **Interactive Tooltips:** Context-sensitive help throughout the system
        - **Guided Workflows:** Step-by-step assistance for complex tasks
        
        **Technical Features:**
        - Natural language query processing
        - Intent recognition and response generation
        - Session-based learning and adaptation
        - Multi-modal help delivery (text, visual, interactive)
        """)
        
    else:  # Feedback & Improvement Cycle
        st.markdown("""
        **Continuous System Enhancement:**
        
        **Feedback Collection Points:**
        - User satisfaction scores on recommendations
        - Policy implementation success rates
        - System accuracy metrics
        - User interaction patterns
        
        **Improvement Mechanisms:**
        - Algorithm parameter tuning based on performance data
        - Model retraining with new repository content
        - UI/UX enhancements from usage analytics
        - Scoring threshold adjustments for optimal accuracy
        
        **Validation Loop:**
        - Real-world outcome tracking → Model validation → Algorithm updates → Performance improvement
        """)

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